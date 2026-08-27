"""Shared types for the question catalogue."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Literal

import pandas as pd


Difficulty = Literal["초급", "중급", "고급"]
QuestionKind = Literal["mcq", "code_blank"]


@dataclass(frozen=True)
class Question:
    id: str
    title: str
    topic: str
    difficulty: Difficulty
    kind: QuestionKind
    prompt: str
    data_factory: Callable[[], pd.DataFrame]
    preview_config: dict[str, Any] = field(default_factory=lambda: {"rows": 8})
    immutable_template: str = ""
    blank_prompt: str = ""
    choices: tuple[str, ...] = ()
    correct_choice: int | None = None
    validator_id: str | None = None
    allowed_methods: frozenset[str] = frozenset()
    hint: str = ""
    solution: str = ""
    explanation: str = ""

