import os
import uuid
from datetime import datetime
from typing import Dict, Any, Optional

from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

from core.parser import extract_blocks
from core.sectioner import assign_sections
from core.jd_analyzer import analyze_job_description
from core.matcher import compute_gap_summary
from core.rewriter import propose_changes
from core.applier import apply_changes_to_docx
from core.verifier import build_verification_questions

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data", "temp")
OUT_DIR = os.path.join(BASE_DIR, "outputs", "tailored")

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(OUT_DIR, exist_ok=True)

app = FastAPI(title="Day07 AI Resume Tailor")

# Allow frontend dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory job store (OK for Day07 dev; later replace with Redis/DB)
JOBS: Dict[str, Dict[str, Any]] = {}


def _require_docx(filename: str) -> None:
    if not filename.lower().endswith(".docx"):
        raise HTTPException(
            status_code=400,
            detail="Only .docx files are supported to preserve formatting. Please convert your resume to Word (.docx) before uploading."
        )


@app.get("/health")
def health():
    return {"status": "ok", "service": "resume-tailor", "time": datetime.utcnow().isoformat()}


@app.post("/analyze")
async def analyze(
    resume: UploadFile = File(...),
    job_description: str = Form(...),
    style: str = Form("Professional"),
    strictness: str = Form("Strict"),  # Strict | Assisted
):
    _require_docx(resume.filename)

    job_id = str(uuid.uuid4())
    in_path = os.path.join(DATA_DIR, f"{job_id}_{resume.filename}")

    content = await resume.read()
    with open(in_path, "wb") as f:
        f.write(content)

    # Parse resume -> sectioned blocks
    blocks = extract_blocks(in_path)
    sectioned = assign_sections(blocks)

    # Analyze JD -> keywords
    jd_info = analyze_job_description(job_description)

    # Gap summary
    gap = compute_gap_summary(sectioned, jd_info)

    # Propose changes (safe, conservative)
    proposed = propose_changes(sectioned, jd_info, style=style)

    # Verification questions if strictness requires (placeholder logic)
    questions = build_verification_questions(gap, strictness=strictness)

    JOBS[job_id] = {
        "job_id": job_id,
        "resume_filename": resume.filename,
        "resume_path": in_path,
        "style": style,
        "strictness": strictness,
        "job_description": job_description,
        "analysis": {
            "sections_detected": sorted(list({b["section"] for b in sectioned})),
            "jd_keywords_top": jd_info["keywords"][:20],
            "gap_summary": gap,
        },
        "proposed_changes": proposed,
        "verification_questions": questions,
        "output_path": None,
        "created_at": datetime.utcnow().isoformat(),
    }

    return {
        "job_id": job_id,
        "analysis": JOBS[job_id]["analysis"],
        "proposed_changes": proposed[:20],  # preview first 20
        "proposed_changes_total": len(proposed),
        "verification_questions": questions,
    }


@app.get("/job/{job_id}")
def get_job(job_id: str):
    if job_id not in JOBS:
        raise HTTPException(status_code=404, detail="job_id not found")
    j = JOBS[job_id]
    return {
        "job_id": job_id,
        "style": j["style"],
        "strictness": j["strictness"],
        "analysis": j["analysis"],
        "proposed_changes_total": len(j["proposed_changes"]),
        "verification_questions": j["verification_questions"],
        "has_output": bool(j["output_path"]),
    }


@app.post("/tailor")
async def tailor(
    job_id: str = Form(...),
    # If Assisted mode: user can answer missing info (JSON string or simple text)
    user_notes: Optional[str] = Form(None),
):
    if job_id not in JOBS:
        raise HTTPException(status_code=404, detail="job_id not found")

    job = JOBS[job_id]

    # If questions exist and strict mode, we block generation until user addresses them
    if job["strictness"].lower() == "strict" and job["verification_questions"]:
        raise HTTPException(
            status_code=409,
            detail="Verification required before tailoring. Please answer the missing-info questions or switch to Assisted mode."
        )

    resume_in = job["resume_path"]
    out_name = f"{job_id}_tailored.docx"
    out_path = os.path.join(OUT_DIR, out_name)

    # Apply proposed changes into docx (conservative, paragraph-level)
    apply_changes_to_docx(
        input_docx_path=resume_in,
        output_docx_path=out_path,
        proposed_changes=job["proposed_changes"],
        user_notes=user_notes or "",
    )

    job["output_path"] = out_path

    return {
        "job_id": job_id,
        "output_filename": out_name,
        "download_url": f"/download/{job_id}",
    }


@app.get("/download/{job_id}")
def download(job_id: str):
    if job_id not in JOBS:
        raise HTTPException(status_code=404, detail="job_id not found")
    out_path = JOBS[job_id].get("output_path")
    if not out_path or not os.path.exists(out_path):
        raise HTTPException(status_code=404, detail="No tailored resume generated yet.")
    return FileResponse(
        out_path,
        filename=os.path.basename(out_path),
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    )
