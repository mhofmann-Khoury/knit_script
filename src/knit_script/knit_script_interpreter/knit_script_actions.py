"""Actions for converting parglare elements into useful code.

This module contains parser actions that convert parglare parsing elements into executable KnitScript code elements.
These actions are called during the parsing process to transform the parsed syntax tree into appropriate expression, statement, and value objects that can be executed by the KnitScript interpreter.
The module provides comprehensive support for all KnitScript language constructs including expressions, statements, control flow, functions, and machine operations.
"""
from __future__ import annotations

import codecs
from enum import Enum
from typing import Any, Iterable

from knitout_interpreter.knitout_operations.knitout_instruction import (
    Knitout_Instruction_Type,
)
from parglare import get_collector
from parglare.parser import LRStackNode
from virtual_knitting_machine.Knitting_Machine_Specification import (
    Knitting_Machine_Type,
    Knitting_Position,
)

from knit_script.knit_script_interpreter.expressions.accessors import (
    Attribute_Accessor_Expression,
)
from knit_script.knit_script_interpreter.expressions.carrier import Carrier_Expression
from knit_script.knit_script_interpreter.expressions.direction import (
    Pass_Direction_Expression,
)
from knit_script.knit_script_interpreter.expressions.expressions import Expression
from knit_script.knit_script_interpreter.expressions.formatted_string import (
    Formatted_String_Value,
)
from knit_script.knit_script_interpreter.expressions.function_expressions import (
    Function_Call,
)
from knit_script.knit_script_interpreter.expressions.Gauge_Expression import (
    Gauge_Expression,
)
from knit_script.knit_script_interpreter.expressions.Indexed_Expression import (
    Indexed_Expression,
    Slice_Index,
)
from knit_script.knit_script_interpreter.expressions.instruction_expression import (
    Needle_Instruction_Exp,
)
from knit_script.knit_script_interpreter.expressions.list_expression import (
    Dictionary_Comprehension,
    Knit_Script_Dictionary,
    Knit_Script_List,
    List_Comp,
    Unpack,
)
from knit_script.knit_script_interpreter.expressions.machine_accessor import (
    Machine_Accessor,
    Sheet_Expression,
)
from knit_script.knit_script_interpreter.expressions.needle_expression import (
    Needle_Expression,
)
from knit_script.knit_script_interpreter.expressions.needle_set_expression import (
    Needle_Set_Expression,
    Needle_Sets,
)
from knit_script.knit_script_interpreter.expressions.not_expression import (
    Not_Expression,
)
from knit_script.knit_script_interpreter.expressions.operator_expressions import (
    Operator_Expression,
)
from knit_script.knit_script_interpreter.expressions.values import (
    Bed_Value,
    Boolean_Value,
    Float_Value,
    Header_ID_Value,
    Int_Value,
    Machine_Position_Value,
    Machine_Type_Value,
    None_Value,
    String_Value,
)
from knit_script.knit_script_interpreter.expressions.variables import (
    Variable_Expression,
)
from knit_script.knit_script_interpreter.expressions.xfer_pass_racking import (
    Xfer_Pass_Racking,
)
from knit_script.knit_script_interpreter.ks_element import KS_Element
from knit_script.knit_script_interpreter.Machine_Specification import (
    Machine_Bed_Position,
)
from knit_script.knit_script_interpreter.statements.Assertion import Assertion
from knit_script.knit_script_interpreter.statements.assignment import Assignment
from knit_script.knit_script_interpreter.statements.branch_statements import (
    If_Statement,
)
from knit_script.knit_script_interpreter.statements.carrier_statements import (
    Cut_Statement,
    Release_Statement,
    Remove_Statement,
)
from knit_script.knit_script_interpreter.statements.code_block_statements import (
    Code_Block,
)
from knit_script.knit_script_interpreter.statements.control_loop_statements import (
    For_Each_Statement,
    While_Statement,
)
from knit_script.knit_script_interpreter.statements.Drop_Pass import Drop_Pass
from knit_script.knit_script_interpreter.statements.function_dec_statement import (
    Function_Declaration,
)
from knit_script.knit_script_interpreter.statements.Import_Statement import (
    Import_Statement,
)
from knit_script.knit_script_interpreter.statements.in_direction_statement import (
    In_Direction_Statement,
)
from knit_script.knit_script_interpreter.statements.instruction_statements import (
    Pause_Statement,
)
from knit_script.knit_script_interpreter.statements.Print import Print
from knit_script.knit_script_interpreter.statements.Push_Statement import Push_Statement
from knit_script.knit_script_interpreter.statements.return_statement import (
    Return_Statement,
)
from knit_script.knit_script_interpreter.statements.Statement import (
    Expression_Statement,
    Statement,
)
from knit_script.knit_script_interpreter.statements.Swap_Statement import Swap_Statement
from knit_script.knit_script_interpreter.statements.try_catch_statements import (
    Try_Catch_Statement,
)
from knit_script.knit_script_interpreter.statements.Variable_Declaration import (
    Variable_Declaration,
)
from knit_script.knit_script_interpreter.statements.With_Statement import With_Statement
from knit_script.knit_script_interpreter.statements.xfer_pass_statement import (
    Xfer_Pass_Statement,
)

action = get_collector()  # some boiler plate parglare code


@action
def program(_parser_node: LRStackNode, __: list, statements: list[Statement]) -> list[Statement]:
    """Create a program from a list of statements.

    Args:
        _parser_node (LRStackNode): The parser element that created this value.
        __ (list): Unused parameter from parser structure.
        statements (list[Statement]): The list of statements to execute in the program.

    Returns:
        list[Statement]: The list of statements representing the complete program.
    """
    return statements


def _in_enum(item: str | Enum, enumeration: Iterable) -> bool:
    """Check if an item exists in an enumeration.

    Args:
        item (str | Enum): Item to compare against enumeration, either as string or enum value.
        enumeration (Iterable): The enumeration class to check membership in.

    Returns:
        bool: True if item is in enumeration, False otherwise.
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
    """Convert a string identifier into an appropriate expression.

    Args:
        parser_node (LRStackNode): The parser element that created this value.
        node (str): The string recognized as an identifier.

    Returns:
        Expression: Variable expression or specialized keyword expression based on the identifier.
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
    """Create a variable declaration statement.

    Args:
        parser_node (LRStackNode): The parser element that created this value.
        __ (list): Ignored parser nodes.
        assign (Assignment): Assignment operation for the variable declaration.

    Returns:
        Variable_Declaration: Variable Declaration Statement that assigns the variable on execution.
    """
    return Variable_Declaration(parser_node, assign)


@action
def declare_global(parser_node: LRStackNode, __: list, assign: Assignment) -> Variable_Declaration:
    """Create a global variable declaration statement.

    Args:
        parser_node (LRStackNode): The parser element that created this value.
        __ (list): Ignored parser nodes.
        assign (Assignment): Assignment operation for the global variable declaration.

    Returns:
        Variable_Declaration: Variable Declaration Statement that assigns the global variable on execution.
    """
    return Variable_Declaration(parser_node, assign, is_global=True)


@action
def assertion(parser_node: LRStackNode, __: list, exp: Expression, error: Expression | None = None) -> Assertion:
    """Create an assertion statement.

    Args:
        parser_node (LRStackNode): The parser element that created this value.
        __ (list): Ignored parser nodes.
        exp (Expression): Expression to evaluate assertion condition.
        error (Expression | None, optional): Error message expression to report if assertion fails. Defaults to None.

    Returns:
        Assertion: Assertion Statement that validates the condition during execution.
    """
    return Assertion(parser_node, exp, error)


@action
def print_statement(parser_node: LRStackNode, __: list, exp: Expression) -> Print:
    """Create a print statement.

    Args:
        parser_node (LRStackNode): The parser element that created this value.
        __ (list): Ignored parser nodes.
        exp (Expression): Expression to print to output.

    Returns:
        Print: Print Statement that outputs the expression value.
    """
    return Print(parser_node, exp)


@action
def try_catch(parser_node: LRStackNode, __: list, try_block: Statement, catch_block: Statement, errors: list[Expression]) -> Try_Catch_Statement:
    """Create a try-catch statement.

    Args:
        parser_node (LRStackNode): The parser element that created this value.
        __ (list): Ignored parser nodes.
        try_block (Statement): Statements to execute in try branch.
        catch_block (Statement): Statements to execute in catch branch.
        errors (list[Expression]): List of exception expressions to catch.

    Returns:
        Try_Catch_Statement: Try Catch statement for exception handling.
    """
    return Try_Catch_Statement(parser_node, try_block, catch_block, errors=errors)


@action
def exception_assignment(parser_node: LRStackNode, __: list, except_val: Expression, var_name: Variable_Expression) -> Assignment:
    """Create assignment with reversed syntax for catch statements.

    Args:
        parser_node (LRStackNode): The parser element that created this value.
        __ (list): Unused parameter.
        except_val (Expression): The exception expression to allow.
        var_name (Variable_Expression): The name of the variable for storing the caught exception.

    Returns:
        Assignment: An assignment operation for binding the exception to a variable.
    """
    return Assignment(parser_node, var_name.variable_name, except_val)


@action
def pause_statement(parser_node: LRStackNode, __: list) -> Pause_Statement:
    """Create a pause statement.

    Args:
        parser_node (LRStackNode): The parser element that created this value.
        __ (list): Ignored parser nodes.

    Returns:
        Pause_Statement: Pause statement that halts execution temporarily.
    """
    return Pause_Statement(parser_node)


@action
def assignment(parser_node: LRStackNode, __: list, var_name: Variable_Expression, exp: Expression) -> Assignment:
    """Create an assignment expression.

    Args:
        parser_node (LRStackNode): The parser element that created this value.
        __ (list): Ignored parser nodes.
        var_name (Variable_Expression): Variable identifier to assign to.
        exp (Expression): Expression to assign as the variable value.

    Returns:
        Assignment: Assignment expression which evaluates to the assigned expression value.
    """
    return Assignment(parser_node, var_name.variable_name, exp)


# NUMBERS #

@action
def float_exp(parser_node: LRStackNode, node: str) -> Float_Value:
    """Create a float value expression.

    Args:
        parser_node (LRStackNode): The parser element that created this value.
        node (str): The number string to parse as a float.

    Returns:
        Float_Value: The floating point number expression.
    """
    return Float_Value(parser_node, node)


@action
def int_exp(parser_node: LRStackNode, node: str) -> Int_Value:
    """Create an integer value expression.

    Args:
        parser_node (LRStackNode): The parser element that created this value.
        node (str): The number string to parse as an integer.

    Returns:
        Int_Value: The integer number expression.
    """
    return Int_Value(parser_node, node)


@action
def direction_exp(parser_node: LRStackNode, nodes: list) -> Pass_Direction_Expression:
    """Create a direction expression.

    Args:
        parser_node (LRStackNode): The parser element that created this value.
        nodes (list): Single node list with direction keyword.

    Returns:
        Pass_Direction_Expression: Pass direction expression for carriage movement.
    """
    return Pass_Direction_Expression(parser_node, nodes[0])


@action
def string(parser_node: LRStackNode, node: str) -> String_Value:
    """Create a string value expression.

    Args:
        parser_node (LRStackNode): The parser element that created this value.
        node (str): String value including quotes.

    Returns:
        String_Value: Expression storing the decoded string value.
    """
    string_value = node.strip("\"")
    decode_string = codecs.decode(string_value, 'unicode_escape')
    return String_Value(parser_node, decode_string)


@action
def f_string_section(parser_node: LRStackNode, __: list, exp: Expression | None = None, string_value: str | None = None) -> Expression:
    """Create an expression from a section of a formatted string.

    Args:
        parser_node (LRStackNode): The parser element that created this value.
        __ (list): Unused parameter.
        exp (Expression | None, optional): Expression in formatting section. Defaults to None.
        string_value (str | None, optional): String literal in formatting section. Defaults to None.

    Returns:
        Expression: Expression representing the formatted string section value.
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
    """Create a formatted string expression.

    Args:
        parser_node (LRStackNode): The parser element that created this value.
        __ (list): Unused parameter.
        sections (list[Expression]): F string sections parsed as expressions.

    Returns:
        Formatted_String_Value: Formatted string expression that combines sections.
    """
    return Formatted_String_Value(parser_node, sections)


@action
def call_list(_parser_node: LRStackNode, __: list, params: list[Expression] | None = None, kwargs: list[Assignment] | None = None) -> tuple[list[Expression], list[Assignment]]:
    """Create a call list with parameters and keyword arguments.

    Args:
        _parser_node (LRStackNode): The parser element that created this value.
        __ (list): Unused parameter.
        params (list[Expression] | None, optional): The positional parameters in the call list. Defaults to None.
        kwargs (list[Assignment] | None, optional): The keyword parameters in the call list. Defaults to None.

    Returns:
        tuple[list[Expression], list[Assignment]]: Tuple of positional parameters and keyword arguments.
    """
    if params is None:
        params = []
    if kwargs is None:
        kwargs = []
    return params, kwargs


@action
def function_call(parser_node: LRStackNode, __: list, func_name: Variable_Expression, args: tuple[list[Expression], list[Assignment]] | None) -> Function_Call:
    """Create a function call expression.

    Args:
        parser_node (LRStackNode): The parser element that created this value.
        __ (list): Unused parameter.
        func_name (Variable_Expression): Name of the function being called.
        args (tuple[list[Expression], list[Assignment]] | None): The arguments passed to the function as tuple of positional and keyword arguments.

    Returns:
        Function_Call: The function call expression.
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
    """Create a list expression.

    Args:
        parser_node (LRStackNode): The parser element that created this value.
        __ (list): Unused parameter.
        exps (list[Expression]): Expressions in the list.

    Returns:
        Knit_Script_List: The list expression containing the specified elements.
    """
    return Knit_Script_List(parser_node, exps)


@action
def list_comp(parser_node: LRStackNode, __: list, fill_exp: Expression, variables: list[Variable_Expression], iter_exp: Expression, comp_cond: Expression = None) -> List_Comp:
    """Create a list comprehension expression.

    Args:
        parser_node (LRStackNode): The parser element that created this value.
        __ (list): Unused parameter.
        fill_exp (Expression): Expression that fills the list for each iteration.
        variables (list[Variable_Expression]): Variables to fill from the iterable.
        iter_exp (Expression): The iterable expression to iterate over.
        comp_cond (Expression, optional): Condition expression to evaluate for including a value. Defaults to None.

    Returns:
        List_Comp: List comprehension expression that generates a list from iteration.
    """
    return List_Comp(parser_node, fill_exp, variables, iter_exp, comp_cond)


@action
def indexed_value(parser_node: LRStackNode, __: list, item: Expression, key: Slice_Index | Knit_Script_List, assign: Expression) -> Indexed_Expression:
    """Create an indexed value expression.

    Args:
        parser_node (LRStackNode): The parser element that created this value.
        __ (list): Unused parameter.
        item (Expression): Item expression to index into.
        key (Slice_Index | Knit_Script_List): Key expression to index by.
        assign (Expression): Optional assignment expression for indexed assignment.

    Returns:
        Indexed_Expression: Expression that evaluates indexed access or assignment.
    """
    if isinstance(key, Knit_Script_List):
        key = key.expressions[0]
    return Indexed_Expression(parser_node, item, key, assign)


@action
def slice_index(parser_node: LRStackNode, __: list, start: Expression | None, end: Expression | list[Expression | None]) -> Slice_Index:
    """Create a slice index expression.

    Args:
        parser_node (LRStackNode): The parser element that created this value.
        __ (list): Unused parameter.
        start (Expression | None): Start index expression for the slice.
        end (Expression | list[Expression | None]): End index expression or list of expressions for the slice.

    Returns:
        Slice_Index: Slice index expression for list/string slicing operations.
    """
    spacer = None
    if isinstance(end, list):
        if len(end) > 1:
            spacer = end[1]
        end = end[0]
    return Slice_Index(start, end, spacer, parser_node)


@action
def dict_assign(_parser_node: LRStackNode, __: list, key: Expression, exp: Expression) -> tuple[Expression, Expression]:
    """Collect key value pair for dictionary construction.

    Args:
        _parser_node (LRStackNode): The parser element that created this value.
        __ (list): Unused parameter.
        key (Expression): Key expression for the dictionary entry.
        exp (Expression): Value expression for the dictionary entry.

    Returns:
        tuple[Expression, Expression]: Tuple of key and value expressions.
    """
    return key, exp


@action
def dict_expression(parser_node: LRStackNode, __: list, kwargs: list[tuple[Expression, Expression]]) -> Knit_Script_Dictionary:
    """Create a dictionary expression.

    Args:
        parser_node (LRStackNode): The parser element that created this value.
        __ (list): Unused parameter.
        kwargs (list[tuple[Expression, Expression]]): Key-value pairs for the dictionary.

    Returns:
        Knit_Script_Dictionary: The dictionary expression containing the specified key-value pairs.
    """
    return Knit_Script_Dictionary(parser_node, kwargs)


@action
def dict_comp(parser_node: LRStackNode, __: list,
              key: Expression, value: Expression, variables: list[Variable_Expression], iter_exp: Expression, comp_cond: Expression | None = None) -> Dictionary_Comprehension:
    """Create a dictionary comprehension expression.

    Args:
        parser_node (LRStackNode): The parser element that created this value.
        __ (list): Unused parameter.
        key (Expression): Key expression for each dictionary entry.
        value (Expression): Value expression for each dictionary entry.
        variables (list[Variable_Expression]): Variables to assign from the iterable.
        iter_exp (Expression): The iterable expression to iterate over.
        comp_cond (Expression | None, optional): Conditional expression to filter entries. Defaults to None.

    Returns:
        Dictionary_Comprehension: Dictionary comprehension expression that generates a dictionary from iteration.
    """
    return Dictionary_Comprehension(parser_node, key, value, variables, iter_exp, comp_cond)


@action
def unpack(parser_node: LRStackNode, __: list, exp: Expression) -> Unpack:
    """Create an unpack expression.

    Args:
        parser_node (LRStackNode): The parser element that created this value.
        __ (list): Unused parameter.
        exp (Expression): Expression to unpack into individual elements.

    Returns:
        Unpack: Unpacking expression for spreading iterable elements.
    """
    return Unpack(parser_node, exp)


@action
def code_block(parser_node: LRStackNode, __: list, statements: list[Statement]) -> Code_Block:
    """Create a code block statement.

    Args:
        parser_node (LRStackNode): The parser element that created this value.
        __ (list): Ignored parser nodes.
        statements (list[Statement]): Statements to execute within the code block scope.

    Returns:
        Code_Block: Scoped code block that executes statements in a sub-scope.
    """
    return Code_Block(parser_node, statements)


@action
def elif_statement(_parser_node: LRStackNode, __: list, exp: Expression, stmnt: Statement) -> tuple[Expression, Statement]:
    """Create components of an elif statement.

    Args:
        _parser_node (LRStackNode): The parser element that created this value.
        __ (list): Ignored parser nodes.
        exp (Expression): Condition expression to test for the elif branch.
        stmnt (Statement): Statement to execute when the condition is true.

    Returns:
        tuple[Expression, Statement]: Tuple of condition expression and statement to execute when true.
    """
    return exp, stmnt


@action
def else_statement(_parser_node: LRStackNode, __: list, false_statement: Code_Block) -> Code_Block:
    """Create an else statement.

    Args:
        _parser_node (LRStackNode): The parser element that created this value.
        __ (list): Unused parameter.
        false_statement (Code_Block): Code block to execute when all conditions are false.

    Returns:
        Code_Block: The code block to execute in the else branch.
    """
    return false_statement


@action
def if_statement(parser_node: LRStackNode, __: list, condition: Expression, true_statement: Code_Block, elifs: list[tuple[Expression, Statement]], else_stmt: Code_Block | None) -> If_Statement:
    """Create an if statement with optional elif and else branches.

    Args:
        parser_node (LRStackNode): The parser element that created this value.
        __ (list): Unused parameter.
        condition (Expression): Primary branching condition for the if statement.
        true_statement (Code_Block): Statement to execute when the primary condition is true.
        elifs (list[tuple[Expression, Statement]]): List of elif conditions and their corresponding statements.
        else_stmt (Code_Block | None): Statement to execute when all conditions are false.

    Returns:
        If_Statement: Complete if statement with all conditional branches.
    """
    while len(elifs) > 0:
        elif_tuple = elifs.pop()
        else_stmt = If_Statement(parser_node, elif_tuple[0], elif_tuple[1], else_stmt)
    return If_Statement(parser_node, condition, true_statement, else_stmt)


@action
def while_statement(parser_node: LRStackNode, __: list, condition: Expression, while_block: Code_Block) -> While_Statement:
    """Create a while-statement.

    Args:
        parser_node (LRStackNode): The parser element that created this value.
        __ (list): Unused parameter.
        condition (Expression): Condition expression to evaluate for each iteration.
        while_block (Code_Block): The statement block to execute with each iteration.

    Returns:
        While_Statement: While loop statement for conditional iteration.
    """
    return While_Statement(parser_node, condition, while_block)


@action
def for_each_statement(parser_node: LRStackNode, __: list, variables: list[Variable_Expression], iters: list[Expression], block: Code_Block) -> For_Each_Statement:
    """Create a for each statement.

    Args:
        parser_node (LRStackNode): The parser element that created this value.
        __ (list): Unused parameter.
        variables (list[Variable_Expression]): Variables to assign on each iteration of the iterable.
        iters (list[Expression]): Iterable expressions to iterate over.
        block (Code_Block): Statement block to execute with each iteration.

    Returns:
        For_Each_Statement: For each loop statement for iterating over collections.
    """
    if len(iters) == 1:
        return For_Each_Statement(parser_node, variables, iters[0], block)
    else:
        return For_Each_Statement(parser_node, variables, iters, block)


@action
def as_assignment(parser_node: LRStackNode, __: list, variable: Variable_Expression, exp: Expression) -> Assignment:
    """Create an assignment using 'as' syntax.

    Args:
        parser_node (LRStackNode): The parser element that created this value.
        __ (list): Unused parameter.
        variable (Variable_Expression): Variable to assign the expression result to.
        exp (Expression): Expression to evaluate and assign.

    Returns:
        Assignment: Assignment operation using 'as' syntax.
    """
    if isinstance(variable, Header_ID_Value):
        variable = Variable_Expression(parser_node, variable.hid_str)
    return Assignment(parser_node, var_name=variable.variable_name, value_expression=exp)


@action
def with_statement(parser_node: LRStackNode, __: list, assigns: list[Assignment], block: Code_Block) -> With_Statement:
    """Create a with statement for scoped resource management.

    Args:
        parser_node (LRStackNode): The parser element that created this value.
        __ (list): Unused parameter.
        assigns (list[Assignment]): Assignment operations to perform in the with scope.
        block (Code_Block): Block to execute within the with context.

    Returns:
        With_Statement: With statement for managing scoped resources and assignments.
    """
    return With_Statement(parser_node, block, assigns)


@action
def needle_instruction(_parser_node: LRStackNode, __: list, inst: str) -> Knitout_Instruction_Type:
    """Create a needle instruction type from keyword.

    Args:
        _parser_node (LRStackNode): The parser element that created this value.
        __ (list): Unused parameter.
        inst (str): Instruction keyword string.

    Returns:
        Knitout_Instruction_Type: Needle instruction type for knitting operations.
    """
    return Knitout_Instruction_Type.get_instruction(inst)


@action
def instruction_assignment(parser_node: LRStackNode, __: list, inst: Expression, needles: list[Expression]) -> Needle_Instruction_Exp:
    """Create a needle instruction expression.

    Args:
        parser_node (LRStackNode): The parser element that created this value.
        __ (list): Unused parameter.
        inst (Expression): Instruction expression to apply to needles.
        needles (list[Expression]): Needle expressions to apply the instruction to.

    Returns:
        Needle_Instruction_Exp: Needle instruction expression for applying operations to needles.
    """
    return Needle_Instruction_Exp(parser_node, inst, needles)


@action
def carriage_pass(parser_node: LRStackNode, __: list, pass_dir: Expression, instructions: list[Needle_Instruction_Exp]) -> In_Direction_Statement:
    """Create a carriage pass statement.

    Args:
        parser_node (LRStackNode): The parser element that created this value.
        __ (list): Unused parameter.
        pass_dir (Expression): Direction expression for the carriage pass.
        instructions (list[Needle_Instruction_Exp]): List of needle instructions to apply during the pass.

    Returns:
        In_Direction_Statement: Carriage pass statement that executes instructions in a specific direction.
    """
    return In_Direction_Statement(parser_node, pass_dir, instructions)


@action
def needle_id(parser_node: LRStackNode, needle_node: str) -> Needle_Expression:
    """Create a needle expression from identifier.

    Args:
        parser_node (LRStackNode): The parser element that created this value.
        needle_node (str): String representing the needle identifier.

    Returns:
        Needle_Expression: Needle expression for referencing specific needles.
    """
    return Needle_Expression(parser_node, needle_node)


@action
def sheet_id(parser_node: LRStackNode, sheet_node: str) -> Sheet_Expression:
    """Create a sheet expression from identifier.

    Args:
        parser_node (LRStackNode): The parser element that created this value.
        sheet_node (str): String representing the sheet identifier.

    Returns:
        Sheet_Expression: Sheet expression for referencing specific sheets.
    """
    return Sheet_Expression(parser_node, sheet_node)


@action
def carrier(parser_node: LRStackNode, carrier_node: str) -> Carrier_Expression:
    """Create a carrier expression from identifier.

    Args:
        parser_node (LRStackNode): The parser element that created this value.
        carrier_node (str): String describing the carrier identifier.

    Returns:
        Carrier_Expression: Carrier expression for referencing yarn carriers.
    """
    return Carrier_Expression(parser_node, carrier_node)


@action
def return_statement(parser_node: LRStackNode, __: list, exp: Expression) -> Return_Statement:
    """Create a return statement.

    Args:
        parser_node (LRStackNode): The parser element that created this value.
        __ (list): Unused parameter.
        exp (Expression): Expression to return as the function result.

    Returns:
        Return_Statement: Return statement for exiting functions with a value.
    """
    return Return_Statement(parser_node, exp)


@action
def param_list(_parser_node: LRStackNode, __: list, args: list[Variable_Expression] | None = None, kwargs: list[Assignment] | None = None) -> tuple[list[Variable_Expression], list[Assignment]]:
    """Create a parameter list for function definitions.

    Args:
        _parser_node (LRStackNode): The parser element that created this value.
        __ (list): Unused parameter.
        args (list[Variable_Expression] | None, optional): List of positional parameter identifiers. Defaults to None.
        kwargs (list[Assignment] | None, optional): List of keyword parameter assignments with default values. Defaults to None.

    Returns:
        tuple[list[Variable_Expression], list[Assignment]]: Tuple of positional parameters and keyword parameter assignments.
    """
    if args is None:
        args = []
    if kwargs is None:
        kwargs = []
    return args, kwargs


@action
def function_declaration(parser_node: LRStackNode, __: list,
                         func_name: Variable_Expression, params: tuple[list[Variable_Expression], list[Assignment]] | None, block: Statement) -> Function_Declaration:
    """Create a function declaration.

    Args:
        parser_node (LRStackNode): The parser element that created this value.
        __ (list): Unused parameter.
        func_name (Variable_Expression): Name of the function being declared.
        params (tuple[list[Variable_Expression], list[Assignment]] | None): Parameter list as tuple of positional and keyword parameters.
        block (Statement): Function body statement to execute when called.

    Returns:
        Function_Declaration: The function declaration that defines a callable function.
    """
    if params is None:
        params = [], []
    args = params[0]
    kwargs = params[1]
    return Function_Declaration(parser_node, func_name.variable_name, args, kwargs, block)


@action
def expression(parser_node: LRStackNode, nodes: list[str | KS_Element | Expression]) -> Expression:
    """Create an expression from parser nodes.

    Args:
        parser_node (LRStackNode): The parser element that created this value.
        nodes (list[str | KS_Element | Expression]): Parser nodes to combine into an expression.

    Returns:
        Expression: Combined expression based on the parser nodes and operators.
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
    """Create a negation expression.

    Args:
        parser_node (LRStackNode): The parser element that created this value.
        __ (list): Unused parameter.
        exp (Expression): Expression to negate.

    Returns:
        Not_Expression: Negation expression that inverts the boolean value.
    """
    return Not_Expression(parser_node, exp)


@action
def xfer_rack(parser_node: LRStackNode, __: list, is_across: str | None = None, dist_exp: Expression | None = None, side_id: Expression | None = None) -> Xfer_Pass_Racking:
    """Create a transfer racking specification.

    Args:
        parser_node (LRStackNode): The parser element that created this value.
        __ (list): Unused parameter.
        is_across (str | None, optional): Indicator if transfer is directly across beds. Defaults to None.
        dist_exp (Expression | None, optional): The needle offset expression for transfer. Defaults to None.
        side_id (Expression | None, optional): Offset direction expression. Defaults to None.

    Returns:
        Xfer_Pass_Racking: Transfer pass racking specification for needle transfers.
    """
    if is_across is not None:
        return Xfer_Pass_Racking(parser_node, distance_expression=None, direction_expression=None)
    return Xfer_Pass_Racking(parser_node, distance_expression=dist_exp, direction_expression=side_id)


@action
def xfer_pass(parser_node: LRStackNode, __: list, needles: list[Expression], rack_val: Xfer_Pass_Racking, bed: Expression | None = None, slider: str | None = None) -> Xfer_Pass_Statement:
    """Create a transfer pass statement.

    Args:
        parser_node (LRStackNode): The parser element that created this value.
        __ (list): Unused parameter.
        needles (list[Expression]): Needle expressions to start transfer from.
        rack_val (Xfer_Pass_Racking): Racking specification for the transfers.
        bed (Expression | None, optional): Target bed expression for transfers. Defaults to None.
        slider (str | None, optional): Indicator if transferring to slider needles. Defaults to None.

    Returns:
        Xfer_Pass_Statement: Transfer pass statement for moving loops between needles.
    """
    return Xfer_Pass_Statement(parser_node, rack_val, needles, bed, slider is not None)


@action
def accessor(parser_node: LRStackNode, __: list, exp: Expression, attribute: Expression) -> Attribute_Accessor_Expression:
    """Create an attribute accessor expression.

    Args:
        parser_node (LRStackNode): The parser element that created this value.
        __ (list): Unused parameter.
        exp (Expression): Expression to access attributes from.
        attribute (Expression): Attribute expression to access.

    Returns:
        Attribute_Accessor_Expression: Accessor expression for getting object attributes.
    """
    return Attribute_Accessor_Expression(parser_node, exp, attribute)


@action
def exp_statement(parser_node: LRStackNode, __: list, exp: Expression) -> Expression_Statement:
    """Create an expression statement.

    Args:
        parser_node (LRStackNode): The parser element that created this value.
        __ (list): Unused parameter.
        exp (Expression): Expression to execute as a statement.

    Returns:
        Expression_Statement: Statement that executes an expression for its side effects.
    """
    return Expression_Statement(parser_node, exp)


@action
def cut_statement(parser_node: LRStackNode, __: list, exps: list[Expression]) -> Cut_Statement:
    """Create a cut statement for yarn carriers.

    Args:
        parser_node (LRStackNode): The parser element that created this value.
        __ (list): Unused parameter.
        exps (list[Expression]): Carrier expressions to cut.

    Returns:
        Cut_Statement: Cut statement for severing yarn carriers.
    """
    return Cut_Statement(parser_node, exps)


@action
def release_statement(parser_node: LRStackNode, __: list) -> Release_Statement:
    """Create a release statement for the current carrier.

    Args:
        parser_node (LRStackNode): The parser element that created this value.
        __ (list): Unused parameter.

    Returns:
        Release_Statement: Release statement for releasing the current active carrier.
    """
    return Release_Statement(parser_node)


@action
def remove_statement(parser_node: LRStackNode, __: list, exps: list[Expression]) -> Remove_Statement:
    """Create a remove statement for yarn carriers.

    Args:
        parser_node (LRStackNode): The parser element that created this value.
        __ (list): Unused parameter.
        exps (list[Expression]): Carrier expressions to remove/out.

    Returns:
        Remove_Statement: Remove statement for moving carriers out of working area.
    """
    return Remove_Statement(parser_node, exps)


@action
def gauge_exp(parser_node: LRStackNode, __: list, sheet_exp: Expression, gauge: Expression) -> Gauge_Expression:
    """Create a gauge expression.

    Args:
        parser_node (LRStackNode): The parser element that created this value.
        __ (list): Unused parameter.
        sheet_exp (Expression): Sheet expression for the gauge.
        gauge (Expression): Gauge value expression.

    Returns:
        Gauge_Expression: Gauge expression for sheet configuration.
    """
    return Gauge_Expression(parser_node, sheet_exp, gauge)


@action
def drop_pass(parser_node: LRStackNode, __: list, needles: list[Expression]) -> Drop_Pass:
    """Create a drop pass statement.

    Args:
        parser_node (LRStackNode): The parser element that created this value.
        __ (list): Unused parameter.
        needles (list[Expression]): Needle expressions to drop loops from.

    Returns:
        Drop_Pass: Drop pass statement for releasing loops from needles.
    """
    return Drop_Pass(parser_node, needles)


@action
def push_to(_parser_node: LRStackNode, __: list, push_val: str | list) -> str | Expression:
    """Create a push target specification.

    Args:
        _parser_node (LRStackNode): The parser element that created this value.
        __ (list): Unused parameter.
        push_val (str | list): Front, back, or a specific layer value specification.

    Returns:
        str | Expression: Identifying string or expression for the layer value.
    """
    if isinstance(push_val, list):
        return push_val[1]
    return push_val


@action
def push_dir(_parser_node: LRStackNode, __: list, amount: Expression, direction: str) -> tuple[Expression, str]:
    """Create a push direction specification.

    Args:
        _parser_node (LRStackNode): The parser element that created this value.
        __ (list): Unused parameter.
        amount (Expression): Amount expression to push.
        direction (str): Direction string to push in.

    Returns:
        tuple[Expression, str]: Tuple of push amount and direction.
    """
    return amount, direction


@action
def push_statement(parser_node: LRStackNode, __: list, needles: list[Expression], push_val: str | Expression | tuple[Expression, str]) -> Push_Statement:
    """Create a push statement for layer management.

    Args:
        parser_node (LRStackNode): The parser element that created this value.
        __ (list): Unused parameter.
        needles (list[Expression]): Needle expressions to push layer values for.
        push_val (str | Expression | tuple[Expression, str]): Push value specification.

    Returns:
        Push_Statement: Push statement for managing needle layer positions.
    """
    return Push_Statement(parser_node, needles, push_val)


@action
def swap_statement(parser_node: LRStackNode, __: list, needles: list[Expression], swap_type: str, value: Expression) -> Swap_Statement:
    """Create a swap statement for layer management.

    Args:
        parser_node (LRStackNode): The parser element that created this value.
        __ (list): Unused parameter.
        needles (list[Expression]): The needle expressions to perform swaps with.
        swap_type (str): Type of value to swap with.
        value (Expression): The value expression to swap with.

    Returns:
        Swap_Statement: Swap statement for exchanging layer positions.
    """
    return Swap_Statement(parser_node, needles, swap_type, value)


@action
def pass_second(_parser_node: LRStackNode, nodes: list[Any]) -> Any:
    """Return the second node in a list.

    Args:
        _parser_node (LRStackNode): The parser element that created this value.
        nodes (list[Any]): Parser nodes.

    Returns:
        Any: The second node in the list.
    """
    return nodes[1]


@action
def import_statement(parser_node: LRStackNode, __: list, src: Expression, alias: Expression | None) -> Import_Statement:
    """Create an import statement.

    Args:
        parser_node (LRStackNode): The parser element that created this value.
        __ (list): Unused parameter.
        src (Expression): Source module expression to import.
        alias (Expression | None): Alias expression to assign in variable scope.

    Returns:
        Import_Statement: Import statement for loading external modules.
    """
    return Import_Statement(parser_node, src, alias)
