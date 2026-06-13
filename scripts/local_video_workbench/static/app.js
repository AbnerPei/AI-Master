const state = {
  pollingTimer: null,
  currentJob: null,
  capabilities: null,
};

const DEFAULT_API_BASE = "http://127.0.0.1:8765";
const API_BASE = window.location.protocol === "file:" ? DEFAULT_API_BASE : "";

const elements = {
  videoPath: document.getElementById("videoPath"),
  outputDir: document.getElementById("outputDir"),
  pickVideoButton: document.getElementById("pickVideoButton"),
  pickOutputButton: document.getElementById("pickOutputButton"),
  startButton: document.getElementById("startButton"),
  openOutputButton: document.getElementById("openOutputButton"),
  launchHint: document.getElementById("launchHint"),
  formMessage: document.getElementById("formMessage"),
  capabilityCards: document.getElementById("capabilityCards"),
  jobHeadline: document.getElementById("jobHeadline"),
  stageList: document.getElementById("stageList"),
  logStream: document.getElementById("logStream"),
  resultFiles: document.getElementById("resultFiles"),
  previewMarkdown: document.getElementById("previewMarkdown"),
};

async function requestJson(url, options = {}) {
  const fullUrl = `${API_BASE}${url}`;
  let response;
  try {
    response = await fetch(fullUrl, {
      headers: {
        "Content-Type": "application/json",
      },
      ...options,
    });
  } catch (error) {
    const prefix =
      window.location.protocol === "file:"
        ? `当前页面是通过 \`file://\` 打开的，请先运行 \`python3 scripts/local_video_workbench_app.py\`，再确保本地服务可访问：\`${DEFAULT_API_BASE}\`。`
        : `无法连接本地服务，请确认已经运行 \`python3 scripts/local_video_workbench_app.py\`。`;
    throw new Error(`${prefix} 原始错误：${error.message || "网络请求失败。"}`);
  }

  const payload = await response.json();
  if (!response.ok) {
    const message = payload?.error?.message || "请求失败。";
    throw new Error(message);
  }
  return payload;
}

function setMessage(message, tone = "info") {
  elements.formMessage.textContent = message;
  elements.formMessage.dataset.tone = tone;
}

function updateLaunchHint() {
  if (window.location.protocol === "file:") {
    elements.launchHint.innerHTML =
      `当前页面通过 <code>file://</code> 打开，但“选择视频 / 选择目录”仍会调用本地服务 <code>${escapeHtml(DEFAULT_API_BASE)}</code> 来弹出系统选择器。请先运行 <code>python3 scripts/local_video_workbench_app.py</code>。`;
    return;
  }
  elements.launchHint.textContent = "";
}

function renderCapabilities(capabilities) {
  state.capabilities = capabilities;
  const cards = [
    { title: "`ffmpeg`", ok: Boolean(capabilities.ffmpeg_available), detail: capabilities.ffmpeg_available || "未检测到" },
    { title: "`ffprobe`", ok: Boolean(capabilities.ffprobe_available), detail: capabilities.ffprobe_available || "未检测到" },
    { title: "本地 `ASR`", ok: Boolean(capabilities.local_asr_available), detail: capabilities.local_asr_available ? "可尝试本地转录" : "当前不可用" },
    { title: "`OpenAI` 兜底", ok: Boolean(capabilities.openai_key_available), detail: capabilities.openai_key_available ? "已检测到 `API Key`" : "未配置 `API Key`" },
  ];
  elements.capabilityCards.innerHTML = cards
    .map(
      (card) => `
        <div class="cap-card">
          <strong>${card.title}</strong>
          <span class="${card.ok ? "yes" : "no"}">${card.ok ? "已就绪" : "未就绪"}</span>
          <p>${escapeHtml(card.detail)}</p>
        </div>
      `,
    )
    .join("");
}

function renderStages(job) {
  if (!job) {
    elements.stageList.innerHTML = '<div class="stage-item pending"><strong>等待任务</strong><span>pending</span></div>';
    return;
  }
  elements.stageList.innerHTML = job.progress
    .map(
      (stage, index) => `
        <div class="stage-item ${stage.status}">
          <div>
            <strong>${index + 1}. ${escapeHtml(stage.label)}</strong>
          </div>
          <span>${escapeHtml(stage.status)}</span>
        </div>
      `,
    )
    .join("");
}

function renderLogs(job) {
  if (!job || !job.logs.length) {
    elements.logStream.textContent = "暂无日志。";
    elements.logStream.classList.add("empty-state");
    return;
  }
  elements.logStream.classList.remove("empty-state");
  elements.logStream.innerHTML = job.logs
    .map(
      (entry) => `
        <div class="log-entry ${entry.level}">
          <strong>${escapeHtml(entry.timestamp)} · ${escapeHtml(entry.level.toUpperCase())}</strong>
          <div>${escapeHtml(entry.message)}</div>
        </div>
      `,
    )
    .join("");
  elements.logStream.scrollTop = elements.logStream.scrollHeight;
}

function renderResults(job) {
  if (!job || !job.result_files.length) {
    elements.resultFiles.textContent = "尚未生成结果文件。";
    elements.resultFiles.classList.add("empty-state");
    return;
  }
  elements.resultFiles.classList.remove("empty-state");
  elements.resultFiles.innerHTML = job.result_files
    .map(
      (item) => `
        <div class="result-item">
          <div class="result-meta">
            <strong>${escapeHtml(item.label)}</strong>
            <code>${escapeHtml(item.path)}</code>
          </div>
        </div>
      `,
    )
    .join("");
}

function renderPreview(job) {
  if (!job || !job.preview_markdown) {
    elements.previewMarkdown.textContent = "等待任务完成后展示预览。";
    return;
  }
  elements.previewMarkdown.textContent = job.preview_markdown;
}

function updateControls(job) {
  const isRunning = job?.status === "running";
  elements.startButton.disabled = isRunning;
  elements.pickVideoButton.disabled = isRunning;
  elements.pickOutputButton.disabled = isRunning;
  elements.videoPath.disabled = isRunning;
  elements.outputDir.disabled = isRunning;

  const openPath = job?.run_dir || elements.outputDir.value.trim();
  elements.openOutputButton.disabled = !openPath;
  elements.openOutputButton.dataset.path = openPath || "";
}

function renderJob(job) {
  state.currentJob = job;
  renderStages(job);
  renderLogs(job);
  renderResults(job);
  renderPreview(job);
  updateControls(job);

  if (!job) {
    elements.jobHeadline.textContent = "当前没有运行中的任务。";
    return;
  }

  const statusTextMap = {
    queued: "等待中",
    running: "运行中",
    succeeded: "已完成",
    failed: "已失败",
  };
  elements.jobHeadline.textContent = `任务 ${job.job_id} · ${statusTextMap[job.status] || job.status} · 当前阶段：${job.stage_label}`;

  if (job.status === "failed" && job.error?.message) {
    setMessage(job.error.message, "error");
  } else if (job.status === "succeeded") {
    setMessage("任务完成，可以查看结果并打开输出目录。", "success");
  }
}

async function refreshJob() {
  const payload = await requestJson("/api/job", { method: "GET" });
  renderJob(payload.job);
}

function startPolling() {
  stopPolling();
  state.pollingTimer = window.setInterval(async () => {
    try {
      await refreshJob();
      if (state.currentJob?.status !== "running") {
        stopPolling();
      }
    } catch (error) {
      stopPolling();
      setMessage(error.message || "轮询任务状态失败。", "error");
    }
  }, 1200);
}

function stopPolling() {
  if (state.pollingTimer) {
    window.clearInterval(state.pollingTimer);
    state.pollingTimer = null;
  }
}

async function pickPath(endpoint, targetInput) {
  try {
    setMessage("正在等待系统选择器返回。");
    const payload = await requestJson(endpoint, { method: "POST", body: "{}" });
    if (payload.cancelled) {
      setMessage("已取消选择。", "warning");
      return;
    }
    targetInput.value = payload.path || "";
    setMessage("路径已更新。", "success");
    updateControls(state.currentJob);
  } catch (error) {
    setMessage(error.message || "打开系统选择器失败。", "error");
  }
}

function pickVideoPath() {
  pickPath("/api/pick-video", elements.videoPath);
}

function pickOutputDir() {
  pickPath("/api/pick-output-dir", elements.outputDir);
}

async function startJob() {
  const videoPath = elements.videoPath.value.trim();
  const outputDir = elements.outputDir.value.trim();
  if (!videoPath || !outputDir) {
    setMessage("启动前请先选择视频文件和输出目录。", "error");
    return;
  }

  try {
    setMessage("正在启动任务。");
    const payload = await requestJson("/api/start-job", {
      method: "POST",
      body: JSON.stringify({
        video_path: videoPath,
        output_dir: outputDir,
      }),
    });
    renderJob(payload.job);
    startPolling();
    setMessage("任务已启动，开始轮询状态。", "success");
  } catch (error) {
    setMessage(error.message || "启动任务失败。", "error");
  }
}

async function openOutputPath() {
  const path = elements.openOutputButton.dataset.path;
  if (!path) {
    setMessage("当前没有可打开的输出路径。", "warning");
    return;
  }
  try {
    await requestJson("/api/open-output-dir", {
      method: "POST",
      body: JSON.stringify({ path }),
    });
    setMessage("已请求系统打开输出目录。", "success");
  } catch (error) {
    setMessage(error.message || "打开输出目录失败。", "error");
  }
}

function escapeHtml(value) {
  return value
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#39;");
}

async function bootstrap() {
  updateLaunchHint();
  try {
    const capabilities = await requestJson("/api/capabilities", { method: "GET" });
    renderCapabilities(capabilities);
  } catch (error) {
    setMessage(error.message || "读取能力状态失败。", "error");
  }

  try {
    await refreshJob();
  } catch (error) {
    setMessage(error.message || "读取当前任务状态失败。", "error");
  }
}

elements.pickVideoButton.addEventListener("click", pickVideoPath);
elements.pickOutputButton.addEventListener("click", pickOutputDir);
elements.startButton.addEventListener("click", startJob);
elements.openOutputButton.addEventListener("click", openOutputPath);

bootstrap();
