from typing import List, Dict, Optional
from core.parser import ResumeBlock

SECTION_HEADERS = {
    "SUMMARY": ["summary", "professional summary", "profile"],
    "SKILLS": ["skills", "technical skills", "core competencies"],
    "EXPERIENCE": ["experience", "work experience", "employment"],
    "PROJECTS": ["projects", "academic projects", "personal projects"],
    "EDUCATION": ["education", "academic background"],
}

def normalize(text: str) -> str:
    return " ".join(text.lower().strip().split())

def is_section_header(text: str) -> Optional[str]:
    n = normalize(text)
    for section, variants in SECTION_HEADERS.items():
        if n in [normalize(v) for v in variants]:
            return section
    return None

def assign_sections(blocks: List[ResumeBlock]) -> List[Dict]:
    current = "OTHER"
    out: List[Dict] = []
    for b in blocks:
        header = is_section_header(b.text)
        if header:
            current = header
            continue  # skip header content from being rewritten
        out.append({"para_index": b.para_index, "text": b.text, "section": current})
    return out
