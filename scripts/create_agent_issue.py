import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GH_EXE = shutil.which("gh") or r"C:\Program Files\GitHub CLI\gh.exe"

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")


def run(command, check=True):
    completed = subprocess.run(
        command,
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        errors="replace",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if check and completed.returncode != 0:
        message = completed.stderr.strip() or completed.stdout.strip()
        raise SystemExit(f"Command failed: {' '.join(command)}\n{message}")
    return completed


def ensure_label(name, color, description):
    existing = run([GH_EXE, "label", "list", "--limit", "200", "--json", "name"], check=False)
    if existing.returncode != 0:
        raise SystemExit(existing.stderr.strip() or "Unable to list labels")
    labels = {item["name"] for item in json.loads(existing.stdout or "[]")}
    if name in labels:
        return
    run([GH_EXE, "label", "create", name, "--color", color, "--description", description])


def build_body(args):
    return f"""## 目標

{args.goal}

## 背景

{args.context}

## 允許修改範圍

{args.allowed_scope}

## 驗收標準

{args.acceptance}

## 交接確認

- [x] 這個任務足夠小，可以用 demo PR 審查。
- [x] cloud agent 可以開 PR 交給人類審查。
"""


def main():
    parser = argparse.ArgumentParser(description="建立第一階段 simulator 使用的 GitHub Issue。")
    parser.add_argument("--title", default="[agent-task] 產生 demo 交接證據")
    parser.add_argument("--goal", default="產生一份小型、可審查的成果，用來證明本地端 AI 到 cloud agent 的交接流程可以運作。")
    parser.add_argument("--context", default="這是本地端 AI -> GitHub Issue -> Cloud Agent -> 人類審查的 MVP demo。")
    parser.add_argument("--allowed-scope", default="cloud-agent-output/** and DEMO_RESULTS.md")
    parser.add_argument(
        "--acceptance",
        default="- 已建立 Pull Request。\n- PR 有連回這個 issue。\n- 產出內容容易讓人類審查。",
    )
    parser.add_argument("--dry-run", action="store_true", help="只列印 issue 內容，不建立 GitHub Issue。")
    args = parser.parse_args()

    body = build_body(args)
    if args.dry_run:
        print(f"# {args.title}\n\n{body}")
        return

    run([GH_EXE, "auth", "status"])
    ensure_label("local-ai", "2563A8", "由本地端 AI 交接腳本建立的 Issue。")
    ensure_label("cloud-agent:ready", "2F8F55", "第一階段 Cloud Agent Simulator 可以接手這個 Issue。")

    with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".md", delete=False) as temp_file:
        temp_file.write(body)
        temp_path = temp_file.name

    try:
        result = run(
            [
                GH_EXE,
                "issue",
                "create",
                "--title",
                args.title,
                "--body-file",
                temp_path,
                "--label",
                "local-ai",
                "--label",
                "cloud-agent:ready",
            ]
        )
    finally:
        Path(temp_path).unlink(missing_ok=True)

    print(result.stdout.strip())


if __name__ == "__main__":
    if sys.version_info < (3, 9):
        raise SystemExit("Python 3.9+ is required.")
    main()
