const $ = (id) => document.getElementById(id);
const show = (id) => $(id).hidden = false;
const hide = (id) => $(id).hidden = true;
const setError = (msg) => { const e = $("error"); if (msg) { e.textContent = msg; show("error"); } else { hide("error"); } };

const state = {
  sessionId: null,
  currentItem: null,
  selectedChoice: null,
  identity: null,   // {student_id, role, course, teach_variant, consent_given}
};

// Forward ?student= and ?token= query params on every API call so the
// backend's _resolve_student_id can bind the session to the right
// per-student key. Same-origin fetches already inherit them via
// document.location, but the server's start endpoint reads them from
// the REQUEST query string so we attach them explicitly.
function withQuery(path) {
  const sp = new URLSearchParams(window.location.search);
  const passthrough = new URLSearchParams();
  for (const k of ["student", "student_id", "token"]) {
    const v = sp.get(k);
    if (v) passthrough.set(k, v);
  }
  const q = passthrough.toString();
  if (!q) return path;
  return path + (path.includes("?") ? "&" : "?") + q;
}

async function api(path, opts = {}) {
  const r = await fetch(withQuery(path), {
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

// ── Identity + privacy (wired 2026-05-30 to /api/me, /api/me/consent,
//    and /api/me/delete) ─────────────────────────────────────────────────
async function loadIdentity() {
  try {
    const me = await api("/api/me");
    state.identity = me;
    const label = $("identity");
    if (me.student_id && me.student_id !== "anon") {
      label.textContent = `Signed in as ${me.student_id}` +
        (me.role !== "student" ? ` (${me.role})` : "");
      show("identity");
    }
    $("consent-toggle").checked = !!me.consent_given;
    $("privacy-id").textContent = `Student key: ${me.student_id}` +
      (me.teach_variant ? ` · variant: ${me.teach_variant}` : "");
  } catch (e) {
    console.warn("identity load failed", e);
  }
}

function openPrivacy()  { $("privacy-modal").hidden = false; }
function closePrivacy() {
  $("privacy-modal").hidden = true;
  $("privacy-status").textContent = "";
}

async function toggleConsent(e) {
  const given = !!e.target.checked;
  try {
    await api("/api/me/consent", {
      method: "POST",
      body: JSON.stringify({ given }),
    });
    $("privacy-status").textContent = given
      ? "Consent recorded."
      : "Consent revoked.";
  } catch (err) {
    $("privacy-status").textContent = `Could not save: ${err.message}`;
    e.target.checked = !given;
  }
}

async function deleteMyData() {
  if (!confirm("This will delete your mastery, progression history, and " +
                "A/B assignment. The deletion is logged. Continue?")) return;
  try {
    const res = await api("/api/me/delete", { method: "POST" });
    $("privacy-status").textContent =
      `Deleted ${JSON.stringify(res.deleted_rows)} — restarting session…`;
    setTimeout(() => location.reload(), 900);
  } catch (err) {
    $("privacy-status").textContent = `Delete failed: ${err.message}`;
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
  // Privacy drawer
  $("open-privacy").addEventListener("click", openPrivacy);
  $("close-privacy").addEventListener("click", closePrivacy);
  $("consent-toggle").addEventListener("change", toggleConsent);
  $("delete-data").addEventListener("click", deleteMyData);

  loadIdentity();
  startSession();
});
