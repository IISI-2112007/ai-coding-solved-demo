import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def require(condition, message):
    if not condition:
        raise SystemExit(f"FAIL: {message}")
    print(f"OK: {message}")


required_files = [
    "package.json",
    "package-lock.json",
    "tsconfig.json",
    "vite.config.js",
    "src/main.ts",
    "src/flow.ts",
    "src/flow.test.ts",
    "scripts/check-dangerous-dom.mjs",
    "scripts/check_local_markdown_links.py",
    "scripts/issue_security_gate.py",
    "scripts/create_demo_issue.py",
    "tests/test_issue_security_gate.py",
    ".github/agents/implementer.agent.md",
    ".github/agents/owasp-security-reviewer.agent.md",
    ".github/copilot-instructions.md",
    ".github/workflows/issue-security-intake.yml",
    ".github/workflows/security-gate.yml",
    ".github/workflows/pr-preview.yml",
    "docs/security/owasp-top-10-2025-checklist.md",
    "docs/security/owasp-control-matrix.md",
    "docs/tutorial/README.md",
    "docs/tutorial/architecture.md",
    "docs/tutorial/create-issue.md",
    "docs/tutorial/cloud-agent.md",
    "docs/tutorial/ai-security-review.md",
    "docs/tutorial/human-pr-review.md",
    "docs/tutorial/demo-script.md",
    "docs/tutorial/current-status.md",
    "README.md",
]

for relative in required_files:
    require((ROOT / relative).is_file(), f"{relative} exists")

package = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))
readme = (ROOT / "README.md").read_text(encoding="utf-8")
main_source = (ROOT / "src/main.ts").read_text(encoding="utf-8")
flow_source = (ROOT / "src/flow.ts").read_text(encoding="utf-8")
security_workflow = (ROOT / ".github/workflows/security-gate.yml").read_text(encoding="utf-8")
intake_workflow = (ROOT / ".github/workflows/issue-security-intake.yml").read_text(encoding="utf-8")
preview_workflow = (ROOT / ".github/workflows/pr-preview.yml").read_text(encoding="utf-8")
copilot_instructions = (ROOT / ".github/copilot-instructions.md").read_text(encoding="utf-8")
checklist = (ROOT / "docs/security/owasp-top-10-2025-checklist.md").read_text(encoding="utf-8")
matrix = (ROOT / "docs/security/owasp-control-matrix.md").read_text(encoding="utf-8")
create_demo = (ROOT / "scripts/create_demo_issue.py").read_text(encoding="utf-8")
tutorial = (ROOT / "docs/tutorial/README.md").read_text(encoding="utf-8")

for script in ("lint", "lint:docs", "test", "test:python", "security:dom", "build", "verify"):
    require(script in package["scripts"], f"package.json defines {script}")

require("Cloud Agent Flow Lab" in readme, "README is the Flow Lab entrypoint")
require("```mermaid" in readme, "README includes the end-to-end diagram")
require("GitHub Actions 不是 cloud agent" in readme, "README separates Actions from Cloud Agent")
require("textContent" in main_source, "UI renders untrusted output with textContent")
require(not re.search(r"\.innerHTML\s*=", main_source), "main.ts has no innerHTML assignment")
require("security:approved" in flow_source and "security:blocked" in flow_source, "flow model includes approved and blocked paths")
require("actions/dependency-review-action@v4" in security_workflow, "Security Gate includes dependency review")
require("github/codeql-action/analyze@v4" in security_workflow, "Security Gate includes CodeQL")
require("npm run security:dom" in security_workflow, "Security Gate includes DOM XSS check")
require("issue_security_gate.py" in intake_workflow, "Issue workflow runs deterministic gate")
require("security:blocked" in intake_workflow, "Issue workflow can block unsafe tasks")
require("<!-- issue-security-intake -->" in intake_workflow, "Issue workflow finds the existing security report marker")
require("--method PATCH" in intake_workflow, "Issue workflow updates an existing security report comment")
require("npm run build" in preview_workflow and "dist/." in preview_workflow, "Preview deploys Vite build output")
require("required_contexts: []" in preview_workflow, "Preview deployment is independent from other check results")
require("transient_environment: true" in preview_workflow, "Preview deployment is marked as transient")
require("Copilot review 只能提供 Comment" in copilot_instructions, "Copilot instructions state AI review limitation")
for number in range(1, 11):
    require(f"A{number:02d}:2025" in checklist, f"checklist includes A{number:02d}:2025")
require("Automated" in matrix and "AI-assisted" in matrix and "Human review" in matrix, "matrix separates control owners")
require('"safe"' in create_demo and '"unsafe"' in create_demo, "demo script includes Safe and Unsafe scenarios")
require("args.dry_run or not args.create" in create_demo, "demo Issue creation defaults to dry-run")
require("copilot-swe-agent[bot]" in create_demo, "Safe scenario assigns the real Copilot cloud agent")
require('"custom_agent": custom_agent' in create_demo, "Safe scenario selects the Implementer custom agent")
require("10 至 15 分鐘" in tutorial, "tutorial declares a short onboarding path")

print("OK: Cloud Agent Flow Lab structure verification complete")
