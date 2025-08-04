"""KnitScript Exceptions Package

This package contains all exception classes used throughout the KnitScript programming language for knitting machine control.
This exception hierarchy provides detailed error reporting for various failure odes that can occur during script parsing, compilation, and execution.

Exception Hierarchy:
    Knit_Script_Exception (base)
    ├── Knit_Script_Assertion_Exception - Assertion failures in KnitScript programs
    ├── Parsing_Exception - Syntax and parsing errors in KnitScript source code
    ├── Needle_Instruction_Type_Exception - Invalid instruction types for needle operations
    ├── Incompatible_In_Carriage_Pass_Exception - Incompatible instructions in same pass
    ├── Required_Direction_Exception - Missing direction for yarn-carrier operations
    ├── Repeated_Needle_Exception - Attempting to work same needle multiple times
    ├── All_Needle_Operation_Exception - Invalid all-needle operations without proper racking
    ├── No_Declared_Carrier_Exception - Missing working carrier declaration
    ├── Gauge_Value_Exception - Invalid gauge settings beyond machine capabilities
    ├── Sheet_Value_Exception - Invalid sheet values for current gauge
    ├── Sheet_Peeling_Stacked_Loops_Exception - Cannot peel stacked loops to separated state
    ├── Sheet_Peeling_Blocked_Loops_Exception - Loops blocked from returning due to conflicts
    └── Lost_Sheet_Loops_Exception - Loops lost during sheet operations
"""
