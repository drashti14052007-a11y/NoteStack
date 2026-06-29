const API = "http://127.0.0.1:8000";

let categoryConfig   = null;
let selectedCategory = null;
let radarChart       = null;

// ── Screen navigation ────────────────────────────────────────
function showScreen(id) {
  document.querySelectorAll(".screen").forEach(s => s.classList.remove("active"));
  document.getElementById(id).classList.add("active");
  window.scrollTo({ top: 0, behavior: "smooth" });
}

// ── Init: fetch category config ──────────────────────────────
async function init() {
  try {
    const res = await fetch(`${API}/categories`);
    categoryConfig = await res.json();
  } catch(e) {
    alert("Cannot reach NoteStack backend. Make sure it is running on port 8000.");
  }
}

// ── Welcome → Category ───────────────────────────────────────
document.getElementById("btn-start").addEventListener("click", () => {
  if (!categoryConfig) {
    alert("Still connecting to backend. Please try again in a moment.");
    return;
  }
  showScreen("screen-category");
});

document.getElementById("btn-back-welcome").addEventListener("click", () => {
  showScreen("screen-welcome");
});

// ── Category → Sliders ───────────────────────────────────────
document.querySelectorAll(".cat-card").forEach(card => {
  card.addEventListener("click", () => {
    document.querySelectorAll(".cat-card").forEach(c => c.classList.remove("active"));
    card.classList.add("active");
    selectedCategory = card.dataset.cat;
    buildSliders(selectedCategory);
    document.getElementById("slider-cat-label").textContent = capitalize(selectedCategory);
    showScreen("screen-sliders");
  });
});

document.getElementById("btn-back-category").addEventListener("click", () => {
  showScreen("screen-category");
});

function buildSliders(cat) {
  const targets   = categoryConfig[cat].targets;
  const container = document.getElementById("sliders-grid");
  container.innerHTML = "";

  targets.forEach((t, i) => {
    const label = t.replace(/_/g, " ");
    const row   = document.createElement("div");
    row.className = "slider-row";
    row.innerHTML = `
      <div class="slider-top">
        <span class="slider-label">${label}</span>
        <span class="slider-val" id="val-${i}">5</span>
      </div>
      <input type="range" min="1" max="10" step="0.5" value="5" id="slider-${i}"
             oninput="document.getElementById('val-${i}').textContent = this.value"/>
    `;
    container.appendChild(row);
  });
}

// ── Sliders → Results ────────────────────────────────────────
document.getElementById("btn-formulate").addEventListener("click", async () => {
  if (!selectedCategory) return;

  const targets = categoryConfig[selectedCategory].targets;
  const scores  = targets.map((_, i) =>
    parseFloat(document.getElementById(`slider-${i}`).value)
  );

  document.getElementById("loading").classList.remove("hidden");

  try {
    const res  = await fetch(`${API}/formulate`, {
      method:  "POST",
      headers: { "Content-Type": "application/json" },
      body:    JSON.stringify({ category: selectedCategory, target_scores: scores }),
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || "Request failed");
    displayResults(data, scores);
    showScreen("screen-results");
  } catch(err) {
    const toast = document.getElementById("error-toast");
    document.getElementById("error-msg").textContent = "Could not reach NoteStack API. Is the backend running?";
    toast.classList.remove("hidden");
    setTimeout(() => toast.classList.add("hidden"), 4000);
  } finally {
    document.getElementById("loading").classList.add("hidden");
  }
});

document.getElementById("btn-back-sliders").addEventListener("click", () => {
  showScreen("screen-sliders");
});

// ── Display results ──────────────────────────────────────────
function displayResults(data, scores) {
  document.getElementById("result-cat-label").textContent = capitalize(data.category);

  // Formulation table
  const tbody = document.getElementById("formulation-body");
  tbody.innerHTML = "";
  Object.entries(data.formulation).forEach(([k, v]) => {
    const tr = document.createElement("tr");
    const label = k.replace(/_pct$/, " %").replace(/_/g, " ")
      .replace(/\b\w/g, c => c.toUpperCase());
    tr.innerHTML = `<td>${label}</td><td>${v}%</td>`;
    tbody.appendChild(tr);
  });

  // Confidence card
  const conf      = data.confidence_pct;
  const confColor = conf >= 85 ? "var(--success)" : conf >= 65 ? "#b07d10" : "var(--danger)";
  const confMsg   = conf >= 85
    ? "High confidence — this target is achievable with the suggested formulation."
    : conf >= 65
    ? "Moderate confidence — closest achievable formulation given the targets."
    : "Low confidence — some targets may be outside the achievable range.";

  document.getElementById("confidence-card").innerHTML = `
    <span style="font-size:13px;font-weight:600;color:${confColor}">Confidence: ${conf}%</span>
    &nbsp;<span style="font-size:11px;color:var(--ink-muted)">· Residual error: ${data.residual_error}</span>
    <p style="margin-top:6px;font-size:11px;color:var(--ink-muted);line-height:1.5">${confMsg}</p>
  `;

  // Compliance
  const c = data.compliance;
  const statusClass = c.status === "COMPLIANT"  ? "status-compliant"
                    : c.status === "ADVISORY"    ? "status-advisory"
                    :                              "status-noncompliant";
  let compHTML = `<span class="compliance-status ${statusClass}">${c.status}</span>`;
  c.passed.forEach(p   => compHTML += complianceItem("pass", p));
  c.warnings.forEach(w => compHTML += complianceItem("warn", w));
  c.flags.forEach(f    => compHTML += complianceItem("fail", f));
  document.getElementById("compliance-box").innerHTML = compHTML;

  // Score breakdown cards
  const scoreGrid  = document.getElementById("score-cards-grid");
  scoreGrid.innerHTML = "";
  const predScores = data.predicted_scores;
  const targScores = data.target_scores;
  const scoreKeys  = Object.keys(predScores);
  scoreKeys.forEach((key, idx) => {
    const pred   = predScores[key];
    const targ   = targScores[key];
    const pct    = Math.round((pred / 10) * 100);
    const isLast = idx === scoreKeys.length - 1;
    const isOdd  = scoreKeys.length % 2 !== 0;
    const card   = document.createElement("div");
    card.className = "score-card" + (isLast && isOdd ? " full-width" : "");
    card.innerHTML = `
      <div class="score-card-label">${key.replace(/_/g, " ")}</div>
      <div class="score-card-vals">
        <span class="score-predicted">${pred}</span>
        <span class="score-target">target ${targ}</span>
      </div>
      <div class="score-bar-track">
        <div class="score-bar-fill" style="width:${pct}%"></div>
      </div>
    `;
    scoreGrid.appendChild(card);
  });

  // Radar chart
  const labels   = Object.keys(predScores).map(k => k.replace(/_/g, " "));
  const predVals = Object.values(predScores);
  const targVals = Object.values(targScores);

  if (radarChart) radarChart.destroy();
  const ctx = document.getElementById("radar-chart").getContext("2d");
  radarChart = new Chart(ctx, {
    type: "radar",
    data: {
      labels,
      datasets: [
        {
          label:               "Target",
          data:                targVals,
          borderColor:         "rgba(139,69,19,0.7)",
          backgroundColor:     "rgba(139,69,19,0.08)",
          pointBackgroundColor:"rgba(139,69,19,0.9)",
          pointRadius:         4,
        },
        {
          label:               "Predicted",
          data:                predVals,
          borderColor:         "rgba(201,168,108,0.85)",
          backgroundColor:     "rgba(201,168,108,0.1)",
          pointBackgroundColor:"rgba(201,168,108,1)",
          pointRadius:         4,
        },
      ],
    },
    options: {
      scales: {
        r: {
          min: 0, max: 10,
          ticks: {
            color: "#9b8b72",
            backdropColor: "transparent",
            stepSize: 2,
            font: { size: 10 }
          },
          grid:        { color: "rgba(221,213,191,0.7)" },
          angleLines:  { color: "rgba(221,213,191,0.5)" },
          pointLabels: { color: "#3d3326", font: { size: 11, family: "'Inter', sans-serif" } },
        },
      },
      plugins: {
        legend: {
          labels: {
            color: "#6b5c48",
            font: { size: 11, family: "'Inter', sans-serif" },
            boxWidth: 12,
          }
        },
      },
    },
  });

  // PDF download button
  document.getElementById("btn-download-pdf").onclick = async () => {
    const btn = document.getElementById("btn-download-pdf");
    btn.textContent = "Generating PDF…";
    btn.disabled = true;
    try {
      const res = await fetch(`${API}/report`, {
        method:  "POST",
        headers: { "Content-Type": "application/json" },
        body:    JSON.stringify({ category: data.category, target_scores: scores }),
      });
      if (!res.ok) throw new Error("Failed to generate report");
      const blob = await res.blob();
      const url  = URL.createObjectURL(blob);
      const filename = `notestack_${data.category}_report.pdf`;

      const a    = document.createElement("a");
      a.href     = url;
      a.download = filename;
      a.click();

      showDownloadToast(filename, url);
    } catch(e) {
      alert("Could not generate PDF. Is the backend running?");
    } finally {
      btn.textContent = "Download PDF report";
      btn.disabled = false;
    }
  };
}

function complianceItem(type, text) {
  const dotClass = type === "pass" ? "dot-pass" : type === "warn" ? "dot-warn" : "dot-fail";
  return `<div class="compliance-item">
    <span class="dot ${dotClass}"></span>
    <span>${text}</span>
  </div>`;
}

// ── Download success toast ──────────────────────────────────
let downloadToastTimer = null;

function showDownloadToast(filename, blobUrl) {
  const toast   = document.getElementById("download-toast");
  const sub     = document.getElementById("download-toast-sub");
  const openBtn = document.getElementById("download-toast-open");
  const closeBtn= document.getElementById("download-toast-close");

  sub.textContent = filename;
  toast.classList.remove("hidden");

  // restart animation cleanly
  toast.classList.remove("show");
  void toast.offsetWidth; // force reflow so the transition replays
  requestAnimationFrame(() => toast.classList.add("show"));

  openBtn.onclick = () => window.open(blobUrl, "_blank");
  closeBtn.onclick = () => hideDownloadToast();

  if (downloadToastTimer) clearTimeout(downloadToastTimer);
  downloadToastTimer = setTimeout(hideDownloadToast, 6000);
}

function hideDownloadToast() {
  const toast = document.getElementById("download-toast");
  toast.classList.remove("show");
  setTimeout(() => toast.classList.add("hidden"), 300);
}

// ── Reset ────────────────────────────────────────────────────
document.getElementById("btn-reset").addEventListener("click", () => {
  document.querySelectorAll(".cat-card").forEach(c => c.classList.remove("active"));
  selectedCategory = null;
  showScreen("screen-welcome");
});

// ── Helpers ──────────────────────────────────────────────────
function capitalize(str) {
  return str.charAt(0).toUpperCase() + str.slice(1);
}

// ── Start ────────────────────────────────────────────────────
init();