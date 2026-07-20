# 如何進行人類 PR 審查

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

## 單一帳號限制

GitHub 不允許指派 Copilot 執行 Issue 的同一個使用者 Approve 該 Copilot PR。因此本個人 repository 若只有一位 maintainer：

- 人類仍可逐項審查並以 merge／不 merge 做最後決定。
- 不應設定無人能滿足的 required approving review。
- 若要正式展示 Approve gate，請加入第二位有 write 權限的 collaborator，再要求一個 human approval。

Copilot 的 Comment review 不可用來替代這個 human approval。
