import argparse
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def safe_issue_number(value):
    return "".join(character for character in value if character.isdigit()) or "manual"


def main():
    parser = argparse.ArgumentParser(description="為第一階段 simulator 產生可審查的 cloud-agent output。")
    parser.add_argument("--issue-number", required=True)
    parser.add_argument("--issue-title", required=True)
    parser.add_argument("--issue-body", required=True)
    parser.add_argument("--repository", required=True)
    parser.add_argument("--run-url", required=True)
    args = parser.parse_args()

    issue_number = safe_issue_number(args.issue_number)
    output_dir = ROOT / "cloud-agent-output" / f"issue-{issue_number}"
    output_dir.mkdir(parents=True, exist_ok=True)

    generated_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
    issue_url = f"https://github.com/{args.repository}/issues/{issue_number}"

    summary = f"""# Cloud Agent Simulator 產出：Issue #{issue_number}

## 任務

{args.issue_title}

## 來源

- Issue: {issue_url}
- Workflow run：{args.run_url}
- 產生時間：{generated_at}

## Agent 判讀

Cloud Agent Simulator 已接手這個 Issue，保留原始需求，並產生這份可審查的輸出。
這個 MVP 刻意讓產出維持小範圍，讓人類 reviewer 可以在 merge 前檢查 diff。

## 原始 Issue 內容

```text
{args.issue_body.strip()}
```

## 人工審查清單

- [ ] 產出內容有回應 Issue 目標。
- [ ] 修改檔案仍在允許修改範圍內。
- [ ] PR 有連回原始 Issue。
- [ ] reviewer 可以在 merge 前要求修改。
"""

    pr_body = f"""# Cloud Agent Simulator 結果

Closes #{issue_number}

## 發生了什麼

GitHub Actions Cloud Agent Simulator 已接手 issue #{issue_number}，產生小範圍、可審查的輸出，並開啟這個 PR 交給人類 reviewer。

## 需要審查的檔案

- `cloud-agent-output/issue-{issue_number}/summary.md`
- `DEMO_RESULTS.md`

## 人工審查清單

- [ ] 確認這個 PR 對應原始 Issue。
- [ ] 確認產出內容容易理解。
- [ ] 確認修改檔案可以接受。
- [ ] 決定 approve、request changes 或 close PR。

## Workflow run

{args.run_url}
"""

    results = f"""# Demo 結果

最新一次 Cloud Agent Simulator 執行：

- Issue: {issue_url}
- 標題：{args.issue_title}
- 產生時間：{generated_at}
- Workflow run：{args.run_url}

這個 PR 刻意保留為人類審查後再 merge。
"""

    (output_dir / "summary.md").write_text(summary, encoding="utf-8")
    (output_dir / "pr-body.md").write_text(pr_body, encoding="utf-8")
    (ROOT / "DEMO_RESULTS.md").write_text(results, encoding="utf-8")


if __name__ == "__main__":
    main()
