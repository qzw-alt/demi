"""AgentManager — 只读 Agent 列表查询，供 agents:request 使用。"""
import json, logging, os, threading
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)
_file_locks: Dict[str, threading.Lock] = {}
_lock = threading.Lock()

def _get_lock(path: str) -> threading.Lock:
    with _lock:
        if path not in _file_locks:
            _file_locks[path] = threading.Lock()
        return _file_locks[path]

class AgentManager:
    DEFAULT = [{"id":"main","name":"main","identity":{"name":"默认助手","emoji":"🤖"}}]

    def __init__(self, sessions_dir: str):
        self._path = os.path.join(sessions_dir, "agents.json")
        self._lock = _get_lock(self._path)

    def list(self) -> List[Dict[str, Any]]:
        with self._lock:
            try:
                with open(self._path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                agents = data.get("agents") if isinstance(data, dict) else data
                if isinstance(agents, list):
                    # 注入 soulId（从 lightsoul config 读取）
                    self._inject_soul_ids(agents)
                    return agents
            except FileNotFoundError:
                pass
            except (json.JSONDecodeError, OSError) as e:
                logger.warning("[agent_manager] read %s: %s", self._path, e)
            agents = [dict(a) for a in self.DEFAULT]
            self._inject_soul_ids(agents)
            os.makedirs(os.path.dirname(self._path), exist_ok=True)
            t = self._path + ".tmp"
            try:
                with open(t, "w", encoding="utf-8") as f:
                    json.dump({"agents": agents}, f, ensure_ascii=False, indent=2)
                    f.flush(); os.fsync(f.fileno())
                os.replace(t, self._path)
                logger.info("[agent_manager] init %s", self._path)
            except OSError: pass
            return agents

    def _inject_soul_ids(self, agents: List[Dict[str, Any]]) -> None:
        """从 lightsoul config 读取 agentId→soulId 映射，注入到 agent 条目。

        hermes_soul.sh 默认写入 $HOME/.config/lightsoul/config.json（XDG 标准路径），
        因此必须从同一路径读取，不能用 ~/.hermes/.config/lightsoul/config.json（hermes 旧路径）。
        """
        # hermes_soul.sh 默认写入路径（$HOME/.config/lightsoul/config.json）
        home = os.path.expanduser("~")
        ls_config = os.path.join(home, ".config", "lightsoul", "config.json")
        if not os.path.exists(ls_config):
            return
        try:
            with open(ls_config, "r", encoding="utf-8") as f:
                soul_map = json.load(f)
            if not isinstance(soul_map, dict):
                return
            for a in agents:
                sid = soul_map.get(a.get("id", ""))
                if sid:
                    a["soulId"] = sid
        except Exception:
            pass
