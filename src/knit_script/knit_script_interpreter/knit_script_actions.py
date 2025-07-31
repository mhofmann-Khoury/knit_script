"""Actions for converting parglare elements into useful code"""
from __future__ import annotations
import codecs
from enum import Enum
from typing import Any, Iterable

from knitout_interpreter.knitout_operations.knitout_instruction import Knitout_Instruction_Type
from parglare import get_collector
from parglare.parser import LRStackNode
from virtual_knitting_machine.Knitting_Machine_Specification import Knitting_Machine_Type, Knitting_Position

from knit_script.knit_script_interpreter.expressions.Gauge_Expression import Gauge_Expression
from knit_script.knit_script_interpreter.expressions.Indexed_Expression import Slice_Index, Indexed_Expression
from knit_script.knit_script_interpreter.expressions.accessors import Attribute_Accessor_Expression
from knit_script.knit_script_interpreter.expressions.carrier import Carrier_Expression
from knit_script.knit_script_interpreter.expressions.direction import Pass_Direction_Expression
from knit_script.knit_script_interpreter.expressions.expressions import Expression
from knit_script.knit_script_interpreter.expressions.formatted_string import Formatted_String_Value
from knit_script.knit_script_interpreter.expressions.function_expressions import Function_Call
from knit_script.knit_script_interpreter.expressions.instruction_expression import Needle_Instruction_Exp
from knit_script.knit_script_interpreter.expressions.list_expression import Knit_Script_List, Knit_Script_Dictionary, List_Comp, Dictionary_Comprehension, Unpack
from knit_script.knit_script_interpreter.expressions.machine_accessor import Machine_Accessor, Sheet_Expression
from knit_script.knit_script_interpreter.expressions.needle_expression import Needle_Expression
from knit_script.knit_script_interpreter.expressions.needle_set_expression import Needle_Sets, Needle_Set_Expression
from knit_script.knit_script_interpreter.expressions.not_expression import Not_Expression
from knit_script.knit_script_interpreter.expressions.operator_expressions import Operator_Expression
from knit_script.knit_script_interpreter.expressions.values import (Boolean_Value, Bed_Value, Float_Value, Int_Value, String_Value, None_Value,
                                                                    Machine_Position_Value, Machine_Type_Value, Header_ID_Value)
from knit_script.knit_script_interpreter.expressions.variables import Variable_Expression
from knit_script.knit_script_interpreter.expressions.xfer_pass_racking import Xfer_Pass_Racking
from knit_script.knit_script_interpreter.knit_script_values.Machine_Specification import Machine_Bed_Position
from knit_script.knit_script_interpreter.ks_element import KS_Element
from knit_script.knit_script_interpreter.statements.Assertion import Assertion
from knit_script.knit_script_interpreter.statements.Drop_Pass import Drop_Pass
from knit_script.knit_script_interpreter.statements.Import_Statement import Import_Statement
from knit_script.knit_script_interpreter.statements.Print import Print
from knit_script.knit_script_interpreter.statements.Push_Statement import Push_Statement
from knit_script.knit_script_interpreter.statements.Statement import Statement, Expression_Statement
from knit_script.knit_script_interpreter.statements.Swap_Statement import Swap_Statement
from knit_script.knit_script_interpreter.statements.Variable_Declaration import Variable_Declaration
from knit_script.knit_script_interpreter.statements.With_Statement import With_Statement
from knit_script.knit_script_interpreter.statements.assignment import Assignment
from knit_script.knit_script_interpreter.statements.branch_statements import If_Statement
from knit_script.knit_script_interpreter.statements.carrier_statements import Cut_Statement, Remove_Statement, Release_Statement
from knit_script.knit_script_interpreter.statements.code_block_statements import Code_Block
from knit_script.knit_script_interpreter.statements.control_loop_statements import While_Statement, For_Each_Statement
from knit_script.knit_script_interpreter.statements.function_dec_statement import Function_Declaration
from knit_script.knit_script_interpreter.statements.in_direction_statement import In_Direction_Statement
from knit_script.knit_script_interpreter.statements.instruction_statements import Pause_Statement
from knit_script.knit_script_interpreter.statements.return_statement import Return_Statement
from knit_script.knit_script_interpreter.statements.try_catch_statements import Try_Catch_Statement
from knit_script.knit_script_interpreter.statements.xfer_pass_statement import Xfer_Pass_Statement

action = get_collector()  # some boiler plate parglare code


@action
def program(_parser_node: LRStackNode, __: list, statements: list[Statement]) -> list[Statement]:
    """Creates a program from a list of statements.
    
    Args:
        _parser_node: The parser element that created this value
        __: Unused parameter
        statements: The list of statements to execute
        
    Returns:
        The list of statements
    """
    return statements


def _in_enum(item: str | Enum, enumeration: Iterable) -> bool:
    """Checks if an item exists in an enumeration.
    
    Args:
        item: Item to compare against Enum
        enumeration: The enumeration class
        
    Returns:
        True if item is in enumeration, False otherwise
    """
    if isinstance(item, str):
        return (item in [i.value for i in enumeration]) or (item in [i.name for i in enumeration])
    try:
        return item in enumeration
    except KeyError as _:
        return False


# basic expressions and statements
@action
def identifier(parser_node: LRStackNode, node: str) -> Expression:
    """Converts a string identifier into an appropriate expression.
    
    Args:
        parser_node: The parser element that created this value ignored parglare context
        node: The string recognized as an identifier
        
    Returns:
        Variable expression or withheld keyword
    """
    if node == "None":
        return None_Value(parser_node)
    elif node == "True" or node == "False":
        return Boolean_Value(parser_node, node)
    elif _in_enum(node, Machine_Bed_Position):
        return Bed_Value(parser_node, node)
    elif _in_enum(node, Knitting_Position):
        return Machine_Position_Value(parser_node, node)
    elif _in_enum(node, Knitting_Machine_Type):
        return Machine_Type_Value(parser_node, node)
    elif node == "machine":
        return Machine_Accessor(parser_node)
    elif _in_enum(node, Needle_Sets):
        return Needle_Set_Expression(parser_node, node)
    else:
        return Variable_Expression(parser_node, node)


@action
def declare_variable(parser_node: LRStackNode, __: list, assign: Assignment) -> Variable_Declaration:
    """Creates a variable declaration statement.
    
    Args:
        parser_node: The parser element that created this value ignored parglare context
        __: Ignored nodes
        assign: Assignment before eol punctuation
        
    Returns:
        Variable Declaration Statement that assigns the variable on execution
    """
    return Variable_Declaration(parser_node, assign)


@action
def declare_global(parser_node: LRStackNode, __: list, assign: Assignment) -> Variable_Declaration:
    """Creates a global variable declaration statement.
    
    Args:
        parser_node: The parser element that created this value ignored parglare context
        __: Ignored nodes
        assign: Assignment before eol punctuation
        
    Returns:
        Variable Declaration Statement that assigns the global variable on execution
    """
    return Variable_Declaration(parser_node, assign, is_global=True)


@action
def assertion(parser_node: LRStackNode, __: list, exp: Expression, error: Expression | None = None) -> Assertion:
    """Creates an assertion statement.
    
    Args:
        parser_node: The parser element that created this value ignored parglare context
        __: Ignored nodes
        exp: Expression to evaluate assertion by
        error: Error to report (optional)
        
    Returns:
        Assertion Statement
    """
    return Assertion(parser_node, exp, error)


@action
def print_statement(parser_node: LRStackNode, __: list, exp: Expression) -> Print:
    """Creates a print statement.
    
    Args:
        parser_node: The parser element that created this value ignored parglare context
        __: Ignored nodes
        exp: Expression to print
        
    Returns:
        Print Statement
    """
    return Print(parser_node, exp)


@action
def try_catch(parser_node: LRStackNode, __: list, try_block: Statement, catch_block: Statement, errors: list[Expression]) -> Try_Catch_Statement:
    """Creates a try-catch statement.
    
    Args:
        parser_node: The parser element that created this value ignored parglare context
        __: Ignored nodes
        try_block: Statements to execute in try branch
        catch_block: Statements to execute in catch branch
        errors: Errors to accept
        
    Returns:
        Try Catch statement
    """
    return Try_Catch_Statement(parser_node, try_block, catch_block, errors=errors)


@action
def exception_assignment(parser_node: LRStackNode, __: list, except_val: Expression, var_name: Variable_Expression) -> Assignment:
    """Creates assignment with reversed syntax for catch statements.
    
    Args:
        parser_node: The parser element that created this value
        __: Unused parameter
        except_val: The exception to allow
        var_name: The name of the variable for the error
        
    Returns:
        An assignment operation for this error
    """
    return Assignment(parser_node, var_name.variable_name, except_val)


@action
def pause_statement(parser_node: LRStackNode, __: list) -> Pause_Statement:
    """Creates a pause statement.
    
    Args:
        parser_node: The parser element that created this value ignored parglare context
        __: Ignored nodes
        
    Returns:
        Pause statement
    """
    return Pause_Statement(parser_node)


@action
def assignment(parser_node: LRStackNode, __: list, var_name: Variable_Expression, exp: Expression) -> Assignment:
    """Creates an assignment expression.
    
    Args:
        parser_node: The parser element that created this value ignored parglare context
        __: Ignored nodes
        var_name: Processed identifier to variable name
        exp: Expression to assign variable value
        
    Returns:
        Assignment expression which evaluates to expression value
    """
    # todo: ensure that typing is checking identifier not over shadowing keywords
    return Assignment(parser_node, var_name.variable_name, exp)


# NUMBERS #

@action
def float_exp(parser_node: LRStackNode, node: str) -> Float_Value:
    """Creates a float value expression.
    
    Args:
        parser_node: The parser element that created this value ignored parglare context
        node: The number string
        
    Returns:
        The positive number specified
    """
    return Float_Value(parser_node, node)


@action
def int_exp(parser_node: LRStackNode, node: str) -> Int_Value:
    """Creates an integer value expression.
    
    Args:
        parser_node: The parser element that created this value ignored parglare context
        node: The number string
        
    Returns:
        The positive number specified
    """
    return Int_Value(parser_node, node)


@action
def direction_exp(parser_node: LRStackNode, nodes: list) -> Pass_Direction_Expression:
    """Creates a direction expression.
    
    Args:
        parser_node: The parser element that created this value
        nodes: Single node list with direction keyword
        
    Returns:
        Pass direction expression
    """
    return Pass_Direction_Expression(parser_node, nodes[0])


@action
def string(parser_node: LRStackNode, node: str) -> String_Value:
    """Creates a string value expression.
    
    Args:
        parser_node: The parser element that created this value ignored parglare context
        node: String value
        
    Returns:
        Expression storing quote
    """
    string_value = node.strip("\"")
    decode_string = codecs.decode(string_value, 'unicode_escape')
    return String_Value(parser_node, decode_string)


@action
def f_string_section(parser_node: LRStackNode, __: list, exp: Expression | None = None, string_value: str | None = None) -> Expression:
    """Creates an expression from a section of a formatted string.
    
    Args:
        parser_node: The parser element that created this value ignored parglare context
        __: Unused parameter
        exp: Expression in formatting
        string_value: String in formatting
        
    Returns:
        Expression of string value of a section of a formatted string
    """
    if exp is not None:
        return exp
    else:
        assert isinstance(string_value, str)
        string_value = string_value.encode().decode('unicode_escape')
        prior_char_index = parser_node.start_position - 1
        if prior_char_index >= 0:
            prior_char = parser_node.input_str[prior_char_index]
            while prior_char.isspace():
                string_value = prior_char + string_value
                prior_char_index -= 1
                if prior_char_index >= 0:
                    prior_char = parser_node.input_str[prior_char_index]
                else:
                    prior_char = None
        return String_Value(parser_node, string_value)


@action
def formatted_string(parser_node: LRStackNode, __: list, sections: list[Expression]) -> Formatted_String_Value:
    """Creates a formatted string expression.
    
    Args:
        parser_node: The parser element that created this value ignored parglare context
        __: Unused parameter
        sections: F string sections parsed as expressions
        
    Returns:
        Formatted string expression
    """
    return Formatted_String_Value(parser_node, sections)


@action
def call_list(_parser_node: LRStackNode, __: list, params: list[Expression] | None = None,
              kwargs: list[Assignment] | None = None) -> tuple[list[Expression], list[Assignment]]:
    """Creates a call list with parameters and keyword arguments.
    
    Args:
        _parser_node: The parser element that created this value
        __: Unused parameter
        params: The parameters in the call list
        kwargs: The keyword set parameters in the call list
        
    Returns:
        Tuple of parameters and kwargs
    """
    if params is None:
        params = []
    if kwargs is None:
        kwargs = []
    return params, kwargs


@action
def function_call(parser_node: LRStackNode, __: list, func_name: Variable_Expression,
                  args: tuple[list[Expression], list[Assignment]] | None) -> Function_Call:
    """Creates a function call expression.
    
    Args:
        parser_node: The parser element that created this value
        __: Unused parameter
        func_name: Name of the function being called
        args: The arguments passed to the function
        
    Returns:
        The function call
    """
    if args is None:
        params = []
        kwargs = []
    else:
        params = args[0]
        kwargs = args[1]
    return Function_Call(parser_node, func_name, params, kwargs)


@action
def list_expression(parser_node: LRStackNode, __: list, exps: list[Expression]) -> Knit_Script_List:
    """Creates a list expression.
    
    Args:
        parser_node: The parser element that created this value
        __: Unused parameter
        exps: Expressions in the list
        
    Returns:
        The list expression
    """
    return Knit_Script_List(parser_node, exps)


@action
def list_comp(parser_node: LRStackNode, __: list, fill_exp: Expression, variables: list[Variable_Expression], iter_exp: Expression, comp_cond: Expression = None) -> List_Comp:
    """Creates a list comprehension expression.
    
    Args:
        parser_node: The parser element that created this value
        __: Unused parameter
        fill_exp: Expression that fills the list
        variables: Variables to fill from iterable
        iter_exp: The iterable to pass over
        comp_cond: Condition to evaluate for adding a value
        
    Returns:
        List comprehension
    """
    return List_Comp(parser_node, fill_exp, variables, iter_exp, comp_cond)


@action
def indexed_value(parser_node: LRStackNode, __: list, item: Expression, key: Slice_Index | Knit_Script_List, assign: Expression) -> Indexed_Expression:
    """Creates an indexed value expression.
    
    Args:
        parser_node: The parser element that created this value
        __: Unused parameter
        item: Item to index
        key: Key to index by
        assign: Optional assignment
        
    Returns:
        Expression that evaluates assignment
    """
    if isinstance(key, Knit_Script_List):
        key = key.expressions[0]
    return Indexed_Expression(parser_node, item, key, assign)


@action
def slice_index(parser_node: LRStackNode, __: list, start: Expression | None, end: Expression | list[Expression | None]) -> Slice_Index:
    """Creates a slice index expression.
    
    Args:
        parser_node: The parser element that created this value
        __: Unused parameter
        start: Start index expression
        end: End index expression or list of expressions
        
    Returns:
        Slice index expression
    """
    spacer = None
    if isinstance(end, list):
        if len(end) > 1:
            spacer = end[1]
        end = end[0]
    return Slice_Index(start, end, spacer, parser_node)


@action
def dict_assign(_parser_node: LRStackNode, __: list, key: Expression, exp: Expression) -> tuple[Expression, Expression]:
    """Collects key value pair for dictionary.
    
    Args:
        _parser_node: The parser element that created this value
        __: Unused parameter
        key: Key expression
        exp: Value expression
        
    Returns:
        Tuple of key and value
    """
    return key, exp


@action
def dict_expression(parser_node: LRStackNode, __: list, kwargs: list[tuple[Expression, Expression]]) -> Knit_Script_Dictionary:
    """Creates a dictionary expression.
    
    Args:
        parser_node: The parser element that created this value
        __: Unused parameter
        kwargs: Key value pairs
        
    Returns:
        The dictionary
    """
    return Knit_Script_Dictionary(parser_node, kwargs)


@action
def dict_comp(parser_node: LRStackNode, __: list, key: Expression, value: Expression,
              variables: list[Variable_Expression], iter_exp: Expression, comp_cond: Expression | None = None) -> Dictionary_Comprehension:
    """Creates a dictionary comprehension expression.
    
    Args:
        parser_node: The parser element that created this value
        __: Unused parameter
        key: Key expression
        value: Value expression
        variables: Variables to parse from iterable
        iter_exp: The iterable to parse over
        comp_cond: Conditional on variables to skip specific designs
        
    Returns:
        Dictionary comprehension
    """
    return Dictionary_Comprehension(parser_node, key, value, variables, iter_exp, comp_cond)


@action
def unpack(parser_node: LRStackNode, __: list, exp: Expression) -> Unpack:
    """Creates an unpack expression.
    
    Args:
        parser_node: The parser element that created this value
        __: Unused parameter
        exp: Expression to unpack
        
    Returns:
        Unpacking expression
    """
    return Unpack(parser_node, exp)


@action
def code_block(parser_node: LRStackNode, __: list, statements: list[Statement]) -> Code_Block:
    """Creates a code block statement.
    
    Args:
        parser_node: The parser element that created this value ignored parglare context
        __: Ignored nodes
        statements: Statements to execute in sub scope
        
    Returns:
        Scoping block
    """
    return Code_Block(parser_node, statements)


@action
def elif_statement(_parser_node: LRStackNode, __: list, exp: Expression, stmnt: Statement) -> tuple[Expression, Statement]:
    """Creates components of an elif statement.
    
    Args:
        _parser_node: The parser element that created this value ignored parglare context
        __: Ignored nodes
        exp: Expression to test on elif
        stmnt: Statement to execute on true result
        
    Returns:
        Tuple of expression and statement to execute when true
    """
    return exp, stmnt


@action
def else_statement(_parser_node: LRStackNode, __: list, false_statement: Code_Block) -> Code_Block:
    """Creates an else statement.
    
    Args:
        _parser_node: The parser element that created this value
        __: Unused parameter
        false_statement: Code block to execute when false
        
    Returns:
        The code to execute when false
    """
    return false_statement


@action
def if_statement(parser_node: LRStackNode, __: list,
                 condition: Expression, true_statement: Code_Block,
                 elifs: list[tuple[Expression, Statement]],
                 else_stmt: Code_Block | None) -> If_Statement:
    """Creates an if statement.
    
    Args:
        parser_node: The parser element that created this value
        __: Unused parameter.
        condition: Branching condition.
        true_statement: Statement to execute on true.
        elifs: List of else-if conditions and statements.
        else_stmt: Statement to execute on false.
        
    Returns:
        If statement
    """
    while len(elifs) > 0:
        elif_tuple = elifs.pop()
        else_stmt = If_Statement(parser_node, elif_tuple[0], elif_tuple[1], else_stmt)
    return If_Statement(parser_node, condition, true_statement, else_stmt)


@action
def while_statement(parser_node: LRStackNode, __: list, condition: Expression, while_block: Code_Block) -> While_Statement:
    """Creates a while statement.
    
    Args:
        parser_node: The parser element that created this value
        __: Unused parameter
        condition: Condition to evaluate on while
        while_block: The statement to execute with each iteration
        
    Returns:
        While statement
    """
    return While_Statement(parser_node, condition, while_block)


@action
def for_each_statement(parser_node: LRStackNode, __: list, variables: list[Variable_Expression], iters: list[Expression], block: Code_Block) -> For_Each_Statement:
    """Creates a for each statement.
    
    Args:
        parser_node: The parser element that created this value
        __: Unused parameter
        variables: To assign on each iteration of iterable
        iters: Iterable to iterate over
        block: Statement to execute with each iteration
        
    Returns:
        For each statement
    """
    if len(iters) == 1:
        return For_Each_Statement(parser_node, variables, iters[0], block)
    else:
        return For_Each_Statement(parser_node, variables, iters, block)


@action
def as_assignment(parser_node: LRStackNode, __: list, variable: Variable_Expression, exp: Expression) -> Assignment:
    """Creates an assignment using 'as' syntax.
    
    Args:
        parser_node: The parser element that created this value
        __: Unused parameter
        variable: Variable to assign to
        exp: Expression to assign
        
    Returns:
        Assignment value
    """
    if isinstance(variable, Header_ID_Value):
        variable = Variable_Expression(parser_node, variable.hid_str)
    return Assignment(parser_node, var_name=variable.variable_name, value_expression=exp)


@action
def with_statement(parser_node: LRStackNode, __: list, assigns: list[Assignment], block: Code_Block) -> With_Statement:
    """Creates a with statement.
    
    Args:
        parser_node: The parser element that created this value
        __: Unused parameter.
        assigns: Assignments for block.
        block: Block to execute.
        
    Returns:
        With statement
    """
    return With_Statement(parser_node, block, assigns)


@action
def needle_instruction(_parser_node: LRStackNode, __: list, inst: str) -> Knitout_Instruction_Type:
    """Creates a needle instruction type.
    
    Args:
        _parser_node: The parser element that created this value
        __: Unused parameter
        inst: Instruction keyword
        
    Returns:
        Needle instruction
    """
    return Knitout_Instruction_Type.get_instruction(inst)


@action
def instruction_assignment(parser_node: LRStackNode, __: list, inst: Expression, needles: list[Expression]) -> Needle_Instruction_Exp:
    """Creates a needle instruction expression.
    
    Args:
        parser_node: The parser element that created this value
        __: Unused parameter
        inst: Instruction to apply to needles.
        needles: Needles to apply instruction to.
        
    Returns:
        Needle instruction expression
    """
    return Needle_Instruction_Exp(parser_node, inst, needles)


@action
def carriage_pass(parser_node: LRStackNode, __: list, pass_dir: Expression, instructions: list[Needle_Instruction_Exp]) -> In_Direction_Statement:
    """Creates a carriage pass statement.
    
    Args:
        parser_node: The parser element that created this value
        __: Unused parameter
        pass_dir: Direction to apply instructions in
        instructions: Instructions to apply
        
    Returns:
        In direction statement
    """
    return In_Direction_Statement(parser_node, pass_dir, instructions)


@action
def needle_id(parser_node: LRStackNode, needle_node: str) -> Needle_Expression:
    """Creates a needle expression.
    
    Args:
        parser_node: The parser element that created this value
        needle_node: Node representing needle
        
    Returns:
        Needle expression
    """
    return Needle_Expression(parser_node, needle_node)


@action
def sheet_id(parser_node: LRStackNode, sheet_node: str) -> Sheet_Expression:
    """Creates a sheet expression.
    
    Args:
        parser_node: The parser element that created this value
        sheet_node: String representing sheet
        
    Returns:
        Sheet expression
    """
    return Sheet_Expression(parser_node, sheet_node)


@action
def carrier(parser_node: LRStackNode, carrier_node: str) -> Carrier_Expression:
    """Creates a carrier expression.
    
    Args:
        parser_node: The parser element that created this value
        carrier_node: String describing carrier
        
    Returns:
        Carrier expression
    """
    return Carrier_Expression(parser_node, carrier_node)


@action
def return_statement(parser_node: LRStackNode, __: list, exp: Expression) -> Return_Statement:
    """Creates a return statement.
    
    Args:
        parser_node: The parser element that created this value
        __: Unused parameter
        exp: Expression to return
        
    Returns:
        Return statement
    """
    return Return_Statement(parser_node, exp)


@action
def param_list(_parser_node: LRStackNode, __: list, args: list[Variable_Expression] | None = None,
               kwargs: list[Assignment] | None = None) -> tuple[list[Variable_Expression], list[Assignment]]:
    """Creates a parameter list for function definitions.
    
    Args:
        _parser_node: The parser element that created this value
        __: Unused parameter
        args: List of argument identifiers
        kwargs: List of keyword assignments
        
    Returns:
        Tuple of arguments and keyword assignments
    """
    if args is None:
        args = []
    if kwargs is None:
        kwargs = []
    return args, kwargs


@action
def function_declaration(parser_node: LRStackNode, __: list, func_name: Variable_Expression,
                         params: tuple[list[Variable_Expression], list[Assignment]] | None,
                         block: Statement) -> Function_Declaration:
    """Creates a function declaration.
    
    Args:
        parser_node: The parser element that created this value
        __: Unused parameter
        func_name: Name of the function
        params: List of variables for arguments, list of key word assignments
        block: Body to execute
        
    Returns:
        The function declaration
    """
    if params is None:
        params = [], []
    args = params[0]
    kwargs = params[1]
    return Function_Declaration(parser_node, func_name.variable_name, args, kwargs, block)


@action
def expression(parser_node: LRStackNode, nodes: list[str | KS_Element | Expression]) -> Expression:
    """Creates an expression from parser nodes.
    
    Args:
        parser_node: The parser element that created this value ignored parglare context
        nodes: Nodes to parse into expression
        
    Returns:
        Expression
    """
    if len(nodes) == 1:
        return nodes[0]
    if nodes[0] == "(":
        return nodes[1]
    elif len(nodes) == 4:
        if nodes[1] == "is":
            is_op = Operator_Expression(parser_node, nodes[0], nodes[1], nodes[3])
            if nodes[2] is not None:
                return Not_Expression(parser_node, is_op)
            else:
                return is_op
        else:  # not in operation
            return Not_Expression(parser_node, Operator_Expression(parser_node, nodes[0], nodes[2], nodes[3]))
    else:
        return Operator_Expression(parser_node, nodes[0], nodes[1], nodes[2])


@action
def negation(parser_node: LRStackNode, __: list, exp: Expression) -> Not_Expression:
    """Creates a negation expression.
    
    Args:
        parser_node: The parser element that created this value
        __: Unused parameter
        exp: Expression to negate
        
    Returns:
        Not expression
    """
    return Not_Expression(parser_node, exp)


@action
def xfer_rack(parser_node: LRStackNode, __: list, is_across: str | None = None,
              dist_exp: Expression | None = None, side_id: Expression | None = None) -> Xfer_Pass_Racking:
    """Creates a transfer racking specification.
    
    Args:
        parser_node: The parser element that created this value
        __: Unused parameter
        is_across: True, if xfer is directly across beds
        dist_exp: The needle offset for xfer
        side_id: Offset direction
        
    Returns:
        Xfer pass racking
    """
    if is_across is not None:
        return Xfer_Pass_Racking(parser_node, distance_expression=None, direction_expression=None)
    return Xfer_Pass_Racking(parser_node, distance_expression=dist_exp, direction_expression=side_id)


@action
def xfer_pass(parser_node: LRStackNode, __: list, needles: list[Expression],
              rack_val: Xfer_Pass_Racking,
              bed: Expression | None = None,
              slider: str | None = None) -> Xfer_Pass_Statement:
    """Creates a transfer pass statement.
    
    Args:
        parser_node: The parser element that created this value
        __: Unused parameter
        needles: Needles to start xfer from
        rack_val: Racking for xfers
        bed: Beds to land on. Exclude needles already on bed
        slider: True if transferring to sliders
        
    Returns:
        Xfer pass statement
    """
    return Xfer_Pass_Statement(parser_node, rack_val, needles, bed, slider is not None)


@action
def accessor(parser_node: LRStackNode, __: list, exp: Expression, attribute: Expression) -> Attribute_Accessor_Expression:
    """Creates an attribute accessor expression.
    
    Args:
        parser_node: The parser element that created this value
        __: Unused parameter
        exp: Expression to get from
        attribute: Attribute to collect
        
    Returns:
        Accessor expression
    """
    return Attribute_Accessor_Expression(parser_node, exp, attribute)


@action
def exp_statement(parser_node: LRStackNode, __: list, exp: Expression) -> Expression_Statement:
    """Creates an expression statement.
    
    Args:
        parser_node: The parser element that created this value
        __: Unused parameter
        exp: Expression to execute
        
    Returns:
        Execution of expression
    """
    return Expression_Statement(parser_node, exp)


@action
def cut_statement(parser_node: LRStackNode, __: list, exps: list[Expression]) -> Cut_Statement:
    """Creates a cut statement.
    
    Args:
        parser_node: The parser element that created this value
        __: Unused parameter
        exps: Carriers to cut
        
    Returns:
        Cut statement
    """
    return Cut_Statement(parser_node, exps)


@action
def release_statement(parser_node: LRStackNode, __: list) -> Release_Statement:
    """Creates a release statement for current carrier.
    
    Args:
        parser_node: The parser element that created this value
        __: Unused parameter
        
    Returns:
        Release statement for current carrier
    """
    return Release_Statement(parser_node)


@action
def remove_statement(parser_node: LRStackNode, __: list, exps: list[Expression]) -> Remove_Statement:
    """Creates a remove statement.
    
    Args:
        parser_node: The parser element that created this value
        __: Unused parameter
        exps: Carriers to out
        
    Returns:
        Remove statement
    """
    return Remove_Statement(parser_node, exps)


@action
def gauge_exp(parser_node: LRStackNode, __: list, sheet_exp: Expression, gauge: Expression) -> Gauge_Expression:
    """Creates a gauge expression.
    
    Args:
        parser_node: The parser element that created this value
        __: Unused parameter
        sheet_exp: Sheet value
        gauge: Gauge value
        
    Returns:
        Gauge expression
    """
    return Gauge_Expression(parser_node, sheet_exp, gauge)


@action
def drop_pass(parser_node: LRStackNode, __: list, needles: list[Expression]) -> Drop_Pass:
    """Creates a drop pass statement.
    
    Args:
        parser_node: The parser element that created this value
        __: Unused parameter
        needles: Needles to drop from
        
    Returns:
        Drop pass
    """
    return Drop_Pass(parser_node, needles)


@action
def push_to(_parser_node: LRStackNode, __: list, push_val: str | list) -> str | Expression:
    """Creates a push target specification.
    
    Args:
        _parser_node: The parser element that created this value
        __: Unused parameter
        push_val: Front, back, or a specific layer value
        
    Returns:
        Identifying string or expression layer value
    """
    if isinstance(push_val, list):
        return push_val[1]
    return push_val


@action
def push_dir(_parser_node: LRStackNode, __: list, amount: Expression, direction: str) -> tuple[Expression, str]:
    """Creates a push direction specification.
    
    Args:
        _parser_node: The parser element that created this value
        __: Unused parameter
        amount: Value to push
        direction: Direction to push
        
    Returns:
        Tuple of amount and direction
    """
    return amount, direction


@action
def push_statement(parser_node: LRStackNode, __: list, needles: list[Expression], push_val: str | Expression | tuple[Expression, str]) -> Push_Statement:
    """Creates a push statement.
    
    Args:
        parser_node: The parser element that created this value
        __: Unused parameter
        needles: Needles to push layer value
        push_val: Specification of push value
        
    Returns:
        Push statement
    """
    return Push_Statement(parser_node, needles, push_val)


@action
def swap_statement(parser_node: LRStackNode, __: list, needles: list[Expression], swap_type: str, value: Expression) -> Swap_Statement:
    """Creates a swap statement.
    
    Args:
        parser_node: The parser element that created this value
        __: Unused parameter
        needles: The needles to do this swap with
        swap_type: Type of value to swap with
        value: The value to swap with
        
    Returns:
        Swap statement
    """
    return Swap_Statement(parser_node, needles, swap_type, value)


@action
def pass_second(_parser_node: LRStackNode, nodes: list[Any]) -> Any:
    """Returns the second node in a list.
    
    Args:
        _parser_node: The parser element that created this value
        nodes: Nodes parsed
        
    Returns:
        The second node in the list
    """
    return nodes[1]


@action
def import_statement(parser_node: LRStackNode, __: list, src: Expression, alias: Expression | None) -> Import_Statement:
    """Creates an import statement.
    
    Args:
        parser_node: The parser element that created this value
        __: Unused parameter
        src: Source module
        alias: Alias to assign in variable scope
        
    Returns:
        Import statement
    """
    return Import_Statement(parser_node, src, alias)
