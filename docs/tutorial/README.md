# Cloud Agent Flow Lab 操作教學

本教學讓第一次接觸 repository 的人，在 10 至 15 分鐘內理解並操作完整流程。

## 建議閱讀順序

1. [完整架構](architecture.md)：先分清楚 Local AI、Cloud Agent、AI review、Actions 與人類。
2. [建立 Issue](create-issue.md)：學會寫出可交接、可阻擋的任務。
3. [Cloud Agent](cloud-agent.md)：指派真正的 GitHub Copilot cloud agent 並查看 session。
4. [AI 與 OWASP 審查](ai-security-review.md)：要求 Copilot code review 並解讀 findings。
5. [人類 PR 審查](human-pr-review.md)：先看 Preview，再看 diff、checks 與風險。
6. [完整 Demo 腳本](demo-script.md)：實際跑 Safe 與 Unsafe 兩條路徑。
7. [目前完成度](current-status.md)：確認哪些已有證據、哪些仍需人工動作。

## 最小操作

```powershell
npm ci --ignore-scripts
npm run verify
npm run dev
```

另一個終端執行：

```powershell
python scripts/create_demo_issue.py --scenario safe --dry-run
python scripts/create_demo_issue.py --scenario unsafe --dry-run
```

先閱讀 dry-run，再決定是否加上 `--create`。這個順序可避免把未檢查的 Issue 直接送到 GitHub。
