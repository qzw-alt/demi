# ============================================================
# Git Push Helper — GitHub via local proxy (port 10808)
# ============================================================
# Usage: dot-source this script, then push any repo:
#   . .\git-push-helper.ps1
#   Push-GitHub -RepoPath "C:\path\to\repo" -Branch "main"
# ============================================================

$Script:__ProxyPort = 10808
$Script:__GitHubToken = $null

function Set-GitHubToken { param([string]$Token) $Script:__GitHubToken = $Token }

function Push-GitHub {
    param(
        [Parameter(Mandatory)] [string]$RepoPath,
        [string]$Branch = "master",
        [string]$Remote = "origin"
    )
    if (-not $Script:__GitHubToken) { Write-Error "Run Set-GitHubToken first"; return }
    $env:http_proxy  = "http://127.0.0.1:$Script:__ProxyPort"
    $env:https_proxy = "http://127.0.0.1:$Script:__ProxyPort"
    $env:NO_PROXY    = ""
    $basic = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes("x:$Script:__GitHubToken"))
    git -C $RepoPath -c http.sslBackend=openssl -c http.extraheader="Authorization: Basic $basic" push $Remote $Branch
}

# Also: clone helper
function Clone-GitHub {
    param(
        [Parameter(Mandatory)] [string]$RepoUrl,
        [Parameter(Mandatory)] [string]$DestPath
    )
    $env:http_proxy  = "http://127.0.0.1:$Script:__ProxyPort"
    $env:https_proxy = "http://127.0.0.1:$Script:__ProxyPort"
    $env:NO_PROXY    = ""
    git -c http.sslBackend=openssl clone $RepoUrl $DestPath
}

Write-Host "[git-push-helper] Loaded. Commands: Push-GitHub, Clone-GitHub"
