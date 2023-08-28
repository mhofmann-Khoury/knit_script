"""Errors associated with gauging schema"""

from knit_script.Knit_Errors.Knit_Script_Error import Knit_Script_Error
from knit_script.knitting_machine.Machine_State import Machine_State


class Gauge_Value_Error(Knit_Script_Error):
    """
        Raised when gauge is set beyond machine's capabilities
    """
    def __init__(self, gauge: int):
        super().__init__(f"Gauge must be between 0 and {Machine_State.MAX_GAUGE} but got {gauge}")
        self._gauge = gauge

    @property
    def gauge(self) -> int:
        """
        :return: The gauge that raised the error
        """
        return self._gauge

class Sheet_Value_Error(Knit_Script_Error):
    """
        Raised when sheet is set to an unacceptable value
    """
    def __init__(self, sheet: int, current_gauge:int):
        super().__init__( f"Sheet must be between 0 and gauge {current_gauge} but got {sheet}")
        self._sheet = sheet
        self._current_gauge = current_gauge

    @property
    def sheet(self) -> int:
        """
        :return: Sheet that caused the error
        """
        return self._sheet

    @property
    def current_gauge(self) -> int:
        """
        :return: Gauge at time of error
        """
        return self._current_gauge