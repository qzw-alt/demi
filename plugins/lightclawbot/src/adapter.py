"""
LightClaw adapter — main coordinator class and module singleton.
Mirrors: src/gateway.ts

D1 多租户改造:
    - 不再继承 ``NativeSocketMixin``；该 mixin 上的全部状态机已搬到
      :class:`socket.per_uin_session._PerUinSession`。
    - adapter 内为每个 UIN 维护一条独立 :class:`_PerUinSession`，
      按 ``chat_id → uin`` 路由 outbound / 处理 inbound。
    - 单 UIN 部署时行为与重构前完全等价（single-session fast path）。
    - 多 UIN 部署时各 session 的 WS / ACK / Reliable 全部隔离，
      修复了原先 ``_fetch_ticket`` 永远只用 ``_api_keys[0]`` 的关键 BUG。
"""

import asyncio
import json
import logging
import os
from collections import OrderedDict
from typing import Dict, List, Optional, Tuple

from gateway.platforms.base import BasePlatformAdapter
from gateway.config import PlatformConfig

from .config import (
    API_PATH_TICKET,
    DEFAULT_API_BASE_URL,
    DEFAULT_WS_BASE_URL,
    EVENT_HANDSHAKE,
    EVENT_HISTORY_REQUEST,
    EVENT_MESSAGE_ACK,
    EVENT_MESSAGE_PRIVATE,
    EVENT_SESSIONS_REQUEST,
    EVENT_CHAT_REQUEST,
    EVENT_AGENTS_REQUEST,
    FileDownloadStatus,
    KIND_FILE_DOWNLOAD,
    generate_msg_id,
)
from .socket.per_uin_session import _PerUinSession
from .inbound import InboundMixin
from .outbound import OutboundMixin
from .download_handler import DownloadHandlerMixin
from .tenancy import resolve_effective_api_key, set_api_key_map
from .usage_tracker import SessionUsageTracker

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# HTTP response body 截断工具（用于 /cgi/ticket 等接口的错误诊断）
# ---------------------------------------------------------------------------
# 上游返回非预期 Content-Type（如网关拦截页 / HTML 错误页）时，我们需要
# 把响应体落到日志里排查——但 HTML 页动辄数 KB，全量打印会打爆日志盘。
# 采用「头部 + 尾部」双段截断：头部通常含 HTTP 错误标题，尾部通常含堆栈
# 或时间戳，中段用省略号占位。
_BODY_HEAD_LEN = 400
_BODY_TAIL_LEN = 200


def _truncate_body(text: str) -> str:
    """将响应体压缩到日志友好长度。

    * 全空/None → ``"<empty>"``
    * 长度 ≤ HEAD+TAIL+相关标识 → 原样返回（去除首尾空白）
    * 否则：头 400 字符 + " ...[truncated N chars]... " + 尾 200 字符

    换行 / 制表符替换为可见转义，避免日志被多行 HTML 撑开影响可读性。
    """
    if not text:
        return "<empty>"
    stripped = text.strip()
    if not stripped:
        return "<whitespace-only>"
    # 短内容直接返回，只做换行转义。
    max_inline = _BODY_HEAD_LEN + _BODY_TAIL_LEN + 32
    if len(stripped) <= max_inline:
        return stripped.replace("\n", "\\n").replace("\t", "\\t")
    head = stripped[:_BODY_HEAD_LEN].replace("\n", "\\n").replace("\t", "\\t")
    tail = stripped[-_BODY_TAIL_LEN:].replace("\n", "\\n").replace("\t", "\\t")
    return (
        f"{head} ...[truncated {len(stripped) - _BODY_HEAD_LEN - _BODY_TAIL_LEN} "
        f"chars]... {tail}"
    )


async def _read_body_snippet(resp) -> str:
    """从 aiohttp 响应对象中安全提取截断后的响应体片段。

    读取本身失败时返回 ``"<read-failed: ...>"``——诊断日志不能因读体失败
    而丢失原始 status/headers 上下文。
    """
    try:
        raw = await resp.text(errors="replace")
    except Exception as exc:  # pylint: disable=broad-except
        return f"<read-failed: {type(exc).__name__}: {exc}>"
    return _truncate_body(raw)


# ---------------------------------------------------------------------------
# Bounded round-chat context (LRU)
# ---------------------------------------------------------------------------
# ``_round_chat_ctx`` 记录每个 sender 当前轮次的 (business_chat_id, agent_id)
# 上下文。stop_typing 阶段不主动清理（attachment 等 post-stop_typing 链路
# 仍可能读取），只由下一次 inbound 覆盖写入。多租户 Hermes 实例长期运行时，
# 长期不活跃的 sender 条目会缓慢积压——虽然每条只是两个短字符串组成的 tuple，
# 但没有上限意味着理论上无界。用 OrderedDict + 写入淘汰做 O(1) LRU 上限。
#
# 上限选择：多租户实例并发活跃用户数通常远小于 1000；给足 4096 作为安全余量
# 既覆盖极端峰值，又把内存占用锁定在 KB 级（每条 tuple ~200 字节）。
_ROUND_CHAT_CTX_MAX = 4096


class _BoundedRoundChatCtx(OrderedDict):
    """有上限的 sender → (business_chat_id, agent_id) 映射。

    行为：
      * 写入自动追加到尾部（``move_to_end``），已存在的 key 更新值时同样刷新
        位置——保证「最近写入 = 最新活跃」。
      * 超过 ``max_size`` 时从头部弹出最老条目（``popitem(last=False)``）。
      * 读操作 (``get``/``__getitem__``) **不** 刷新 LRU 顺序。因为业务
        时序上「先 inbound 写、后 outbound 读」，读时该 sender 必然刚
        被写为最新，无需再刷新；避免读路径承担 O(1) 额外开销。

    这里刻意继承自 ``OrderedDict`` 而非包装组合，让下游代码可以像普通
    dict 一样使用（``.get()`` / ``.pop()`` / ``in`` 等 API 保持不变）。
    """

    def __init__(self, max_size: int = _ROUND_CHAT_CTX_MAX) -> None:
        super().__init__()
        self._max_size = max_size

    def __setitem__(self, key, value) -> None:
        # 覆盖写：先移到尾部再赋值，保证「最近写 = 最新」。
        if key in self:
            self.move_to_end(key, last=True)
        super().__setitem__(key, value)
        # 超上限时从头部（最老）淘汰。使用 while 是为了理论上处理
        # ``max_size`` 被动态调小的场景；正常运行只会执行 0 或 1 次。
        while len(self) > self._max_size:
            evicted_key, _ = self.popitem(last=False)
            logger.debug(
                "[lightclaw] _round_chat_ctx evicted oldest entry: sender=%s "
                "(size=%d, max=%d)",
                evicted_key, len(self), self._max_size,
            )


class LightClawAdapter(
    InboundMixin,
    OutboundMixin,
    DownloadHandlerMixin,
    BasePlatformAdapter,
):
    """
    Hermes gateway adapter for LightClaw-compatible servers.

    Connects via native WebSocket (aiohttp), receives message:private events,
    dispatches them to Hermes AIAgent, and sends responses back.

    Protocol:
    - Auth:      POST /cgi/ticket  → { code:0, data:{ id:"<uin>",
                                                       client:{ extra:'{"botId":"..."}' },
                                                       ticket:"..." } }
    - Transport: Native WebSocket  wss://<domain>/ws/agent?ticket=<ticket>&enableMultiLogin=false
    - Framing:   Raw JSON  { "event": "<name>", "data": {...} }
    - Handshake: server sends { "event": "__handshake__", "data": { "id": "<socket_id>" } }
    - ACK:       server sends { "event": "message:ack", "data": { "relatedMsgId": "<msgId>" } }
    """

    # Streaming mode: GatewayStreamConsumer sends first chunk via send(),
    # then updates via edit_message() with accumulated text, and finally
    # calls edit_message(finalize=True) to close the stream.
    SUPPORTS_MESSAGE_EDITING = True
    REQUIRES_EDIT_FINALIZE = True

    def __init__(self, config: PlatformConfig):
        from gateway.config import Platform
        super().__init__(config, Platform("lightclawbot"))

        extra = config.extra or {}

        # API key — 多用户隔离格式 LIGHTCLAW_API_KEY_${UIN}
        # `extra.api_keys` (yaml list) is kept as a forward-compat hook for
        # future multi-tenant deployments; not used in current deployments.
        if extra.get("api_keys"):
            self._api_keys: List[str] = list(extra["api_keys"])
        else:
            api_keys_from_env = []
            for key in os.environ:
                if key.startswith("LIGHTCLAW_API_KEY_"):
                    value = os.environ[key].strip()
                    if value:
                        api_keys_from_env.append(value)
            self._api_keys = api_keys_from_env

        # Server URLs — default to config.py constants; env overrides are kept
        # as an operational escape hatch for private deployments / staging.
        self._ws_base_url: str  = os.getenv("LIGHTCLAW_WS_URL",       DEFAULT_WS_BASE_URL)
        self._api_base_url: str = os.getenv("LIGHTCLAW_API_BASE_URL", DEFAULT_API_BASE_URL)

        # Identity (resolved on connect, stable across reconnects)
        self._bot_client_id: str        = ""
        self._api_key_map: Dict[str, str] = {}   # uin → apiKey (populated during _resolve_identity)

        # Per-chat round msgId
        self._round_ids: Dict[str, str] = {}

        # Per-chat "last closed round" msgId.  Populated by stop_typing()
        # when it closes an active round; consumed by outbound.send() so
        # that any output arriving AFTER stop_typing but BEFORE the next
        # inbound (e.g. framework-routed attachment links) can reuse the
        # same msgId instead of opening a brand-new standalone round.
        # Cleared by inbound when a new turn begins.
        self._last_round_id: Dict[str, str] = {}

        # Per-chat flag: whether the current round has already emitted a
        # stream_chunk.  Used by OutboundMixin.send() to prepend "\n\n"
        # before non-first chunks so front-end concatenation matches the
        # visual breaks seen in the history view.
        self._round_has_content: Dict[str, bool] = {}

        # Per-chat snapshot of accumulated text (cursor-stripped) for
        # edit_message() delta computation in streaming mode.
        self._edit_snapshot: Dict[str, str] = {}

        # (multi-agent _incoming_agent_ids removed: only one agent "main" is supported)

        # Per-chat 业务会话上下文：sender → (business_chat_id, agent_id)
        # 由 inbound 在每轮开始时写入，outbound 在 _persist_turn_usage /
        # _resolve_session_id_for_chat 中读出以还原与 inbound 完全一致的 sessionKey
        # （`agent:{agent_id}:{CHANNEL_KEY}:dm:{sender}[:{chat_id}]`）。
        # 没有该上下文时回退到 legacy 无 chatId 后缀的形式，兼容旧前端。
        # stop_typing 不清理（attachment 等 post-stop_typing 链路仍可能需要解析），
        # 由下一次 inbound 覆盖写入。使用 ``_BoundedRoundChatCtx`` LRU 上限，
        # 防止长期不活跃的 sender 条目在多租户长运行实例上无界积压。
        self._round_chat_ctx: Dict[str, Tuple[str, str]] = _BoundedRoundChatCtx()

        # ── Token usage (per-turn delta over session-cumulative counters) ──
        # Snapshots Hermes' cumulative SQLite counters at turn start and
        # diffs them at turn end to derive this turn's consumption.  The
        # tracker is constructed below, once sessions_dir is resolved, so it
        # locates state.db from the same authoritative path the rest of the
        # plugin uses (never a hardcoded path / username).

        # Per-chat inbound msgId, echoed as `replyToMsgId` on the usage frame.
        self._round_reply_to: Dict[str, str] = {}

        # Per-chat guard: round msgId already emitted (stop_typing fires
        # multiple times per turn; we emit usage at most once).
        self._round_usage_emitted: Dict[str, str] = {}

        # Per-chat list of attachments seen on inbound messages.
        # Used by history persistence / outbound enrichment.  Entries are
        # dicts of shape {"name", "mimeType", "url"} where url is always
        # a `localfile://` URI (mirrors TS `publicMediaUrls`).
        self._inbound_attachments: Dict[str, list] = {}

        # Per-chat list of file paths extracted from write_file tool_start
        # messages during a turn.  Used by the model-independent fallback in
        # stop_typing() to auto-deliver files when the model omits MEDIA: tags.
        self._pending_file_paths: Dict[str, list] = {}

        # Per-chat set of absolute paths already delivered via send_document()
        # in the current turn (populated by the framework's MEDIA: →
        # _deliver_media_from_response path).  Used by _deliver_pending_files()
        # to avoid duplicate links.
        self._delivered_paths: Dict[str, set] = {}

        # ── Thinking step state (per-chat, per-turn) ──
        # 用于在 tool_progress 文本旁路并发一帧 thinking_step（kind='thinking_step'）
        # 给前端做"思考过程时间线"渲染。本期只发 running 帧。
        # 由 inbound 在新一轮开始时清理（与其他 per-turn 状态同步）。
        #
        # _step_seq:        chat_id → 本轮已分配的最大 seq（从 0 自增，前端用于排序）
        # _step_count:      chat_id → 本轮已生成 stepId 的编号（用于 step-{N}-{tool}）
        # _last_tool_step:  chat_id → 最近一次 running 帧的元信息（stepId/seq/toolName/type）。
        #                   阶段一暂不发 done，仅为阶段二预留 done 帧合并锚点。
        self._step_seq: Dict[str, int] = {}
        self._step_count: Dict[str, int] = {}
        self._last_tool_step: Dict[str, dict] = {}

        # _emitted_tool_lines: chat_id → 本轮已发过 thinking_step 的工具行
        #   文本集合（line_stripped），用于跨 send() / edit_message() 路径
        #   去重，避免同一工具行被重复渲染为时间线行。
        #   inbound 在新一轮开始时清空。
        self._emitted_tool_lines: Dict[str, set] = {}

        # Sessions directory for history reading
        hermes_home = os.environ.get("HERMES_HOME") or os.path.expanduser("~/.hermes")
        self._sessions_dir: str = (
            extra.get("sessions_dir")
            or os.getenv("LIGHTCLAW_SESSIONS_DIR")
            or os.path.join(hermes_home, "sessions")
        )

        # Token usage tracker — resolves state.db relative to the sessions
        # dir above (state.db is its sibling), so it follows custom install
        # locations and never assumes a hardcoded path / username.
        self._usage_tracker: SessionUsageTracker = SessionUsageTracker(
            sessions_dir=self._sessions_dir,
        )

        # (multi-agent _agent_prompts removed: only one agent "main" is supported)

        # ── 多 UIN 会话管理（D1 改造） ─────────────────────────────
        # _sessions       : uin → _PerUinSession（每 UIN 一条独立 WS 连接）
        # _chat_to_uin    : chat_id → uin 的路由表，inbound 落地后写入，
        #                   outbound 据此把 frame 路由回正确的 session
        # _stopped        : 全局停止开关（adapter.disconnect 时置位）
        # _aiohttp        : adapter 共享的 ClientSession（HTTP + ws_connect 都用它）
        self._sessions: Dict[str, _PerUinSession] = {}
        self._chat_to_uin: Dict[str, str] = {}
        self._stopped: bool = False
        self._aiohttp = None  # aiohttp.ClientSession，connect() 时构造

    # ------------------------------------------------------------------
    # Session routing helpers
    # ------------------------------------------------------------------

    def _resolve_session_for_chat(self, chat_id: Optional[str]) -> Optional[_PerUinSession]:
        """根据 chat_id 找到对应 session。

        路由优先级（D2 完善版）：
            1. ``_chat_to_uin[chat_id]`` 已记录 → 取对应 session（最快、最准）
            2. 通过 :mod:`tenancy` 反查 chat_id 对应的 apiKey，再用 apiKey
               反查 ``_sessions``：覆盖 inbound 还没到达就先 outbound 的极端
               场景（cron 投递、首次拉历史等）。命中后回写路由表。
            3. 单 session 部署 → 直接返回那唯一一个（保证单 UIN 等价）
            4. 找不到 → ``None`` （outbound 调用方需自行 fallback / 报错）

        ⚠️ 不再隐式取"任意一个 session"作为兜底——多 UIN 场景下错误路由
        会把帧打到错误的租户上，宁可丢帧并打 warning，由上层显式处理。
        """
        if chat_id is not None:
            uin = self._chat_to_uin.get(chat_id)
            if uin is not None:
                sess = self._sessions.get(uin)
                if sess is not None:
                    return sess

            # tenancy 反查：sender_id (chat_id) → apiKey → uin → session
            try:
                api_key = resolve_effective_api_key(sender_id=chat_id)
            except Exception:
                api_key = ""
            if api_key:
                for uin, sess in self._sessions.items():
                    if sess.api_key == api_key:
                        # 回写缓存，下次直接命中
                        self._chat_to_uin[chat_id] = uin
                        return sess

        # 单 session fast path：保证单 UIN 部署完全等价
        if len(self._sessions) == 1:
            return next(iter(self._sessions.values()))

        return None

    def _any_session(self) -> Optional[_PerUinSession]:
        """返回任意一个 session（多 UIN 时用于 fallback / 启动期边界）。"""
        for sess in self._sessions.values():
            return sess
        return None

    # ------------------------------------------------------------------
    # Backward-compatible reliable / WS facade (used by mixins)
    # ------------------------------------------------------------------
    #
    # InboundMixin / OutboundMixin / DownloadHandlerMixin 在重构前直接通过
    # ``self._reliable`` / ``self._ws_emit`` / ``self._socket_id`` 操作单
    # 一个 emitter / WS。改造后这些字段不再有意义，但为了不在 mixin 内部
    # 大改逻辑（D1 阶段目标"单 UIN 等价"），我们在 adapter 层保留这些
    # 名字作为**会话感知 facade**：每次访问按 chat_id（或 fallback 任意 session）
    # 路由到具体 _PerUinSession。
    #
    # 调用约定：
    #   * mixin 中用 ``self._fire_and_forget(event, data)`` / ``self._emit_reliable(...)``
    #     发帧时，``data`` 一定包含 ``"to"``（即 chat_id），adapter 据此路由。
    #   * 兼容字段 ``self._reliable`` 仅作为 truthiness 探针保留 —— mixin 中
    #     有大量 ``if not self._reliable: return`` 早退判断，必须保持有意义。

    @property
    def _reliable(self) -> Optional[object]:
        """True 当至少一个 session 已 ready；mixin 仅用其 truthiness 探活。

        历史代码会用 ``self._reliable`` 做对象比较，但所有路径最终都会
        走 ``_fire_and_forget`` / ``_emit_reliable``（已被 facade 重写），
        所以这里返回 *任意* 一个有效 reliable 对象即可。
        """
        sess = self._any_session()
        return sess.reliable if sess is not None else None

    def _fire_and_forget(self, event: str, data: dict) -> None:
        """会话感知的 fire-and-forget 发送。

        覆盖 :class:`OutboundMixin._fire_and_forget`，根据 ``data["to"]``
        路由到对应 :class:`_PerUinSession` 的 reliable emitter。
        """
        chat_id = data.get("to") or data.get("from")
        sess = self._resolve_session_for_chat(chat_id)
        if sess is None:
            logger.warning(
                "[lightclaw] fire_and_forget dropped (no session for chat=%s, event=%s)",
                chat_id, event,
            )
            return
        msg_id = data.get("msgId")
        kind = data.get("kind", "?")
        content = data.get("content", "")
        content_preview = content[:40] if content else ""
        if not sess.connected:
            # 故障隔离（D3）：路由到断线 session 不丢帧 —— ws_emit 内
            # ws.closed 时会静默 return，但 reliable.emit_with_ack 走的
            # pause/resume 路径会自动暂存并在重连后重发。fire-and-forget
            # 没有重试，所以这里降级为可见的 info 而非 warning，避免误报。
            logger.info(
                "[lightclaw uin=%s] fire_and_forget while session offline (will drop): "
                "kind=%s to=%s msgId=%s",
                sess.uin or "?", kind, chat_id, msg_id,
            )
        logger.info(
            "[lightclaw uin=%s] fire_and_forget: kind=%s to=%s msgId=%s content='%s'",
            sess.uin or "?", kind, chat_id, msg_id, content_preview,
        )
        sess.emit_fire_and_forget(event, data)

    async def _emit_reliable(self, event: str, data: dict) -> bool:
        """会话感知的 reliable 发送。

        故障隔离（D3）：当目标 session 当前 disconnected 时，仍然把消息
        交给 :class:`ReliableEmitter` —— 它处于 paused 状态，会把消息暂存
        到 ``_pending`` 并在 session 重连（``resume()``）时自动重发。
        因此本方法不会因为短暂断线而丢失关键帧，但调用方需要意识到
        ``await`` 可能阻塞到首次 ACK 或最终 give-up。
        """
        chat_id = data.get("to") or data.get("from")
        sess = self._resolve_session_for_chat(chat_id)
        if sess is None:
            logger.warning(
                "[lightclaw] emit_reliable dropped (no session for chat=%s, event=%s)",
                chat_id, event,
            )
            return False
        msg_id = data.get("msgId")
        kind = data.get("kind", "?")
        if not sess.connected:
            logger.info(
                "[lightclaw uin=%s] emit_reliable while session offline (queued): "
                "event=%s kind=%s to=%s msgId=%s",
                sess.uin or "?", event, kind, chat_id, msg_id,
            )
        logger.info(
            "[lightclaw uin=%s] emit_reliable: event=%s kind=%s to=%s msgId=%s",
            sess.uin or "?", event, kind, chat_id, msg_id,
        )
        return await sess.emit_with_ack(event, data, msg_id)

    @property
    def _session(self):
        """共享的 aiohttp.ClientSession（inbound._process_files / download_handler 等用它）。"""
        return self._aiohttp

    # ------------------------------------------------------------------
    # Identity resolution
    # ------------------------------------------------------------------

    async def _resolve_identity(self) -> None:
        """
        POST /cgi/ticket for each API key to get botClientId and the tenant's uin.

        Response shape::

            { code: 0,
              data: {
                id: "<uin>",                               # tenant user id
                client: { extra: '{"botId":"<botId>"}' },  # JSON string
                ticket: "..."
              }
            }

        Populates:
            self._bot_client_id   — any non-empty botId (first key wins)
            self._api_key_map     — { uin: apiKey, ... }  (plus apiKey→apiKey
                                     as a safety fallback when uin missing)

        And pushes the result into :mod:`.tenancy` so tool handlers and the
        download signal handler can resolve the correct apiKey per session.

        错误诊断：
            当上游返回非预期内容（如 HTML 错误页 / 网关拦截页）时，直接
            ``resp.json()`` 会抛 ``ContentTypeError`` 且不带响应体信息，让线上
            排障非常困难。这里改为先 ``resp.text()`` 读原文，再手动
            ``json.loads``：解析失败时把 Content-Type 与截断后的响应体
            落到 WARNING 日志，同时用头 400 字符 + 尾 200 字符的方式截断
            以兼顾"看得到关键错误页文案"和"日志体积可控"（HTML 页动辄
            数 KB，不截断会打爆日志盘）。
        """
        import aiohttp

        url = f"{self._api_base_url}{API_PATH_TICKET}"
        bot_client_id = ""
        api_key_map: Dict[str, str] = {}

        # 对单个 key 发请求，返回解析后的 (uin, bid)，失败抛异常。
        async def _resolve_one_key(
            session: aiohttp.ClientSession, key: str,
        ) -> tuple[str, str]:
            headers = {
                "authorization": f"Bearer {key}",
                "x-product":     "channel",
            }
            async with session.post(
                url, headers=headers,
                timeout=aiohttp.ClientTimeout(total=15),
            ) as resp:
                if resp.status != 200:
                    body_snippet = await _read_body_snippet(resp)
                    raise RuntimeError(
                        f"HTTP {resp.status} "
                        f"content_type={resp.headers.get('Content-Type', '?')} "
                        f"body={body_snippet}"
                    )
                raw_text = await resp.text(errors="replace")
                try:
                    data = json.loads(raw_text)
                except (json.JSONDecodeError, ValueError) as parse_exc:
                    raise RuntimeError(
                        f"non-JSON response: {parse_exc} body={_truncate_body(raw_text)}"
                    )
                if not isinstance(data, dict):
                    raise RuntimeError(
                        f"unexpected payload type: {type(data).__name__} "
                        f"body={_truncate_body(raw_text)}"
                    )
                if data.get("code") != 0:
                    raise RuntimeError(
                        f"code={data.get('code')} message={data.get('message')}"
                    )
                payload = data.get("data") or {}
                extra_str = (payload.get("client") or {}).get("extra", "")
                try:
                    parsed = json.loads(extra_str) if extra_str else {}
                    bid = parsed.get("botId", "")
                except (json.JSONDecodeError, TypeError):
                    bid = ""
                uin = str(payload.get("id") or "").strip()
                return uin, bid

        async with aiohttp.ClientSession() as session:
            for key in self._api_keys:
                last_error = None
                for retry in range(3):
                    try:
                        uin, bid = await _resolve_one_key(session, key)
                    except Exception as exc:
                        last_error = exc
                        # 仅对 transient 错误重试（5xx、连接错误、超时）
                        is_retryable = (
                            isinstance(exc, (aiohttp.ClientError, asyncio.TimeoutError, OSError))
                            or "HTTP 5" in str(exc)
                        )
                        if is_retryable and retry < 2:
                            logger.warning(
                                "[lightclaw] %s transient error for key ***%s "
                                "(retry %d/2): %s",
                                API_PATH_TICKET, key[-4:], retry, exc,
                            )
                            await asyncio.sleep(2.0 * (retry + 1))  # 2s → 4s → 6s
                            continue
                        logger.warning(
                            "[lightclaw] %s failed for key ***%s: %s",
                            API_PATH_TICKET, key[-4:], exc,
                        )
                        break  # non-retryable or exhausted → next key
                    # success
                    if bid and not bot_client_id:
                        bot_client_id = bid
                    if uin:
                        api_key_map[uin] = key
                        logger.info(
                            "[lightclaw] Key ***%s mapped to uin=%s (botId=%s)",
                            key[-4:], uin, bid or "?",
                        )
                    else:
                        api_key_map[key] = key
                        logger.info(
                            "[lightclaw] Key ***%s mapped (botId=%s, no uin returned)",
                            key[-4:], bid or "?",
                        )
                    break  # success → next key

        if not bot_client_id:
            raise RuntimeError(
                "Failed to resolve botClientId from any API key via POST /cgi/ticket"
            )

        self._bot_client_id = bot_client_id
        self._api_key_map   = api_key_map

        # Publish the map into the tenancy module so inbound/outbound/tool
        # code can resolve the correct apiKey for a given sessionKey/senderId.
        default_key = self._api_keys[0] if self._api_keys else ""
        set_api_key_map(api_key_map, default_key)

        # ── 启动期路由预热（D2） ────────────────────────────────
        # chat_id == peer uin 全局唯一；把已识别的所有 uin 自映射进路由表，
        # 让"history-only / cron 投递 / 首次 outbound 早于 inbound"等场景也能
        # 在没有任何 inbound 学习的情况下命中正确的 session。
        for uin in api_key_map:
            if uin and uin not in self._chat_to_uin:
                self._chat_to_uin[uin] = uin

        # ── 自动认领 home channel ──────
        # 单租户：唯一的 uin 就是归属者本人，chat_id == uin，天然是 home。
        # 仅在用户未显式配置时填充，尊重 env / config.yaml 的显式设置：
        #   * 单租户（恰好 1 个 uin）    → 自动设，安全等价于个人微信私聊。
        #   * 多租户（多个 uin）         → 不自动设，否则会把 A 的定时任务投递给 B。
        #   * 已显式配置（home_channel）→ 守卫跳过，绝不覆盖用户设置。
        # 把结果持久化到 LIGHTCLAWBOT_HOME_CHANNEL，保证 cron /
        # send_message 无论从哪个 config 副本读都稳定命中。
        real_uins = [u for u in api_key_map if u and u not in self._api_keys]
        if len(real_uins) == 1 and not getattr(self.config, "home_channel", None):
            sole_uin = real_uins[0]
            try:
                from gateway.config import HomeChannel, Platform

                self.config.home_channel = HomeChannel(
                    platform=Platform("lightclawbot"),
                    chat_id=sole_uin,
                    name="Home",
                )
                if not os.getenv("LIGHTCLAWBOT_HOME_CHANNEL"):
                    try:
                        from hermes_cli.config import save_env_value

                        save_env_value("LIGHTCLAWBOT_HOME_CHANNEL", sole_uin)
                    except Exception as exc:
                        logger.warning(
                            "[lightclaw] persist home channel failed: %s: %s",
                            type(exc).__name__, exc,
                        )
                logger.info(
                    "[lightclaw] Auto home channel = %s (single-tenant)", sole_uin,
                )
            except Exception as exc:
                logger.warning(
                    "[lightclaw] auto home channel failed: %s: %s",
                    type(exc).__name__, exc,
                )

        logger.info(
            "[lightclaw] Bot clientId: %s, %d key(s) mapped",
            bot_client_id, len(api_key_map),
        )

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    async def connect(self, *, is_reconnect: bool = False) -> bool:
        if not self._api_keys:
            logger.error("[lightclaw] No API keys configured")
            self._set_fatal_error("no_api_keys", "No API keys configured", retryable=False)
            return False

        try:
            import aiohttp  # noqa: F401
        except ImportError:
            logger.error("[lightclaw] aiohttp not installed")
            self._set_fatal_error("missing_deps", "aiohttp not installed", retryable=False)
            return False

        try:
            await self._resolve_identity()
        except Exception as exc:
            logger.error("[lightclaw] Identity resolution failed: %s", exc)
            self._set_fatal_error("identity_failed", str(exc), retryable=True)
            return False

        import aiohttp
        self._stopped = False
        self._aiohttp = aiohttp.ClientSession()

        # 为每个已识别的 (uin, apiKey) 启动一条独立 WS session
        if not self._api_key_map:
            logger.error("[lightclaw] _api_key_map empty after identity resolution")
            await self._aiohttp.close()
            self._aiohttp = None
            self._set_fatal_error("identity_failed", "no uin resolved", retryable=True)
            return False

        for uin, api_key in self._api_key_map.items():
            sess = _PerUinSession(
                api_key=api_key,
                uin=uin,
                ws_base_url=self._ws_base_url,
                api_base_url=self._api_base_url,
                aiohttp_session=self._aiohttp,
                on_raw=self._on_session_raw,
                on_connected=self._on_session_connected,
                on_disconnected=self._on_session_disconnected,
                log_prefix=f"[lightclaw uin={uin}]",
            )
            self._sessions[uin] = sess

        # 并发启动所有 session 的连接循环
        # ⚠️ 故障隔离（D2）：单条 session 启动失败（例如某个 apiKey 过期 /
        # 单租户 ticket 拒签）不应阻塞其它租户。任意一条 session 完成首连即
        # 视为 adapter 整体连接成功；全部失败才触发 _set_fatal_error。
        # 先快照，防止 gather 期间 _sessions 被并发修改导致 zip 顺序错乱。
        sessions_snapshot = list(self._sessions.items())
        start_results = await asyncio.gather(
            *(sess.start() for _, sess in sessions_snapshot),
            return_exceptions=True,
        )
        for (uin, _), result in zip(sessions_snapshot, start_results):
            if isinstance(result, Exception):
                logger.warning(
                    "[lightclaw uin=%s] session.start() raised: %s — keeping other sessions",
                    uin, result,
                )

        # 等待至少一条 session 完成首连接（与单 UIN 时旧版 _first_connect_event 行为对齐）
        first_events = [sess.first_connect_event.wait() for sess in self._sessions.values()]
        timed_out = False
        try:
            done, pending = await asyncio.wait(
                [asyncio.create_task(ev) for ev in first_events],
                timeout=20.0,
                return_when=asyncio.FIRST_COMPLETED,
            )
            for task in pending:
                task.cancel()
            if not done:
                timed_out = True
        except asyncio.TimeoutError:
            timed_out = True

        any_connected = any(sess.connected for sess in self._sessions.values())
        if not any_connected:
            logger.error(
                "[lightclaw] No session connected within timeout (timed_out=%s, sessions=%d)",
                timed_out, len(self._sessions),
            )
            self._set_fatal_error(
                "connect_timeout", "No session connected within timeout", retryable=True,
            )
            return False

        if timed_out:
            # 至少一条已连上 → 不阻塞 adapter 启动；其余 session 由各自的
            # 重连循环兜底，等它们后续连上即可参与路由。
            disconnected = [u for u, s in self._sessions.items() if not s.connected]
            logger.warning(
                "[lightclaw] Partial connect: %d/%d sessions up, pending uins=%s",
                len(self._sessions) - len(disconnected), len(self._sessions), disconnected,
            )

        _set_active_adapter(self)
        return True

    async def disconnect(self) -> None:
        self._stopped = True

        # 并发关闭所有 session（先快照，防止 gather 期间 _sessions 被修改导致 zip 顺序错乱）
        if self._sessions:
            sessions_snapshot = list(self._sessions.items())
            results = await asyncio.gather(
                *(sess.stop() for _, sess in sessions_snapshot),
                return_exceptions=True,
            )
            for (uin, _), result in zip(sessions_snapshot, results):
                if isinstance(result, Exception):
                    logger.warning(
                        "[lightclaw uin=%s] session.stop() raised: %s", uin, result,
                    )
            self._sessions.clear()

        # 清空路由表，避免下次 connect 后残留旧 chat_id → 旧 uin 的错误映射
        self._chat_to_uin.clear()

        if self._aiohttp is not None and not self._aiohttp.closed:
            try:
                await self._aiohttp.close()
            except Exception as exc:
                logger.warning("[lightclaw] aiohttp.close() raised: %s", exc)
        self._aiohttp = None

        _set_active_adapter(None)
        self._mark_disconnected()

    # ------------------------------------------------------------------
    # Per-session callbacks
    # ------------------------------------------------------------------

    def _on_session_connected(self, session: _PerUinSession) -> None:
        """任一 session 首次连上时把 adapter 整体标为 connected。"""
        logger.info(
            "[lightclaw uin=%s] Session connected (active=%d/%d)",
            session.uin or "?",
            sum(1 for s in self._sessions.values() if s.connected),
            len(self._sessions),
        )
        if not getattr(self, "_connected", False):
            self._mark_connected()

    def _on_session_disconnected(self, session: _PerUinSession) -> None:
        """所有 session 都断开时把 adapter 标为 disconnected。

        故障隔离（D3）：只要还有任意一条 session 在线，adapter 整体保持
        connected —— 仅断线那条 uin 的用户暂停服务，其余租户不受影响。
        """
        active = [u for u, s in self._sessions.items() if s.connected]
        logger.info(
            "[lightclaw uin=%s] Session disconnected (active=%d/%d, alive_uins=%s)",
            session.uin or "?", len(active), len(self._sessions), active,
        )
        if not active:
            self._mark_disconnected()

    # ------------------------------------------------------------------
    # Health / observability
    # ------------------------------------------------------------------

    def session_status(self) -> Dict[str, dict]:
        """Per-UIN session health snapshot — for ops / diagnostics.

        Returns a ``{uin: {connected, socket_id, pending_acks}}`` dict so
        ``preflight`` / monitoring tooling can inspect each tenant's WS
        independently of adapter-level ``_connected``.
        """
        snap: Dict[str, dict] = {}
        for uin, sess in self._sessions.items():
            snap[uin] = {
                "connected": sess.connected,
                "socket_id": sess.socket_id or "",
                "pending_acks": len(sess._pending_acks),
            }
        return snap

    async def _on_session_raw(self, session: _PerUinSession, raw: str) -> None:
        """每个 session 收到原始帧后回调到这里 —— 派发到对应业务路径。"""
        await self._handle_raw_for_session(session, raw)

    # ------------------------------------------------------------------
    # Raw message dispatch (per session)
    # ------------------------------------------------------------------

    async def _handle_raw_for_session(self, session: _PerUinSession, raw: str) -> None:
        """
        Dispatch incoming WebSocket frames for a specific session.
        Mirrors: src/socket/handlers.ts (but with session context).
        """
        try:
            msg = json.loads(raw)
        except (json.JSONDecodeError, TypeError):
            return

        event = msg.get("event", "")
        data  = msg.get("data") or {}

        if event == EVENT_HANDSHAKE:
            session.socket_id = data.get("id", "")
            logger.info(
                "[lightclaw uin=%s] Handshake, socket_id=%s",
                session.uin or "?", session.socket_id,
            )
            return

        if event == EVENT_MESSAGE_ACK:
            related = data.get("relatedMsgId", "")
            logger.debug(
                "[lightclaw uin=%s] ACK received: relatedMsgId=%s",
                session.uin or "?", related,
            )
            if related:
                session.on_ws_ack(related)
            return

        if event == EVENT_MESSAGE_PRIVATE:
            # 维护 chat_id → uin 路由表：发件人就是后续 outbound 的目标 chat_id
            sender = data.get("from") or ""
            if sender and session.uin:
                self._chat_to_uin[sender] = session.uin

            # ── file:download signalling — separate from the AI pipeline ──
            # The front-end issues `kind=file:download, status=download_req`
            # when the user clicks on a `localfile://` markdown link.  We
            # handle it inline, never forwarding to handle_message().
            if data.get("kind") == KIND_FILE_DOWNLOAD:
                td = (data.get("extra") or {}).get("transferData") or {}
                if td.get("status") == FileDownloadStatus.REQ:
                    asyncio.create_task(self._handle_file_download_req(data))
                # Any other status on a client→adapter frame is ignored:
                # ready / url / error are only ever sent adapter→client.
                return

            # Spawn as background task: handle_message triggers the full
            # agent pipeline (seconds to minutes), must not block the WS
            # read loop.  Matches TS: void (async () => { await handler(msg); })()
            asyncio.create_task(self._handle_incoming_message(data))
            return

        if event == EVENT_HISTORY_REQUEST:
            await self._handle_history_request(data)
            return

        if event == EVENT_SESSIONS_REQUEST:
            await self._handle_sessions_request(data)
            return

        if event == EVENT_CHAT_REQUEST:
            asyncio.create_task(self._handle_chat_request(data))
            return

        # agents:request — Agent 列表查询（只读，已在 IMEventType 中）
        if event == EVENT_AGENTS_REQUEST:
            await self._handle_agents_request(data)
            return

    # ------------------------------------------------------------------
    # Misc
    # ------------------------------------------------------------------

    async def get_chat_info(self, chat_id: str) -> dict:
        return {"name": f"LightClaw DM ({chat_id})", "type": "dm", "chat_id": chat_id}


# ---------------------------------------------------------------------------
# Module-level singleton accessor
# ---------------------------------------------------------------------------

_active_adapter: Optional[LightClawAdapter] = None


def _set_active_adapter(adapter: Optional[LightClawAdapter]) -> None:
    global _active_adapter
    _active_adapter = adapter


def get_active_adapter() -> Optional[LightClawAdapter]:
    """Return the running LightClawAdapter singleton, or None if not started."""
    return _active_adapter
