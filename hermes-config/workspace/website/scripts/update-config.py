import json

# 读取配置文件
with open('/root/.openclaw/openclaw.json', 'r') as f:
    config = json.load(f)

# 添加 load 路径
if 'plugins' not in config:
    config['plugins'] = {}

config['plugins']['load'] = {
    'paths': ['skills/memory-lancedb-pro']
}

# 添加 memory-lancedb-pro 配置
if 'entries' not in config['plugins']:
    config['plugins']['entries'] = {}

config['plugins']['entries']['memory-lancedb-pro'] = {
    'enabled': True,
    'config': {
        'embedding': {
            'apiKey': '84b1936d14a84cfa83631aea1c78a56d.vQTK9kogx83kv2aQ',
            'model': 'embedding-2',
            'baseURL': 'https://open.bigmodel.cn/api/paas/v4',
            'dimensions': 1024
        },
        'dbPath': '~/.openclaw/memory/lancedb-pro',
        'autoCapture': True,
        'autoRecall': True,
        'retrieval': {
            'mode': 'hybrid',
            'vectorWeight': 0.7,
            'bm25Weight': 0.3,
            'topK': 5
        }
    }
}

# 保存配置文件
with open('/root/.openclaw/openclaw.json', 'w') as f:
    json.dump(config, f, indent=2)

print('✅ 配置修改完成')