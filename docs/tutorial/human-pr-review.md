# 如何進行人類 PR 審查

## 你在流程中的角色

你不需要代替 AI 寫程式，也不需要看到綠色勾勾就立刻 Merge。你的工作是確認「需求、畫面、程式變更與安全證據」是否足以接受。

GitHub 上常見的三個動作意義不同：

- `Approve workflows to run`：允許來自 Copilot 或外部 contributor 的 branch 執行 GitHub Actions。這只是允許測試，不是核准 PR，也不會修改 `main`。
- `Approve`：留下人類審查通過的紀錄。PR 仍然存在於 branch，尚未進入 `main`。
- `Merge pull request`：把 PR 的修改正式放入 `main`。這是最後決定，應在 Preview、diff、checks 與 findings 都看過後執行。

`Ready for review` 只是將 Draft PR 轉為可正式審查，不會修改 `main`。

## 最小判斷流程

1. 如果畫面顯示 `Awaiting approval`，先確認 PR 作者與來源，再按 `Approve workflows to run` 讓測試執行。
2. 等待 Security Gate、CodeQL、Dependency Review 與 PR Preview 完成。
3. 打開 Preview 實際操作，不要只看 workflow 顯示成功。
4. 查看 Copilot review findings 與 `Files changed`；有 High、`BLOCK`、越界修改或失敗 checks 時，不得 Merge。
5. 證據都可接受時留下人類 `Approve`，最後再決定是否 Merge。

最安全的節奏是一次只做一個決定：先允許測試，再審查，最後才 Merge。

## 建議順序

1. Issue：確認目標、範圍、安全 label 與驗收標準。
2. Preview：實際操作正常、錯誤與手機畫面，不只看截圖。
3. Files changed：確認沒有越界修改、停用 checks 或加入不必要 dependency。
4. Checks：展開失敗 log；不要只看 workflow 名稱。
5. Copilot findings：確認每個 `BLOCK` 已修正，並查看是否需 re-review。
6. 殘餘風險：判斷 scanner 未涵蓋的設計、權限與操作風險。

## 三種決定

- Request changes：需求不符、High finding、checks 失敗、Preview 錯誤或修改越界。
- Merge：需求、Preview、diff、checks 與殘餘風險都可接受。
- Close：需求方向錯誤、不安全要求不應實作，或成本已不值得繼續。

## 單一帳號與職責分離

本 Demo 已驗證 repository owner 可以對 Copilot cloud agent 建立的 PR 留下人類 `Approve`，再決定是否 Merge。這足以展示「AI 作者、人類核准」的流程，但只有一位 maintainer 時，仍不等於組織治理中的第二人職責分離。

- 個人 Demo：owner 可審查 Copilot PR，留下 Approval 並做最後 Merge 決定。
- 團隊治理：若政策要求第二位人類 reviewer，應加入另一位有適當權限的 collaborator，再以 ruleset 要求獨立 approval。
- Copilot 的 Comment review 不可替代人類 approval，也不會自行阻擋 Merge。

## 本 Demo 的實際例子

- PR #11：Copilot review 與 Actions 都發現安全問題，所以保持不合併。
- PR #13：真正 Copilot cloud agent 完成功能，checks 與 Preview 通過，再由人類 Approve 與 Merge。
- PR #14：修正安全標籤重跑問題，checks 與 Preview 通過，再由人類 Merge。

PR #13 在 Copilot code review request 前已先 Merge，因此該 PR 的人類決定有效，但缺少「合併前 Copilot review」證據。這個順序差異應保留在教材中，而不是補成假成功紀錄。
