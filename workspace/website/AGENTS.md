# AGENTS.md — chinahospitalsguide.com

## GitHub Access
- Repo: https://github.com/qzw-alt/chinahospitalsguide
- Local proxy required: port 10808 (HTTP)
- Git SSL backend: openssl (schannel fails in sandbox)
- Push pattern: `git -c http.sslBackend=openssl push`
- Clone pattern: `git -c http.sslBackend=openssl clone`

### Helper Script
```powershell
. .\scripts\git-push-helper.ps1
Push-GitHub -RepoPath "C:\Users\csdm2\Documents\chinahospitalsguide.com\src"
```

## Tech Stack
- Static HTML site (pre-generated, not Jekyll-templated at runtime)
- Cloudflare Pages / Netlify deployment (uses `_redirects` file)
- Has `_layouts/`, `_includes/` (Nunjucks) for build-time generation

## SEO Context (from GSC data)
- 105 total clicks, ~45K monthly impressions, desktop CTR 0.08%
- 126 404 pages, 499+ unindexed pages (content quality issue May 2026)
- Top traffic: lasik, cataract, hospital rankings pages
- Ranking positions 5-9 average (need CTR improvement)
- Big zero-click problem on hospital ranking pages
