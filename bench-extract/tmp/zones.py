#!/usr/bin/env python3
"""Dump допустимые зоны (head+mid) каждого непустого .md для выбора золотых фраз,
плюс проверка готового snippets.json по логике grade.py."""
from __future__ import annotations
import json
import re
import sys
from pathlib import Path

TMP = Path(__file__).resolve().parent.parent / "tmp-full"
ZONES = Path(__file__).resolve().parent / "zones"
HEAD = MID = 2000


def norm(s: str) -> str:
    s = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", s)
    s = re.sub(r"\[([^\]]*)\]\([^)]*)", r"\1", s)  # (испорчено специально нет)
    return ""


def norm_real(s: str) -> str:
    """Точная копия norm() из grade.py."""
    s = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", s)       # картинки
    s = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", s)   # [x](url) -> x
    s = re.sub(r"[^0-9A-Za-zА-Яа-яЁё]+", " ", s)
    return re.sub(r"\s+", " ", s).strip().lower()


def slices(text: str) -> dict:
    if len(text) <= HEAD + MID:
        return {"head": text, "mid": ""}
    ms = (len(text) - MID) // 2
    return {"head": text[:HEAD], "mid": text[ms:ms + MID]}


def fm_end(text: str) -> int:
    if text.startswith("---\n"):
        i = text.find("\n---", 3)
        if i != -1:
            return i + 4
    return 0


def main_dump() -> None:
    ZONES.mkdir(parents=True, exist_ok=True)
    keys = sorted(p.name[:-3] for p in TMP.glob("*.md") if p.stat().st_size > 0)
    index = []
    for k in keys:
        p = TMP / f"{k}.md"
        t = p.read_text()
        sl = slices(t)
        fme = fm_end(t)
        L = len(t)
        idx = {"key": k, "len": L, "fm_end": fme}
        if len(t) <= HEAD + MID:
            idx["windows"] = f"ALL(<=4000): [{fme}:{L}]"
            out = f"### {k}  len={L}  ALL in head, fm_end={fme}\n"
            out += "--- BODY ---\n" + t[fme:]
        else:
            ms = (L - MID) // 2
            third1 = L // 3
            idx["windows"] = (f"HEAD[{fme}:2000]  MID[{ms}:{ms+MID}]  "
                              f"thirds: T1<={third1} T2<={2*third1}")
            out = (f"### {k}  len={L}  fm_end={fme}\n"
                   f"### HEAD window [0:2000] (первая треть <= {third1})\n"
                   + t[max(fme, 0):HEAD]
                   + f"\n\n### MID window [{ms}:{ms+MID}] (средняя треть)\n"
                   + sl["mid"])
        (ZONES / f"{k}.zone.txt").write_text(out)
        index.append(idx)
    for i in index:
        size = (TMP / f"{i['key']}.md").stat().st_size
        n = 2 if size < 3072 else 3
        boi = json.loads((TMP / f"{i['key']}.boiler.json").read_text())
        print(f"{i['key']:<16} {size:>7}B n_with={n} {i['windows']}"
              + (f"  BOILER={boi}" if boi else ""))


def main_check(path: str) -> bool:
    data = json.loads(Path(path).read_text())
    ok = True
    for key, entry in sorted(data.items()):
        p = TMP / f"{key}.md"
        if not p.exists() or p.stat().st_size == 0:
            print(f"[FAIL] {key}: пустой/отсутствующий .md")
            ok = False
            continue
        t = p.read_text()
        sl = slices(t)
        hay = norm_real(sl["head"] + " " + sl["mid"])
        full = norm_real(t)
        boi = json.loads((TMP / f"{key}.boiler.json").read_text())
        w = entry.get("with") or []
        want_n = 2 if len(t.encode()) < 3072 else 3
        if len(w) < want_n:
            print(f"[FAIL] {key}: with={len(w)} < {want_n}")
            ok = False
        for ph in w:
            if norm_real(ph) in hay:
                if ph in t:
                    pass
                elif ph in sl["head"] or ph in sl["mid"]:
                    pass
                else:
                    print(f"[note] {key}: совпадает только после нормализации: {ph!r}")
            elif norm_real(ph) in full:
                print(f"[FAIL] {key}: фраза вне head+mid окна: {ph!r}")
                ok = False
            else:
                print(f"[FAIL] {key}: фразы НЕТ в файле: {ph!r}")
                ok = False
            if re.search(r"[#*`\[\]()>|]", ph):
                print(f"[WARN] {key}: разметка в фразе: {ph!r}")
            nw = len(norm_real(ph).split())
            if not (4 <= nw <= 12):
                print(f"[WARN] {key}: {nw} слов во фразе: {ph!r}")
        wo = entry.get("without") or []
        exp_wo = boi if boi else []
        if wo != exp_wo:
            print(f"[FAIL] {key}: без-список не равен boiler ({wo} vs {exp_wo})")
            ok = False
        # уникальность ключей соотнесена с наличием файла
    extra = set(data) - {p.name[:-3] for p in TMP.glob("*.md") if p.stat().st_size > 0}
    if extra:
        print(f"[FAIL] лишние ключи: {extra}")
        ok = False
    print("OK" if ok else "ЕСТЬ ОШИБКИ")
    return ok


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "check":
        main_check(sys.argv[2])
    else:
        main_dump()
