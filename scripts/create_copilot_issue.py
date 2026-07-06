import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GH_EXE = shutil.which("gh") or r"C:\Program Files\GitHub CLI\gh.exe"
COPILOT_ASSIGNEE = "@copilot"

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
LABELS = [
    ("local-ai", "2563A8", "由本地端 AI 交接腳本建立的 Issue。"),
    ("copilot-cloud-agent:ready", "8250DF", "第二階段真正 Copilot cloud agent 可以接手這個 Issue。"),
    ("phase-2", "B7791F", "第二階段 MVP 驗證任務。"),
]


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


def repo_args(repo):
    return ["--repo", repo] if repo else []


def ensure_label(name, color, description, repo=None):
    existing = run(
        [GH_EXE, "label", "list", *repo_args(repo), "--limit", "200", "--json", "name"],
        check=False,
    )
    if existing.returncode != 0:
        raise SystemExit(existing.stderr.strip() or "Unable to list labels")
    labels = {item["name"] for item in json.loads(existing.stdout or "[]")}
    if name in labels:
        run([GH_EXE, "label", "edit", name, *repo_args(repo), "--color", color, "--description", description])
        return
    run(
        [
            GH_EXE,
            "label",
            "create",
            name,
            *repo_args(repo),
            "--color",
            color,
            "--description",
            description,
        ]
    )


def build_body(args):
    return f"""## 目標

{args.goal}

## 背景

{args.context}

## 允許修改範圍

{args.allowed_scope}

## 驗收標準

{args.acceptance}

## 人工審查要求

- Copilot cloud agent 完成後必須開 Pull Request，不可直接 merge。
- PR 說明、commit message 與新增文件請優先使用繁體中文。
- reviewer 需要確認 diff 是否符合允許修改範圍，再決定 approve 或 request changes。

## 第二階段備註

- 這個 Issue 不使用 `cloud-agent:ready` label，因此不會觸發第一階段 simulator workflow。
- 這個 Issue 會使用 GitHub CLI 的 `{COPILOT_ASSIGNEE}` 指派方式，用來啟動真正的 GitHub Copilot cloud agent。
"""


def main():
    parser = argparse.ArgumentParser(description="建立第二階段 Copilot cloud agent 使用的 GitHub Issue。")
    parser.add_argument("--repo", help="指定 GitHub repo，例如 IISI-2112007/ai-coding-solved-demo。")
    parser.add_argument("--title", default="[copilot-agent] 第二階段：建立 cloud agent 人工審查證據")
    parser.add_argument(
        "--goal",
        default="請新增一份第二階段執行證據，說明真正 Copilot cloud agent 已接手任務，並準備交由人類審查。",
    )
    parser.add_argument(
        "--context",
        default=(
            "這個 repo 第一階段已用 GitHub Actions simulator 證明 Issue -> PR -> 人類審查流程。"
            "第二階段要改由 GitHub Copilot cloud agent 從 Issue 接手並開 PR。"
        ),
    )
    parser.add_argument(
        "--allowed-scope",
        default="docs/**、README.md、DEMO_RESULTS.md；不要修改 .github/workflows/cloud-agent-simulator.yml。",
    )
    parser.add_argument(
        "--acceptance",
        default=(
            "- Copilot cloud agent 已建立 Pull Request。\n"
            "- PR 說明與新增文件使用繁體中文。\n"
            "- PR 有連回這個 Issue，且人類 reviewer 可以判斷是否 approve。\n"
            "- 若 PR 有可視成果，PR Preview workflow 已產生或說明預覽連結。"
        ),
    )
    parser.add_argument("--create", action="store_true", help="真的建立 GitHub Issue 並指派給 Copilot cloud agent。")
    parser.add_argument("--dry-run", action="store_true", help="只列印 issue 內容，不建立 GitHub Issue。")
    parser.add_argument(
        "--no-assign-copilot",
        action="store_true",
        help="只建立 Issue，不指派給 Copilot cloud agent。這通常只用於權限測試。",
    )
    args = parser.parse_args()

    body = build_body(args)
    labels = [name for name, _, _ in LABELS]
    assign_copilot = not args.no_assign_copilot

    if args.dry_run or not args.create:
        print(f"# {args.title}\n")
        print(body)
        print("## 建立設定\n")
        print(f"- Labels: {', '.join(labels)}")
        print(f"- Assignee: {COPILOT_ASSIGNEE if assign_copilot else '不指派'}")
        print("- 狀態：dry-run，尚未建立 GitHub Issue。")
        return

    run([GH_EXE, "auth", "status"])
    for name, color, description in LABELS:
        ensure_label(name, color, description, repo=args.repo)

    with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".md", delete=False) as temp_file:
        temp_file.write(body)
        temp_path = temp_file.name

    command = [
        GH_EXE,
        "issue",
        "create",
        *repo_args(args.repo),
        "--title",
        args.title,
        "--body-file",
        temp_path,
    ]
    for label in labels:
        command.extend(["--label", label])
    if assign_copilot:
        command.extend(["--assignee", COPILOT_ASSIGNEE])

    try:
        result = run(command)
    finally:
        Path(temp_path).unlink(missing_ok=True)

    print(result.stdout.strip())


if __name__ == "__main__":
    if sys.version_info < (3, 9):
        raise SystemExit("Python 3.9+ is required.")
    main()
