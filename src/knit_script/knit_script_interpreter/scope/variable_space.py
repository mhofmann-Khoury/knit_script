"""Module containing the Variable_Space class."""

from typing import Any


class Variable_Space:
    """Tracks all the variables in a local scope with no protected attributes to accidentally override."""

    def __init__(self) -> None:
        """Initialize an empty variable space."""
        pass

    def __contains__(self, variable_name: str) -> bool:
        """
        Args:
            variable_name (str): The name of the variable to check for existence.

        Returns:
            bool: True if the variable exists, False otherwise.
        """
        return hasattr(self, variable_name)

    def __getitem__(self, variable_name: str) -> Any:
        """
        Args:
            variable_name (str): The name of the variable to access.

        Returns:
            Any: The value of the variable.

        Raises:
            AttributeError: If the variable does not exist.
        """
        return getattr(self, variable_name)

    def __setitem__(self, variable_name: str, value: Any) -> None:
        """
        Set a variable with the given variable name.
        Overrides any variable already defined by that variable name.

        Args:
            variable_name (str): The name of the variable to set.
            value (Any): The value of the variable.
        """
        setattr(self, variable_name, value)

    def __delitem__(self, variable_name: str) -> None:
        """
        Delete the variable with the given key name.

        Args:
            variable_name (str): The name of the variable to delete.

        Raises:
             AttributeError: If the variable does not exist.
        """
        delattr(self, variable_name)
