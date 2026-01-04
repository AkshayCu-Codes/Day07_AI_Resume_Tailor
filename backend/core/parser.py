from dataclasses import dataclass
from typing import List
from docx import Document

@dataclass
class ResumeBlock:
    para_index: int
    text: str

def extract_blocks(doc_path: str) -> List[ResumeBlock]:
    doc = Document(doc_path)
    blocks: List[ResumeBlock] = []
    for i, p in enumerate(doc.paragraphs):
        t = (p.text or "").strip()
        if t:
            blocks.append(ResumeBlock(para_index=i, text=t))
    return blocks
