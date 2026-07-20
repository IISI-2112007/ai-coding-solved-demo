#!/usr/bin/env bash
set -uo pipefail

if npm run verify >/tmp/cloud-agent-quality-gate.log 2>&1; then
  printf '%s\n' '{"decision":"allow"}'
else
  printf '%s\n' '{"decision":"block","reason":"品質或 DOM XSS 檢核失敗。請執行 npm ci --ignore-scripts 與 npm run verify，閱讀失敗輸出並修正後再完成任務。"}'
fi
