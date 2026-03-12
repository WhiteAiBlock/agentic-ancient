#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
LOG_FILE="$ROOT_DIR/MANUS_EXECUTION_LOGS.md"
TMP_LOG="$ROOT_DIR/.manus_exec_tmp.log"
: > "$TMP_LOG"

run_cmd() {
  local label="$1"
  local cmd="$2"
  echo "\n### ${label}" >> "$TMP_LOG"
  echo '```bash' >> "$TMP_LOG"
  echo "$cmd" >> "$TMP_LOG"
  echo '```' >> "$TMP_LOG"
  echo '```text' >> "$TMP_LOG"
  if timeout 25s bash -lc "$cmd" >> "$TMP_LOG" 2>&1; then
    echo "[status] PASS" >> "$TMP_LOG"
  else
    code=$?
    echo "[status] FAIL (exit ${code})" >> "$TMP_LOG"
  fi
  echo '```' >> "$TMP_LOG"
}

{
  echo "# Manus/ClawAi Commit Re-execution Logs"
  echo
  echo "Generated: $(date -u '+%Y-%m-%d %H:%M:%S UTC')"
  echo
  echo "## 1) Commit scan (authors matching Manus/ClawAi)"
  echo '```bash'
  echo "git log --pretty=format:'%h | %an | %ad | %s' --date=iso --all --author='Manus\\|ClawAi'"
  echo '```'
  echo '```text'
  git log --pretty=format:'%h | %an | %ad | %s' --date=iso --all --author='Manus\|ClawAi'
  echo '```'
  echo
  echo "## 2) Re-executed method checks (best-effort, safe mode)"
} > "$LOG_FILE"

run_cmd "Python method: self_learning_engine help" "python3 self_learning_engine.py --help"
run_cmd "Python method: webhook_reader help" "python3 webhook_reader.py --help"
run_cmd "Python method: run_ralph_terminal help" "python3 run_ralph_terminal.py --help"
run_cmd "Python method: clawai_solana_agent help" "python3 clawai_solana_agent.py --help"
run_cmd "Python method: solana tax engine help" "python3 skills/solana-tax/scripts/tax_engine.py --help"
run_cmd "Python method: clawai tax integration dry run" "python3 skills/solana-tax/scripts/clawai_integration.py"
run_cmd "Shell method syntax-check: execute_ralph_cloud" "bash -n execute_ralph_cloud.sh"
run_cmd "Shell method syntax-check: start_clawai" "bash -n start_clawai.sh"
run_cmd "TypeScript compile-check: cryptogene_deployer" "npx tsc --noEmit cryptogene_deployer.ts"
run_cmd "Node method check: run-ralph.js" "node --check run-ralph.js"

cat "$TMP_LOG" >> "$LOG_FILE"
rm -f "$TMP_LOG"

echo "Wrote $LOG_FILE"
