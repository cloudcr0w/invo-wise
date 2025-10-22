import re
from typing import Dict

# Very naive regex helpers for Week 1 demo
NIP_RE = re.compile(r"\b\d{10}\b")
DATE_RE = re.compile(r"\b(\d{4}-\d{2}-\d{2}|\d{2}[./-]\d{2}[./-]\d{4})\b")


def parse_text_to_fields(text: str) -> Dict[str, str]:
    nip = NIP_RE.search(text)
    date = DATE_RE.search(text)
    return {
        "nip": nip.group(0) if nip else "",
        "some_date": date.group(0) if date else "",
    }
