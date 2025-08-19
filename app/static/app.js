// === Config: set your backend URL here ===

const API_BASE_URL = window.location.origin || "http://127.0.0.1:8000";
const LOCUST_URL = API_BASE_URL.replace(/:\d+$/, ":8089");  // swap port

// --- Helpers ---
const $ = (id) => document.getElementById(id);
const toNum = (v) => (v === "" ? NaN : Number(v));

function setLoading(isLoading) {
  $("submit-btn").disabled = isLoading;
  $("loading").classList.toggle("hidden", !isLoading);
}

function showHealth(ok, msg) {
  const el = $("health");
  el.textContent = ok ? "Healthy" : `Unhealthy: ${msg || "?"}`;
  el.style.color = ok ? "var(--success)" : "var(--danger)";
}

// --- Form submit -> /predict ---
async function onSubmit(e) {
  e.preventDefault();
  $("form-error").classList.add("hidden");
  $("result").classList.add("empty");
  setLoading(true);

  // Grab values
  const payload = {
    Pregnancies: toNum($("Pregnancies").value),
    Glucose: toNum($("Glucose").value),
    BloodPressure: toNum($("BloodPressure").value),
    SkinThickness: toNum($("SkinThickness").value),
    Insulin: toNum($("Insulin").value),
    BMI: toNum($("BMI").value),
    DiabetesPedigreeFunction: toNum($("DiabetesPedigreeFunction").value),
    Age: toNum($("Age").value),
  };

  // Basic validation
  const hasNaN = Object.values(payload).some((v) => Number.isNaN(v));
  if (hasNaN) {
    $("form-error").textContent = "Please fill all fields with valid numbers.";
    $("form-error").classList.remove("hidden");
    setLoading(false);
    return;
  }

  try {
    const res = await fetch(`${API_BASE_URL}/predict`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    if (!res.ok) {
      const txt = await res.text();
      throw new Error(`HTTP ${res.status}: ${txt}`);
    }

    const data = await res.json();
    renderResult(data, payload);
  } catch (err) {
    $("form-error").textContent = `Prediction failed: ${err.message}`;
    $("form-error").classList.remove("hidden");
  } finally {
    setLoading(false);
  }
}

// --- Render prediction result ---
function renderResult(data, payload) {
  const { prediction, result, confidence } = data;
  const el = $("result");
  el.classList.remove("empty");

  const confPct = (confidence * 100).toFixed(1);
  const isPositive = String(result).toLowerCase().includes("diabetic") && prediction === 1;

  el.innerHTML = `
    <p><span class="pill ${isPositive ? "warn" : "ok"}">${result}</span></p>
    <p>Prediction: <strong>${prediction}</strong> · Confidence: <strong>${confPct}%</strong></p>
    <details>
      <summary class="subtle">Show payload</summary>
      <pre>${JSON.stringify(payload, null, 2)}</pre>
    </details>
  `;
}

// --- Health, Info, Metrics ---
async function fetchHealth() {
  try {
    const res = await fetch(`${API_BASE_URL}/health`);
    const ok = res.ok;
    let msg = "";
    try { msg = (await res.json()).message || ""; } catch {}
    showHealth(ok, msg);
  } catch (e) {
    showHealth(false, e.message);
  }
}

async function setApiUrl() {
  document.getElementById("swagger-link").href = `${API_BASE_URL}/docs`;
  document.getElementById("redoc-link").href = `${API_BASE_URL}/redoc`;
  document.getElementById("locust-link").href = LOCUST_URL;
} 


async function fetchInfo() {
  const el = $("info");
  try {
    const res = await fetch(`${API_BASE_URL}/info`);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();

    const features = Array.isArray(data.features) ? data.features : [];
    const metrics = data.metrics || {};

    el.innerHTML = `
      <div class="kv">
        <div>Model Type</div><div>${data.model_type || "?"}</div>
        <div>Dataset</div><div>${data.dataset || "?"}</div>
        <div>Features</div><div>${features.length ? features.join(", ") : "?"}</div>
      </div>
    `;
  } catch (e) {
    el.innerHTML = `<p class="error">Failed to load model info: ${e.message}</p>`;
  }
}

function renderMetricsTable(obj) {
  const keys = Object.keys(obj || {});
  if (!keys.length) return "<p class='subtle'>No metrics available.</p>";

  // metrics.json could be either:
  // { "accuracy": 0.9, ... }  OR  { "RandomForest": {...}, "LogReg": {...} }
  const looksNested = typeof obj[keys[0]] === "object";

  if (!looksNested) {
    const rows = Object.entries(obj)
      .map(([k, v]) => `<tr><th>${k}</th><td>${Number(v).toFixed ? Number(v).toFixed(3) : v}</td></tr>`)
      .join("");
    return `<table class="table"><tbody>${rows}</tbody></table>`;
  }

  // Nested: per-model rows
  const metricsSet = new Set();
  keys.forEach((model) => Object.keys(obj[model]).forEach((m) => metricsSet.add(m)));
  const headers = ["Model", ...metricsSet];

  const rows = keys
    .map((model) => {
      const tds = [...metricsSet]
        .map((m) => {
          const val = obj[model][m];
          return `<td>${typeof val === "number" ? val.toFixed(3) : val ?? "-"}</td>`;
        })
        .join("");
      return `<tr><th>${model}</th>${tds}</tr>`;
    })
    .join("");

  const head = headers.map((h) => `<th>${h}</th>`).join("");
  return `<table class="table"><thead><tr>${head}</tr></thead><tbody>${rows}</tbody></table>`;
}

// --- Init ---
document.addEventListener("DOMContentLoaded", () => {
  $("predict-form").addEventListener("submit", onSubmit);
  fetchHealth();
  fetchInfo();
  setApiUrl();
});
