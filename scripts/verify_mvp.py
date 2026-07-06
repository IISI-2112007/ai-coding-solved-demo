from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def require(condition, message):
    if not condition:
        raise SystemExit(f"FAIL: {message}")
    print(f"OK: {message}")


required_files = [
    ".github/ISSUE_TEMPLATE/agent-task.yml",
    ".github/pull_request_template.md",
    ".github/workflows/cloud-agent-simulator.yml",
    "scripts/create_agent_issue.py",
    "scripts/cloud_agent_simulator.py",
    "README.md",
    "docs/operation-flow.md",
    "index.html",
]

for relative in required_files:
    require((ROOT / relative).is_file(), f"{relative} exists")

readme = (ROOT / "README.md").read_text(encoding="utf-8")
flow = (ROOT / "docs/operation-flow.md").read_text(encoding="utf-8")
workflow = (ROOT / ".github/workflows/cloud-agent-simulator.yml").read_text(encoding="utf-8")
issue_template = (ROOT / ".github/ISSUE_TEMPLATE/agent-task.yml").read_text(encoding="utf-8")
create_script = (ROOT / "scripts/create_agent_issue.py").read_text(encoding="utf-8")

require("Local AI" in readme, "README explains Local AI")
require("Cloud Agent" in readme, "README explains Cloud Agent")
require("Human Review" in readme, "README explains Human Review")
require("```mermaid" in readme, "README includes Mermaid flowchart")
require("cloud-agent:ready" in issue_template, "issue template applies cloud-agent ready label")
require("pull-requests: write" in workflow, "workflow can open PRs")
require('"issue"' in create_script and '"create"' in create_script, "local script creates GitHub issues")
require("git push" in flow, "operation flow explains GitHub publishing")

print("OK: MVP structure verification complete")
