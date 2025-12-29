"""Used for tracking global variable space of program execution.

This module provides the Knit_Script_Globals class, which manages the global variable namespace for knit script program execution.
It serves as a container for storing and accessing global variables that persist throughout the execution of a knit script program, including special system variables like exit values.
"""

from __future__ import annotations

from typing import Any


class Knit_Script_Globals:
    """Tracks all the global variables for knit script program execution.

    The Knit_Script_Globals class provides a dynamic namespace for storing global variables that need to persist throughout the execution of a knit script program.
    It uses Python's attribute system to allow flexible variable storage and retrieval, supporting any variable name that is a valid Python identifier.

    This class is designed to be extensible, allowing new global variables to be added dynamically during program execution.
    It provides containment checking to determine whether specific variables have been defined in the global scope.

    """

    def __init__(self) -> None:
        """Initialize the global variable tracker with default values.

        Creates a new instance of the global variable space with the exit_value initialized to None. Additional global variables can be added dynamically by setting attributes on the instance.
        """
        pass

    def __contains__(self, key: str) -> bool:
        """
        Args:
            key (str): The name of the global variable to check for existence.

        Returns:
            bool: True if the global variable exists, False otherwise.
        """
        return hasattr(self, key)

    def __getitem__(self, key: str) -> Any:
        """
        Args:
            key (str): The name of the global variable to access.

        Returns:
            Any: The value of the global variable.

        Raises:
            AttributeError: If the global variable does not exist.
        """
        return getattr(self, key)

    def __setitem__(self, key: str, value: Any) -> None:
        """
        Set a global variable with the given key name.
        Overrides any global variable already defined by that key.

        Args:
            key (str): The name of the global variable to set.
            value (Any): The value of the global variable.
        """
        setattr(self, key, value)

    def __delitem__(self, key: str) -> None:
        """
        Delete the global variable with the given key name.
        Args:
            key (str): The name of the global variable to delete.

        Raises:
             AttributeError: If the global variable does not exist.
        """
        delattr(self, key)
