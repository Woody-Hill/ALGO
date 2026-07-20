from __future__ import annotations

from pathlib import Path
import re
import sys
from typing import Iterable


ROOT_README = Path("README.md")
TARGET_ROOT = Path("problem_solve")
DEFAULT_LANGUAGES = ["java"]

LANG_EXTENSIONS = {
    "java": "java",
    "swift": "swift",
    "python": "py",
    "c++": "cpp",
    "cpp": "cpp",
    "c": "c",
    "javascript": "js",
    "typescript": "ts",
    "kotlin": "kt",
}

DAILY_BLOCK_PATTERN = re.compile(
    r"^###\s*🟨\s*(?P<title>.+?)\s*데일리\s*문제\s*$"
    r"(?P<body>[\s\S]*?)"
    r"(?=^###\s|^##\s|\Z)",
    re.MULTILINE,
)

MARKDOWN_LINK_PATTERN = re.compile(
    r"^(?:[-*]\s*)?\[(?P<title>.+?)]\((?P<url>.+?)\)\s*$"
)


def sanitize(name: str) -> str:
    invalid = r'<>:"/\\|?*'

    for character in invalid:
        name = name.replace(character, "-")

    name = re.sub(r"\s+", " ", name).strip()
    return name.rstrip(".")


def extract_daily_blocks(text: str) -> list[tuple[str, str]]:
    blocks = [
        (
            match.group("title").strip(),
            match.group("body"),
        )
        for match in DAILY_BLOCK_PATTERN.finditer(text)
    ]

    if not blocks:
        raise ValueError(
            "README에서 "
            "'### 🟨 {날짜 또는 회차} 데일리 문제' 형식
