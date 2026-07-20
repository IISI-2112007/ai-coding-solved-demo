# Cloud Agent Flow Lab Copilot Instructions

## Repository 目的

這是一個教學型 TypeScript MVP，用來真實展示：Local AI、GitHub Issue、Copilot cloud agent、Copilot code review、GitHub Actions 安全閘門、PR Preview 與 Human Review。

GitHub Actions 不是 cloud agent。Copilot code review 也不等於人類核准。

## 語言與範圍

- GitHub Issue、PR 說明、review comments、文件與畫面文字預設使用繁體中文。
- 只修改 Issue 允許範圍；不做無關重構，不刪除歷史 demo 證據。
- 不自動 merge。人類 reviewer 保留最後決定權。

## 開發標準

- Runtime：Node.js 20.19 以上；CI 使用 Node.js 24。
- App：Vite + TypeScript；domain logic 放在 `src/flow.ts` 等可測試模組。
- Render：使用 `textContent`、`createElement`、`replaceChildren` 等安全 DOM API。
- 禁止：`innerHTML` 指派、`outerHTML` 指派、`insertAdjacentHTML`、`document.write`、`eval`、`new Function`。
- 不得用 URL／query parameter／前端狀態單獨決定可信權限。
- 新行為需補 Vitest；所有變更需通過 `npm run verify`。

## Copilot code review 安全要求

Review 時讀取 `docs/security/owasp-top-10-2025-checklist.md`，逐項考慮 OWASP Top 10:2025。發現問題時，以繁體中文列出：

1. OWASP 分類。
2. 嚴重度。
3. 具體檔案或行為證據。
4. 影響。
5. 修正建議。
6. 是否應阻擋：`BLOCK` 或 `ADVISORY`。

Broken Access Control、Injection、真實 secret、停用安全 checks、繞過人類審查或未處理的 High finding 一律標示 `BLOCK`。

Copilot review 只能提供 Comment，不得描述成已核准或已阻擋 GitHub merge；是否可合併由 required checks 與人類 reviewer 決定。
