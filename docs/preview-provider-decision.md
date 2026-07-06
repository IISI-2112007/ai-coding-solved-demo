# PR Preview Provider 決策紀錄

## 決策狀態

狀態：已決策

已選方案：A. repo 改 public + GitHub Pages

Owner 已將 repo 改為 public。GitHub Pages 已設定為從 `gh-pages` branch 的 root 發布。

```text
Pages source: gh-pages /
Pages URL: https://iisi-2112007.github.io/ai-coding-solved-demo/
```

PR Preview workflow 現在可以產出可直接開啟的 preview URL。

## 目前已完成

- `PR Preview` workflow 已存在。
- PR #4 已成功跑過 workflow。
- preview 檔案已產出到 `gh-pages/pr-4/`。
- PR #4 已收到繁體中文 preview URL 留言。
- 最新 PR preview deployment 已可提供 `environment_url`。
- preview URL 已用 HTTP 驗證回應 `200`。

可用預覽：

```text
https://iisi-2112007.github.io/ai-coding-solved-demo/pr-4/
```

## 方案比較

| 方案                         | 優點                               | 代價 / 風險                         | 適合情境                         |
| ---------------------------- | ---------------------------------- | ----------------------------------- | -------------------------------- |
| A. repo 改 public + Pages     | 最快、最少外部依賴                 | repo 內容會公開                     | demo repo 沒有敏感內容           |
| B. 保持 private + 支援 Pages  | 留在 GitHub 原生流程               | 需要 GitHub 方案支援 private Pages  | 想維持 GitHub-only               |
| C. 接 Vercel / Netlify       | private repo 也常見，PR preview 強 | 需要外部服務帳號與 token / app 安裝 | 想要成熟 preview deployment      |
| D. 接 Cloudflare Pages        | 可做 branch preview                | 需要外部服務設定                    | 已使用 Cloudflare 或想要低成本   |
| E. 只保留 gh-pages artifact   | 不需要外部設定                     | 不是可直接看的網頁 URL              | 暫時保留 evidence，不急著瀏覽器看 |

## 建議

目前已採用 A：把 repo 改 public，再啟用 GitHub Pages。

若 repo 必須 private，建議選 C：接 Vercel 或 Netlify，讓每個 PR 自動拿到 preview URL。

## 不建議

- 不建議為了 demo 擅自把 private repo 改 public。
- 不建議在 PR comment 留下看似可用但實際 404 的 URL。
- 不建議把 preview workflow 的失敗藏起來，應該明確告訴 reviewer 是 provider 未啟用。

## 下一步

如果未來 repo 必須改回 private，需要重新選一條：

```text
A: 改 public + GitHub Pages
B: 維持 private + 支援 private Pages 的 GitHub 方案
C: Vercel / Netlify
D: Cloudflare Pages
E: 暫時只保留 gh-pages preview 檔案
```

若維持 public repo，現有 `PR Preview` workflow 可以繼續使用 GitHub Pages。
