#!/usr/bin/env python3
"""Общие хелперы для утилит заморозки/оценки (freeze_content, truncate_eval).

snippet_recall — та же нормализация, что в grade.py (симметричная для фразы
и текста), чтобы числа совпадали с августовским baseline.
tail_class    — классификация хвоста content, как в measure_cut.py.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from grade import norm  # noqa: E402

END_SENT = set(".!?…»”’\"'")


def snippet_recall(text: str, phrases: list[str] | None) -> float | None:
    if not phrases:
        return None
    hay = norm(text)
    return round(sum(1 for p in phrases if norm(p) in hay) / len(phrases), 3)


def tail_class(content: str) -> str:
    stripped = content.rstrip()
    if not stripped:
        return "empty"
    if content.endswith("\n\n"):
        return "newline"
    last = stripped[-1]
    if last in END_SENT:
        return "sentence-end"
    if last in ")]}:;,":
        return "soft"
    if last.isalnum():
        return "mid-token"
    return "other"
