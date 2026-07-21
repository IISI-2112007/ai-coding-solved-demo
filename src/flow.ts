import type {
  FlowStage,
  IssueDraft,
  OwaspCategory,
  Scenario,
  ScenarioId,
  SecurityFinding,
  ValidationResult,
} from "./types";

export const OWASP_CATEGORY_LABELS: Record<OwaspCategory, string> = {
  "A01:2025": "A01 存取控制失效",
  "A03:2025": "A03 注入攻擊",
  "A05:2025": "A05 安全設定錯誤",
  "A06:2025": "A06 已知弱點元件",
  "A08:2025": "A08 軟體與資料完整性失效",
};

const stageDefinitions: Omit<FlowStage, "status">[] = [
  {
    id: "local-ai",
    shortLabel: "本地 AI",
    title: "把需求整理成可驗收任務",
    actor: "本地端 AI",
    action: "產生繁體中文 Issue 草稿，明確列出範圍、驗收與禁止事項。",
    evidence: "dry-run 輸出與 Issue body",
    owaspCategories: [],
  },
  {
    id: "issue",
    shortLabel: "Issue",
    title: "Issue 成為交接契約",
    actor: "GitHub Issue",
    action: "保存所有 Agent 與 reviewer 共用的原始需求，不把口頭脈絡藏在本機。",
    evidence: "Issue URL、labels、assignee",
    owaspCategories: [],
  },
  {
    id: "intake",
    shortLabel: "安全初審",
    title: "先判斷需求本身是否安全",
    actor: "Issue safety gate",
    action: "辨識 A01 Broken Access Control 與 A03 Injection 等明確危險要求。",
    evidence: "security:approved 或 security:blocked",
    owaspCategories: ["A01:2025", "A03:2025"],
  },
  {
    id: "cloud-agent",
    shortLabel: "Cloud Agent",
    title: "真正的 Copilot cloud agent 實作",
    actor: "GitHub Copilot cloud agent",
    action: "在 GitHub 的 ephemeral environment 中修改、測試、commit 並開 PR。",
    evidence: "Copilot session、agent branch、commit",
    owaspCategories: ["A03:2025"],
  },
  {
    id: "pull-request",
    shortLabel: "PR",
    title: "用 PR 呈現可追蹤差異",
    actor: "Pull Request",
    action: "連回 Issue，列出修改內容、驗證方式與人類審查重點。",
    evidence: "PR URL 與 Files changed",
    owaspCategories: [],
  },
  {
    id: "ai-review",
    shortLabel: "AI Review",
    title: "Copilot 依 OWASP 提出審查意見",
    actor: "GitHub Copilot code review",
    action: "依 repository instructions 檢查風險並留下 Comment review。",
    evidence: "Copilot review comments",
    owaspCategories: ["A01:2025", "A03:2025", "A05:2025", "A06:2025"],
  },
  {
    id: "actions",
    shortLabel: "Actions",
    title: "可重現的安全閘門決定能否前進",
    actor: "GitHub Actions",
    action: "執行 test、lint、build、DOM XSS、CodeQL 與 dependency review。",
    evidence: "Required status checks",
    owaspCategories: ["A05:2025", "A06:2025", "A08:2025"],
  },
  {
    id: "preview",
    shortLabel: "Preview",
    title: "先看實際成果，不只看 diff",
    actor: "GitHub Pages",
    action: "部署 PR build 產物到獨立網址，供 reviewer 操作確認。",
    evidence: "HTTP 200 Preview URL",
    owaspCategories: [],
  },
  {
    id: "human-review",
    shortLabel: "Human",
    title: "人類整合需求、畫面與風險證據",
    actor: "Human reviewer",
    action: "先操作 Preview，再檢查 diff、tests、AI findings 與未涵蓋風險。",
    evidence: "Approve 或 Request changes",
    owaspCategories: ["A01:2025"],
  },
  {
    id: "decision",
    shortLabel: "Decision",
    title: "只有人類決定是否合併",
    actor: "Repository maintainer",
    action: "安全與需求都成立才 merge；否則退回修改或關閉 PR。",
    evidence: "Merge、退回或拒絕紀錄",
    owaspCategories: [],
  },
];

function makeStages(scenarioId: ScenarioId): FlowStage[] {
  return stageDefinitions.map((stage, index) => {
    if (scenarioId === "blocked") {
      if (index < 2) return { ...stage, status: "complete" };
      if (stage.id === "intake") return { ...stage, status: "blocked" };
      return { ...stage, status: "not-reached" };
    }

    if (index < 8) return { ...stage, status: "complete" };
    if (stage.id === "human-review") return { ...stage, status: "active" };
    return { ...stage, status: "pending" };
  });
}

export function buildScenario(id: ScenarioId): Scenario {
  if (id === "blocked") {
    return {
      id,
      label: "不安全 Issue",
      summary: "Issue 要求以未過濾輸入產生 HTML，並信任可竄改的角色參數。",
      outcome: "安全初審阻擋，不交給實作 Agent；必要時以受控 PR 證明 checks 會失敗。",
      tone: "negative",
      stages: makeStages(id),
    };
  }

  return {
    id,
    label: "安全 Issue",
    summary: "Issue 要求一項小型、可測試的流程功能，且禁止降低既有安全控制。",
    outcome: "Cloud Agent 完成 PR 與 Preview，目前停在人類審查，不自動 merge。",
    tone: "positive",
    stages: makeStages(id),
  };
}

function includesAny(value: string, patterns: RegExp[]): boolean {
  return patterns.some((pattern) => pattern.test(value));
}

export function validateIssueDraft(draft: IssueDraft): ValidationResult {
  const findings: SecurityFinding[] = [];
  const title = draft.title.trim();
  const body = draft.body.trim();
  const allText = `${title}\n${body}`;

  if (title.length < 8 || body.length < 30) {
    findings.push({
      category: "INPUT",
      severity: "medium",
      message: "Issue 必須提供清楚標題與至少 30 字的目標、範圍及驗收內容。",
    });
  }

  if (
    includesAny(allText, [
      /query\s*parameter.{0,30}(admin|管理員)/iu,
      /(admin|管理員).{0,30}query\s*parameter/iu,
      /URL\s*參數.{0,30}(權限|角色|管理員)/iu,
      /(權限|角色|管理員).{0,30}URL\s*參數/iu,
    ])
  ) {
    findings.push({
      category: "A01:2025",
      severity: "high",
      message: "不可用使用者可竄改的 URL／query parameter 決定角色或管理員權限。",
    });
  }

  if (
    includesAny(allText, [
      /innerHTML.{0,40}(未過濾|URL|輸入|參數)/iu,
      /(未過濾|URL|輸入|參數).{0,40}innerHTML/iu,
      /不(?:用|需).{0,20}(escape|sanitize|編碼|過濾)/iu,
    ])
  ) {
    findings.push({
      category: "A05:2025",
      severity: "high",
      message: "未受信任輸入不得直接進入 HTML sink；請使用 textContent 與明確驗證。",
    });
  }

  return {
    allowed: findings.length === 0,
    findings,
  };
}

export function clampStageIndex(index: number, stageCount: number): number {
  if (stageCount <= 0) return 0;
  return Math.min(Math.max(index, 0), stageCount - 1);
}

export function filterStagesByOwaspCategory(
  stages: FlowStage[],
  category: OwaspCategory,
): FlowStage[] {
  return stages.filter((stage) => stage.owaspCategories.includes(category));
}
