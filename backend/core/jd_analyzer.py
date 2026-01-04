import re
from typing import Dict, List

STOPWORDS = set("""
a an the and or to of in for with on at by from as is are be this that you we they i
""".split())

def analyze_job_description(jd: str) -> Dict:
    text = jd.strip()
    tokens = re.findall(r"[A-Za-z][A-Za-z\+\#\.\-]{1,}", text)
    tokens = [t.lower() for t in tokens if t.lower() not in STOPWORDS and len(t) >= 3]

    # naive keyword frequency (Phase 1)
    freq = {}
    for t in tokens:
        freq[t] = freq.get(t, 0) + 1

    keywords = sorted(freq.keys(), key=lambda k: (-freq[k], k))
    return {
        "raw": text,
        "keywords": keywords,
        "keyword_freq": freq,
    }
