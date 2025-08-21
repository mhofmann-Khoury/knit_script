"""KnitScript exceptions that mirror Python's built-in exception types.

This module provides KnitScript-specific exception classes that mirror Python's built-in exception types while adding location information from the parse tree.
 These exceptions maintain compatibility with Python's exception hierarchy while providing enhanced error reporting specific to knit script programs.
"""
from knit_script.knit_script_exceptions.Knit_Script_Exception import (
    Knit_Script_Located_Exception,
)
from knit_script.knit_script_interpreter.ks_element import KS_Element


class Knit_Script_TypeError(Knit_Script_Located_Exception, TypeError):
    """KnitScript-specific TypeError with location information.

    This exception class combines the standard Python TypeError with KnitScript location information,
    providing enhanced error reporting for type-related errors that occur during knit script execution. It maintains compatibility with Python's TypeError while adding parse tree location context.
    """

    def __init__(self, message: str, ks_element: KS_Element):
        """Initialize the Knit_Script_TypeError.

        Args:
            message (str): The error message describing the type error.
            ks_element (KS_Element): The KS_Element from the parse tree that caused the exception.
        """
        Knit_Script_Located_Exception.__init__(self, message, ks_element)
        TypeError.__init__(self, self.message)


class Knit_Script_AttributeError(Knit_Script_Located_Exception, AttributeError):
    """KnitScript-specific AttributeError with location information.

    This exception class combines the standard Python AttributeError with KnitScript location information,
    providing enhanced error reporting for attribute access errors that occur during knit script execution.
    It maintains compatibility with Python's AttributeError while adding parse tree location context.
    """

    def __init__(self, message: str, ks_element: KS_Element):
        """Initialize the Knit_Script_AttributeError.

        Args:
            message (str): The error message describing the attribute error.
            ks_element (KS_Element): The KS_Element from the parse tree that caused the exception.
        """
        Knit_Script_Located_Exception.__init__(self, message, ks_element)
        AttributeError.__init__(self, self.message)


class Knit_Script_NameError(Knit_Script_Located_Exception, NameError):
    """KnitScript-specific NameError with location information.

    This exception class combines the standard Python NameError with KnitScript location information,
    providing enhanced error reporting for name resolution errors that occur during knit script execution.
    It maintains compatibility with Python's NameError while adding parse tree location context.
    """

    def __init__(self, message: str, ks_element: KS_Element):
        """Initialize the Knit_Script_NameError.

        Args:
            message (str): The error message describing the name resolution error.
            ks_element (KS_Element): The KS_Element from the parse tree that caused the exception.
        """
        Knit_Script_Located_Exception.__init__(self, message, ks_element)
        NameError.__init__(self, self.message)


class Knit_Script_IndexError(Knit_Script_Located_Exception, IndexError):
    """KnitScript-specific IndexError with location information.

    This exception class combines the standard Python IndexError with KnitScript location information,
    providing enhanced error reporting for indexing errors that occur during knit script execution.
    It maintains compatibility with Python's IndexError while adding parse tree location context.
    """

    def __init__(self, message: str, ks_element: KS_Element):
        """Initialize the Knit_Script_IndexError.

        Args:
            message (str): The error message describing the indexing error.
            ks_element (KS_Element): The KS_Element from the parse tree that caused the exception.
        """
        Knit_Script_Located_Exception.__init__(self, message, ks_element)
        IndexError.__init__(self, self.message)


class Knit_Script_KeyError(Knit_Script_Located_Exception, KeyError):
    """KnitScript-specific KeyError with location information.

    This exception class combines the standard Python KeyError with KnitScript location information,
    providing enhanced error reporting for key access errors that occur during knit script execution.
    It maintains compatibility with Python's KeyError while adding parse tree location context.
    """

    def __init__(self, message: str, ks_element: KS_Element):
        """Initialize the Knit_Script_KeyError.

        Args:
            message (str): The error message describing the key access error.
            ks_element (KS_Element): The KS_Element from the parse tree that caused the exception.
        """
        Knit_Script_Located_Exception.__init__(self, message, ks_element)
        KeyError.__init__(self, self.message)


class Knit_Script_ImportError(Knit_Script_Located_Exception, ImportError):
    """KnitScript-specific ImportError with location information.

    This exception class combines the standard Python ImportError with KnitScript location information,
    providing enhanced error reporting for module import errors that occur during knit script execution.
    It maintains compatibility with Python's ImportError while adding parse tree location context.
    """

    def __init__(self, message: str, ks_element: KS_Element):
        """Initialize the Knit_Script_ImportError.

        Args:
            message (str): The error message describing the import error.
            ks_element (KS_Element): The KS_Element from the parse tree that caused the exception.
        """
        Knit_Script_Located_Exception.__init__(self, message, ks_element)
        ImportError.__init__(self, self.message)


class Knit_Script_ValueError(Knit_Script_Located_Exception, ValueError):
    """KnitScript-specific ValueError with location information.

    This exception class combines the standard Python ValueError with KnitScript location information,
    providing enhanced error reporting for value-related errors that occur during knit script execution.
    It maintains compatibility with Python's ValueError while adding parse tree location context.
    """

    def __init__(self, message: str, ks_element: KS_Element):
        """Initialize the Knit_Script_ValueError.

        Args:
            message (str): The error message describing the value error.
            ks_element (KS_Element): The KS_Element from the parse tree that caused the exception.
        """
        Knit_Script_Located_Exception.__init__(self, message, ks_element)
        ValueError.__init__(self, self.message)
