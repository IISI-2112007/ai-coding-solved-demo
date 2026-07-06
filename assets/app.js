const stages = {
  local: {
    kicker: "本地觸發",
    title: "本地端 AI 發起任務",
    body: "本地端 AI 先把需求整理成繁體中文 Issue，再透過 GitHub CLI 建立任務入口。",
    points: [
      "第一階段使用 scripts/create_agent_issue.py。",
      "第二階段使用 scripts/create_copilot_issue.py。",
      "任務格式包含目標、背景、允許修改範圍與驗收標準。"
    ]
  },
  issue: {
    kicker: "GitHub Issue",
    title: "Issue 是任務交接契約",
    body: "Issue template 固定任務欄位，讓 cloud agent 和人類 reviewer 看到同一份輸入。",
    points: [
      "目標說明要完成什麼。",
      "允許修改範圍限制可改檔案。",
      "驗收標準定義完成證據。"
    ]
  },
  cloud: {
    kicker: "Cloud Agent",
    title: "雲端 agent 接手",
    body: "第一階段由 GitHub Actions simulator 接手；第二階段由 Copilot cloud agent 從 Issue 接手並開 PR。",
    points: [
      "simulator 使用 cloud-agent:ready label。",
      "Copilot cloud agent 使用 copilot-cloud-agent:ready label。",
      "兩條路線最後都回到 PR 交給人類審查。"
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
  preview: {
    kicker: "PR Preview",
    title: "先看網頁成果",
    body: "第三階段會把 PR branch 部署到 gh-pages 的 pr-編號路徑，並在 PR 留下預覽網址。",
    points: [
      "預覽不是正式 production。",
      "每個 PR 可以有自己的 preview URL。",
      "人類可以先看成果，再回到 PR 看 diff 與 checks。"
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
  progressLabel.textContent = `${done} / ${total} 已完成`;
  progressBar.style.width = `${percent}%`;
}

stageButtons.forEach((button) => {
  button.addEventListener("click", () => renderStage(button.dataset.stage));
});

checks.forEach((check) => {
  check.addEventListener("change", updateProgress);
});

updateProgress();
