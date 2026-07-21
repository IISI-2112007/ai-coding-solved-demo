import { describe, expect, it } from "vitest";

import { buildScenario, clampStageIndex, validateIssueDraft } from "./flow";

describe("Cloud Agent 流程模型", () => {
  it("安全情境停在人類審查，不會自動 merge", () => {
    const scenario = buildScenario("safe");
    expect(scenario.stages.find((stage) => stage.id === "human-review")?.status).toBe("active");
    expect(scenario.stages.find((stage) => stage.id === "decision")?.status).toBe("pending");
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
