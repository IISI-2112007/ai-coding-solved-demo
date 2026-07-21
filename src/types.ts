export type ScenarioId = "safe" | "blocked";

export type OwaspCategory =
  | "A01:2025"
  | "A03:2025"
  | "A05:2025"
  | "A06:2025"
  | "A08:2025";

export type StageStatus = "complete" | "active" | "pending" | "blocked" | "not-reached";

export type StageId =
  | "local-ai"
  | "issue"
  | "intake"
  | "cloud-agent"
  | "pull-request"
  | "ai-review"
  | "actions"
  | "preview"
  | "human-review"
  | "decision";

export interface FlowStage {
  id: StageId;
  shortLabel: string;
  title: string;
  actor: string;
  action: string;
  evidence: string;
  status: StageStatus;
  owaspCategories: OwaspCategory[];
}

export interface Scenario {
  id: ScenarioId;
  label: string;
  summary: string;
  outcome: string;
  tone: "positive" | "negative";
  stages: FlowStage[];
}

export interface IssueDraft {
  title: string;
  body: string;
}

export interface SecurityFinding {
  category: "A01:2025" | "A05:2025" | "INPUT";
  severity: "high" | "medium";
  message: string;
}

export interface ValidationResult {
  allowed: boolean;
  findings: SecurityFinding[];
}
