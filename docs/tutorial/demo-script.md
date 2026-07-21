# Safe／Unsafe 完整 Demo 腳本

## Demo 前檢查

```powershell
gh auth status
npm ci --ignore-scripts
npm run verify
python scripts/create_demo_issue.py --scenario safe --dry-run
python scripts/create_demo_issue.py --scenario unsafe --dry-run
```

## 第一幕：Unsafe Issue 被擋下

1. 執行 `python scripts/create_demo_issue.py --scenario unsafe --create`。
2. 打開新 Issue，看 `Issue Security Intake` run。
3. 確認 Issue 具有 `security:blocked`。
4. 確認留言映射 A01 與 A05，且 Assignees 沒有 Copilot。
5. 說明這裡是 deterministic Issue gate，不是假裝 AI reviewer。

## 第二幕：Safe Issue 交給真正 Cloud Agent

1. 執行 `python scripts/create_demo_issue.py --scenario safe --create`。
2. 確認先出現 `security:pending`，再變成 `security:approved`。
3. 確認腳本之後才指派 `implementer` custom agent。
4. 在 Issue／PR timeline 打開 `View session`，證明是 Copilot cloud agent。
5. 等 Copilot 開 PR，檢查 commit、diff 與繁體中文說明。

## 第三幕：AI、Actions、Preview 與人類

1. 要求 Copilot code review，查看 OWASP finding 格式。
2. 等 `Security Gate` 的三個 jobs 完成。
3. 打開 PR comment 中的 Preview URL，確認 HTTP 200 並操作功能。
4. 用 [人類 PR 審查](human-pr-review.md) 的六個步驟判斷。
5. 不在 Demo 中自動 merge；停在 Request changes 或人工 merge 決定。

## Demo 成功證據

- Unsafe Issue URL、blocked label、初審留言、未指派狀態。
- Safe Issue URL、Copilot assignee、Agent session、PR URL。
- Copilot review、三個 Security Gate jobs、Preview URL 與 HTTP 200。
- 人類最終決定紀錄。
