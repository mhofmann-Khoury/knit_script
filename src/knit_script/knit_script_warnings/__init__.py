"""
Knit Script Warnings Package
============================

This package provides warning classes for the Knit Script interpreter,
alerting users to potentially problematic code patterns that don't cause errors but may lead to unexpected behavior.

Warning Classes
---------------

Base Warning:
    Knit_Script_Warning: Base class for all knit script warnings, extends Python's RuntimeWarning with knit script specific formatting and context.

Variable Scope Warnings:
    Shadow_Variable_Warning: Raised when a variable declaration shadows an existing variable in an outer scope.

Machine State Warnings:
    Sheet_Beyond_Gauge_Warning: Raised when sheet settings exceed current gauge limits, causing automatic correction.

Warning System
--------------

The warning system follows Python's standard warning framework while providing knit script specific context and formatting.
All warnings inherit from Knit_Script_Warning which provides:

- Consistent message formatting with "KnitScript Warning:" prefix
- Integration with Python's warning filtering system
- Contextual information about the problematic code

Warnings are raised using Python's warnings.warn() function and can
be controlled through standard Python warning filters.

Usage
-----

Warnings are automatically raised by the interpreter when potentially
problematic situations are detected. Users can control warning behavior
through Python's warning system:

- warnings.simplefilter('ignore') to suppress all warnings
- warnings.filterwarnings() for fine-grained control
- Custom warning handlers for logging or processing

"""
