"""KnitScript Expressions Package

This package contains all expression classes used in the KnitScript programming language.
Expressions are evaluable components that return values when processed in a KnitScript execution context.
They form the building blocks of KnitScript programs for performing calculations, accessing machine state, and manipulating, data structures.

Expression Categories:

"""

from __future__ import annotations

# Base expression class and utilities
from .expressions import Expression, get_expression_value_list

# Value expressions (context-free)
from .values import (
    None_Value,
    Int_Value,
    Float_Value,
    Boolean_Value,
    String_Value,
    Bed_Value,
    Machine_Position_Value,
    Machine_Type_Value,
    Header_ID_Value,
)

# Variable and attribute access
from .variables import Variable_Expression
from .accessors import Attribute_Accessor_Expression

# Machine and hardware expressions
from .machine_accessor import Machine_Accessor, Sheet_Expression
from .needle_expression import Needle_Expression
from .needle_set_expression import Needle_Set_Expression, Needle_Sets
from .carrier import Carrier_Expression
from .direction import Pass_Direction_Expression
from .Gauge_Expression import Gauge_Expression

# Instruction expressions
from .instruction_expression import Needle_Instruction_Exp, Machine_Instruction_Exp
from .xfer_pass_racking import Xfer_Pass_Racking

# Collection and data structure expressions
from .list_expression import (
    Knit_Script_List,
    Knit_Script_Dictionary,
    List_Comp,
    Dictionary_Comprehension,
    Unpack,
    Sliced_List,
)

# Indexing and slicing
from .Indexed_Expression import Indexed_Expression, Slice_Index

# Operator expressions
from .operator_expressions import Operator_Expression, Operator
from .not_expression import Not_Expression

# Function expressions
from .function_expressions import Function_Call

# String processing
from .formatted_string import Formatted_String_Value

# Define what gets exported with "from expressions import *"
__all__ = [
    # Base expression and utilities
    "Expression",
    "get_expression_value_list",

    # Value expressions
    "None_Value",
    "Int_Value",
    "Float_Value",
    "Boolean_Value",
    "String_Value",
    "Bed_Value",
    "Machine_Position_Value",
    "Machine_Type_Value",
    "Header_ID_Value",

    # Variable and attribute access
    "Variable_Expression",
    "Attribute_Accessor_Expression",

    # Machine and hardware expressions
    "Machine_Accessor",
    "Sheet_Expression",
    "Needle_Expression",
    "Needle_Set_Expression",
    "Needle_Sets",
    "Carrier_Expression",
    "Pass_Direction_Expression",
    "Gauge_Expression",

    # Instruction expressions
    "Needle_Instruction_Exp",
    "Machine_Instruction_Exp",
    "Xfer_Pass_Racking",

    # Collection and data structure expressions
    "Knit_Script_List",
    "Knit_Script_Dictionary",
    "List_Comp",
    "Dictionary_Comprehension",
    "Unpack",
    "Sliced_List",

    # Indexing and slicing
    "Indexed_Expression",
    "Slice_Index",

    # Operator expressions
    "Operator_Expression",
    "Operator",
    "Not_Expression",

    # Function expressions
    "Function_Call",

    # String processing
    "Formatted_String_Value",
]
