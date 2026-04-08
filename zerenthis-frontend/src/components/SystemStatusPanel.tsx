"use client";

import { useEffect, useState } from "react";
import { getAutomationStatus, getHealth } from "@/lib/api";

type Props = {
  refreshKey?: number;
};

export default function SystemStatusPanel({ refreshKey = 0 }: Props) {
  const [health, setHealth] = useState<any>(null);
  const [automation, setAutomation] = useState<any>(null);

  const load = async () => {
    const [h, a] = await Promise.all([
      getHealth(),
      getAutomationStatus(),
    ]);
    setHealth(h);
    setAutomation(a);
  };

  useEffect(() => {
    load();
  }, [refreshKey]);

  const healthy = health?.status === "ok";

  return (
    <div style={{
      background: "#111827",
      padding: "16px",
      borderRadius: "14px",
      border: "1px solid #1f2937"
    }}>
      <h2 style={{ marginTop: 0 }}>System Status</h2>

      <div style={{ display: "grid", gap: "10px" }}>
        <div style={{
          background: "#0b1220",
          borderRadius: "10px",
          padding: "10px 12px",
          border: "1px solid #1f2937"
        }}>
          <div style={{ fontSize: "12px", color: "#9ca3af" }}>Backend Health</div>
          <div style={{ color: healthy ? "#10b981" : "#ef4444", fontWeight: 700, marginTop: "4px" }}>
            {health?.status || "unknown"}
          </div>
        </div>

        <div style={{
          background: "#0b1220",
          borderRadius: "10px",
          padding: "10px 12px",
          border: "1px solid #1f2937"
        }}>
          <div style={{ fontSize: "12px", color: "#9ca3af" }}>Automation Status</div>
          <div style={{ color: "#e5e7eb", marginTop: "4px" }}>
            {automation?.status || automation?.state || automation?.message || "No status yet"}
          </div>
        </div>
      </div>
    </div>
  );
}
