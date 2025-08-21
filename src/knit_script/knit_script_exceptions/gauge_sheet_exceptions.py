"""This module contains Knit Script Exceptions related to the gauge and sheet management system.

These exceptions are raised when the code reaches an error state caused by mismanagement of gauge and sheet configurations in multi-sheet knitting operations.
The exceptions provide detailed information about gauge limits, sheet boundaries, and complex sheet peeling operations that are essential for advanced knitting techniques.
"""
from __future__ import annotations

from virtual_knitting_machine.machine_components.needles.Needle import Needle

from knit_script.knit_script_exceptions.Knit_Script_Exception import (
    Knit_Script_Exception,
)


class Gauge_Value_Exception(Knit_Script_Exception):
    """Exception raised when gauge is set beyond the machine's capabilities.

    This exception occurs when attempting to set a gauge value that is outside the acceptable range for the knitting machine,
     typically when the gauge is too low (less than 1) or too high (exceeding machine limits).
     The gauge value determines the number of sheets in multi-sheet knitting configurations and must be within the machine's supported range.
    """

    def __init__(self, gauge: int) -> None:
        """Initialize the Gauge_Value_Exception.

        Args:
            gauge (int): The invalid gauge value that was provided and caused the exception.
        """
        super().__init__(f"Gauge must be between 0 and and the MAX_GAUGE but got {gauge}")


class Sheet_Value_Exception(Knit_Script_Exception):
    """Exception raised when sheet is set to an unacceptable value.

    This exception occurs when attempting to set an active sheet number that is outside the valid range for the current gauge configuration.
    Sheet numbers must be between 0 and gauge-1, as each sheet represents one layer in the multi-sheet gauge configuration.
    """

    def __init__(self, sheet: int, current_gauge: int) -> None:
        """Initialize the Sheet_Value_Exception.

        Args:
            sheet (int): The invalid sheet value that was provided.
            current_gauge (int): The current gauge setting that defines the valid range for sheet values.
        """
        super().__init__(f"Sheet must be between 0 and gauge {current_gauge} but got {sheet}")


class Sheet_Peeling_Stacked_Loops_Exception(Knit_Script_Exception):
    """Exception raised when trying to peel loops that cannot be returned to a separated state.

    This exception occurs during sheet peeling operations when loops that were recorded on both front and back needles cannot be properly separated
     and returned to their original positions due to the current machine state. This typically happens when the peeling process encounters stacked loops that cannot be cleanly separated.
    """

    def __init__(self, front_needle: Needle, back_needle: Needle) -> None:
        """Initialize the Sheet_Peeling_Stacked_Loops_Exception.

        Args:
            front_needle (Needle): The front needle with recorded loops that cannot be properly separated.
            back_needle (Needle): The back needle with recorded loops that cannot be properly separated.
        """
        super().__init__(f"Loops recorded on {front_needle} and {back_needle}, but peeled loops cannot be returned to a seperated state")


class Sheet_Peeling_Blocked_Loops_Exception(Knit_Script_Exception):
    """Exception raised when loops cannot be returned due to blocking loops on the target needle.

    This exception occurs during sheet reset operations when loops need to be transferred back to their recorded positions but are blocked by existing loops on the target needle.
    This prevents the proper restoration of the sheet configuration.
    """

    def __init__(self, return_to_needle: Needle, return_from_needle: Needle) -> None:
        """Initialize the Sheet_Peeling_Blocked_Loops_Exception.

        Args:
            return_to_needle (Needle): The needle that has blocking loops preventing the return operation.
            return_from_needle (Needle): The needle attempting to return loops to the blocked target.
        """
        super().__init__(f"Cannot return loops from {return_from_needle} because loops are held on {return_to_needle}")


class Lost_Sheet_Loops_Exception(Knit_Script_Exception):
    """Exception raised when loops are lost and the sheet cannot be reset.

    This exception occurs when loops that were recorded on a needle during sheet operations are no longer present when attempting to reset the sheet,
    indicating that the loops have been lost or moved unexpectedly. This prevents the sheet from being properly restored to its recorded state.
    """

    def __init__(self, recorded_needle: Needle) -> None:
        """Initialize the Lost_Sheet_Loops_Exception.

        Args:
            recorded_needle (Needle): The needle where loops were recorded but are now lost.
        """
        super().__init__(f"Lost loops recorded on {recorded_needle}. Sheet cannot be reset.")
