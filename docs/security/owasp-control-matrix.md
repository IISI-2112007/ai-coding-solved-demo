# OWASP Top 10:2025 Control Matrix

這份 matrix 說明各風險主要由哪一層控制。`Automated` 代表可重現檢核，`AI-assisted` 代表情境判讀，`Human review` 代表仍需人類決策，`Not applicable` 必須附理由。

## A01 Broken Access Control

- Automated：Issue 規則檢核與相關單元測試。
- AI-assisted：Copilot 檢查信任邊界與權限邏輯。
- Human review：確認需求與角色模型合理。
- 現況：靜態 demo 沒有 production authorization；新增真實權限功能時不可標示 Not applicable。

## A02 Security Misconfiguration

- Automated：workflow、build 與 branch checks 狀態。
- AI-assisted：檢查設定是否暴露資訊或弱化防護。
- Human review：確認 Preview 與 production 邊界。

## A03 Software Supply Chain Failures

- Automated：`npm ci`、lockfile、dependency review、CodeQL。
- AI-assisted：判斷新增 dependency 是否必要與可信。
- Human review：核對供應鏈風險與 action publisher。

## A04 Cryptographic Failures

- Automated：GitHub secret scanning 與禁止真實 credential 的 repository 政策。
- AI-assisted：檢查敏感資料處理與不當加密設計。
- Human review：判斷資料敏感度。
- 現況：此靜態 demo 不儲存真實 secret，也不實作 cryptography。

## A05 Injection

- Automated：`security:dom`、Vitest、ESLint、CodeQL。
- AI-assisted：追蹤未受信任資料到 sink 的資料流。
- Human review：操作 Preview 並檢查輸入輸出。

## A06 Insecure Design

- Automated：只能確認文件與必要流程存在，不能證明設計安全。
- AI-assisted：威脅情境與繞過路徑分析。
- Human review：對需求、信任邊界與殘餘風險做最後判斷。

## A07 Authentication Failures

- Automated：Issue gate 會阻擋以 URL 參數決定管理員角色的要求。
- AI-assisted：審查 authentication 與 session 設計。
- Human review：確認身份生命週期。
- 現況：production authentication 不在此靜態 demo 範圍。

## A08 Software or Data Integrity Failures

- Automated：lockfile、Actions、PR head SHA 與 deployment status。
- AI-assisted：檢查 integrity control 是否被繞過。
- Human review：確認實際 Preview 對應正確 PR。

## A09 Security Logging and Alerting Failures

- Automated：Issue comment、labels、Actions logs 與 check conclusions。
- AI-assisted：評估事件證據是否足夠且沒有敏感資料。
- Human review：確認 blocked／approved 決策可追蹤。

## A10 Mishandling of Exceptional Conditions

- Automated：empty input、邊界與 blocked path tests；必要 job 不使用 `continue-on-error`。
- AI-assisted：尋找 fail-open、timeout 與例外吞沒。
- Human review：確認錯誤狀態對使用者與 reviewer 足夠清楚。

## 不可宣稱的事項

- Scanner 綠燈不等於 OWASP Top 10 全部符合。
- Copilot 沒有留言不等於沒有安全問題。
- Preview 可開不等於 production 可安全部署。
- 本 matrix 不構成滲透測試、稽核報告或合規認證。
