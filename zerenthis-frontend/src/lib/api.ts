const BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";

async function safeJson(path: string, options?: RequestInit) {
  try {
    const res = await fetch(`${BASE_URL}${path}`, {
      cache: "no-store",
      ...options,
    });

    const text = await res.text();
    try {
      return JSON.parse(text);
    } catch {
      return { raw: text, ok: res.ok, status: res.status };
    }
  } catch (error: any) {
    return {
      error: true,
      message: error?.message || "Request failed",
      path,
    };
  }
}

export async function getHealth() {
  return safeJson("/health");
}

export async function runAutopilot() {
  return safeJson("/api/automation/run-once", {
    method: "POST",
  });
}

export async function getLeaderboard() {
  return safeJson("/api/performance/leaderboard");
}

export async function getAutomationStatus() {
  return safeJson("/api/automation/status");
}

export async function getTargets() {
  const primary = await safeJson("/api/intelligence/run", {
    method: "POST",
  });

  if (!primary?.error) return primary;

  return safeJson("/api/targets");
}

export async function runAutonomyLoop(iterations = 3, delay = 1) {
  return safeJson("/api/autonomy/run", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ iterations, delay }),
  });
}
