from typing import List, Dict
from docx import Document

def apply_changes_to_docx(
    input_docx_path: str,
    output_docx_path: str,
    proposed_changes: List[Dict],
    user_notes: str = "",
) -> None:
    """
    Applies changes at paragraph-level by replacing the paragraph text.
    Formatting caveat: paragraph-level replacement may reset run-level styling.
    Phase 2 improvement: run-aware replacement. (We’ll do this later.)
    """
    doc = Document(input_docx_path)

    # index proposals by paragraph index
    by_idx = {c["para_index"]: c for c in proposed_changes}

    for i, p in enumerate(doc.paragraphs):
        if i not in by_idx:
            continue
        change = by_idx[i]
        # Replace paragraph text
        p.text = change["after"]

    doc.save(output_docx_path)
