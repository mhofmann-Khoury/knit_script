"""
Knit Script Interpreter Statements Package
==========================================

This package contains all statement types for the Knit Script interpreter.
Statements are executable language constructs that perform actions or control program flow but do not return values (unlike expressions).

Statement Categories
-------------------

Core Language Statements:
    Statement: Base class for all statements.
    Expression_Statement: Wrapper for evaluating expressions as statements.
    Code_Block: Executes multiple statements in a new scope.

Assignment and Variables:
    Assignment: Assigns values to variables in local or global scope.
    Variable_Declaration: Declares variables in current or global scope.
    With_Statement: Sets variables temporarily within a statement block.

Control Flow:
    If_Statement: Conditional execution with if-else branches.
    While_Statement: Loop execution while condition is true.
    For_Each_Statement: Iteration over iterable collections.
    Try_Catch_Statement: Exception handling with try-catch blocks.

Function Management:
    Function_Declaration: Declares user-defined functions.
    Function_Signature: Function object for parameter binding and execution.
    Return_Statement: Returns values from functions and exits function scope.

Module System:
    Import_Statement: Imports Python modules and knit script files.

Machine Operations:
    In_Direction_Statement: Executes needle instructions in specified direction.
    Carriage_Pass_Specification: Manages collections of needle operations.
    Drop_Pass: Specialized pass for dropping stitches.
    Push_Statement: Modifies layer positions of needles in stacking hierarchy.
    Swap_Statement: Swaps stitch layers between needles.
    Xfer_Pass_Statement: Executes transfer operations with racking control.

Carrier and Yarn Management:
    Cut_Statement: Cuts yarn carriers.
    Release_Statement: Releases yarn inserting hook.
    Remove_Statement: Removes carriers from bed without cutting.

Output and Debugging:
    Print: Prints to console and adds comments to knitout.
    Pause_Statement: Pauses machine execution.
    Assertion: Tests conditions with optional error messages.

Architecture
-----------

All statement classes inherit from the base Statement class and implement the execute() method to define their behavior.
Statements operate within a Knit_Script_Context that provides access to:
- Variable scopes (local, global, machine)
- Machine state and operations
- Knitout instruction generation
- Parser and execution environment

The statement system integrates closely with the expression system, scope management, and machine simulation components.
"""

from __future__ import annotations

# Core statement classes
from .Statement import Statement, Expression_Statement
from .assignment import Assignment
from .code_block_statements import Code_Block

# Control flow statements
from .branch_statements import If_Statement
from .control_loop_statements import While_Statement, For_Each_Statement
from .try_catch_statements import Try_Catch_Statement

# Function-related statements
from .function_dec_statement import Function_Declaration, Function_Signature
from .return_statement import Return_Statement

# Module system
from .Import_Statement import Import_Statement

# Machine operation statements
from .in_direction_statement import In_Direction_Statement
from .Carriage_Pass_Specification import Carriage_Pass_Specification
from .Drop_Pass import Drop_Pass
from .Push_Statement import Push_Statement
from .Swap_Statement import Swap_Statement

# Carrier and yarn statements
from .carrier_statements import Cut_Statement, Release_Statement, Remove_Statement

# Variable management
from .Variable_Declaration import Variable_Declaration
from .With_Statement import With_Statement

# Specialized machine operations
from .xfer_pass_statement import Xfer_Pass_Statement

# Output and debugging statements
from .Print import Print
from .instruction_statements import Pause_Statement
from .Assertion import Assertion

# Define what gets imported with "from knit_script.statements import *"
__all__ = [
    # Core statement types
    'Statement',
    'Expression_Statement',
    'Assignment',
    'Code_Block',

    # Control flow
    'If_Statement',
    'While_Statement',
    'For_Each_Statement',
    'Try_Catch_Statement',

    # Functions
    'Function_Declaration',
    'Function_Signature',
    'Return_Statement',

    # Module system
    'Import_Statement',

    # Variable management
    'Variable_Declaration',
    'With_Statement',

    # Machine operations
    'In_Direction_Statement',
    'Carriage_Pass_Specification',
    'Drop_Pass',
    'Push_Statement',
    'Swap_Statement',
    'Xfer_Pass_Statement',

    # Carrier management
    'Cut_Statement',
    'Release_Statement',
    'Remove_Statement',

    # Output and debugging
    'Print',
    'Pause_Statement',
    'Assertion',
]
