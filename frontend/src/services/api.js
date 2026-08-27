/**
 * Backend ile iletişim katmanı.
 * Bkz. backend/app/security/auth.py — x-role / x-participant-id header modeli.
 */
const BASE_URL = `${import.meta.env.VITE_API_BASE_URL ?? ""}/api`;

async function request(path, { method = "GET", role, participantId, body } = {}) {
  const headers = { "Content-Type": "application/json" };
  if (role) headers["x-role"] = role;
  if (participantId) headers["x-participant-id"] = participantId;

  const res = await fetch(`${BASE_URL}${path}`, {
    method,
    headers,
    body: body !== undefined ? JSON.stringify(body) : undefined,
  });

  if (!res.ok) {
    let detail = res.statusText;
    try {
      const errBody = await res.json();
      detail = errBody.detail ?? detail;
    } catch {
      // ignore
    }
    throw new Error(detail);
  }
  return res.json();
}

export function createSession(auth, session) {
  return request("/session", { method: "POST", ...auth, body: session });
}

export function submitDailyBehavior(auth, behavior) {
  return request("/daily-behavior", { method: "POST", ...auth, body: behavior });
}

export function submitReactionTrials(auth, trials) {
  return request("/reaction-trials", { method: "POST", ...auth, body: trials });
}

export function submitAttentionTrials(auth, trials) {
  return request("/attention-trials", { method: "POST", ...auth, body: trials });
}

export function submitTaskSwitchTrials(auth, trials) {
  return request("/task-switch-trials", { method: "POST", ...auth, body: trials });
}

export function fetchResearchDashboard(auth) {
  return request("/research/dashboard", { ...auth });
}

export function fetchHealth() {
  return request("/health");
}
