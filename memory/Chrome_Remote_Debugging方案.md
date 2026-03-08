# Chrome Remote Debugging - 浏览器自动化方案

> 来源：伟烨发现 | 日期：2026-02-25

## 背景
OpenClaw自带的浏览器控制（agent browser、Playwright MCP等）效果不太好，伟烨发现用Chrome Remote Debugging模式效果更佳。

## 方案原理
用Chrome的 `--remote-debugging-port` 模式启动浏览器，让AI直接操作一个真实浏览器实例。

## 优势
- ✅ 权限高，能做上传视频/图片等复杂操作
- ✅ 行为更像真人，不容易被平台检测
- ✅ 比各种MCP方案稳定

## 风险
- ⚠️ 权限给的高有风险
- 建议：使用专门的操作账号/机器，不要登录有敏感信息的账号

## Windows启动命令示例
```bash
chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\chrome-profile"
```

## Mac/Linux启动
```bash
google-chrome --remote-debugging-port=9222 --user-data-dir=~/chrome-profile
```

## 连接方式
- 端口：9222
- 通过CDP协议连接
- OpenClaw可通过浏览器配置连接

## 适用场景
- TK自动化发布
- 亚马逊前台操作
- 批量上传视频/图片
- 评论回复自动化

## 注意事项
1. 一台专门的电脑只登录营销账号
2. 不要登录个人敏感账号
3. IP保持稳定

---

*备注：服务器端已安装Puppeteer，也可实现基础浏览器自动化*
