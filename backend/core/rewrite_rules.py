from typing import Dict, List

BANNED_PHRASES = [
    "leveraged cutting-edge",
    "state-of-the-art",
    "robust and scalable",
    "synergized",
    "results-driven professional",
    "dynamic and fast-paced environment",
]

STYLE_PROFILES: Dict[str, Dict] = {
    "Professional": {"max_len": 220, "tone": "neutral"},
    "Concise": {"max_len": 140, "tone": "direct"},
    "Impact-Oriented": {"max_len": 200, "tone": "outcome"},
    "Technical": {"max_len": 220, "tone": "technical"},
    "Executive": {"max_len": 220, "tone": "leadership"},
}

def sanitize_text(text: str) -> str:
    out = text
    for p in BANNED_PHRASES:
        out = out.replace(p, "")
    return " ".join(out.split()).strip()

def clamp_length(text: str, max_len: int) -> str:
    if len(text) <= max_len:
        return text
    return text[: max_len - 1].rstrip() + "…"
