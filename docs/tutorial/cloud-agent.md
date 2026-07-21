# 如何指派與查看 GitHub Copilot Cloud Agent

## 指派前

Issue 必須有 `security:approved` 且沒有 `security:blocked`。Custom agent profile 必須已存在於目標 branch；repository-level agents 位於 `.github/agents/`。

## 從 GitHub 網頁指派

1. 打開 Safe Issue。
2. 在右側 `Assignees` 選擇 `Copilot`。
3. 在指派視窗選擇目標 repository、starting branch 與 `Flow Lab Implementer` custom agent。
4. 確認 additional instructions 沒有要求越過 Issue 範圍。
5. 送出後，Issue timeline 應出現 Copilot 反應與 draft PR。

## 從本地腳本指派

`scripts/create_demo_issue.py --scenario safe --create` 會在 Issue gate 通過後呼叫 GitHub Issue API，指派 `copilot-swe-agent[bot]`，並以 `custom_agent: implementer` 明確選用 repository custom agent。可用 `--base-branch` 與 `--custom-agent` 調整；網頁指派視窗也提供相同選擇。

## 查看 Agent session

1. 在 Issue timeline 打開 Copilot 建立的 PR。
2. 在 PR 的 `Copilot started work` 事件點選 `View session`。
3. 檢查 Agent 是否讀取 Issue、執行 tests，以及是否遇到 firewall 或 dependency 問題。
4. Agent 完成後檢查 commit 與 PR body，不要只看摘要。

Issue 指派後新增的 Issue comment 不會自動傳給該 session。需求變更請在 Copilot 建立的 open PR 留言並提及 `@copilot`。

## 必須知道的限制

- GitHub Actions 提供 Cloud Agent 的 ephemeral environment，但 workflow 本身不是 Agent。
- Public repository 目前不能使用 Copilot Automations，因此本 demo 不宣稱 Issue opened 會自動啟動另一個 cloud agent。
- 若指派者就是 repository 唯一維護者，GitHub 不允許該指派者正式 Approve Copilot 產生的 PR；需要第二位 collaborator 才能使用 required human approval。
