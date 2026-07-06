from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def require(condition, message):
    if not condition:
        raise SystemExit(f"FAIL: {message}")
    print(f"OK: {message}")


required_files = [
    ".github/ISSUE_TEMPLATE/agent-task.yml",
    ".github/ISSUE_TEMPLATE/copilot-agent-task.yml",
    ".github/pull_request_template.md",
    ".github/workflows/cloud-agent-simulator.yml",
    ".github/workflows/pr-preview.yml",
    "scripts/create_agent_issue.py",
    "scripts/create_copilot_issue.py",
    "scripts/cloud_agent_simulator.py",
    "README.md",
    "docs/end-to-end-process.md",
    "docs/phase-2-copilot-cloud-agent.md",
    "docs/phase-3-pr-preview.md",
    "docs/operation-flow.md",
    "index.html",
]

for relative in required_files:
    require((ROOT / relative).is_file(), f"{relative} exists")

readme = (ROOT / "README.md").read_text(encoding="utf-8")
flow = (ROOT / "docs/operation-flow.md").read_text(encoding="utf-8")
workflow = (ROOT / ".github/workflows/cloud-agent-simulator.yml").read_text(encoding="utf-8")
preview_workflow = (ROOT / ".github/workflows/pr-preview.yml").read_text(encoding="utf-8")
issue_template = (ROOT / ".github/ISSUE_TEMPLATE/agent-task.yml").read_text(encoding="utf-8")
copilot_template = (ROOT / ".github/ISSUE_TEMPLATE/copilot-agent-task.yml").read_text(encoding="utf-8")
create_script = (ROOT / "scripts/create_agent_issue.py").read_text(encoding="utf-8")
copilot_script = (ROOT / "scripts/create_copilot_issue.py").read_text(encoding="utf-8")
phase3 = (ROOT / "docs/phase-3-pr-preview.md").read_text(encoding="utf-8")
end_to_end = (ROOT / "docs/end-to-end-process.md").read_text(encoding="utf-8")

require("Local AI" in readme, "README explains Local AI")
require("Cloud Agent" in readme, "README explains Cloud Agent")
require("Human Review" in readme, "README explains Human Review")
require("```mermaid" in readme, "README includes Mermaid flowchart")
require("cloud-agent:ready" in issue_template, "issue template applies cloud-agent ready label")
require("copilot-cloud-agent:ready" in copilot_template, "Copilot issue template applies phase-2 label")
require("pull-requests: write" in workflow, "workflow can open PRs")
require("github.event.issue.labels.*.name" in workflow, "workflow checks labels by exact name")
require("gh-pages" in preview_workflow, "preview workflow deploys to gh-pages")
require("environment_url" in preview_workflow, "preview workflow records a deployment URL")
require('"issue"' in create_script and '"create"' in create_script, "local script creates GitHub issues")
require("@copilot" in copilot_script, "phase-2 script uses the GitHub CLI Copilot assignee")
require("繁體中文" in copilot_script, "phase-2 script requests Traditional Chinese output")
require("PR Preview" in phase3, "phase-3 document explains PR Preview")
require("Issue + 指派 @copilot" in end_to_end, "end-to-end doc explains Copilot trigger")
require("資安" in end_to_end, "end-to-end doc covers security gate")
require("git push" in flow, "operation flow explains GitHub publishing")

print("OK: MVP structure verification complete")
