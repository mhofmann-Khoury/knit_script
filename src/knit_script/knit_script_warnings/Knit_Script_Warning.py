"""A Module containing the base class for Knitting Script Warnings."""
from virtual_knitting_machine.machine_components.needles.Sheet_Needle import Sheet_Identifier


class Knit_Script_Warning(RuntimeWarning):
    """
        Warnings caused by error-prone code in Knit Script.
    """

    def __init__(self, message: str):
        self.message = f"\nKnitScript Warning: {message}"
        super().__init__(self.message)


class Shadow_Variable_Warning(Knit_Script_Warning):

    def __init__(self, variable_name: str):
        super().__init__(f"Variable <{variable_name}> shadows a variable in the outer scope.")


class Sheet_Beyond_Gauge_Warning(Knit_Script_Warning):

    def __init__(self, sheet: int | Sheet_Identifier, gauge: int):
        super().__init__(f"Knit Script Warning: Gauge of {gauge} is greater than current sheet {sheet} so sheet is set to {gauge - 1}")
