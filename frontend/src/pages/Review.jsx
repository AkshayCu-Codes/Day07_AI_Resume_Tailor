import React, { useState } from "react";
import ChangePreview from "../components/ChangePreview.jsx";

export default function Review({ ctx }) {
  const [error, setError] = useState("");

  const a = ctx.analysis || {};
  const gap = (a.gap_summary || {});
  const missing = gap.missing_top || [];

  function next() {
    setError("");
    // Strict mode blocks if verification questions exist (backend enforces too)
    if (ctx.strictness === "Strict" && (ctx.verificationQuestions || []).length > 0) {
      setError("Verification required in Strict mode. Switch to Assisted mode or implement verification capture in Phase 2.");
      return;
    }
    ctx.setStep("download");
  }

  return (
    <div className="card">
      <h3>Review</h3>
      <p className="muted">
        Proposed edits are conservative and designed to keep the resume human-written.
      </p>

      <div className="row" style={{ marginTop: 12 }}>
        <div className="col">
          <h4>Detected Sections</h4>
          <div className="muted">{(a.sections_detected || []).join(", ") || "—"}</div>

          <h4 style={{ marginTop: 16 }}>Top JD Keywords</h4>
          <div className="muted">{(a.jd_keywords_top || []).slice(0, 12).join(", ") || "—"}</div>

          <h4 style={{ marginTop: 16 }}>Gap Snapshot</h4>
          <div className="muted">
            Missing (top): {missing.length ? missing.join(", ") : "None detected"}
          </div>

          {(ctx.verificationQuestions || []).length > 0 && (
            <div className="warn" style={{ marginTop: 14 }}>
              <b>Verification Needed:</b> Your JD includes keywords not found in the resume text.
              In Strict mode, the backend will block tailoring until the user provides factual evidence.
            </div>
          )}
        </div>

        <div className="col">
          <h4>Proposed Changes (Preview)</h4>
          <div className="muted" style={{ marginBottom: 10 }}>
            Showing {ctx.changesPreview.length} of {ctx.changesTotal} proposed edits.
          </div>
          <ChangePreview changes={ctx.changesPreview} />
        </div>
      </div>

      {error && <div className="error" style={{ marginTop: 14 }}>{error}</div>}

      <div style={{ marginTop: 16, display: "flex", gap: 10 }}>
        <button className="btn-secondary" onClick={() => ctx.setStep("upload")}>Start Over</button>
        <button className="btn-primary" onClick={next}>Generate Tailored Resume</button>
      </div>
    </div>
  );
}
