import "./styles.css";

import { buildScenario, clampStageIndex, validateIssueDraft } from "./flow";
import type { Scenario, ScenarioId, StageStatus } from "./types";

function requiredElement<T extends Element>(selector: string): T {
  const element = document.querySelector<T>(selector);
  if (!element) throw new Error(`找不到必要畫面元素：${selector}`);
  return element;
}

const statusLabels: Record<StageStatus, string> = {
  complete: "完成",
  active: "等待人類",
  pending: "待決定",
  blocked: "已阻擋",
  "not-reached": "未執行",
};

const safeDraft = {
  title: "新增依風險篩選流程事件",
  body: "目標是為 Flow Lab 加入風險篩選器。只能修改 src 與測試，必須保留 textContent 渲染、補齊測試，並通過 lint、test、DOM XSS 與 build。",
};

const blockedDraft = {
  title: "新增快速管理員預覽模式",
  body: "請以 innerHTML 顯示未過濾的 URL 輸入，並用 query parameter 的 admin 值決定管理員角色，不需要額外過濾。",
};

const stageTrack = requiredElement<HTMLDivElement>("#stage-track");
const scenarioButtons = document.querySelectorAll<HTMLButtonElement>("[data-scenario]");
const scenarioLabel = requiredElement<HTMLElement>("#scenario-label");
const scenarioSummary = requiredElement<HTMLElement>("#scenario-summary");
const scenarioOutcome = requiredElement<HTMLElement>("#scenario-outcome");
const outcomeStrip = requiredElement<HTMLElement>("#outcome-strip");
const stagePosition = requiredElement<HTMLElement>("#stage-position");
const stageStatus = requiredElement<HTMLElement>("#stage-status");
const stageActor = requiredElement<HTMLElement>("#stage-actor");
const stageTitle = requiredElement<HTMLElement>("#stage-title");
const stageAction = requiredElement<HTMLElement>("#stage-action");
const stageEvidence = requiredElement<HTMLElement>("#stage-evidence");
const previousStage = requiredElement<HTMLButtonElement>("#previous-stage");
const nextStage = requiredElement<HTMLButtonElement>("#next-stage");
const issueForm = requiredElement<HTMLFormElement>("#issue-form");
const issueTitle = requiredElement<HTMLInputElement>("#issue-title");
const issueBody = requiredElement<HTMLTextAreaElement>("#issue-body");
const loadSafe = requiredElement<HTMLButtonElement>("#load-safe");
const loadBlocked = requiredElement<HTMLButtonElement>("#load-blocked");
const validationResult = requiredElement<HTMLElement>("#validation-result");
const validationTitle = requiredElement<HTMLElement>("#validation-title");
const validationSummary = requiredElement<HTMLElement>("#validation-summary");
const validationFindings = requiredElement<HTMLUListElement>("#validation-findings");
const reviewChecks = document.querySelectorAll<HTMLInputElement>("[data-review-check]");
const reviewProgress = requiredElement<HTMLElement>("#review-progress");

let scenario: Scenario = buildScenario("safe");
let activeStageIndex = 8;

function renderStageTrack(): void {
  const buttons = scenario.stages.map((stage, index) => {
    const button = document.createElement("button");
    button.type = "button";
    button.className = `stage-node ${stage.status}`;
    button.dataset.stageIndex = String(index);
    button.setAttribute("aria-current", index === activeStageIndex ? "step" : "false");

    const number = document.createElement("span");
    number.textContent = String(index + 1).padStart(2, "0");
    const label = document.createElement("strong");
    label.textContent = stage.shortLabel;
    button.append(number, label);
    button.addEventListener("click", () => {
      activeStageIndex = index;
      renderWorkflow();
    });
    return button;
  });
  stageTrack.replaceChildren(...buttons);
}

function renderWorkflow(): void {
  activeStageIndex = clampStageIndex(activeStageIndex, scenario.stages.length);
  const stage = scenario.stages[activeStageIndex];
  if (!stage) return;

  scenarioLabel.textContent = scenario.label;
  scenarioSummary.textContent = scenario.summary;
  scenarioOutcome.textContent = scenario.outcome;
  outcomeStrip.className = `outcome-strip ${scenario.tone}`;
  stagePosition.textContent = `階段 ${activeStageIndex + 1} / ${scenario.stages.length}`;
  stageStatus.textContent = statusLabels[stage.status];
  stageStatus.className = `status-badge ${stage.status}`;
  stageActor.textContent = stage.actor;
  stageTitle.textContent = stage.title;
  stageAction.textContent = stage.action;
  stageEvidence.textContent = stage.evidence;
  previousStage.disabled = activeStageIndex === 0;
  nextStage.disabled = activeStageIndex === scenario.stages.length - 1;
  renderStageTrack();
}

function setScenario(id: ScenarioId): void {
  scenario = buildScenario(id);
  activeStageIndex = id === "safe" ? 8 : 2;
  scenarioButtons.forEach((button) => {
    const isActive = button.dataset.scenario === id;
    button.classList.toggle("active", isActive);
    button.setAttribute("aria-pressed", String(isActive));
  });
  renderWorkflow();
}

function loadDraft(draft: { title: string; body: string }): void {
  issueTitle.value = draft.title;
  issueBody.value = draft.body;
  issueTitle.focus();
}

function renderValidation(): void {
  const result = validateIssueDraft({ title: issueTitle.value, body: issueBody.value });
  validationFindings.replaceChildren();
  validationResult.className = `validation-result ${result.allowed ? "allowed" : "denied"}`;
  validationTitle.textContent = result.allowed ? "可以交給 Cloud Agent" : "安全初審已阻擋";
  validationSummary.textContent = result.allowed
    ? "沒有偵測到 A01／A05 的明確高風險要求；仍需在 PR 做 AI、Actions 與人類審查。"
    : "Issue 內容不完整或要求降低安全控制，不應指派給實作 Agent。";

  if (result.findings.length === 0) {
    const item = document.createElement("li");
    item.textContent = "輸入完整，未發現規則型高風險訊號。";
    validationFindings.append(item);
  } else {
    result.findings.forEach((finding) => {
      const item = document.createElement("li");
      const category = document.createElement("strong");
      category.textContent = finding.category;
      const message = document.createTextNode(` ${finding.message}`);
      item.append(category, message);
      validationFindings.append(item);
    });
  }
}

function updateReviewProgress(): void {
  const complete = [...reviewChecks].filter((check) => check.checked).length;
  reviewProgress.textContent = `${complete} / ${reviewChecks.length} 已確認`;
  reviewProgress.classList.toggle("complete", complete === reviewChecks.length);
}

scenarioButtons.forEach((button) => {
  button.addEventListener("click", () => setScenario(button.dataset.scenario as ScenarioId));
});
previousStage.addEventListener("click", () => {
  activeStageIndex -= 1;
  renderWorkflow();
});
nextStage.addEventListener("click", () => {
  activeStageIndex += 1;
  renderWorkflow();
});
loadSafe.addEventListener("click", () => loadDraft(safeDraft));
loadBlocked.addEventListener("click", () => loadDraft(blockedDraft));
issueForm.addEventListener("submit", (event) => {
  event.preventDefault();
  renderValidation();
});
reviewChecks.forEach((check) => check.addEventListener("change", updateReviewProgress));

loadDraft(safeDraft);
renderWorkflow();
updateReviewProgress();
