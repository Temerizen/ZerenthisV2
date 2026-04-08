"use client";

import { useEffect, useState } from "react";
import RunAutopilot from "@/components/RunAutopilot";
import LoopControlPanel from "@/components/LoopControlPanel";
import LeaderboardPanel from "@/components/LeaderboardPanel";
import SystemStatusPanel from "@/components/SystemStatusPanel";
import TargetsPanel from "@/components/TargetsPanel";

export default function DashboardPage() {
  const [refreshKey, setRefreshKey] = useState(0);
  const [autoRefresh, setAutoRefresh] = useState(true);

  const refreshAll = () => setRefreshKey((x) => x + 1);

  useEffect(() => {
    if (!autoRefresh) return;
    const timer = setInterval(() => {
      setRefreshKey((x) => x + 1);
    }, 15000);
    return () => clearInterval(timer);
  }, [autoRefresh]);

  return (
    <div>
      <div style={{ marginBottom: "20px" }}>
        <h1 style={{ fontSize: "30px", marginBottom: "8px" }}>
          Zerenthis Control Center
        </h1>
        <p style={{ color: "#9ca3af", margin: 0 }}>
          Run ? Log ? Score ? Decide ? Change ? Repeat
        </p>
      </div>

      <div style={{
        display: "flex",
        gap: "12px",
        marginBottom: "18px",
        flexWrap: "wrap"
      }}>
        <button
          onClick={refreshAll}
          style={{
            padding: "10px 14px",
            background: "#1f2937",
            color: "white",
            border: "1px solid #374151",
            borderRadius: "8px",
            cursor: "pointer"
          }}
        >
          Refresh All
        </button>

        <button
          onClick={() => setAutoRefresh((v) => !v)}
          style={{
            padding: "10px 14px",
            background: autoRefresh ? "#065f46" : "#3f3f46",
            color: "white",
            border: "none",
            borderRadius: "8px",
            cursor: "pointer"
          }}
        >
          Auto Refresh: {autoRefresh ? "ON" : "OFF"}
        </button>
      </div>

      <div style={{
        display: "grid",
        gridTemplateColumns: "1.05fr 1.05fr 1.2fr",
        gap: "16px",
        alignItems: "start"
      }}>
        <SystemStatusPanel refreshKey={refreshKey} />
        <RunAutopilot onRan={refreshAll} />
        <TargetsPanel refreshKey={refreshKey} />

        <LoopControlPanel onRan={refreshAll} />
        <LeaderboardPanel refreshKey={refreshKey} />
        <div style={{
          background: "#111827",
          padding: "16px",
          borderRadius: "14px",
          border: "1px solid #1f2937",
          minHeight: "220px"
        }}>
          <h2 style={{ marginTop: 0 }}>Mission Frame</h2>
          <div style={{ display: "grid", gap: "10px" }}>
            <div style={{
              background: "#0b1220",
              border: "1px solid #1f2937",
              borderRadius: "10px",
              padding: "10px 12px"
            }}>
              <div style={{ color: "#9ca3af", fontSize: "12px" }}>Current Phase</div>
              <div style={{ fontWeight: 700, marginTop: "4px" }}>Phase A Continuation</div>
            </div>

            <div style={{
              background: "#0b1220",
              border: "1px solid #1f2937",
              borderRadius: "10px",
              padding: "10px 12px"
            }}>
              <div style={{ color: "#9ca3af", fontSize: "12px" }}>Primary Objective</div>
              <div style={{ marginTop: "4px" }}>Premium control surface for autonomous operation</div>
            </div>

            <div style={{
              background: "#0b1220",
              border: "1px solid #1f2937",
              borderRadius: "10px",
              padding: "10px 12px"
            }}>
              <div style={{ color: "#9ca3af", fontSize: "12px" }}>Next Horizon</div>
              <div style={{ marginTop: "4px" }}>Execution UI + feedback loop visibility</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
