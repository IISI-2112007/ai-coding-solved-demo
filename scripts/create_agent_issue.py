import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GH_EXE = shutil.which("gh") or r"C:\Program Files\GitHub CLI\gh.exe"


def run(command, check=True):
    completed = subprocess.run(
        command,
        cwd=ROOT,
        text=True,
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
    return f"""## Goal

{args.goal}

## Context

{args.context}

## Allowed scope

{args.allowed_scope}

## Acceptance criteria

{args.acceptance}

## Handoff confirmation

- [x] This task is small enough for a demo PR.
- [x] The cloud agent may open a PR for human review.
"""


def main():
    parser = argparse.ArgumentParser(description="Create a GitHub Issue for the cloud-agent MVP demo.")
    parser.add_argument("--title", default="[agent-task] Generate demo handoff evidence")
    parser.add_argument("--goal", default="Generate a small reviewable output that proves the cloud-agent handoff works.")
    parser.add_argument("--context", default="This is an MVP demo for local AI to GitHub Issue to Cloud Agent to human review.")
    parser.add_argument("--allowed-scope", default="cloud-agent-output/** and DEMO_RESULTS.md")
    parser.add_argument(
        "--acceptance",
        default="- A PR is opened.\n- The PR links to the issue.\n- The output is easy for a human to review.",
    )
    parser.add_argument("--dry-run", action="store_true", help="Print the issue body without creating anything.")
    args = parser.parse_args()

    body = build_body(args)
    if args.dry_run:
        print(f"# {args.title}\n\n{body}")
        return

    run([GH_EXE, "auth", "status"])
    ensure_label("local-ai", "2563A8", "Issue was created by the local AI handoff script.")
    ensure_label("cloud-agent:ready", "2F8F55", "Cloud agent simulator may accept this issue.")

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
