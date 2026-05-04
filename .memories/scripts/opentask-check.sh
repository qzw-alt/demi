#!/bin/bash
# 检查OpenTask新任务的脚本

OPENTASK_TOKEN="ot_1f4dddf923c1b987038969aa95ea898450c0900ec5d8959c5682d1082e834e91"

echo "=== 检查OpenTask新任务 ==="
echo "时间: $(date)"

# 获取最新任务
response=$(curl -s "https://opentask.ai/api/tasks?sort=new&limit=10")

# 检查是否有我可以投标的新任务
echo "$response" | python3 -c "
import sys, json

d = json.load(sys.stdin)
tasks = d.get('tasks', [])

print(f'发现 {len(tasks)} 个最新任务')

my_skills = ['python', 'automation', 'bot', 'telegram', 'web', 'development', 'code', 'data', 'analysis', 'writing', 'content', 'medical', 'health']

for t in tasks:
    title = t.get('title', '').lower()
    budget = t.get('budgetText', '面议')
    task_id = t.get('id')
    
    # 检查是否匹配我的技能
    matched = any(skill in title for skill in my_skills)
    
    if matched:
        print(f'\\n🎯 匹配任务!')
        print(f'   标题: {t.get(\"title\")}')
        print(f'   预算: {budget}')
        print(f'   ID: {task_id}')
        print(f'   链接: https://opentask.ai/task/{task_id}')
" 2>/dev/null

echo ""
echo "=== 检查完成 ==="
