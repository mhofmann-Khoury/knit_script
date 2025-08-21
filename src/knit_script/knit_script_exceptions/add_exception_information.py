"""Module containting a method to update exceptions with location information about the statement that triggered them."""

from knit_script.knit_script_exceptions.Knit_Script_Exception import (
    Knit_Script_Located_Exception,
)
from knit_script.knit_script_exceptions.python_style_exceptions import (
    Knit_Script_AttributeError,
    Knit_Script_ImportError,
    Knit_Script_IndexError,
    Knit_Script_KeyError,
    Knit_Script_NameError,
    Knit_Script_TypeError,
    Knit_Script_ValueError,
)
from knit_script.knit_script_interpreter.ks_element import KS_Element


def add_exception_to_statement(e: Exception, element: KS_Element) -> Knit_Script_Located_Exception:
    """
    Raises a Knit_Script Located Exception located at the given Knit Script Element for easier Knitscript debugging.
    Args:
        e (Exception): the exception to update to fit a KS element.
        element (KS_Element): The Knit Script Element used to locate the exception source in the knitscript file.
    """
    if not isinstance(e, Knit_Script_Located_Exception):
        if isinstance(e, TypeError):
            return Knit_Script_TypeError(str(e), element)
        elif isinstance(e, NameError):
            return Knit_Script_NameError(str(e), element)
        elif isinstance(e, AttributeError):
            return Knit_Script_AttributeError(str(e), element)
        elif isinstance(e, IndexError):
            return Knit_Script_IndexError(str(e), element)
        elif isinstance(e, KeyError):
            return Knit_Script_KeyError(str(e), element)
        elif isinstance(e, ImportError):
            return Knit_Script_ImportError(str(e), element)
        elif isinstance(e, ValueError):
            return Knit_Script_ValueError(str(e), element)
        else:
            return Knit_Script_Located_Exception(e, element)
    else:
        return e
