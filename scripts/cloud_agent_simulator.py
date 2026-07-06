import argparse
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def safe_issue_number(value):
    return "".join(character for character in value if character.isdigit()) or "manual"


def main():
    parser = argparse.ArgumentParser(description="Generate reviewable cloud-agent output for an issue.")
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

    summary = f"""# Cloud Agent Output For Issue #{issue_number}

## Task

{args.issue_title}

## Source

- Issue: {issue_url}
- Workflow run: {args.run_url}
- Generated at: {generated_at}

## Agent interpretation

The cloud-agent simulator accepted the issue, preserved the original request, and generated this reviewable output.
This MVP intentionally keeps the output small so a human can inspect the diff before merge.

## Original issue body

```text
{args.issue_body.strip()}
```

## Human reviewer checklist

- [ ] The output responds to the issue goal.
- [ ] The changed files stay inside the allowed scope.
- [ ] The PR links back to the issue.
- [ ] The reviewer can request changes before merge.
"""

    pr_body = f"""# Cloud Agent Simulator Result

Closes #{issue_number}

## What happened

The GitHub Actions cloud-agent simulator accepted issue #{issue_number}, generated a small reviewable output, and opened this PR for human review.

## Files to review

- `cloud-agent-output/issue-{issue_number}/summary.md`
- `DEMO_RESULTS.md`

## Human review checklist

- [ ] Confirm this PR corresponds to the issue.
- [ ] Confirm generated output is understandable.
- [ ] Confirm the changed files are acceptable.
- [ ] Approve, request changes, or close the PR.

## Workflow run

{args.run_url}
"""

    results = f"""# Demo Results

Latest cloud-agent simulator run:

- Issue: {issue_url}
- Title: {args.issue_title}
- Generated at: {generated_at}
- Workflow run: {args.run_url}

The generated PR is intentionally reviewable by a human before merge.
"""

    (output_dir / "summary.md").write_text(summary, encoding="utf-8")
    (output_dir / "pr-body.md").write_text(pr_body, encoding="utf-8")
    (ROOT / "DEMO_RESULTS.md").write_text(results, encoding="utf-8")


if __name__ == "__main__":
    main()
