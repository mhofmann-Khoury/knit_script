"""
Knit Script Interpreter Statements Package
==========================================

This package contains all statement types for the Knit Script interpreter.
Statements are executable language constructs that perform actions or control program flow but do not return values (unlike expressions).

Statement Categories
--------------------

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
------------

All statement classes inherit from the base Statement class and implement the execute() method to define their behavior.
Statements operate within a Knit_Script_Context that provides access to:
- Variable scopes (local, global, machine)
- Machine state and operations
- Knitout instruction generation
- Parser and execution environment

The statement system integrates closely with the expression system, scope management, and machine simulation components.
"""
