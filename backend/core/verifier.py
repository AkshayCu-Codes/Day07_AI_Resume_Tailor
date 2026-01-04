from typing import Dict, List

def build_verification_questions(gap_summary: Dict, strictness: str = "Strict") -> List[Dict]:
    """
    Phase 1:
    - Strict mode: if JD top keywords missing, we ask user to confirm experience (yes/no + notes).
    - Assisted mode: we allow tailoring without blocking (questions still shown as optional).
    """
    missing = gap_summary.get("missing_top", [])[:10]
    if not missing:
        return []

    questions = []
    for kw in missing:
        questions.append({
            "keyword": kw,
            "question": f"Do you have experience with '{kw}' that can be truthfully added or rephrased from existing work? If yes, provide 1–2 lines of factual evidence.",
            "required": True if strictness.lower() == "strict" else False
        })

    return questions
