#!/usr/bin/env python3
"""Аудит snippets.json: для каждой with-фразы показать точный исходный спан
в .md, его смещения и зону (голова/середина, треть документа)."""
from __future__ import annotations
import json
import re
from pathlib import Path

TMP = Path(__file__).resolve().parent.parent / "tmp-full"
HEAD = MID = 2000


def norm(s: str) -> str:
    s = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", s)
    s = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", s)
    s = re.sub(r"[^0-9A-Za-zА-Яа-яЁё]+", " ", s)
    return re.sub(r"\s+", " ", s).strip().lower()


def fm_end(text: str) -> int:
    if text.startswith("---\n"):
        i = text.find("\n---", 3)
        if i != -1:
            return i + 4
    return 0


def locate(text: str, phrase: str):
    """Найти исходный спан фразы: идём по нормализованным словам."""
    ph = norm(phrase).split()
    if not ph:
        return None
    toks = [(m.group(), m.start(), m.end()) for m in re.finditer(r"\S+", text)]
    n = len(toks)
    # словарь нормализованных токенов-слов (без пунктуации)
    def w(tok):
        x = re.sub(r"[^0-9A-Za-zА-Яа-яЁё]+", "", tok)
        return x.lower() or None
    ws = [w(t[0]) for t in toks]
    # фразовые слова могут быть разбиты на несколько исходных токенов
    flat = []   # (word, tok_idx)
    for i, token in enumerate(toks):
        parts = [p for p in re.split(r"[^0-9A-Za-zА-Яа-яЁё]+", token[0]) if p]
        for p in parts:
            flat.append((p.lower(), i))
    hits = []
    for start in range(len(flat) - len(ph) + 1):
        if [flat[start + k][0] for k in range(len(ph))] == ph:
            i0 = flat[start][1]
            i1 = flat[start + len(ph) - 1][1]
            hits.append((toks[i0][1], toks[i1][2],
                         text[toks[i0][1]:toks[i1][2]]))
    if not hits:
        return None
    fme_val = fm_end(text)
    body = [h for h in hits if h[0] >= fme_val]
    return (body or hits)[0]


data = json.loads(Path(__file__).resolve().parent.parent / "snippets.json".read_text())
problems = []
for key, entry in sorted(data.items()):
    t = (TMP / f"{key}.md").read_text()
    L = len(t)
    ms = (L - MID) // 2 if L > HEAD + MID else 0
    fme = 4 if not t.startswith("---\n") else (t.find("\n---", 3) + 4)
    print(f"== {key} len={L} mid_start={ms} fm_end={fme}")
    used_spans = []
    for i, p in enumerate(entry["with"]):
        hit = locate(t, p)
        if hit is None:
            print(f"   [{i}] НЕ НАЙДЕНО: {p!r}")
            problems.append(key)
            continue
        a, b, src = hit
        zones = []
        zones.append("head" if a < HEAD else "MID")
        third = "T1" if b <= L // 3 else ("T2" if a < 2 * L // 3 else "T3!")
        overlap = any(not (b <= x or a >= y) for x, y in used_spans)
        used_spans.append((a, b))
        in_fm = a < fme
        mark = f"{'FRONTMATTER!' if in_fm else ''}{' OVERLAP!' if overlap else ''}"
        print(f"   [{i}] {a:>5}-{b:<5} {zones[0]}/{third}{mark}")
        print(f"         src: {src[:160]!r}")


print("\nпроблемные:", problems or "нет")
