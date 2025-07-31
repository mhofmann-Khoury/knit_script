"""A module containing the base class for Knitting Script warnings."""
from virtual_knitting_machine.machine_components.needles.Sheet_Needle import Sheet_Identifier


class Knit_Script_Warning(RuntimeWarning):
    """Base class for warnings caused by error-prone code in Knit Script."""

    def __init__(self, message: str):
        """Initialize the Knit_Script_Warning.

        Args:
            message: The warning message to display.
        """
        self.message = f"\nKnitScript Warning: {message}"
        super().__init__(self.message)


class Shadow_Variable_Warning(Knit_Script_Warning):
    """Warning raised when a variable shadows another variable in an outer scope."""

    def __init__(self, variable_name: str):
        """Initialize the Shadow_Variable_Warning.

        Args:
            variable_name: The name of the variable that is shadowing another variable.
        """
        super().__init__(f"Variable <{variable_name}> shadows a variable in the outer scope.")


class Sheet_Beyond_Gauge_Warning(Knit_Script_Warning):
    """Warning raised when the sheet setting exceeds the current gauge limits."""

    def __init__(self, sheet: int | Sheet_Identifier, gauge: int):
        """Initialize the Sheet_Beyond_Gauge_Warning.

        Args:
            sheet: The sheet value that exceeds the gauge.
            gauge: The current gauge setting that limits the sheet value.
        """
        super().__init__(f"Gauge of {gauge} is greater than current sheet {sheet} so sheet is set to {gauge - 1}")