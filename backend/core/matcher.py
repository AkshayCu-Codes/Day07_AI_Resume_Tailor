from typing import Dict, List

def compute_gap_summary(sectioned_blocks: List[Dict], jd_info: Dict) -> Dict:
    resume_text = " ".join(b["text"].lower() for b in sectioned_blocks)
    jd_keywords = jd_info.get("keywords", [])

    covered = []
    missing = []

    # conservative: treat keyword present if substring exists
    for kw in jd_keywords[:50]:
        if kw in resume_text:
            covered.append(kw)
        else:
            missing.append(kw)

    return {
        "covered_top": covered[:20],
        "missing_top": missing[:20],
        "missing_count_top50": len(missing),
    }
