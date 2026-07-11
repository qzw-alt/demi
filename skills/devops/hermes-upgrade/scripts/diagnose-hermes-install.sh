#!/bin/bash
# diagnose-hermes-install.sh
# One-shot diagnosis of HOW Hermes Agent was installed on this machine.
# Output drives the upgrade-path decision in hermes-upgrade skill.
#
# Usage: bash diagnose-hermes-install.sh
#        bash diagnose-hermes-install.sh --json    (machine-readable output)

set -e

JSON_MODE=0
[ "${1:-}" = "--json" ] && JSON_MODE=1

# Helper: emit a key/value line. JSON mode emits {"key": "value"} lines;
# text mode emits "KEY: value".
emit() {
  local key="$1"
  local val="$2"
  if [ "$JSON_MODE" = "1" ]; then
    val_escaped=$(printf '%s' "$val" | python3 -c 'import sys,json; print(json.dumps(sys.stdin.read()))')
    echo "  \"$key\": $val_escaped"
  else
    echo "$key: $val"
  fi
}

if [ "$JSON_MODE" = "1" ]; then echo "{"; fi

# 1. Current version
VERSION=$(hermes --version 2>/dev/null | head -1 | sed 's/Hermes Agent v//; s/ .*//')
emit "current_version" "${VERSION:-unknown}"

# 2. Hermes binary location
HERMES_BIN=$(which hermes 2>/dev/null || echo "not-found")
emit "hermes_binary" "$HERMES_BIN"

# 3. Hermes source tree state
SOURCE_DIR="$HOME/.hermes/hermes-agent"
if [ ! -d "$SOURCE_DIR" ]; then
  STATE="ABSENT"
  SIZE="0"
  Mtime=""
elif [ -d "$SOURCE_DIR/.git" ]; then
  STATE="GIT_REPO"
  SIZE=$(du -sh "$SOURCE_DIR" 2>/dev/null | cut -f1)
  Mtime=$(stat -c '%y' "$SOURCE_DIR" 2>/dev/null)
else
  STATE="NON_GIT_SOURCE_TREE"
  SIZE=$(du -sh "$SOURCE_DIR" 2>/dev/null | cut -f1)
  Mtime=$(stat -c '%y' "$SOURCE_DIR" 2>/dev/null)
fi
emit "source_state" "$STATE"
emit "source_dir" "$SOURCE_DIR"
emit "source_size" "$SIZE"
emit "source_mtime" "${Mtime:-n/a}"

# 4. pip status
PIP_PKG=$(pip show hermes-agent 2>/dev/null | grep -E "^Version:" | awk '{print $2}')
if [ -n "$PIP_PKG" ]; then
  emit "pip_installed" "yes"
  emit "pip_version" "$PIP_PKG"
else
  emit "pip_installed" "no"
fi

# 5. Disk space at ~/.hermes
DISK_FREE=$(df -h "$HOME/.hermes" 2>/dev/null | tail -1 | awk '{print $4}')
emit "disk_free_at_hermes" "${DISK_FREE:-unknown}"

# 6. Recommendation (text mode only)
if [ "$JSON_MODE" = "0" ]; then
  echo ""
  echo "--- RECOMMENDED UPGRADE PATH ---"
  case "$STATE" in
    GIT_REPO)
      echo "State: GIT_REPO — installed via git clone"
      echo "Path:  hermes update (will git pull)"
      ;;
    NON_GIT_SOURCE_TREE)
      echo "State: NON_GIT_SOURCE_TREE — installed via installer or manual extract"
      echo "        No .git/ directory; both 'hermes update' and 'install.sh' will fail."
      echo "Path:  Backup the source tree, then run installer:"
      echo "         mv ~/.hermes/hermes-agent ~/.hermes/hermes-agent.bak-\$(date +%Y%m%d-%H%M%S)"
      echo "         curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash -s -- --skip-setup"
      if [ -n "$SIZE" ] && [ "$SIZE" != "0" ]; then
        echo "        (Old tree size: $SIZE — make sure disk has space for the backup)"
      fi
      ;;
    PIP_ONLY|ABSENT)
      if [ "$STATE" = "ABSENT" ]; then
        echo "State: ABSENT — no source tree, only pip package"
        echo "Path:  pip install --upgrade hermes-agent"
      else
        echo "State: PIP_ONLY — installed via pip"
        echo "Path:  pip install --upgrade hermes-agent"
      fi
      ;;
  esac
  echo ""
  echo "--- POST-UPGRADE VERIFICATION ---"
  echo "  hermes --version"
  echo "  hermes doctor"
  echo "  hermes config check"
  echo "  hermes gateway restart   (if running)"
  echo "  /new                     (in chat: start fresh session for cache)"
else
  echo "}"
fi
