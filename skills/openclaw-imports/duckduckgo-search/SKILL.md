---
name: duckduckgo-search
description: Performs web searches using DuckDuckGo to retrieve real-time information from the internet. Use when the user needs to search for current events, documentation, tutorials, or any information that requires web search capabilities.
allowed-tools: Bash(duckduckgo-search:*), Bash(python:*), Bash(pip:*), Bash(uv:*)
---

# DuckDuckGo Web Search Skill

这个技能通过 DuckDuckGo 搜索引擎实现网络搜索功能，帮助获取实时信息。

## 功能特性

- 🔍 基于 DuckDuckGo 的隐私友好型搜索
- 📰 支持新闻搜索
- 🖼️ 支持图片搜索
- 📹 支持视频搜索
- 🌐 无需 API Key，免费使用
- 🔒 保护隐私，不追踪用户

## 安装

```bash
# 使用 uv 安装（推荐）
uv pip install ddgs

# 或使用 pip 安装
pip install ddgs
```

## ⚠️ 重要：包已更名

**2024年起，`duckduckgo_search` 已更名为 `ddgs`。**
旧包 (`pip install duckduckgo-search`) 可能仍能用，但新包 (`pip install ddgs`) 是官方推荐。

导入方式：
```python
# ❌ 旧方式（可能已弃用）
from duckduckgo_search import DDGS

# ✅ 新方式（推荐）
from ddgs.text import text     # 文本搜索
from ddgs.images import images # 图片搜索
from ddgs.news import news     # 新闻搜索
```

## 快速开始

### 命令行方式（需要先激活正确的Python环境）

```bash
```bash
# 搜索示例
source ~/.hermes/hermes-agent/venv/bin/activate
python -c "
from ddgs.text import text

query = 'your search query'
for r in text(query, max_results=10):
    print(r['title'])
    print(r['href'])
    print(r['body'][:100])
    print()
"
```

## 搜索类型

### 1. 文本搜索 (Text Search)

最常用的搜索方式，返回网页结果：

```bash
python -c "
from ddgs.text import text

query = 'your search query'
for r in text(query, max_results=10):
    print(r['title'])
    print(f\"   URL: {r['href']}\")
    print(f\"   摘要: {r['body'][:100]}...\")
    print()
"
```

### 2. 新闻搜索 (News Search)

搜索最新新闻：

```bash
python -c "
from ddgs.news import news

for r in news('AI technology', max_results=10):
    print(r['title'])
    print(f\"   来源: {r['source']}\")
    print(f\"   时间: {r.get('date', 'N/A')}\")
    print(f\"   链接: {r['url']}\")
    print()
"
```

### 3. 图片搜索 (Image Search)

搜索图片资源：

```bash
python -c "
from ddgs.images import images

for r in images('cute cats', max_results=10):
    print(r['title'])
    print(f\"   图片: {r['image']}\")
    print(f\"   来源: {r['source']}\")
    print()
"
```

### 4. 视频搜索 (Video Search)

搜索视频内容：

```bash
python -c "
from ddgs.videos import videos

for r in videos('Python programming', max_results=10):
    print(r['title'])
    print(f\"   时长: {r.get('duration', 'N/A')}\")
    print(f\"   来源: {r['publisher']}\")
    print(f\"   链接: {r['content']}\")
    print()
"
```

### 5. 即时回答 (Instant Answers)

获取 DuckDuckGo 的即时回答：

```bash
python -c "
from ddgs.answers import answers

for r in answers('what is python programming language'):
    print(r['text'])
"
```

### 6. 建议搜索 (Suggestions)

获取搜索建议：

```bash
python -c "
from ddgs.suggestions import suggestions

for s in suggestions('python'):
    print(s['phrase'])
"
```

### 7. 地图搜索 (Maps Search)

搜索地点信息：

```bash
python -c "
from ddgs.maps import maps

for r in maps('coffee shop', place='Beijing, China', max_results=10):
    print(r['title'])
    print(f\"   地址: {r['address']}\")
    print(f\"   电话: {r.get('phone', 'N/A')}\")
    print()
"
```

## 实用脚本

### 通用搜索函数

创建一个可复用的搜索脚本：

```bash
python -c "
from ddgs.text import text
from ddgs.news import news

def web_search(query, search_type='text', max_results=5):
    '''
    执行 DuckDuckGo 搜索
    '''
    if search_type == 'text':
        return list(text(query, max_results=max_results))
    elif search_type == 'news':
        return list(news(query, max_results=max_results))
    return []

# 使用示例
for r in web_search('Python 3.12 new features', max_results=5):
    print(r['title'])
    print(r['href'])
"
```

### 多关键词批量搜索

```bash
python -c "
from ddgs.text import text
import time

queries = [
    'Python best practices 2024',
    'React vs Vue 2024',
    'AI development tools'
]

for query in queries:
    print(f'搜索: {query}')
    results = list(text(query, max_results=3))
    print(f'   找到 {len(results)} 个结果')
    time.sleep(1)  # 避免请求过快
"
```

## 参数说明

### 地区代码 (region)

| 代码 | 地区 |
|------|------|
| `cn-zh` | 中国 |
| `us-en` | 美国 |
| `uk-en` | 英国 |
| `jp-jp` | 日本 |
| `kr-kr` | 韩国 |
| `wt-wt` | 全球 (无地区限制) |

### 时间限制 (timelimit)

| 值 | 含义 |
|----|------|
| `d` | 过去 24 小时 |
| `w` | 过去一周 |
| `m` | 过去一月 |
| `y` | 过去一年 |
| `None` | 不限制 |

### 安全搜索 (safesearch)

| 值 | 含义 |
|----|------|
| `on` | 严格过滤 |
| `moderate` | 适度过滤 (默认) |
| `off` | 关闭过滤 |

## 错误处理

```bash
python -c "
from duckduckgo_search import DDGS
from duckduckgo_search.exceptions import DuckDuckGoSearchException

try:
    with DDGS() as ddgs:
        results = list(ddgs.text('test query', max_results=5))
        print(f'✅ 搜索成功，找到 {len(results)} 个结果')
except DuckDuckGoSearchException as e:
    print(f'❌ 搜索出错: {e}')
except Exception as e:
    print(f'❌ 未知错误: {e}')
"
```

## 使用代理

如果需要使用代理：

```bash
python -c "
from duckduckgo_search import DDGS

# 设置代理
proxy = 'http://127.0.0.1:7890'  # 替换为你的代理地址

with DDGS(proxy=proxy) as ddgs:
    results = list(ddgs.text('test query', max_results=5))
    print(f'通过代理搜索成功，找到 {len(results)} 个结果')
"
```

## 常见问题

**搜索返回空结果？**
```bash
# 1. 检查包是否已安装
pip show ddgs

# 2. 如果报错找不到包，尝试安装
pip install ddgs

# 3. 确保使用正确的 Python 环境
source ~/.hermes/hermes-agent/venv/bin/activate

# 4. 验证安装
python -c "from ddgs.text import text; print(list(text('test', max_results=1)))"
```

**安装失败？**
```bash
# 确保 pip 是最新版本
pip install --upgrade pip
pip install ddgs
```

**请求被限制？**
```bash
# 添加延迟避免过快请求
import time
time.sleep(1)
```

## 备选方案：当 ddgs 失败时

如果 `ddgs` 搜索返回空结果（或需要获取更详细页面内容），使用浏览器方式：

### 方案A：Bing HTML 搜索（无需登录）
```
# 使用 lite.duckduckgo.com（轻量版，避免 Cloudflare）
https://lite.duckduckgo.com/50x/?q=your+search+query

# 或使用 Bing（注意可能被 Cloudflare 拦截）
https://www.bing.com/search?q=your+search+query
```

### 方案B：Browserbase 抓取（已配置时）
使用 `browser_navigate` + `browser_snapshot` 访问搜索结果页面。

### 方案C：直接访问竞品网站
当需要分析竞品网站结构时，直接用浏览器访问：
```
browser_navigate → https://competitor-site.com
browser_snapshot → 查看页面元素
browser_vision → 获取视觉截图
```

## 与其他工具集成

### 结合 browser 获取详细内容

```bash
# 1. 用 ddgs 搜索获取 URL
source ~/.hermes/hermes-agent/venv/bin/activate
python -c "
from ddgs.text import text
for r in text('medical tourism Thailand', max_results=5):
    print(r['href'])
"

# 2. 用浏览器打开并分析
browser_navigate → <URL from search>
browser_snapshot → 获取页面结构
browser_vision → 获取视觉截图
```

## 注意事项

⚠️ **使用建议**：

1. **遵守使用频率限制**：避免短时间内大量请求
2. **合理设置结果数量**：不要一次请求过多结果
3. **添加适当延迟**：批量搜索时在请求之间添加 `time.sleep()`
4. **处理异常情况**：始终添加错误处理代码
5. **尊重版权**：搜索结果仅供参考，注意内容版权
