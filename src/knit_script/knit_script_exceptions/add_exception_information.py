"""Module containing a method to update exceptions with location information about the statement that triggered them."""

from parglare.common import position_context

from knit_script.knit_script_exceptions.Knit_Script_Exception import Knit_Script_Located_Exception
from knit_script.knit_script_interpreter.ks_element import KS_Element

_KNITSCRIPT_NOTE = "Raised in when Processing KnitScript"


def has_ks_notes(error: BaseException) -> bool:
    """
    Args:
        error (BaseException): The error raised to determine if it has already been marked with knitscript context information.

    Returns:
        bool: True if the error has been annotated with knitscript context information.

    """
    return isinstance(error, Knit_Script_Located_Exception) or (hasattr(error, "__notes__") and error.__notes__[0] == _KNITSCRIPT_NOTE)


def add_ks_information_to_error(error: BaseException, element: KS_Element) -> BaseException:
    """
    Args:
        error (BaseException): The error raised to add location and Knitscript context to.
        element (KS_Element): The Knit Script Element used to locate the exception source in the knitscript file.

    Returns:
        BaseException: The same exception modified with notes that document the location in the knitscript file that triggered the error.
    """
    if has_ks_notes(error):
        return error  # Already annotated, return as is.
    file_str = ""
    if element.location.file_name is not None:
        file_str = f"in file {element.location.file_name}"
    error.add_note(_KNITSCRIPT_NOTE)
    error.add_note(f"\t{error.__class__.__name__}{file_str} on line {element.location.line}")
    error.add_note(f"\t{position_context(element.location.input_str, element.location.start_position)}")
    return error
