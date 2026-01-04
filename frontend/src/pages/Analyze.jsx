import React, { useState } from "react";

export default function Analyze({ ctx }) {
  const [status, setStatus] = useState({ state: "idle", msg: "" });

  async function runAnalyze() {
    setStatus({ state: "loading", msg: "Analyzing resume and job description…" });

    const form = new FormData();
    form.append("resume", ctx.resumeFile);
    form.append("job_description", ctx.jobDescription);
    form.append("style", ctx.style);
    form.append("strictness", ctx.strictness);

    try {
      const res = await fetch(`${ctx.API_BASE}/analyze`, { method: "POST", body: form });
      const data = await res.json();

      if (!res.ok) {
        setStatus({ state: "error", msg: data.detail || "Analysis failed." });
        return;
      }

      ctx.setJobId(data.job_id);
      ctx.setAnalysis(data.analysis);
      ctx.setChangesPreview(data.proposed_changes || []);
      ctx.setChangesTotal(data.proposed_changes_total || 0);
      ctx.setVerificationQuestions(data.verification_questions || []);

      setStatus({ state: "success", msg: "Analysis complete." });
      ctx.setStep("review");
    } catch (e) {
      setStatus({ state: "error", msg: "Backend is unavailable. Start FastAPI first." });
    }
  }

  return (
    <div className="card">
      <h3>Analyze</h3>
      <p className="muted">
        This step extracts resume sections, analyzes JD keywords, identifies gaps, and proposes conservative edits.
      </p>

      <div style={{ display: "flex", gap: 10, marginTop: 12 }}>
        <button className="btn-primary" onClick={runAnalyze}>Run Analysis</button>
        <button className="btn-ghost" onClick={() => ctx.setStep("upload")}>Back</button>
      </div>

      {status.state === "loading" && <div className="warn" style={{ marginTop: 14 }}>{status.msg}</div>}
      {status.state === "success" && <div className="success" style={{ marginTop: 14 }}>{status.msg}</div>}
      {status.state === "error" && <div className="error" style={{ marginTop: 14 }}>{status.msg}</div>}
    </div>
  );
}
