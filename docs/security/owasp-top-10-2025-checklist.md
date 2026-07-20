# OWASP Top 10:2025 檢核清單

此清單供 Issue 初審、GitHub Copilot code review、Actions gate 與人類 reviewer 共用。基準採 [OWASP Top 10:2025](https://owasp.org/Top10/)。

## Review Finding 格式

每個 finding 必須包含 OWASP 分類、嚴重度、證據、影響、修正建議，以及 `BLOCK` 或 `ADVISORY` 決策。

## A01:2025 Broken Access Control

- 權限是否由可信端執行 deny-by-default 檢查？
- 是否信任 query parameter、前端 hidden field 或 local storage 的角色值？
- 是否可能讀取、修改或刪除其他使用者的資料？
- 本 demo 若要求以 URL 參數決定管理員角色，必須 `BLOCK`。

## A02:2025 Security Misconfiguration

- 是否關閉必要的安全設定、checks 或防護 header？
- 錯誤訊息是否暴露路徑、設定或敏感資料？
- 開發與預覽設定是否被誤當成 production？

## A03:2025 Software Supply Chain Failures

- 新 dependency 是否必要、來源可信、版本鎖定且可由 dependency review 檢查？
- GitHub Actions 是否只使用可信 publisher 的 action？
- 是否修改 lockfile、跳過 integrity 或加入不明 install script？

## A04:2025 Cryptographic Failures

- 是否把真實 secret、token、密碼或敏感資料寫入 repository、log 或前端 bundle？
- 是否自行發明加密或使用已知弱演算法？
- 教學用 negative test 不得使用可被誤認為真實 credential 的字串。

## A05:2025 Injection

- 未受信任資料是否進入 HTML、JavaScript、shell、SQL 或 template sink？
- DOM 是否使用 `textContent` 等安全 API？
- `innerHTML`、`outerHTML`、`insertAdjacentHTML`、`document.write`、`eval`、`new Function` 一律視為高風險證據並優先 `BLOCK`。

## A06:2025 Insecure Design

- 需求本身是否要求繞過安全控制或人類審查？
- 是否有威脅情境、信任邊界與失敗處理？
- 是否把 AI review 當作唯一安全控制？

## A07:2025 Authentication Failures

- 是否把容易猜測或可竄改的值當成登入或身份證明？
- Session、token 與登出行為是否符合應用需求？
- 本靜態 demo 不實作真實登入；若新增 authentication，必須另做 server-side 設計審查。

## A08:2025 Software or Data Integrity Failures

- build、deployment 與更新來源是否可追蹤？
- 是否繞過 PR、lockfile、required checks 或來源驗證？
- Preview 是否精確對應 PR head SHA？

## A09:2025 Security Logging and Alerting Failures

- 安全檢核失敗是否留下可追蹤的 Actions、Issue 或 PR 證據？
- log 是否足以重建事件，又不暴露敏感資料？
- blocked Issue 是否有分類、理由與處理時間？

## A10:2025 Mishandling of Exceptional Conditions

- 失敗、空輸入、timeout、404 與外部服務錯誤是否有安全預設？
- 安全 scanner 或 workflow 失敗時是否 fail closed？
- 是否用 `continue-on-error` 或 `|| true` 隱藏必要 gate 的失敗？

## 阻擋基準

以下情況不得 merge：Critical／High finding 未解決、A01 或 A05 可被利用、真實 secret、必要 checks 被停用、Preview 與 PR SHA 不一致，或人類 reviewer 尚未做最後決定。
