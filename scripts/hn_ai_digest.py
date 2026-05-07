#!/usr/bin/env python3
"""
Hacker News AI 热门速览
- 抓取 Top 30 帖子
- 筛选 AI/ML/编程 相关内容
- 按热度排序，输出摘要
"""

import json
import urllib.request
import time
import sys
from datetime import datetime

# AI 相关关键词（不区分大小写）
AI_KEYWORDS = [
    'ai', 'artificial intelligence', 'machine learning', 'ml',
    'llm', 'gpt', 'claude', 'openai', 'anthropic', 'google deepmind',
    'neural', 'deep learning', 'transformer', 'nlp', 'nlu',
    'agent', 'rag', 'embedding', 'inference', 'training',
    'model', 'models', 'benchmark', 'vision', 'multimodal',
    'langchain', 'rag', 'copilot', 'cursor', 'vibe coding',
    'hugging face', 'mistral', 'llama', 'gemini', 'copilot',
    'stable diffusion', 'diffusion', 'sora', 'video generation',
    'automation', 'autonomous', 'agent', 'reasoning', 'reasoner',
    'swe-bench', 'coding', 'programming', 'developer tools'
]

def fetch_top_stories(limit=30):
    """获取 HN Top Stories"""
    try:
        with urllib.request.urlopen('https://hacker-news.firebaseio.com/v0/topstories.json', timeout=10) as r:
            ids = json.loads(r.read())
        return ids[:limit]
    except Exception as e:
        print(f"Error fetching top stories: {e}", file=sys.stderr)
        return []

def fetch_item(item_id):
    """获取单个帖子详情"""
    try:
        with urllib.request.urlopen(f'https://hacker-news.firebaseio.com/v0/item/{item_id}.json', timeout=5) as r:
            return json.loads(r.read())
    except:
        return None

def is_ai_related(title, url=''):
    """判断是否是 AI 相关内容"""
    text = (title + ' ' + url).lower()
    return any(kw in text for kw in AI_KEYWORDS)

def score_ai_relevance(title, url=''):
    """给 AI 相关性打分，用于排序"""
    text = (title + ' ' + url).lower()
    score = 0
    high_value = ['openai', 'anthropic', 'google deepmind', 'claude', 'gpt', 'llm', 'agent', 'reasoning']
    medium_value = ['ai', 'machine learning', 'neural', 'model', 'benchmark']
    
    for kw in high_value:
        if kw in text: score += 10
    for kw in medium_value:
        if kw in text: score += 5
    return score

def main():
    print(f"🔍 HN AI Digest - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    # 获取 Top 30
    ids = fetch_top_stories(30)
    print(f"获取到 {len(ids)} 个帖子...", file=sys.stderr)
    
    # 获取详情并筛选
    ai_posts = []
    for i, item_id in enumerate(ids):
        item = fetch_item(item_id)
        if not item or not item.get('title'):
            continue
        
        title = item['title']
        url = item.get('url', '')
        score = item.get('score', 0)
        
        if is_ai_related(title, url):
            ai_score = score_ai_relevance(title, url)
            ai_posts.append({
                'id': item_id,
                'title': title,
                'url': url,
                'hn_score': score,
                'ai_score': ai_score,
                'author': item.get('by', ''),
                'comments': item.get('descendants', 0)
            })
        
        # 避免请求过快
        if i % 5 == 0:
            time.sleep(0.2)
    
    # 按 AI 相关性 + HN 热度排序
    ai_posts.sort(key=lambda x: x['ai_score'] * 100 + x['hn_score'], reverse=True)
    
    print(f"\n找到 {len(ai_posts)} 个 AI 相关帖子\n")
    
    if not ai_posts:
        print("今天没有找到足够多 AI 相关的热门帖子")
        return
    
    # 输出 Top 8
    output = []
    output.append(f"🔥 HN AI 热门速览")
    output.append(f"📅 {datetime.now().strftime('%Y-%m-%d')}\n")
    
    for i, p in enumerate(ai_posts[:8], 1):
        domain = ''
        if p['url']:
            domain = p['url'].split('/')[2] if '://' in p['url'] else ''
            domain = f"({domain})"
        
        output.append(f"{i}. ↑{p['hn_score']} | 💬{p['comments']}")
        output.append(f"   {p['title']}")
        if domain:
            output.append(f"   {domain}")
        output.append("")
    
    # 推荐阅读
    top3 = ai_posts[:3]
    if top3:
        output.append("💡 值得一看:")
        for p in top3:
            output.append(f"   • {p['title']} (↑{p['hn_score']})")
    
    print('\n'.join(output))

if __name__ == '__main__':
    main()
