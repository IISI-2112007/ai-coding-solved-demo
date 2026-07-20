# GitHub Agent 能力與限制

最後查證日期：2026-07-20。

## 本專案採用的真實角色

1. GitHub Copilot cloud agent：從 Issue 接手程式修改並建立 PR。
2. GitHub Copilot code review：依 `.github/copilot-instructions.md` 與 OWASP checklist 提出 Comment review。
3. GitHub Actions：執行可重現且可設為 required check 的安全閘門。
4. Human reviewer：決定 Request changes、接受風險或 merge。

## 為何不宣稱兩個 Agent 自動核准

GitHub 支援 repository custom agents，Issue 指派時也能選擇 custom agent；但 GitHub.com 的 agent profile `handoffs` 目前不支援。Copilot code review 只會留下 Comment，不會產生 Approve 或 Request changes，也不會自行阻擋 merge。

因此本 MVP 不把「Implementer Agent → Security Reviewer Agent」描述成可信任的自動核准鏈。安全 Reviewer 提供判讀，Actions 與 branch rules 負責 enforcement，人類保留最後決定。

## Public repository 限制

Copilot Automations 可以在 Issue 或 PR 事件自動啟動 cloud agent，但目前只支援 private／internal repositories。本 repository 是 public，因此不使用 Automations 假裝自動 Agent 串接。

## 官方依據

- [Creating custom agents for Copilot cloud agent](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/create-custom-agents)
- [Custom agents configuration](https://docs.github.com/en/copilot/reference/custom-agents-configuration)
- [Using GitHub Copilot code review on GitHub](https://docs.github.com/en/copilot/how-tos/copilot-on-github/use-copilot-agents/copilot-code-review)
- [About Copilot automations](https://docs.github.com/en/copilot/concepts/agents/cloud-agent/about-automations)
