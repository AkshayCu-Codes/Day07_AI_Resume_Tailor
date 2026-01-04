import React, { useState, useMemo } from "react";
import Upload from "./pages/Upload.jsx";
import Analyze from "./pages/Analyze.jsx";
import Review from "./pages/Review.jsx";
import Download from "./pages/Download.jsx";

const API_BASE = "http://127.0.0.1:8000";

export default function App() {
  const [step, setStep] = useState("upload");
  const [resumeFile, setResumeFile] = useState(null);
  const [jobDescription, setJobDescription] = useState("");
  const [style, setStyle] = useState("Professional");
  const [strictness, setStrictness] = useState("Strict");

  const [jobId, setJobId] = useState(null);
  const [analysis, setAnalysis] = useState(null);
  const [changesPreview, setChangesPreview] = useState([]);
  const [changesTotal, setChangesTotal] = useState(0);
  const [verificationQuestions, setVerificationQuestions] = useState([]);
  const [tailorResult, setTailorResult] = useState(null);

  const ctx = useMemo(() => ({
    API_BASE,
    step, setStep,
    resumeFile, setResumeFile,
    jobDescription, setJobDescription,
    style, setStyle,
    strictness, setStrictness,
    jobId, setJobId,
    analysis, setAnalysis,
    changesPreview, setChangesPreview,
    changesTotal, setChangesTotal,
    verificationQuestions, setVerificationQuestions,
    tailorResult, setTailorResult
  }), [
    step, resumeFile, jobDescription, style, strictness,
    jobId, analysis, changesPreview, changesTotal, verificationQuestions, tailorResult
  ]);

  return (
    <div style={{ padding: "24px", maxWidth: "1100px", margin: "0 auto" }}>
      <h1>AI Resume Tailor</h1>
      <p style={{ color: "#555" }}>
        DOCX-only, format-preserving resume tailoring with humanized rewriting.
      </p>

      {step === "upload" && <Upload ctx={ctx} />}
      {step === "analyze" && <Analyze ctx={ctx} />}
      {step === "review" && <Review ctx={ctx} />}
      {step === "download" && <Download ctx={ctx} />}
    </div>
  );
}
