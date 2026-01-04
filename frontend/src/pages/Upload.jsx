import React, { useState } from "react";
import FileUpload from "../components/FileUpload.jsx";
import StyleSelector from "../components/StyleSelector.jsx";

export default function Upload({ ctx }) {
  const [error, setError] = useState("");

  function next() {
    setError("");
    if (!ctx.resumeFile) return setError("Please upload your resume in .docx format.");
    if (!ctx.resumeFile.name.toLowerCase().endsWith(".docx")) {
      return setError("Only .docx resumes are supported to preserve formatting. Please convert your PDF to Word (.docx).");
    }
    if (!ctx.jobDescription.trim()) return setError("Please paste the job description.");
    ctx.setStep("analyze");
  }

  return (
    <div className="card">
      <div className="row">
        <div className="col">
          <h3>Upload Resume (DOCX only)</h3>
          <p className="muted">
            To keep fonts, spacing, bullets, and layout intact, this system accepts Word (.docx) resumes only.
          </p>
          <FileUpload
            onFile={(f) => ctx.setResumeFile(f)}
            accept=".docx"
          />
          {ctx.resumeFile && (
            <p className="muted">Selected: <b>{ctx.resumeFile.name}</b></p>
          )}
        </div>

        <div className="col">
          <h3>Job Description</h3>
          <textarea
            value={ctx.jobDescription}
            placeholder="Paste the job description here..."
            onChange={(e) => ctx.setJobDescription(e.target.value)}
          />
          <div style={{ marginTop: 12 }}>
            <StyleSelector
              style={ctx.style}
              setStyle={ctx.setStyle}
              strictness={ctx.strictness}
              setStrictness={ctx.setStrictness}
            />
          </div>
        </div>
      </div>

      {error && <div className="error" style={{ marginTop: 14 }}>{error}</div>}

      <div style={{ marginTop: 16, display: "flex", gap: 10 }}>
        <button className="btn-primary" onClick={next}>Analyze Resume</button>
      </div>
    </div>
  );
}
