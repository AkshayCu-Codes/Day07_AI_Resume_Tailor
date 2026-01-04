import React, { useState } from "react";

export default function Download({ ctx }) {
  const [status, setStatus] = useState({ state: "idle", msg: "" });
  const [downloadUrl, setDownloadUrl] = useState("");

  async function generate() {
    setStatus({ state: "loading", msg: "Generating tailored resume…" });

    const form = new FormData();
    form.append("job_id", ctx.jobId);

    try {
      const res = await fetch(`${ctx.API_BASE}/tailor`, { method: "POST", body: form });
      const data = await res.json();

      if (!res.ok) {
        setStatus({ state: "error", msg: data.detail || "Tailoring failed." });
        return;
      }

      setDownloadUrl(`${ctx.API_BASE}${data.download_url}`);
      ctx.setTailorResult(data);
      setStatus({ state: "success", msg: "Tailored resume ready." });
    } catch (e) {
      setStatus({ state: "error", msg: "Backend is unavailable. Start FastAPI first." });
    }
  }

  return (
    <div className="card">
      <h3>Download</h3>
      <p className="muted">
        The system edits your DOCX in place and returns a tailored DOCX download.
      </p>

      <div style={{ display: "flex", gap: 10, marginTop: 12 }}>
        <button className="btn-primary" onClick={generate}>Generate</button>
        <button className="btn-ghost" onClick={() => ctx.setStep("review")}>Back</button>
      </div>

      {status.state === "loading" && <div className="warn" style={{ marginTop: 14 }}>{status.msg}</div>}
      {status.state === "success" && <div className="success" style={{ marginTop: 14 }}>{status.msg}</div>}
      {status.state === "error" && <div className="error" style={{ marginTop: 14 }}>{status.msg}</div>}

      {downloadUrl && (
        <div style={{ marginTop: 14 }}>
          <a href={downloadUrl} target="_blank" rel="noreferrer">
            Download tailored resume (.docx)
          </a>
        </div>
      )}
    </div>
  );
}
