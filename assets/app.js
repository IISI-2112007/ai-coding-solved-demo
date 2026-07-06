const stages = {
  local: {
    kicker: "Local trigger",
    title: "本地端 AI 發起任務",
    body: "本地端 AI 先把需求整理成 issue body，再透過 GitHub CLI 建立任務 issue。",
    points: [
      "使用 scripts/create_agent_issue.py。",
      "Issue 會帶上 local-ai label。",
      "任務格式包含 goal、context、allowed scope、acceptance criteria。"
    ]
  },
  issue: {
    kicker: "GitHub Issue",
    title: "Issue 是任務交接契約",
    body: "Issue template 固定任務欄位，讓 cloud agent 和 human reviewer 看到同一份輸入。",
    points: [
      "Goal 說明要完成什麼。",
      "Allowed scope 限制可改範圍。",
      "Acceptance criteria 定義完成證據。"
    ]
  },
  cloud: {
    kicker: "Cloud Agent Simulator",
    title: "GitHub Actions 在雲端接手",
    body: "當 issue 有 cloud-agent:ready label，workflow 會建立 branch 並產生 reviewable output。",
    points: [
      "執行 scripts/cloud_agent_simulator.py。",
      "產生 cloud-agent-output/issue-*。",
      "更新 DEMO_RESULTS.md。"
    ]
  },
  pr: {
    kicker: "Pull Request",
    title: "成果以 PR 呈現",
    body: "Cloud agent 不直接 merge；它只開 PR，讓成果可以被人類查看、討論與要求修改。",
    points: [
      "PR body 連回 issue。",
      "Diff 顯示 agent 產出。",
      "Reviewer 可以逐檔檢查。"
    ]
  },
  review: {
    kicker: "Human Review",
    title: "人類保留最後審查權",
    body: "MVP 的重點是證明 cloud agent 的成果不會直接進主線，而是先交給人類 review。",
    points: [
      "Approve 代表接受成果。",
      "Request changes 代表要求修改。",
      "Close PR 代表拒絕這次產出。"
    ]
  }
};

const stageButtons = document.querySelectorAll(".flow-step");
const stageKicker = document.querySelector("#stage-kicker");
const stageTitle = document.querySelector("#stage-title");
const stageBody = document.querySelector("#stage-body");
const stagePoints = document.querySelector("#stage-points");
const checks = document.querySelectorAll("[data-check]");
const progressLabel = document.querySelector("#progress-label");
const progressBar = document.querySelector("#progress-bar");

function renderStage(stageKey) {
  const stage = stages[stageKey];
  stageKicker.textContent = stage.kicker;
  stageTitle.textContent = stage.title;
  stageBody.textContent = stage.body;
  stagePoints.innerHTML = "";

  stage.points.forEach((point) => {
    const item = document.createElement("li");
    item.textContent = point;
    stagePoints.appendChild(item);
  });

  stageButtons.forEach((button) => {
    const isActive = button.dataset.stage === stageKey;
    button.classList.toggle("active", isActive);
    button.setAttribute("aria-selected", String(isActive));
  });
}

function updateProgress() {
  const done = [...checks].filter((check) => check.checked).length;
  const total = checks.length;
  const percent = total === 0 ? 0 : Math.round((done / total) * 100);
  progressLabel.textContent = `${done} / ${total} complete`;
  progressBar.style.width = `${percent}%`;
}

stageButtons.forEach((button) => {
  button.addEventListener("click", () => renderStage(button.dataset.stage));
});

checks.forEach((check) => {
  check.addEventListener("change", updateProgress);
});

updateProgress();
