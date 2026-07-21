# 目前完成度與限制

最後更新：2026-07-21。

## 已完成並有 GitHub 證據

- Vite + TypeScript Flow Lab 可 build。
- Safe／Blocked 流程模型與 Issue 初審可互動。
- Vitest、Python tests、ESLint 與 DOM XSS scanner 可執行。
- Implementer／OWASP Security Reviewer custom agent profiles 已建立。
- Issue Security Intake、Security Gate、CodeQL、dependency review 與 Vite PR Preview workflows 已建立。
- OWASP Top 10:2025 checklist、control matrix 與完整繁體中文教學已建立。
- Unsafe Issue #10 具有 `security:blocked`、A01／A05 與唯一一則可重跑更新的 `BLOCK` 留言；未指派 Copilot。
- Unsafe PR #11 具有 Copilot code review 與 Actions 阻擋證據，保持不合併。
- Safe Issue #12 由真正 Copilot cloud agent 接手並建立 PR #13。
- PR #13 的 Security Gate、CodeQL、Dependency Review 與 PR Preview 全數通過。
- PR #13 Preview 已實測 HTTP 200，人類已完成 Approve 與 Merge。
- PR #14 已修正安全標籤重跑一致性；合併後重跑 Issue #10，`security:blocked` 仍保留且 marker 留言仍只有一則。

## 尚未完成

- PR #13 在要求 Copilot code review 前已由人類合併，因此缺少同一張 Safe PR 的合併前 Copilot review 證據。
- 最終 PPT 尚待納入最新 Issue、PR、checks、Preview 與上述順序限制的真實截圖。
- Branch protection／ruleset 是否要求所有 checks，仍需 repository owner 依方案與管理權限確認。

## 平台限制

- Repository 是 public，Copilot Automations 目前不可用。
- Copilot code review 只留下 Comment，不會阻擋 merge。
- 指派 Copilot 的同一使用者不能 Approve 該 PR；required human approval 需要第二位 collaborator。
- GitHub App integration 對本 repository 的部分寫入操作可能回傳 403；repository 寫入改用已登入且具有權限的 GitHub CLI。

尚未有真實 URL 的項目一律標示待驗證，不製作假成功證據。
