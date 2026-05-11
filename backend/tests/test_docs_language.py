from __future__ import annotations

import re
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
DOC_PATTERNS = ("README.md", "docs/*.md", "doc/*.md")
FENCED_CODE_RE = re.compile(r"```.*?```", re.DOTALL)
INLINE_CODE_RE = re.compile(r"`[^`]*`")
MARKDOWN_LINK_RE = re.compile(r"\[([^\]]+)\]\([^)]+\)")
WORD_RE = re.compile(r"[A-Za-zА-Яа-яЁё]+")
CYRILLIC_RE = re.compile(r"[А-Яа-яЁё]")
LATIN_RE = re.compile(r"[A-Za-z]")


def _published_docs() -> list[Path]:
    docs: list[Path] = []
    for pattern in DOC_PATTERNS:
        docs.extend(sorted(REPO_ROOT.glob(pattern)))
    return docs


def _normalize_markdown(text: str) -> str:
    text = FENCED_CODE_RE.sub(" ", text)
    text = INLINE_CODE_RE.sub(" ", text)
    text = MARKDOWN_LINK_RE.sub(r"\1", text)
    return text


def _cyrillic_ratio(text: str) -> float:
    words = WORD_RE.findall(text)
    if not words:
        return 0.0
    cyrillic_words = sum(1 for word in words if CYRILLIC_RE.search(word))
    latin_words = sum(1 for word in words if LATIN_RE.search(word) and not CYRILLIC_RE.search(word))
    total = cyrillic_words + latin_words
    if total == 0:
        return 0.0
    return cyrillic_words / total


def test_published_docs_are_written_in_russian() -> None:
    docs = _published_docs()

    assert docs, "Не найдено опубликованных markdown-документов для проверки"

    failures: list[str] = []
    for path in docs:
        text = _normalize_markdown(path.read_text(encoding="utf-8"))
        ratio = _cyrillic_ratio(text)
        if ratio < 0.5:
            failures.append(f"{path.relative_to(REPO_ROOT)}: доля русского текста {ratio:.0%}")

    assert not failures, "Документы должны быть на русском языке:\n" + "\n".join(failures)
