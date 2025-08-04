"""Used for tracking global variable space of program execution"""
from __future__ import annotations
from typing import Any


class Knit_Script_Globals:
    """Tracks all the global variables."""

    def __init__(self) -> None:
        self.exit_value: Any = None

    def __contains__(self, key: str) -> bool:
        return hasattr(self, key)
