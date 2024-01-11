"""Actions for converting parglare elements into useful code"""
import os
from typing import Union, Optional

from parglare import get_collector

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
from knit_script.knit_script_interpreter.expressions.values import Boolean_Value, Bed_Value, Float_Value, Int_Value, String_Value, None_Value, Machine_Position_Value, \
    Machine_Type_Value, Header_ID_Value
from knit_script.knit_script_interpreter.expressions.variables import Variable_Expression
from knit_script.knit_script_interpreter.expressions.xfer_pass_racking import Xfer_Pass_Racking
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
# some boiler plate parglare code
from knit_script.knit_script_interpreter.statements.xfer_pass_statement import Xfer_Pass_Statement
from knit_script.knitout_interpreter.knitout_structures.knitout_instructions.instruction import Instruction_Type
from knit_script.knitting_machine.machine_components.machine_position import Machine_Bed_Position, Machine_Position
from knit_script.knitting_machine.machine_specification.Machine_Type import Machine_Type

action = get_collector()


@action
def program(_, __, statements: list[Statement]) ->  list[Statement]:
    """
    :param _: The parser element that created this value
    :param __:
    :param statements: the list of statements to execute
    :return: statements
    """
    return statements


def _in_enum(item, enumeration) -> bool:
    """
    :param enumeration: The enumeration class
    :param item: item to compare against Enum
    :return:
    """
    if isinstance(item, str):
        return (item in [i.value for i in enumeration]) or (item in [i.name for i in enumeration])
    try:
        return item in enumeration
    except KeyError as _:
        return False


# basic expressions and statements
@action
def identifier(parser_node, node: str) -> Expression:
    """
    :param parser_node: The parser element that created this value ignored parglare context
    :param node: the string recognized as an identifier
    :return: variable expression or withheld keyword
    """
    if node == "None":
        return None_Value(parser_node)
    elif node == "True" or node == "False":
        return Boolean_Value(parser_node, node)
    elif _in_enum(node, Machine_Bed_Position):
        return Bed_Value(parser_node, node)
    elif _in_enum(node, Machine_Position):
        return Machine_Position_Value(parser_node, node)
    elif _in_enum(node, Machine_Type):
        return Machine_Type_Value(parser_node, node)
    # elif _in_enum(node, Header_ID):
    #     return Header_ID_Value(parser_node, node)
    elif node == "machine":
        return Machine_Accessor(parser_node)
    elif _in_enum(node, Needle_Sets):
        return Needle_Set_Expression(parser_node, node)
    else:
        return Variable_Expression(parser_node, node)


@action
def declare_variable(parser_node, __, assign: Assignment) -> Variable_Declaration:
    """
    :param assign: assignment before eol punctuation
    :param parser_node: The parser element that created this value ignored parglare context
    :param __: ignored nodes
    :return: Variable Declaration Statement that assigns the variable on execution
    """
    return Variable_Declaration(parser_node, assign)


@action
def declare_global(parser_node, __, assign: Assignment) -> Variable_Declaration:
    """
    :param assign: assignment before eol punctuation
    :param parser_node: The parser element that created this value ignored parglare context
    :param __: ignored nodes
    :return: Variable Declaration Statement that assigns the global variable on execution
    """
    return Variable_Declaration(parser_node, assign, is_global=True)


@action
def assertion(parser_node, __, exp: Expression, error: Optional[Expression] = None) -> Assertion:
    """
    :param __: ignored nodes
    :param error: error to report
    :param parser_node: The parser element that created this value ignored parglare context
    :param exp: expression to evaluate assertion by
    :return: Assertion Statement
    """
    return Assertion(parser_node, exp, error)


@action
def print_statement(parser_node, __, exp: Expression) -> Print:
    """
    :param parser_node: The parser element that created this value ignored parglare context.
    :param __: Ignored nodes.
    :param exp: Expression to print.
    :return: Print Statement
    """
    return Print(parser_node, exp)


@action
def try_catch(parser_node, __, try_block: Statement, catch_block: Statement, errors: list[Expression]) -> Try_Catch_Statement:
    """
    :param errors: errors to accept
    :param parser_node: The parser element that created this value ignored parglare context.
    :param __: ignored nodes.
    :param try_block: statements to execute in try branch
    :param catch_block: statements to execute in catch branch
    :return: Try Catch
    """
    return Try_Catch_Statement(parser_node, try_block, catch_block, errors=errors)


@action
def exception_assignment(parser_node, __, except_val: Expression, var_name: Variable_Expression) -> Assignment:
    """
    Reversed assignment syntax for catch statements
    :param parser_node: The parser element that created this value
    :param __:
    :param except_val: the exception to allow
    :param var_name: the name of the variable for the error
    :return: an assignment operation for this error
    """
    return Assignment(parser_node, var_name.variable_name, except_val)


@action
def pause_statement(parser_node, __) -> Pause_Statement:
    """
    :param parser_node: The parser element that created this value ignored parglare context
    :param __: ignored nodes
    :return: Pause statement
    """
    return Pause_Statement(parser_node)


@action
def assignment(parser_node, __, var_name: Variable_Expression, exp: Expression):
    """
    :param parser_node: The parser element that created this value ignored parglare context
    :param __: ignored nodes
    :param var_name: processed identifier to variable name
    :param exp: expression to assign variable value
    :return: assignment expression which evaluates to expression value
    """
    # todo: ensure that typing is checking identifier not over shadowing keywords
    return Assignment(parser_node, var_name.variable_name, exp)


# NUMBERS #

@action
def float_exp(parser_node, node: str) -> Float_Value:
    """
    :param parser_node: The parser element that created this value ignored parglare context
    :param node: the number string
    :return: the positive number specified
    """
    return Float_Value(parser_node, node)


@action
def int_exp(parser_node, node: str) -> Int_Value:
    """
    :param parser_node: The parser element that created this value ignored parglare context
    :param node: the number string
    :return: the positive number specified
    """
    return Int_Value(parser_node, node)


@action
def direction_exp(parser_node, nodes: list) -> Pass_Direction_Expression:
    """
    
    :param parser_node: The parser element that created this value 
    :param nodes: single node list with direction keyword
    :return: pass direction
    """
    return Pass_Direction_Expression(parser_node, nodes[0])


@action
def string(parser_node, node: str) -> String_Value:
    """
    :param parser_node: The parser element that created this value ignored parglare context
    :param node: string value
    :return: Expression storing quote
    """
    no_quotes = node.strip("\"")
    return String_Value(parser_node, no_quotes)


@action
def f_string_section(parser_node, __, exp: Optional[Expression] = None, string_value: Optional[str] = None) -> Expression:
    """
    :param __:
    :param exp: expression in formatting
    :param string_value: string in formatting
    :param parser_node: The parser element that created this value ignored parglare context
    :return: Expression of string value of a section of a formatted string
    """
    if exp is not None:
        return exp
    else:
        string_value = string_value.replace("\\n", os.linesep)
        return String_Value(parser_node, string_value)


@action
def formatted_string(parser_node, __, sections: list[Expression]) -> Formatted_String_Value:
    """
    :param __:
    :param sections: f string sections parsed as expressions
    :param parser_node: The parser element that created this value ignored parglare context
    :return: Formatted string expression
    """
    return Formatted_String_Value(parser_node, sections)


@action
def call_list(_, __, params: Optional[list[Expression]] = None,
              kwargs: Optional[list[Assignment]] = None) -> tuple[list[Expression], list[Assignment]]:
    """
    :param _: The parser element that created this value
    :param __:
    :param params: the parameters in the call list
    :param kwargs: the keyword set parameters in the call list
    :return: parameters and kwargs
    """
    if params is None:
        params = []
    if kwargs is None:
        kwargs = []
    return params, kwargs


@action
def function_call(parser_node, __, func_name: Variable_Expression,
                  args: tuple[list[Expression], list[Assignment]]) -> Function_Call:
    """
    :param parser_node: The parser element that created this value
    :param __:
    :param func_name: name of the function being called
    :param args: the arguments passed to the function
    :return: the function call
    """
    if args is None:
        params = []
        kwargs = []
    else:
        params = args[0]
        kwargs = args[1]
    return Function_Call(parser_node, func_name, params, kwargs)


@action
def list_expression(parser_node, __, exps: list[Expression]) -> Knit_Script_List:
    """
    :param parser_node: The parser element that created this value
    :param __:
    :param exps: Expressions in the list.
    :return: The list expression
    """
    return Knit_Script_List(parser_node, exps)


@action
def list_comp(parser_node, __, fill_exp: Expression, variables: list[Variable_Expression], iter_exp: Expression, comp_cond: Expression = None) -> List_Comp:
    """
    :param parser_node: The parser element that created this value
    :param __:
    :param fill_exp: Expression that fills the list
    :param variables: Variables to fill from iterable
    :param iter_exp: the iterable to pass over
    :param comp_cond: condition to evaluate for adding a value
    :return: List comprehension
    """
    return List_Comp(parser_node, fill_exp, variables, iter_exp, comp_cond)


@action
def indexed_value(parser_node, __, item: Expression, key: Slice_Index | Knit_Script_List, assign: Expression) -> Indexed_Expression:
    """
    :param parser_node:
    :param __:
    :param item: item to index
    :param key: key to index by
    :param assign: optional assignment
    :return: expression that evaluations assignment
    """
    if isinstance(key, Knit_Script_List):
        key = key.expressions[0]
    return Indexed_Expression(parser_node, item, key, assign)


@action
def slice_index(parser_node, __, start: Expression | None, end: Expression | list[Expression | None]) -> Slice_Index:
    """
    :param parser_node:
    :param __:
    :param start:
    :param end:
    :return:
    """
    spacer = None
    if isinstance(end, list):
        if len(end) > 1:
            spacer = end[1]
        end = end[0]
    return Slice_Index(start, end, spacer, parser_node)


@action
def dict_assign(_, __, key: Expression, exp: Expression) -> tuple[Expression, Expression]:
    """
    collect key value pair
    :param _: The parser element that created this value
    :param __:
    :param key: key expression
    :param exp: value expression
    :return: key, value
    """
    return key, exp


@action
def dict_expression(parser_node, __, kwargs: list[tuple[Expression, Expression]]):
    """
    :param parser_node: The parser element that created this value
    :param __:
    :param kwargs: key value pairs
    :return: The dictionary
    """
    return Knit_Script_Dictionary(parser_node, kwargs)


@action
def dict_comp(parser_node, __, key: Expression, value: Expression,
              variables: list[Variable_Expression], iter_exp: Expression, comp_cond: Optional[Expression] = None) -> Dictionary_Comprehension:
    """
    :param comp_cond: conditional on variables to skip specific designs
    :param parser_node: The parser element that created this value
    :param __:
    :param key: key expression
    :param value: value expression
    :param variables: variables to parse from iterable
    :param iter_exp: the iterable to parse over
    :return: Dictionary comprehension
    """
    return Dictionary_Comprehension(parser_node, key, value, variables, iter_exp, comp_cond)


@action
def unpack(parser_node, __, exp: Expression) -> Unpack:
    """
    :param parser_node: The parser element that created this value
    :param __:
    :param exp: Expression to unpack.
    :return: Unpacking expression
    """
    return Unpack(parser_node, exp)


@action
def code_block(parser_node, __, statements: list[Statement]) -> Code_Block:
    """
    :param parser_node: The parser element that created this value ignored parglare context
    :param __: ignored nodes.
    :param statements: Statements to execute in sub scope
    :return: scoping block
    """
    return Code_Block(parser_node, statements)


@action
def elif_statement(_, __, exp: Expression, stmnt: Statement) -> tuple[Expression, Statement]:
    """
    components of an elif statement
    :param _: The parser element that created this value ignored parglare context
    :param __: ignored nodes.
    :param exp: expression to test on elif.
    :param stmnt: statement to execute on true result
    :return: expression and statement to execute when true
    """
    return exp, stmnt


@action
def else_statement(_, __, false_statement: Code_Block) -> Code_Block:
    """
    :param _: The parser element that created this value
    :param __:
    :param false_statement: code block to execute when false
    :return: the code to execute when false
    """
    return false_statement


@action
def if_statement(parser_node, __,
                 condition: Expression, true_statement: Code_Block,
                 elifs: list[tuple[Expression, Statement]],
                 else_stmt: Optional[Code_Block]) -> If_Statement:
    """

    :param elifs: list of else-if conditions and statements
    :param parser_node: The parser element that created this value
    :param __:
    :param condition: branching condition
    :param true_statement: statement to execute on true.
    :param else_stmt: statement to execute on false
    :return: if statement
    """
    while len(elifs) > 0:
        elif_tuple = elifs.pop()
        else_stmt = If_Statement(parser_node, elif_tuple[0], elif_tuple[1], else_stmt)
    return If_Statement(parser_node, condition, true_statement, else_stmt)


@action
def while_statement(parser_node, __, condition: Expression, while_block: Code_Block) -> While_Statement:
    """

    :param parser_node: The parser element that created this value
    :param __:
    :param condition: condition to evaluate on while
    :param while_block: the statement to execute with each iteration
    :return:
    """
    return While_Statement(parser_node, condition, while_block)


@action
def for_each_statement(parser_node, __, variables: list[Variable_Expression], iters: list[Expression], block: Code_Block) -> For_Each_Statement:
    """
    :param parser_node: The parser element that created this value
    :param __:
    :param variables: To assign on each iteration of iterable.
    :param iters: Iterable to iterate over.
    :param block: Statement to execute with each iteration
    :return: For each statement
    """
    if len(iters) == 1:
        return For_Each_Statement(parser_node, variables, iters[0], block)
    else:
        return For_Each_Statement(parser_node, variables, iters, block)


@action
def as_assignment(parser_node, __, variable: Variable_Expression, exp: Expression) -> Assignment:
    """
    :param parser_node: The parser element that created this value
    :param __:
    :param variable: variable to assign to
    :param exp: expression to assign
    :return: Assignment value
    """
    if isinstance(variable, Header_ID_Value):
        variable = Variable_Expression(parser_node, variable.hid_str)
    return Assignment(parser_node, var_name=variable.variable_name, value_expression=exp)


@action
def with_statement(parser_node, __, assigns: list[Assignment], block: Code_Block) -> With_Statement:
    """
    :param parser_node: The parser element that created this value
    :param __:
    :param assigns: Assignments for block.
    :param block: Block to execute.
    :return: With statement
    """
    return With_Statement(parser_node, block, assigns)


@action
def needle_instruction(_, __, inst: str) -> Instruction_Type:
    """
    :param _: The parser element that created this value
    :param __:
    :param inst: instruction keyword
    :return: needle instruction
    """
    return Instruction_Type.get_instruction(inst)


@action
def instruction_assignment(parser_node, __, inst: Expression, needles: list[Expression]) -> Needle_Instruction_Exp:
    """
    :param parser_node: The parser element that created this value
    :param __:
    :param inst: Instruction to apply to needles.
    :param needles: Needles to apply instruction to
    :return: Needle instruction expression
    """
    return Needle_Instruction_Exp(parser_node, inst, needles)


@action
def carriage_pass(parser_node, __, pass_dir: Expression, instructions: list[Needle_Instruction_Exp]) -> In_Direction_Statement:
    """
    :param parser_node: The parser element that created this value
    :param __:
    :param pass_dir: direction to apply instructions in
    :param instructions: instructions to apply
    :return: in direction statement.
    """
    return In_Direction_Statement(parser_node, pass_dir, instructions)


@action
def needle_id(parser_node, needle_node: str) -> Needle_Expression:
    """
    :param parser_node: The parser element that created this value
    :param needle_node: node representing needle.
    :return: Needle expression
    """
    return Needle_Expression(parser_node, needle_node)


@action
def sheet_id(parser_node, sheet_node: str) -> Sheet_Expression:
    """
    :param parser_node: The parser element that created this value
    :param sheet_node: string representing sheet
    :return: sheet expression
    """
    return Sheet_Expression(parser_node, sheet_node)


@action
def carrier(parser_node, carrier_node: str) -> Carrier_Expression:
    """
    :param parser_node: The parser element that created this value
    :param carrier_node: string describing carrier
    :return: carrier expression
    """
    return Carrier_Expression(parser_node, carrier_node)


@action
def return_statement(parser_node, __, exp: Expression) -> Return_Statement:
    """
    :param parser_node: The parser element that created this value
    :param __:
    :param exp: expression to return
    :return: return statement
    """
    return Return_Statement(parser_node, exp)


@action
def param_list(_, __, args: Optional[list[Variable_Expression]] = None,
               kwargs: Optional[list[Assignment]] = None) -> tuple[list[Variable_Expression], list[Assignment]]:
    """
    :param _: The parser element that created this value
    :param __:
    :param args: List of argument identifiers.
    :param kwargs: List of keyword assignments
    :return: arguments and keyword assignments
    """
    if args is None:
        args = []
    if kwargs is None:
        kwargs = []
    return args, kwargs


@action
def function_declaration(parser_node, __, func_name: Variable_Expression,
                         params: Optional[tuple[list[Variable_Expression], list[Assignment]]],
                         block: Statement) -> Function_Declaration:
    """
    :param parser_node: The parser element that created this value
    :param __:
    :param func_name: Name of the function.
    :param params: List of variables for arguments, list of key word assignments
    :param block: body to execute
    :return: the function declaration
    """
    if params is None:
        params = [], []
    args = params[0]
    kwargs = params[1]
    return Function_Declaration(parser_node, func_name.variable_name, args, kwargs, block)


@action
def expression(parser_node, nodes: list) -> Expression:
    """
    :param parser_node: The parser element that created this value ignored parglare context
    :param nodes: nodes to parse into expression.
    :return: Expression
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
def negation(parser_node, __, exp: Expression) -> Not_Expression:
    """
    :param parser_node: The parser element that created this value
    :param __:
    :param exp: expression to negate
    :return: not expression
    """
    return Not_Expression(parser_node, exp)


@action
def xfer_rack(parser_node, __, is_across: Optional[str] = None,
              dist_exp: Optional[Expression] = None, side_id: Optional[Expression] = None) -> Xfer_Pass_Racking:
    """
    :param parser_node: The parser element that created this value
    :param __:
    :param is_across: True, if xfer is directly across beds.
    :param dist_exp: The needle offset for xfer.
    :param side_id: Offset direction.
    :return: Xfer pass racking
    """
    return Xfer_Pass_Racking(parser_node, is_across is not None, dist_exp, side_id)


@action
def xfer_pass(parser_node, __, needles: list[Expression],
              rack_val: Xfer_Pass_Racking,
              bed: Optional[Expression] = None,
              slider: Optional[str] = None) -> Xfer_Pass_Statement:
    """

    :param parser_node: The parser element that created this value
    :param __:
    :param rack_val: Racking for xfers
    :param needles: needles to start xfer from
    :param bed: beds to land on. Exclude needles already on bed
    :param slider: True if transferring to sliders
    :return: xfer pass statement
    """
    return Xfer_Pass_Statement(parser_node, rack_val, needles, bed, slider is not None)


@action
def accessor(parser_node, __, exp: Expression, attribute: Expression) -> Attribute_Accessor_Expression:
    """
    :param parser_node: The parser element that created this value
    :param __:
    :param exp: expression to get from
    :param attribute: attribute to collect
    :return: accessor
    """
    return Attribute_Accessor_Expression(parser_node, exp, attribute)


@action
def exp_statement(parser_node, __, exp: Expression) -> Expression_Statement:
    """
    :param parser_node: The parser element that created this value
    :param __:
    :param exp: expression to execute
    :return: execution of expression
    """
    return Expression_Statement(parser_node, exp)


@action
def cut_statement(parser_node, __, exps: list[Expression]) -> Cut_Statement:
    """
    :param parser_node: The parser element that created this value
    :param __:
    :param exps: carriers to cut
    :return: cut statement
    """
    return Cut_Statement(parser_node, exps)

@action
def release_statement(parser_node, __) -> Release_Statement:
    """
    :param parser_node: The parser element that created this value
    :param __:
    :return: Release statement for current carrier
    """
    return Release_Statement(parser_node)


@action
def remove_statement(parser_node, __, exps: list[Expression]) -> Remove_Statement:
    """
    :param parser_node: The parser element that created this value
    :param __:
    :param exps: carriers to out
    :return: remove statement
    """
    return Remove_Statement(parser_node, exps)


@action
def gauge_exp(parser_node, __, sheet_exp: Expression, gauge: Expression) -> Gauge_Expression:
    """

    :param parser_node: The parser element that created this value
    :param __:
    :param sheet_exp: sheet value
    :param gauge: gauge value
    :return: Gauge expression
    """
    return Gauge_Expression(parser_node, sheet_exp, gauge)


@action
def drop_pass(parser_node, __, needles: list[Expression]) -> Drop_Pass:
    """
    :param parser_node: The parser element that created this value
    :param __:
    :param needles: needles to drop from
    :return: drop pass
    """
    return Drop_Pass(parser_node, needles)


@action
def push_to(_, __, push_val: Union[str, list]) -> Union[str, Expression]:
    """
    :param _: The parser element that created this value
    :param __:
    :param push_val: front, back, or a specific layer value
    :return: identifying string or expression layer value
    """
    if isinstance(push_val, list):
        return push_val[1]
    return push_val


@action
def push_dir(_, __, amount: Expression, direction: str) -> tuple[Expression, str]:
    """
    :param _: The parser element that created this value
    :param __:
    :param amount: Value to push.
    :param direction: Direction to push
    :return: amount, direction
    """
    return amount, direction


@action
def push_statement(parser_node, __, needles: list[Expression], push_val: Union[str, Expression, tuple[Expression, str]]) -> Push_Statement:
    """

    :param parser_node: The parser element that created this value
    :param __:
    :param needles: Needles to push layer value
    :param push_val: specification of push value.
    :return: Push statement
    """
    return Push_Statement(parser_node, needles, push_val)


@action
def swap_statement(parser_node, __, needles: list[Expression], swap_type: str, value: Expression) -> Swap_Statement:
    """
    :param parser_node: The parser element that created this value
    :param __:
    :param needles: The needles to do this swap with.
    :param swap_type: Type of value to swap with
    :param value: the value to swap with
    :return: swap statement
    """
    return Swap_Statement(parser_node, needles, swap_type, value)


@action
def pass_second(_, nodes: list):
    """
    :param _: The parser element that created this value
    :param nodes: nodes parsed
    :return: the second node in the list
    """
    return nodes[1]


@action
def import_statement(parser_node, __, src: Expression, alias: Optional[Expression]) -> Import_Statement:
    """

    :param parser_node: The parser element that created this value
    :param __:
    :param src: source module
    :param alias: alias to assign in variable scope
    :return:
    """
    return Import_Statement(parser_node, src, alias)
