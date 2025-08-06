"""
Knit Script Interpreter Scope Management Package
================================================

This package provides comprehensive scope and variable management for the Knit Script interpreter,
 handling global variables, local scopes, machine state, and module imports.

The scope system manages a hierarchical variable structure that supports:
- Global variable tracking across the entire program execution.
- Local scopes for functions and control structures.
- Machine-specific variables (gauge, carrier, racking, sheet, direction).
- Module import and namespace management.
- Python scope integration for built-in functions and variables.

Classes Overview
----------------

Global Scope Management:
    Knit_Script_Globals: Tracks global variables and program exit values.

Local Scope Management:
    Knit_Script_Scope: Main scope manager handling variable hierarchy, function scopes, module scopes, and machine state.
    Variable_Scope: Legacy variable scope implementation for function-level variable management.

Machine State Management:
    Machine_Scope: Manages machine-specific variables and state.
    Machine_Variables: Enumeration of machine variable names and accessors.

Module Management:
    Knit_Script_Module: Handles module imports and namespace organization.

Supporting Classes:
    Gauged_Sheet_Record: Manages sheet configurations for different gauge settings

Key Features
------------

Hierarchical Scoping:
    - Parent-child scope relationships.
    - Variable shadowing with warnings.
    - Scope-specific variable resolution.

Machine Integration:
    - Direct machine state management.
    - Automatic validation of machine parameters.
    - Integration with virtual knitting machine components.

Module System:
    - Python module integration.
    - Knit script module imports.
    - Namespace path resolution.

Error Handling:
    - Custom exceptions for invalid gauge/sheet values.
    - Comprehensive warning system for scope conflicts.
    - Graceful handling of undefined variables.

Architecture Notes
------------------

The scope system follows a tree-like hierarchy where:
- Root scope contains global variables and machine state.
- Function scopes can return values and have isolated local variables.
- Module scopes persist in the variable namespace for later access.
- Machine scopes provide direct access to knitting machine state.

Variable resolution follows Python-like semantics:
1. Check local scope (current and parent scopes).
2. Check module scope if available.
3. Check global scope.
4. Check Python built-in scope.
5. Raise NameError if not found.
"""
