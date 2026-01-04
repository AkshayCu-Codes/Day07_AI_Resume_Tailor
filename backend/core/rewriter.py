from typing import Dict, List
from core.rewrite_rules import STYLE_PROFILES, sanitize_text, clamp_length

TARGET_SECTIONS = {"SUMMARY", "SKILLS", "EXPERIENCE", "PROJECTS"}

def propose_changes(sectioned_blocks: List[Dict], jd_info: Dict, style: str = "Professional") -> List[Dict]:
    """
    Phase 1: Conservative "keyword alignment" proposals.
    We do NOT invent new claims. We only:
      - tighten language
      - optionally inject existing JD keywords IF already present elsewhere in resume text
    """
    profile = STYLE_PROFILES.get(style, STYLE_PROFILES["Professional"])
    max_len = profile["max_len"]

    resume_text = " ".join(b["text"].lower() for b in sectioned_blocks)
    jd_keywords = jd_info.get("keywords", [])[:25]

    proposals: List[Dict] = []

    for b in sectioned_blocks:
        if b["section"] not in TARGET_SECTIONS:
            continue

        original = b["text"]
        updated = original

        # Minimal: if a JD keyword exists somewhere in resume and not in this line, we MAY add it lightly (only for PROJECTS/SKILLS)
        if b["section"] in {"SKILLS", "PROJECTS"}:
            for kw in jd_keywords[:8]:
                if kw in resume_text and kw not in updated.lower():
                    # gentle append; does not create new claim, because keyword exists in resume elsewhere
                    updated = f"{updated} ({kw})"
                    break

        updated = sanitize_text(updated)
        updated = clamp_length(updated, max_len)

        if updated != original:
            proposals.append({
                "para_index": b["para_index"],
                "section": b["section"],
                "before": original,
                "after": updated,
                "reason": f"Style={style}; conservative keyword alignment",
                "risk": "low"
            })

    return proposals
