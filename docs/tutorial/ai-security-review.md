# 如何執行 AI 與 OWASP 審查

## 要求 Copilot code review

在 PR 頁面右側 `Reviewers` 對 Copilot 點選 `Request`，或執行：

```powershell
gh pr edit <PR-NUMBER> --repo IISI-2112007/ai-coding-solved-demo --add-reviewer @copilot
```

Copilot 會讀取 base branch 的 `.github/copilot-instructions.md`，並依 `docs/security/owasp-top-10-2025-checklist.md` 提出繁體中文 findings。

## Finding 應包含

- OWASP 分類。
- Critical、High、Medium 或 Low。
- 具體檔案、程式行為或 Issue 文字證據。
- 可能影響。
- 修正建議。
- `BLOCK` 或 `ADVISORY`。

## Copilot review 不會做的事

Copilot code review 固定留下 Comment，不會送出 Approve 或 Request changes，也不會算入 required approvals。因此：

- `BLOCK` 是給人類與維護者的明確建議。
- 真正的 merge enforcement 來自 required checks／branch rules。
- 人類必須確認 High finding 已修正或明確拒絕合併。

## Actions 安全閘門

`Security Gate` 包含：

- `品質與 DOM XSS`：ESLint、Vitest、Python tests、DOM sink scanner、Vite build。
- `Dependency review`：新增 High 以上 dependency 風險即失敗。
- `CodeQL (javascript-typescript)`：使用 `security-extended` queries。

這些 checks 可重複執行，但仍無法證明 A01 到 A10 全部安全。責任分配請看 [control matrix](../security/owasp-control-matrix.md)。
