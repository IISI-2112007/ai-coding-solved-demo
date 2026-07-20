# 目前完成度與限制

最後更新：2026-07-20。

## 已完成並有本機證據

- Vite + TypeScript Flow Lab 可 build。
- Safe／Blocked 流程模型與 Issue 初審可互動。
- Vitest、Python tests、ESLint 與 DOM XSS scanner 可執行。
- Implementer／OWASP Security Reviewer custom agent profiles 已建立。
- Issue Security Intake、Security Gate、CodeQL、dependency review 與 Vite PR Preview workflows 已建立。
- OWASP Top 10:2025 checklist、control matrix 與完整繁體中文教學已建立。

## 既有 GitHub 基線證據

- Issue #3 與 PR #4 證明真正 Copilot cloud agent 曾接手。
- PR #4 Preview 曾實測 HTTP 200。
- GitHub Pages 目前從 `gh-pages` root 發布。

## 等待本版本進入 default branch 後驗證

- Custom agents 是否出現在 GitHub Issue 指派選單。
- Unsafe Issue 是否取得 `security:blocked` 與 A01／A05 留言。
- Safe Issue 是否在 `security:approved` 後指派 Copilot 並產生 PR。
- 新 Security Gate、Copilot OWASP review 與 Vite Preview 的 GitHub URLs。
- Branch protection 的 required check contexts。
- 最終 PPT 的 GitHub 證據截圖。

## 平台限制

- Repository 是 public，Copilot Automations 目前不可用。
- Copilot code review 只留下 Comment，不會阻擋 merge。
- 指派 Copilot 的同一使用者不能 Approve 該 PR；required human approval 需要第二位 collaborator。
- GitHub connector 與本機 GitHub CLI 目前是不同帳號；repository 寫入使用具有 ADMIN 權限的 `gh` 登入帳號。

尚未有真實 URL 的項目一律標示待驗證，不製作假成功證據。
