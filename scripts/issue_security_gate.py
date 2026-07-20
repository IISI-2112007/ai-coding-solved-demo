import argparse
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path


REPORT_MARKER = "<!-- issue-security-intake -->"


@dataclass(frozen=True)
class Finding:
    category: str
    severity: str
    message: str


def scan_issue(title: str, body: str) -> list[Finding]:
    title = title.strip()
    body = body.strip()
    text = f"{title}\n{body}"
    findings: list[Finding] = []

    if len(title) < 8 or len(body) < 30:
        findings.append(
            Finding(
                "INPUT",
                "Medium",
                "Issue 必須提供清楚標題與至少 30 字的目標、範圍及驗收內容。",
            )
        )

    access_patterns = [
        r"query\s*parameter.{0,30}(admin|管理員)",
        r"(admin|管理員).{0,30}query\s*parameter",
        r"URL\s*參數.{0,30}(權限|角色|管理員)",
        r"(權限|角色|管理員).{0,30}URL\s*參數",
    ]
    if any(re.search(pattern, text, re.IGNORECASE | re.DOTALL) for pattern in access_patterns):
        findings.append(
            Finding(
                "A01:2025",
                "High",
                "不可用使用者可竄改的 URL／query parameter 決定角色或管理員權限。",
            )
        )

    injection_patterns = [
        r"innerHTML.{0,40}(未過濾|URL|輸入|參數)",
        r"(未過濾|URL|輸入|參數).{0,40}innerHTML",
        r"不(?:用|需).{0,20}(escape|sanitize|編碼|過濾)",
    ]
    if any(re.search(pattern, text, re.IGNORECASE | re.DOTALL) for pattern in injection_patterns):
        findings.append(
            Finding(
                "A05:2025",
                "High",
                "未受信任輸入不得直接進入 HTML sink；請使用 textContent 與明確驗證。",
            )
        )

    return findings


def build_report(status: str, findings: list[Finding]) -> str:
    if status == "approved":
        detail = "未偵測到規則型高風險要求，可以進入 Copilot cloud agent 實作階段。"
        action = "下一步：由本地端腳本或人類將 Issue 指派給 Copilot。"
    else:
        lines = [f"- **{item.category} / {item.severity}**：{item.message}" for item in findings]
        detail = "\n".join(lines)
        action = "決策：`BLOCK`。不得指派給實作 Agent；先修正 Issue 或保留為 negative test 證據。"

    return f"""{REPORT_MARKER}
## OWASP Issue 安全初審

狀態：`security:{status}`

{detail}

{action}

> 這是 deterministic gate，不是 Copilot AI review。PR 仍須經過 Copilot code review、Actions 與人類審查。
"""


def write_github_output(path: Path, status: str) -> None:
    with path.open("a", encoding="utf-8", newline="\n") as stream:
        stream.write(f"status={status}\n")
        stream.write(f"blocked={'true' if status == 'blocked' else 'false'}\n")


def read_required_text(value: str | None, file_path: Path | None, name: str) -> str:
    if value is not None:
        return value
    if file_path is not None:
        return file_path.read_text(encoding="utf-8")
    raise SystemExit(f"必須提供 --{name} 或 --{name}-file。")


def main() -> None:
    parser = argparse.ArgumentParser(description="檢查 GitHub Issue 是否包含明確 OWASP 高風險要求。")
    parser.add_argument("--title")
    parser.add_argument("--title-file", type=Path)
    parser.add_argument("--body")
    parser.add_argument("--body-file", type=Path)
    parser.add_argument("--report-file", type=Path)
    parser.add_argument("--github-output", type=Path)
    args = parser.parse_args()

    title = read_required_text(args.title, args.title_file, "title")
    body = read_required_text(args.body, args.body_file, "body")
    findings = scan_issue(title, body)
    status = "approved" if not findings else "blocked"
    report = build_report(status, findings)

    if args.report_file:
        args.report_file.write_text(report, encoding="utf-8", newline="\n")
    if args.github_output:
        write_github_output(args.github_output, status)

    print(
        json.dumps(
            {"status": status, "findings": [asdict(finding) for finding in findings]},
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
