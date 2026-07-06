# 第二階段：Copilot Cloud Agent

## 目標

第二階段要證明這條流程：

```text
本地端 AI -> GitHub Issue -> GitHub Copilot cloud agent -> Pull Request -> Human Review
```

第一階段的 GitHub Actions 只是 simulator。第二階段的重點是讓 GitHub Copilot cloud agent 真正從 Issue 接手，完成後建立 PR，最後仍由人類 reviewer 決定是否接受。

## 官方流程

GitHub 官方文件描述了三種相關入口：

- 從 GitHub Issue 指派給 Copilot cloud agent。
- 從 GitHub CLI 使用 `gh agent-task create` 建立 agent task。
- 從 IDE、mobile、API 等入口啟動 Copilot session。

本 repo 的第二階段採用 Issue 指派路線，因為它最符合 demo 需求：本地端 AI 建立 Issue，cloud agent 完成後開 PR，人類再審查。

## 前置條件

- GitHub CLI 已登入目前帳號。
- repo 已推上 GitHub。
- GitHub Copilot cloud agent 已在帳號與 repo 可用。
- repo 設定允許 Copilot cloud agent 接手 Issue。
- 使用者接受建立 Issue 並用 `@copilot` 指派方式可能會啟動 agent session。

## 建立 Issue

先 dry-run：

```powershell
python scripts/create_copilot_issue.py --repo IISI-2112007/ai-coding-solved-demo --dry-run
```

確認內容後建立：

```powershell
python scripts/create_copilot_issue.py --repo IISI-2112007/ai-coding-solved-demo --create
```

預設 Issue 內容會要求：

- Issue、PR 說明與新增文件使用繁體中文。
- Copilot cloud agent 開 PR，不直接 merge。
- reviewer 依照 Issue 的允許修改範圍檢查 diff。

## 追蹤結果

建立後可以用：

```powershell
& 'C:\Program Files\GitHub CLI\gh.exe' issue list --repo IISI-2112007/ai-coding-solved-demo --label copilot-cloud-agent:ready --limit 5
& 'C:\Program Files\GitHub CLI\gh.exe' pr list --repo IISI-2112007/ai-coding-solved-demo --state all --limit 10
```

如果目前 GitHub CLI 支援 `agent-task`，也可以查看：

```powershell
& 'C:\Program Files\GitHub CLI\gh.exe' agent-task list --repo IISI-2112007/ai-coding-solved-demo
```

## 與第一階段的差異

- 第一階段：`cloud-agent:ready` 觸發 GitHub Actions simulator。
- 第二階段：`copilot-cloud-agent:ready` 用於標記真正 Copilot cloud agent 任務。
- 第二階段不使用 `cloud-agent:ready`，避免 simulator 誤接手。

## 失敗時的判斷

如果 `--create` 失敗，通常代表其中一個條件尚未成立：

- 目前帳號或 repo 尚未啟用 Copilot cloud agent。
- `@copilot` 不能在這個 repo 建立 agent assignment。
- GitHub CLI 版本或 GitHub 端 API 行為已變更。
- repo 權限不足。

這時候仍可保留繁體中文 Issue，改由 GitHub 網頁手動指派給 Copilot，或改用 `gh agent-task create` 直接建立 cloud agent task。
