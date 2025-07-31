"""Used for tracking global variable space of program execution"""
from __future__ import annotations
from typing import Any


class Knit_Script_Globals:
    """Tracks all the global variables."""

    def __init__(self) -> None:
        self.values: dict[str, Any] = {}
        self._exit_value: Any = None

    def copy(self) -> Knit_Script_Globals:
        """Create a shallow copy of the current values.

        Returns:
            Knit_Script_Globals: Shallow copy of the current values.
        """
        copy_values = Knit_Script_Globals()
        copy_values.values = {k: v for k, v in self.values.items()}
        copy_values._exit_value = self._exit_value
        return copy_values

    @property
    def exit_value(self) -> Any:
        """Get the return value for whole knit script execution.

        Returns:
            Any: Return value for whole knit script execution.
        """
        return self._exit_value

    @exit_value.setter
    def exit_value(self, value: Any) -> None:
        self._exit_value = value

    def __getitem__(self, key: str) -> Any:
        return getattr(self, key)

    def __setitem__(self, key: str, value: Any) -> None:
        setattr(self, key, value)

    def __delitem__(self, key: str) -> None:
        delattr(self, key)

    def __contains__(self, key: str) -> bool:
        return hasattr(self, key)
