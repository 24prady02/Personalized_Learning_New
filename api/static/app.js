const $ = (id) => document.getElementById(id);
const show = (id) => $(id).hidden = false;
const hide = (id) => $(id).hidden = true;
const setError = (msg) => { const e = $("error"); if (msg) { e.textContent = msg; show("error"); } else { hide("error"); } };

const state = {
  sessionId: null,
  currentItem: null,
  selectedChoice: null,
};

async function api(path, opts = {}) {
  const r = await fetch(path, {
    headers: { "Content-Type": "application/json" },
    ...opts,
  });
  if (!r.ok) {
    const txt = await r.text().catch(() => r.statusText);
    throw new Error(`${r.status}: ${txt}`);
  }
  return r.json();
}

function renderItem(item) {
  $("quiz-title").textContent = item.title;
  $("quiz-code").textContent = item.code;
  $("quiz-question").textContent = item.question;
  const list = $("quiz-options");
  list.innerHTML = "";
  item.options.forEach((opt) => {
    const li = document.createElement("li");
    li.dataset.key = opt.key;
    li.innerHTML = `<span class="opt-key">${opt.key}</span><span>${escapeHtml(opt.text)}</span>`;
    li.addEventListener("click", () => selectChoice(opt.key));
    list.appendChild(li);
  });
  state.selectedChoice = null;
  $("submit-choice").disabled = true;
}

function selectChoice(key) {
  state.selectedChoice = key;
  document.querySelectorAll("#quiz-options li").forEach((li) => {
    li.classList.toggle("selected", li.dataset.key === key);
  });
  $("submit-choice").disabled = false;
}

function escapeHtml(s) {
  return s.replace(/[&<>"']/g, (c) => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", "\"": "&quot;", "'": "&#39;",
  }[c]));
}

async function startSession() {
  setError(null);
  try {
    const data = await api("/api/start");
    state.sessionId = data.session_id;
    state.currentItem = data.item;
    renderItem(data.item);
    hide("step-belief");
    hide("step-probe");
    hide("step-correct");
    hide("step-done");
    show("step-quiz");
  } catch (e) {
    setError(`Could not load a question: ${e.message}`);
  }
}

async function submitChoice() {
  if (!state.selectedChoice) return;
  setError(null);
  $("submit-choice").disabled = true;
  try {
    await api("/api/answer", {
      method: "POST",
      body: JSON.stringify({
        session_id: state.sessionId,
        choice: state.selectedChoice,
        belief: "",
      }),
    });
    hide("step-quiz");
    $("belief-input").value = "";
    $("submit-belief").disabled = true;
    show("step-belief");
    $("belief-input").focus();
  } catch (e) {
    setError(e.message);
    $("submit-choice").disabled = false;
  }
}

async function submitBelief() {
  const belief = $("belief-input").value.trim();
  if (!belief) return;
  setError(null);
  $("submit-belief").disabled = true;
  show("loading");
  try {
    const data = await api("/api/correct", {
      method: "POST",
      body: JSON.stringify({
        session_id: state.sessionId,
        belief,
      }),
    });
    handleCorrectResponse(data, "step-belief");
  } catch (e) {
    setError(e.message);
    $("submit-belief").disabled = false;
  } finally {
    hide("loading");
  }
}

async function submitProbe() {
  const ans = $("probe-input").value.trim();
  if (!ans) return;
  setError(null);
  $("submit-probe").disabled = true;
  show("loading");
  try {
    const data = await api("/api/probe_answer", {
      method: "POST",
      body: JSON.stringify({
        session_id: state.sessionId,
        probe_answer: ans,
      }),
    });
    handleCorrectResponse(data, "step-probe");
  } catch (e) {
    setError(e.message);
    $("submit-probe").disabled = false;
  } finally {
    hide("loading");
  }
}

// Branches on the backend's response type — show probe Step 2.5 when the
// grader wants a follow-up, otherwise show the explanation Step 3.
function handleCorrectResponse(data, hideStep) {
  hide(hideStep);
  if (data.type === "probe") {
    renderProbe(data);
    show("step-probe");
    $("probe-input").focus();
  } else {
    renderCorrection(data);
    show("step-correct");
  }
}

function renderProbe(data) {
  const round = data.probe_round || 1;
  const cap = data.probe_round_max || 2;
  $("probe-round-label").textContent =
    `Quick check ${round} of ${cap}` +
    (data.probe_target_level ? ` — target ${data.probe_target_level}` : "");
  $("probe-question").textContent = data.probe_question || "";
  $("probe-input").value = "";
  $("submit-probe").disabled = true;
}

function renderCorrection(data) {
  $("correct-title").textContent = data.title;
  const verdict = $("correct-verdict");
  if (data.your_choice === data.correct_choice) {
    verdict.textContent = `You picked ${data.your_choice} — that's right.`;
    verdict.classList.remove("bad");
    verdict.classList.add("good");
  } else {
    verdict.textContent = `You picked ${data.your_choice}; the answer is ${data.correct_choice}.`;
    verdict.classList.remove("good");
    verdict.classList.add("bad");
  }
  $("correct-explanation").textContent = data.explanation;

  const btn = $("next-question");
  if (data.next_item_id) {
    btn.textContent = "Next question";
    btn.onclick = () => loadNextItem(data.next_item_id);
  } else {
    btn.textContent = "Finish";
    btn.onclick = () => {
      hide("step-correct");
      show("step-done");
    };
  }
}

async function loadNextItem(itemId) {
  setError(null);
  try {
    const item = await api(`/api/item/${itemId}`);
    state.currentItem = item;
    renderItem(item);
    hide("step-correct");
    show("step-quiz");
  } catch (e) {
    setError(e.message);
  }
}

document.addEventListener("DOMContentLoaded", () => {
  $("submit-choice").addEventListener("click", submitChoice);
  $("submit-belief").addEventListener("click", submitBelief);
  $("belief-input").addEventListener("input", (e) => {
    $("submit-belief").disabled = e.target.value.trim().length === 0;
  });
  // Step 2.5 probe wiring
  $("submit-probe").addEventListener("click", submitProbe);
  $("probe-input").addEventListener("input", (e) => {
    $("submit-probe").disabled = e.target.value.trim().length === 0;
  });
  startSession();
});
