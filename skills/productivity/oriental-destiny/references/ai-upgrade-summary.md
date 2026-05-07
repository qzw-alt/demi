# Oriental Destiny — AI 底层升级技术规格
## 2026-05-02 v1

Full spec lives in: `/root/.hermes/workspace/oriental-destiny/docs/TECH_SPEC.md`

## Summary

- **目标**: 静态模板 → AI 动态推理 + 个性化生成
- **模型**: DeepSeek V4 (deepseek-chat)
- **计算层**: 复杂五行链式推理（temperature=0.3）
- **解读层**: 英文个性化文案生成（temperature=0.8）
- **成本**: 自有 API Key，客户端直连
- **回退**: API 失败静默回退静态文案

## Phase Status

- [x] Phase 1 基础设施 (api_deepseek.js, ai_bazi_layer.js, prompts/)
- [ ] Phase 2 计算层实现 (analyzeChart)
- [ ] Phase 3 解读层实现 (generateReading)
- [ ] Phase 4 页面接入 (instant_reading, full_bazi_reading, report_demo)
