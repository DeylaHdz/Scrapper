import re

def clean_text(s: str) -> str:
    s = re.sub(r"\r\n|\r", "\n", s)
    s = re.sub(r"[ \t]+", " ", s)
    s = re.sub(r"\n{3,}", "\n\n", s)
    return s.strip()

def guess_headings(text: str, min_len=3, max_len=120):
    headings = []
    for line in text.splitlines():
        ln = line.strip()
        if not (min_len <= len(ln) <= max_len):
            continue
        if (ln.isupper() and any(c.isalpha() for c in ln)) \
           or re.match(r"^(Cap[ií]tulo|Secci[oó]n|T[ií]tulo|Resumen|Abstract|Introducci[oó]n)\b", ln, re.I) \
           or re.match(r"^(\d+(\.\d+)*\s+).{2,}$", ln):
            headings.append(ln)
    return list(dict.fromkeys(headings))[:100]

def limit_text(text: str, limit: int | None):
    if limit is None or limit <= 0:
        return text
    return text if len(text) <= limit else text[:limit] + "\n\n[... truncado ...]"