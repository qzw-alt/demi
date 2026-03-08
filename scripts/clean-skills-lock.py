import json

lock_file = '/root/.openclaw/workspace/skills/.skills_store_lock.json'
with open(lock_file, 'r') as f:
    data = json.load(f)

# 删除残留技能记录
skills_to_remove = ['find-skills', 'notion', 'obsidian', 'weather']
for skill in skills_to_remove:
    if skill in data.get('skills', {}):
        del data['skills'][skill]
        print(f"✅ 已从锁文件移除: {skill}")

with open(lock_file, 'w') as f:
    json.dump(data, f, indent=4)

print("✅ 锁文件已更新")