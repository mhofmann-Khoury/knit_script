"""Module containing the base class for KnitScript exceptions."""


class Knit_Script_Exception(Exception):
    """Superclass for all exceptions related to processing KnitScript programs."""

    def __init__(self, message: str):
        """Initialize the Knit_Script_Exception.

        Args:
            message (str): The error message to display.
        """
        self.message = f"\nKnit Script Exception: {message}"
        super().__init__(self.message)
