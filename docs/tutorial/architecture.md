# 完整架構

## 主流程

```mermaid
sequenceDiagram
    participant L as Local AI
    participant I as GitHub Issue
    participant G as Issue Safety Gate
    participant C as Copilot Cloud Agent
    participant R as Copilot Code Review
    participant A as GitHub Actions
    participant P as PR Preview
    participant H as Human Reviewer

    L->>I: 建立繁體中文 Safe 或 Unsafe Issue
    I->>G: issues.opened
    G-->>I: security:approved 或 security:blocked
    alt Safe Issue
        L->>C: 通過後指定 implementer custom agent
        C->>I: 讀取 Issue 與 repository instructions
        C->>C: 修改、測試、commit
        C->>R: 開 Pull Request
        R-->>H: OWASP Comment review
        A-->>H: Quality、DOM XSS、Dependency、CodeQL checks
        P-->>H: HTTP 200 可操作預覽
        H-->>C: Request changes
        H-->>I: 接受成果並 merge
    else Unsafe Issue
        G-->>I: BLOCK 並保留證據
        Note over I,C: 不指派 Implementer，不產生可合併程式碼
    end
```

## 為何不是兩個 Agent 自動核准

GitHub custom agents 可以在 Issue 指派時選擇，但 GitHub.com 目前不支援 agent profile 的 `handoffs`。Copilot code review 固定留下 Comment，不能形成 required approval。

因此真正的責任分工是：

- Implementer custom agent：實作。
- OWASP Security Reviewer custom agent：唯讀分析或示範用專家角色。
- Copilot code review：PR 上的 AI review。
- GitHub Actions：可重現的 enforcement。
- Human reviewer：最後決定。

## 信任邊界

- Issue 文字是輸入，不因為來自 AI 就可信。
- Copilot 產生的程式仍需按一般 PR 檢查。
- AI review 是建議，不是 required approval。
- Actions 綠燈只能證明已執行的檢核，不代表完整 OWASP 合規。
- Preview 只能證明該 PR head 的畫面可操作，不代表 production 安全。
