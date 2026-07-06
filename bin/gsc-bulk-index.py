#!/usr/bin/env python3
"""
GSC Full-Scope 自动化 (token 升级后跑)
1. 提交 sitemap
2. URL Inspection 70 个 URL 索引请求
"""
import os
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

TOK = os.path.expanduser("~/.hermes/gsc/token.json")
SCOPES = ["https://www.googleapis.com/auth/webmasters"]  # FULL scope
creds = Credentials.from_authorized_user_file(TOK, scopes=SCOPES)
service = build("searchconsole", "v1", credentials=creds, cache_discovery=False)

SITE = "https://oriental-destiny.com/"

# 1. 提交 sitemap
print("[1] 提交 sitemap ...")
try:
    r = service.sitemaps().submit(siteUrl=SITE, feedpath="/sitemap.xml").execute()
    print(f"   ✓ Sitemap submitted: {r}")
except HttpError as e:
    print(f"   ✗ {e.resp.status}: {e.content.decode()[:300]}")

# 2. URL Inspection 索引请求
print("[2] URL Inspection 索引请求 ...")

# 拿所有应该被索引的 URL
urls_to_index = []
with open("/home/ubuntu/oriental-destiny/sitemap.xml") as f:
    import re
    for m in re.finditer(r"<loc>([^<]+)</loc>", f.read()):
        urls_to_index.append(m.group(1))

# 也补充错过的（即使不在 sitemap）
extra_urls = [
    "https://oriental-destiny.com/index.html",
    "https://oriental-destiny.com/kitchen-feng-shui-stove-wealth-corner.html",
    "https://oriental-destiny.com/living-room-feng-shui-tips.html",
    "https://oriental-destiny.com/bagua-map-guide.html",
    "https://oriental-destiny.com/feng-shui-bathroom.html",
    "https://oriental-destiny.com/hidden-stems-bazi.html",
    "https://oriental-destiny.com/bazi-chart-structure.html",
    "https://oriental-destiny.com/summer-and-the-fire-element-in-bazi.html",
    "https://oriental-destiny.com/summer-fire-element-bazi.html",
]
urls_to_index = sorted(set(urls_to_index + extra_urls))

# URL Inspection 的 subject 是 SITE URL (not domain), 直接用 absolute URLs
# inspect endpoint
print(f"   共 {len(urls_to_index)} 个 URL 待提交")
success = 0
failed = 0
err_messages = []
for i, url in enumerate(urls_to_index):
    if i % 10 == 0:
        print(f"   Progress: {i}/{len(urls_to_index)}")
    try:
        body = {
            "inspectionUrl": url,
            "siteUrl": SITE,
        }
        r = service.urlInspection().index().inspect(body=body).execute()
        if r.get("inspectionResult", {}).get("indexStatusResult", {}).get("verdict") == "PASS":
            success += 1
        else:
            failed += 1
            err_messages.append(f"{url}: {r.get('inspectionResult', {}).get('indexStatusResult', {}).get('verdict')}")
    except HttpError as e:
        if e.resp.status == 429:  # 配额超限
            print(f"   ⚠ 429 quota reached at {i}, 停止")
            break
        failed += 1
        if "PERMISSION_DENIED" not in e.content.decode():
            err_messages.append(f"{url}: {e.content.decode()[:200]}")

print(f"\n=== 结果 ===")
print(f"  ✓ success: {success}")
print(f"  ✗ failed: {failed}")
if err_messages[:5]:
    print(f"  错误示例: {err_messages[:5]}")
