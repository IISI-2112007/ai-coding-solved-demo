import unittest

from scripts.create_demo_issue import build_agent_assignment


class CreateDemoIssueTests(unittest.TestCase):
    def test_assignment_uses_real_copilot_and_custom_agent(self):
        payload = build_agent_assignment(
            "IISI-2112007/ai-coding-solved-demo",
            "main",
            "implementer",
        )

        self.assertEqual(payload["assignees"], ["copilot-swe-agent[bot]"])
        self.assertEqual(payload["agent_assignment"]["custom_agent"], "implementer")
        self.assertEqual(payload["agent_assignment"]["base_branch"], "main")


if __name__ == "__main__":
    unittest.main()
