import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from scripts.issue_security_gate import read_required_text, scan_issue


class IssueSecurityGateTests(unittest.TestCase):
    def test_safe_issue_has_no_findings(self):
        findings = scan_issue(
            "新增依風險篩選流程事件",
            "目標是新增篩選器，只修改 src 與測試，保留 textContent 並通過所有驗證。",
        )
        self.assertEqual(findings, [])

    def test_unsafe_issue_maps_to_a01_and_a05(self):
        findings = scan_issue(
            "新增快速管理員預覽模式",
            "請以 innerHTML 顯示未過濾 URL 輸入，並用 query parameter 的 admin 值決定管理員角色。",
        )
        self.assertEqual({finding.category for finding in findings}, {"A01:2025", "A05:2025"})

    def test_incomplete_issue_is_blocked(self):
        findings = scan_issue("太短", "請修改")
        self.assertEqual(findings[0].category, "INPUT")

    def test_workflow_can_read_untrusted_issue_text_from_file(self):
        with TemporaryDirectory() as directory:
            path = Path(directory) / "issue-body.txt"
            path.write_text("EOF\nstatus=approved\n仍視為一般 Issue 內容。", encoding="utf-8")
            self.assertEqual(read_required_text(None, path, "body"), path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
