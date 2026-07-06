# How to verify a GSC token works for write operations

Verified 2026-07-06.

When the existing `~/.hermes/gsc/token.json` was created with `webmasters.readonly` scope, GSC read commands work (`summary`, `top queries`, `opportunities`, `trends`) but write commands fail with:

```
HTTPError 403: Request had insufficient authentication scopes.
{
  "error": {
    "code": 403,
    "message": "Request had insufficient authentication scopes.",
    "errors": [{"message": "Insufficient Permission"}],
    "status": "PERMISSION_DENIED"
  }
}
```

This affects:
- `service.sitemaps().submit(...)` — needed to push a sitemap into GSC
- `service.urlInspection().index().inspect(...)` — needed to request indexing of individual URLs

The verification recipe (3 commands):

```bash
# 1. Confirm what's in the token
python3 -c "import json; t=json.load(open('/home/ubuntu/.hermes/gsc/token.json')); print(t.get('scopes'))"

# Expected (readonly):
# ['https://www.googleapis.com/auth/webmasters.readonly']
#
# Expected (after upgrade):
# ['https://www.googleapis.com/auth/webmasters']

# 2. List the verified sites (works with readonly)
python3 -c "
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
TOK = '/home/ubuntu/.hermes/gsc/token.json'
creds = Credentials.from_authorized_user_file(TOK, scopes=['https://www.googleapis.com/auth/webmasters.readonly'])
service = build('searchconsole', 'v1', credentials=creds, cache_discovery=False)
print([s['siteUrl'] for s in service.sites().list().execute().get('siteEntry', [])])
"
# Expected: ['https://oriental-destiny.com/', 'sc-domain:chinahospitalsguide.com', 'https://chinahospitalsguide.com/']

# 3. Try a write operation — if it 403s, the token is still readonly
python3 -c "
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
TOK = '/home/ubuntu/.hermes/gsc/token.json'
creds = Credentials.from_authorized_user_file(TOK, scopes=['https://www.googleapis.com/auth/webmasters'])
service = build('searchconsole', 'v1', credentials=creds, cache_discovery=False)
try:
    service.sitemaps().submit(siteUrl='https://oriental-destiny.com/', feedpath='/sitemap.xml').execute()
    print('WRITE_OK: sitemap submitted')
except Exception as e:
    print(f'WRITE_FAIL: {type(e).__name__}: {e}')
"
```

If step 3 fails with 403, the token is readonly and needs upgrade.

## Multi-site token scope (verified 2026-07-06)

The token scopes to `webmasters.readonly` (or `webmasters` after upgrade) work across **every site the user account has verified** on Google Search Console. The same token can:

- Pull GSC data from oriental-destiny.com AND chinahospitalsguide.com (and any other verified site)
- Submit sitemaps to all of them
- Request URL Inspection for URLs on any of them

This means **one token per user account** is enough for all sites. The earlier pattern of "copy `~/.hermes/bin/gsc` to `gsco` and change SITE constant" assumes one token per site — actually you only need ONE token per user account. The script-copy is just for separating the SITE constant so you don't have to pass it as an argument every call.

## Best practice: which scope to use for read scripts

For read-only monitoring scripts (`summary`, `top q`, `top p`, `opportunities`, `trends`):

- **`webmasters.readonly` is preferred** — least-privilege principle, no write capability accidentally exercised
- Use `~/.hermes/bin/gsc` and `~/.hermes/bin/gsco` as-is — they declare `readonly` scope in the auth, so they CAN'T write even if a bug tries to

For write scripts (`submit sitemap`, `bulk URL Inspection request`):

- **`webmasters` (full) is required** — the API will 403 with `readonly`
- After upgrading, ALL scripts in `~/.hermes/bin/` that share the same token will gain write capability. This is fine for trusted scripts; it's risky for any script that takes untrusted input.
- Recommend: keep `gsc` and `gsco` on `webmasters.readonly` for daily monitoring, AND have a separate `gsc-submit-sitemap` / `gsc-bulk-index` that uses the upgraded `webmasters` token.

The simplest safe pattern: one token, full scope. `readonly` reads work fine with full-scope tokens too — the API doesn't downgrade. The cost is one OAuth flow instead of two.