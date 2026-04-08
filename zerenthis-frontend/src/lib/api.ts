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
      return { ok: res.ok, status: res.status, raw: text, path };
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
  return safeJson("/api/autopilot/run", {
    method: "POST",
  });
}

export async function getTargets() {
  return safeJson("/api/targets/rank", {
    method: "POST",
  });
}

export async function getPhaseVerify() {
  return safeJson("/api/phase/verify");
}

export async function runPostingPlan() {
  return safeJson("/api/posting/plan", {
    method: "POST",
  });
}

export async function runPostingPrepare() {
  return safeJson("/api/posting/prepare", {
    method: "POST",
  });
}

export async function runPostingExecute() {
  return safeJson("/api/posting/execute", {
    method: "POST",
  });
}

export async function getPostingResult() {
  return safeJson("/api/posting/result", {
    method: "POST",
  });
}

export async function runRealityLoop() {
  return safeJson("/api/reality/loop", {
    method: "POST",
  });
}

export async function runRealityAutoLoop() {
  return safeJson("/api/reality/auto-loop", {
    method: "POST",
  });
}

export async function runRealityExport() {
  return safeJson("/api/reality/export", {
    method: "POST",
  });
}

export async function runScale() {
  return safeJson("/api/scale/run", {
    method: "POST",
  });
}

export async function runTrafficReal() {
  return safeJson("/api/traffic/real", {
    method: "POST",
  });
}

export async function runTrafficBridge() {
  return safeJson("/api/traffic/bridge", {
    method: "POST",
  });
}
