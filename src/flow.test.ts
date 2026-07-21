import { describe, expect, it } from "vitest";

import {
  OWASP_CATEGORY_LABELS,
  buildScenario,
  clampStageIndex,
  filterStagesByOwaspCategory,
  validateIssueDraft,
} from "./flow";

describe("Cloud Agent 流程模型", () => {
  it("安全情境停在人類審查，且人類決策在其後", () => {
    const scenario = buildScenario("safe");
    const humanReviewIndex = scenario.stages.findIndex((stage) => stage.id === "human-review");
    const decisionIndex = scenario.stages.findIndex((stage) => stage.id === "decision");

    expect(scenario.stages[humanReviewIndex]?.status).toBe("active");
    expect(scenario.stages[decisionIndex]?.status).toBe("pending");
    expect(humanReviewIndex).toBeGreaterThanOrEqual(0);
    expect(decisionIndex).toBeGreaterThan(humanReviewIndex);
  });

  it("不安全情境在安全初審阻擋後不再交給 Cloud Agent", () => {
    const scenario = buildScenario("blocked");
    expect(scenario.stages.find((stage) => stage.id === "intake")?.status).toBe("blocked");
    expect(scenario.stages.find((stage) => stage.id === "cloud-agent")?.status).toBe("not-reached");
  });

  it("辨識 A01 與 A05 的危險 Issue 要求", () => {
    const result = validateIssueDraft({
      title: "請加入快速管理員預覽模式",
      body: "請以 innerHTML 顯示未過濾的 URL 輸入，並用 query parameter 的 admin 值決定管理員角色。",
    });
    expect(result.allowed).toBe(false);
    expect(result.findings.map((finding) => finding.category)).toEqual(
      expect.arrayContaining(["A01:2025", "A05:2025"]),
    );
  });

  it("接受範圍與驗收清楚的安全 Issue", () => {
    const result = validateIssueDraft({
      title: "新增依風險篩選流程事件",
      body: "目標是新增風險篩選器，只能修改 src 與測試；必須保留 textContent 渲染並通過所有驗證。",
    });
    expect(result.allowed).toBe(true);
    expect(result.findings).toHaveLength(0);
  });

  it("阻擋內容不足而無法驗收的 Issue", () => {
    const result = validateIssueDraft({ title: "太短", body: "請修改" });
    expect(result.allowed).toBe(false);
    expect(result.findings[0]?.category).toBe("INPUT");
  });

  it("流程導覽不會超出邊界", () => {
    expect(clampStageIndex(-1, 10)).toBe(0);
    expect(clampStageIndex(12, 10)).toBe(9);
  });
});

describe("OWASP 風險篩選", () => {
  it("依 A01:2025 篩選：回傳含安全初審、AI Review 與人類審查的階段", () => {
    const stages = buildScenario("safe").stages;
    const result = filterStagesByOwaspCategory(stages, "A01:2025");
    const ids = result.map((stage) => stage.id);
    expect(ids).toContain("intake");
    expect(ids).toContain("ai-review");
    expect(ids).toContain("human-review");
    expect(ids).not.toContain("local-ai");
    expect(ids).not.toContain("decision");
  });

  it("依 A03:2025 篩選：回傳含 Cloud Agent、AI Review 與 Actions 的階段（軟體供應鏈）", () => {
    const stages = buildScenario("safe").stages;
    const result = filterStagesByOwaspCategory(stages, "A03:2025");
    const ids = result.map((stage) => stage.id);
    expect(ids).toContain("cloud-agent");
    expect(ids).toContain("ai-review");
    expect(ids).toContain("actions");
    expect(ids).not.toContain("intake");
  });

  it("依 A08:2025 篩選：只回傳 Actions 階段", () => {
    const stages = buildScenario("safe").stages;
    const result = filterStagesByOwaspCategory(stages, "A08:2025");
    const ids = result.map((stage) => stage.id);
    expect(ids).toEqual(["actions"]);
  });

  it("篩選結果在 blocked 情境下與 safe 情境階段 id 相同", () => {
    const safeStages = buildScenario("safe").stages;
    const blockedStages = buildScenario("blocked").stages;
    const safeIds = filterStagesByOwaspCategory(safeStages, "A01:2025").map((s) => s.id);
    const blockedIds = filterStagesByOwaspCategory(blockedStages, "A01:2025").map((s) => s.id);
    expect(safeIds).toEqual(blockedIds);
  });

  it("OWASP_CATEGORY_LABELS 包含所有預期分類的繁體中文標籤", () => {
    expect(OWASP_CATEGORY_LABELS["A01:2025"]).toBeTruthy();
    expect(OWASP_CATEGORY_LABELS["A03:2025"]).toBeTruthy();
    expect(OWASP_CATEGORY_LABELS["A05:2025"]).toBeTruthy();
    expect(OWASP_CATEGORY_LABELS["A06:2025"]).toBeTruthy();
    expect(OWASP_CATEGORY_LABELS["A08:2025"]).toBeTruthy();
  });
});
