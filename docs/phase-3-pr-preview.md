# 第三階段：PR Preview Deployment

## 目標

第三階段補上「不是只看程式碼 diff，而是先看網頁成果」的能力。

```text
Issue -> Copilot cloud agent -> PR -> Preview URL -> Human Review
```

在這個階段，PR 還沒有 merge 到 `main`，但 reviewer 已經可以在 GitHub 上點一個 URL，查看 PR branch 產生的靜態頁面。這讓非工程角色可以先看成果，再決定是否需要深入看 diff。

## main / master 與 preview 的差異

- `main` 或 `master` 通常代表正式版本，正式部署通常只有一個。
- PR preview 可以有很多個，每個 PR 都能有自己的預覽網址。
- PR preview 是臨時審查入口，不等於已接受或已上正式環境。

範例：

```text
main -> production
PR #4 -> https://iisi-2112007.github.io/ai-coding-solved-demo/pr-4/
PR #9 -> https://iisi-2112007.github.io/ai-coding-solved-demo/pr-9/
```

## 這個 repo 的做法

Workflow：

```text
.github/workflows/pr-preview.yml
```

觸發時機：

- PR opened
- PR synchronize
- PR reopened
- PR ready_for_review
- 手動 workflow_dispatch，輸入 PR 編號

部署內容：

- `index.html`
- `assets/`
- `docs/`
- `preview-summary.html`
- `changed-files.txt`

部署位置：

```text
gh-pages branch / pr-{PR_NUMBER}/
```

預覽網址格式：

```text
https://iisi-2112007.github.io/ai-coding-solved-demo/pr-{PR_NUMBER}/
```

## 人類審查方式

Reviewer 建議順序：

1. 先看 PR comment 裡的 preview URL。
2. 看 `preview-summary.html` 確認 PR 編號與來源。
3. 開 `index.html` 看成果畫面。
4. 回到 PR 看 Files changed。
5. 若成果可以接受，再看 checks / security gate。
6. 最後 approve、request changes 或 close。

## 安全邊界

這個 preview workflow 只在同一個 repo 內的 PR 自動執行：

```text
github.event.pull_request.head.repo.full_name == github.repository
```

原因是 preview workflow 需要 `contents: write` 才能推送到 `gh-pages`。不應該讓未知 fork PR 直接拿到這種寫入能力。

## 啟用 GitHub Pages

第一次使用時，需要讓 GitHub Pages 讀取 `gh-pages` branch。

可以在 GitHub 網頁設定：

```text
Settings -> Pages -> Build and deployment -> Deploy from a branch -> gh-pages / root
```

或由 repo owner 用 GitHub API 設定。若 GitHub Pages 尚未啟用，workflow 仍會建立 `gh-pages` branch 和 PR comment，但 preview URL 可能暫時是 404。

## 目前 repo 的實測狀態

這個 workflow 已能把 PR preview 檔案產出到：

```text
gh-pages/pr-4/
```

但目前 private repo 啟用 GitHub Pages 時，GitHub API 回覆：

```text
Your current plan does not support GitHub Pages for this repository.
```

因此第三階段在目前 repo 的狀態是：

- preview 檔案可以產出。
- PR comment 可以指出 preview 檔案位置。
- deployment 可以建立，但會標記為 Pages 尚未啟用。
- 真正可點開的 Pages URL 需要先解決 GitHub Pages 方案或 repo visibility。

可選路線：

- 保持 repo private，改用 Vercel、Netlify、Cloudflare Pages 或其他 preview provider。
- 將 demo repo 改成 public，使用 GitHub Pages。
- 升級或調整 GitHub 方案，讓 private repo 可使用 Pages。

這個 repo 不會自動改 public；那是 owner 的外部決策。

## 驗收標準

- PR 建立或更新時會執行 `PR Preview` workflow。
- workflow 會部署到 `gh-pages/pr-{PR_NUMBER}/`。
- PR 會收到繁體中文 comment，附上 preview URL。
- GitHub deployment 會記錄 `environment_url`。
- 人類可以不拉 local、不看 diff，直接在瀏覽器看 PR 成果。
