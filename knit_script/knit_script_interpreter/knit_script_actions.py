"""Actions for converting parglare elements into useful code"""
from typing import List, Tuple, Union, Optional

from parglare import get_collector

from knit_script.knit_script_interpreter.expressions.Gauge_Expression import Gauge_Expression
from knit_script.knit_script_interpreter.expressions.accessors import Attribute_Accessor_Expression
from knit_script.knit_script_interpreter.expressions.carrier import Carrier_Expression
from knit_script.knit_script_interpreter.expressions.direction import Pass_Direction_Expression
from knit_script.knit_script_interpreter.expressions.expressions import Expression
from knit_script.knit_script_interpreter.expressions.formatted_string import Formatted_String_Value
from knit_script.knit_script_interpreter.expressions.function_expressions import Function_Call
from knit_script.knit_script_interpreter.expressions.instruction_expression import Needle_Instruction_Exp, Needle_Instruction
from knit_script.knit_script_interpreter.expressions.list_expression import Knit_Script_List, Knit_Script_Dictionary, List_Comp, Dictionary_Comprehension, Unpack, Sliced_List
from knit_script.knit_script_interpreter.expressions.machine_accessor import Machine_Accessor, Sheet_Expression
from knit_script.knit_script_interpreter.expressions.needle_expression import Needle_Expression
from knit_script.knit_script_interpreter.expressions.needle_set_expression import Needle_Sets, Needle_Set_Expression
from knit_script.knit_script_interpreter.expressions.not_expression import Not_Expression
from knit_script.knit_script_interpreter.expressions.operator_expressions import Operator_Expression
from knit_script.knit_script_interpreter.expressions.values import Boolean_Value, Bed_Value, Float_Value, Int_Value, String_Value, None_Value, Machine_Position_Value, \
    Machine_Type_Value, Header_ID_Value
from knit_script.knit_script_interpreter.expressions.variables import Variable_Expression
from knit_script.knit_script_interpreter.expressions.xfer_pass_racking import Xfer_Pass_Racking
from knit_script.knit_script_interpreter.header_structure import Header_ID, Machine_Type
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
from knit_script.knit_script_interpreter.statements.carrier_statements import Cut_Statement, Remove_Statement
from knit_script.knit_script_interpreter.statements.code_block_statements import Code_Block
from knit_script.knit_script_interpreter.statements.control_loop_statements import While_Statement, For_Each_Statement
from knit_script.knit_script_interpreter.statements.function_dec_statement import Function_Declaration
from knit_script.knit_script_interpreter.statements.header_statement import Header_Statement
from knit_script.knit_script_interpreter.statements.in_direction_statement import In_Direction_Statement
from knit_script.knit_script_interpreter.statements.instruction_statements import Pause_Statement
from knit_script.knit_script_interpreter.statements.return_statement import Return_Statement
from knit_script.knit_script_interpreter.statements.try_catch_statements import Try_Catch_Statement
# some boiler plate parglare code
from knit_script.knit_script_interpreter.statements.xfer_pass_statement import Xfer_Pass_Statement
from knit_script.knitting_machine.machine_components.machine_position import Machine_Bed_Position, Machine_Position

action = get_collector()


@action
def program(_, __, head: List[Header_Statement], statements: List[Statement]):
    """
    :param _:
    :param __:
    :param head: list of header values to set the machine state
    :param statements: the list of statements to execute
    :return: header, statements
    """
    return head, statements


@action
def header(_, __, type_id: Header_ID_Value, value: Expression):
    """
    :param _:
    :param __:
    :param type_id: Value of header to update
    :param value: the value to update to
    :return: Statement for updating header
    """
    return Header_Statement(type_id, value)


def _in_enum(item, enumeration) -> bool:
    """
    :param enumeration: The enumeration class
    :param item: item to compare against Enum
    :return:
    """
    try:
        return item in enumeration
    except (KeyError, TypeError) as _:
        if isinstance(item, str):
            return (item in [i.value for i in enumeration]) or (item in [i.name for i in enumeration])
    return False


# basic expressions and statements
@action
def identifier(_, node: str) -> Expression:
    """
    :param _: ignored parglare context
    :param node: the string recognized as an identifier
    :return: variable expression or withheld keyword
    """
    if node == "None":
        return None_Value()
    elif node == "True" or node == "False":
        return Boolean_Value(node)
    elif _in_enum(node, Machine_Bed_Position):
        return Bed_Value(node)
    elif _in_enum(node, Machine_Position):
        return Machine_Position_Value(node)
    elif _in_enum(node, Machine_Type):
        return Machine_Type_Value(node)
    elif _in_enum(node, Header_ID):
        return Header_ID_Value(node)
    elif node == "machine":
        return Machine_Accessor()
    elif _in_enum(node, Needle_Sets):
        return Needle_Set_Expression(node)
    else:
        return Variable_Expression(node)


@action
def declare_variable(_, __, assign: Assignment) -> Variable_Declaration:
    """
    :param assign: assignment before eol punctuation
    :param _: ignored parglare context
    :param __: ignored nodes
    :return: Variable Declaration Statement that assigns the variable on execution
    """
    return Variable_Declaration(assign)


@action
def declare_global(_, __, assign: Assignment) -> Variable_Declaration:
    """
    :param assign: assignment before eol punctuation
    :param _: ignored parglare context
    :param __: ignored nodes
    :return: Variable Declaration Statement that assigns the global variable on execution
    """
    return Variable_Declaration(assign, is_global=True)


@action
def assertion(_, __, exp: Expression, error: Optional[Expression] = None) -> Assertion:
    """
    :param __: ignored nodes
    :param error: error to report
    :param _: ignored parglare context
    :param exp: expression to evaluate assertion by
    :return: Assertion Statement
    """
    return Assertion(exp, error)


@action
def print_statement(_, __, exp: Expression) -> Print:
    """
    :param _: ignored parglare context
    :param __: ignored nodes
    :param exp: expression to print
    :return: Print Statement
    """
    return Print(exp)


@action
def try_catch(_, __, try_block: Statement, catch_block: Statement, errors: List[Expression]) -> Try_Catch_Statement:
    """
    :param errors: errors to accept
    :param _: ignored parglare context
    :param __: ignored nodes
    :param try_block: statements to execute in try branch
    :param catch_block: statements to execute in catch branch
    :return: Try Catch
    """
    return Try_Catch_Statement(try_block, catch_block, errors=errors)


@action
def exception_assignment(_, __, except_val: Expression, var_name: Variable_Expression) -> Assignment:
    """
    Reversed assignment syntax for catch statements
    :param _:
    :param __:
    :param except_val: the exception to allow
    :param var_name: the name of the variable for the error
    :return: an assignment operation for this error
    """
    return Assignment(var_name.variable_name, except_val)


@action
def pause_statement(_, __) -> Pause_Statement:
    """
    :param _: ignored parglare context
    :param __: ignored nodes
    :return: Pause statement
    """
    return Pause_Statement()


@action
def assignment(_, __, var_name: Variable_Expression, exp: Expression):
    """
    :param _: ignored parglare context
    :param __: ignored nodes
    :param var_name: processed identifier to variable name
    :param exp: expression to assign variable value
    :return: assignment expression which evaluates to expression value
    """
    # todo: ensure that typing is checking identifier not over shadowing keywords
    return Assignment(var_name.variable_name, exp)


# NUMBERS #

@action
def float_exp(_, node: str) -> Float_Value:
    """
    :param _: ignored parglare context
    :param node: the number string
    :return: the positive number specified
    """
    return Float_Value(node)


@action
def int_exp(_, node: str) -> Int_Value:
    """
    :param _: ignored parglare context
    :param node: the number string
    :return: the positive number specified
    """
    return Int_Value(node)


@action
def direction_exp(_, nodes: list) -> Pass_Direction_Expression:
    """
    
    :param _: 
    :param nodes: single node list with direction keyword
    :return: pass direction
    """
    return Pass_Direction_Expression(nodes[0])


@action
def string(_, node: str) -> String_Value:
    """
    :param _: ignored parglare context
    :param node: string value
    :return: Expression storing quote
    """
    no_quotes = node.strip("\"")
    return String_Value(no_quotes)


@action
def f_string_section(_, __, exp: Optional[Expression] = None, string_value: Optional[str] = None) -> Expression:
    """
    :param __:
    :param exp: expression in formatting
    :param string_value: string in formatting
    :param _: ignored parglare context
    :return: Expression of string value of section of a formatted string
    """
    if exp is not None:
        return exp
    else:
        return String_Value(string_value)


@action
def formatted_string(_, __, sections: List[Expression]) -> Formatted_String_Value:
    """
    :param __:
    :param sections: f string sections parsed as expressions
    :param _: ignored parglare context
    :return: Formatted string expression
    """
    return Formatted_String_Value(sections)


# @action
# def param_kwargs_list(_, __,
#                       args: Optional[List[Expression]],
#                       kwargs: Optional[Tuple[str, List[Assignment]]]) -> Tuple[List[Expression], List[Assignment]]:
#     if args is None:
#         args = []
#     if kwargs is None:
#         kwargs = []
#     else:
#         kwargs = kwargs[1]
#     return args, kwargs


@action
def call_list(_, __, params: Optional[List[Expression]] = None,
              kwargs: Optional[List[Assignment]] = None) -> Tuple[List[Expression], List[Assignment]]:
    """
    :param _:
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
def function_call(_, __, func_name: Variable_Expression,
                  args: Tuple[List[Expression], List[Assignment]]) -> Function_Call:
    """
    :param _:
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
    return Function_Call(func_name, params, kwargs)


@action
def list_expression(_, __, exps: List[Expression]):
    """
    :param _:
    :param __:
    :param exps: expressions in the list
    :return: the list expression
    """
    return Knit_Script_List(exps)


@action
def list_comp(_, __, fill_exp: Expression, variables: List[Variable_Expression], iter_exp: Expression,
              spacer: Optional[Union[str, Expression]] = None, comp_cond: Expression = None) -> List_Comp:
    """
    :param _:
    :param __:
    :param fill_exp: Expression that fills the list
    :param spacer: the spacer value across the variables.
    :param variables: variables to fill from iterable
    :param iter_exp: the iterable to pass over
    :param comp_cond: condition to evaluate for adding a value
    :return: List comprehension
    """
    return List_Comp(fill_exp, spacer, variables, iter_exp, comp_cond)


@action
def started_slice(_, __, start: Expression,
                  end: Optional[Expression],
                  spacer: Optional[Expression]) -> Tuple[Expression, Optional[Expression], Optional[Expression]]:
    """
    :param _:
    :param __:
    :param start: first value in slide
    :param end: end of slice value
    :param spacer: spacing value
    :return: (start expression), (end expression), (spacer expression). End and spacer can be none
    """
    return start, end, spacer


@action
def ended_slice(_, __, end: Expression,
                spacer: Optional[Expression]) -> Tuple[Optional[Expression], Expression, Optional[Expression]]:
    """
    :param _:
    :param __:
    :param end: end of slice value
    :param spacer: spacing value
    :return: (start expression), (end expression), (spacer expression). Start is None. spacer can be none.
    """
    return None, end, spacer


@action
def spacer_slice(_, __, spacer: Expression) -> Tuple[Optional[Expression], Optional[Expression], Expression]:
    """
    :param _:
    :param __:
    :param spacer: spacing value
    :return: (start expression), (end expression), (spacer expression). Start and end are none. Spacer cannot be None
    """
    return None, None, spacer


@action
def slice_data(_, nodes: list) -> Union[Expression, Tuple[Optional[Expression], bool, Optional[Expression], bool, Optional[Expression]]]:
    """
    :param _:
    :param nodes: data from different slicing configurations
    :return: slice values
    """
    slice_values = nodes[0]
    if isinstance(slice_values, Expression):  # index passed
        return slice_values
    else:
        return slice_values[0], slice_values[1] is not None, slice_values[1], slice_values[2] is not None, slice_values[2]


@action
def sliced_list(_, __, iter_exp: Expression, slices: Union[Expression, Tuple[Optional[Expression], bool, Optional[Expression], bool, Optional[Expression]]]) -> Sliced_List:
    """
    :param _: ignored parser context
    :param __: ignored nodes
    :param iter_exp: The iterator to gather the slice from
    :param slices: data about how to form an index or slice
    :return: the slicer statement
    """
    if isinstance(slices, Expression):
        return Sliced_List(iter_exp, start=slices, is_index=True)
    return Sliced_List(iter_exp, slices[0], slices[1], slices[2], slices[3], slices[4])


@action
def dict_assign(_, __, key: Expression, exp: Expression) -> Tuple[Expression, Expression]:
    """
    collect key value pair
    :param _:
    :param __:
    :param key: key expression
    :param exp: value expression
    :return: key, value
    """
    return key, exp


@action
def dict_expression(_, __, kwargs: List[Tuple[Expression, Expression]]):
    """
    :param _:
    :param __:
    :param kwargs: key value pairs
    :return: The dictionary
    """
    return Knit_Script_Dictionary(kwargs)


@action
def dict_comp(_, __, key: Expression, value: Expression,
              variables: List[Variable_Expression], iter_exp: Expression,
              spacer: Optional[Union[str, Expression]] = None, comp_cond: Optional[Expression] = None) -> Dictionary_Comprehension:
    """
    :param spacer: spacing to jump over list
    :param comp_cond: conditional on variables to skip specific designs
    :param _:
    :param __:
    :param key: key expression
    :param value: value expression
    :param variables: variables to parse from iterable
    :param iter_exp: the iterable to parse over
    :return: Dictionary comprehension
    """
    return Dictionary_Comprehension(key, value, variables, iter_exp, spacer, comp_cond)


@action
def unpack(_, __, exp: Expression) -> Unpack:
    """
    :param _:
    :param __:
    :param exp: expression to unpack
    :return: Unpacking expression
    """
    return Unpack(exp)


@action
def code_block(_, __, statements: List[Statement]) -> Code_Block:
    """
    :param _: ignored parglare context
    :param __: ignored nodes
    :param statements: statements to execute in sub scope
    :return: scoping block
    """
    return Code_Block(statements)


# @action
# def else_statement(_, __, stmnt: Statement) -> Statement:
#     """
#     :param _: ignored parglare context
#     :param __: ignored nodes
#     :param stmnt: statement to execute on else
#     :return: statement to execute
#     """
#     return stmnt


@action
def elif_statement(_, __, exp: Expression, stmnt: Statement) -> Tuple[Expression, Statement]:
    """
    components of an elif statement
    :param _: ignored parglare context
    :param __: ignored nodes
    :param exp: expression to test on elif
    :param stmnt: statement to execute on true result
    :return: expression and statement to execute when true
    """
    return exp, stmnt


@action
def else_statement(_, __, false_statement: Code_Block) -> Code_Block:
    """
    :param _:
    :param __:
    :param false_statement: code block to execute when false
    :return: the code to execute when false
    """
    return false_statement


@action
def if_statement(_, __,
                 condition: Expression, true_statement: Code_Block,
                 elifs: List[Tuple[Expression, Statement]],
                 else_stmt: Optional[Code_Block]) -> If_Statement:
    """

    :param elifs: list of else-if conditions and statements
    :param _:
    :param __:
    :param condition: branching condition
    :param true_statement: statement to execute on true
    :param else_stmt: statement to execute on false
    :return: if statement
    """
    while len(elifs) > 0:
        elif_tuple = elifs.pop()
        else_stmt = If_Statement(elif_tuple[0], elif_tuple[1], else_stmt)
    return If_Statement(condition, true_statement, else_stmt)


@action
def while_statement(_, __, condition: Expression, while_block: Code_Block) -> While_Statement:
    """

    :param _:
    :param __:
    :param condition: condition to evaluate on while
    :param while_block: the statement to execute with each iteration
    :return:
    """
    return While_Statement(condition, while_block)


# @action
# def on_bed(_, __, bed: Union[str, Expression], s: Optional[str]) -> Tuple[Union[str, Expression], bool]:
#     return bed, s is not None


# @action
# def every_n(_, __, n: Union[str, Expression]) -> Union[str, Expression]:
#     return n


@action
def for_each_statement(_, __, variables: List[Variable_Expression], iters: List[Expression], block: Code_Block) -> For_Each_Statement:
    """
    :param _:
    :param __:
    :param variables: to assign on each iteration of iterable
    :param iters: iterable to iterate over
    :param block: statement to execute with each iteration
    :return: For each statement
    """
    if len(iters) == 1:
        return For_Each_Statement(variables, iters[0], block)
    else:
        return For_Each_Statement(variables, iters, block)


@action
def as_assignment(_, __, variable: Variable_Expression, exp: Expression) -> Assignment:
    """
    :param _:
    :param __:
    :param variable: variable to assign to
    :param exp: expression to assign
    :return: Assignment value
    """
    return Assignment(var_name=variable.variable_name, value_expression=exp)


@action
def with_statement(_, __, assigns: List[Assignment], block: Code_Block) -> With_Statement:
    """
    :param _:
    :param __:
    :param assigns: assignments for block
    :param block: block to execute
    :return: with statement
    """
    return With_Statement(block, assigns)


@action
def needle_instruction(_, __, inst: str) -> Needle_Instruction:
    """
    :param _:
    :param __:
    :param inst: instruction keyword
    :return: needle instruction
    """
    return Needle_Instruction.get_instruction(inst)


@action
def instruction_assignment(_, __, inst: Expression, needles: List[Expression]) -> Needle_Instruction_Exp:
    """
    :param _:
    :param __:
    :param inst: instruction to apply to needles
    :param needles: needles to apply instruction to
    :return: Needle instruction expression
    """
    return Needle_Instruction_Exp(inst, needles)


@action
def carriage_pass(_, __, pass_dir: Expression, instructions: List[Needle_Instruction_Exp]) -> In_Direction_Statement:
    """
    :param _:
    :param __:
    :param pass_dir: direction to apply instructions in
    :param instructions: instructions to apply
    :return: in direction statement
    """
    return In_Direction_Statement(pass_dir, instructions)


@action
def needle_id(_, needle_node: str) -> Needle_Expression:
    """
    :param _:
    :param needle_node: node representing needle
    :return: Needle expression
    """
    return Needle_Expression(needle_node)


@action
def sheet_id(_, sheet_node: str) -> Sheet_Expression:
    """
    :param _:
    :param sheet_node: string representing sheet
    :return: sheet expression
    """
    return Sheet_Expression(sheet_node)


@action
def carrier(_, carrier_node: str) -> Carrier_Expression:
    """
    :param _:
    :param carrier_node: string describing carrier
    :return: carrier expression
    """
    return Carrier_Expression(carrier_node)


@action
def return_statement(_, __, exp: Expression) -> Return_Statement:
    """
    :param _:
    :param __:
    :param exp: expression to return
    :return: return statement
    """
    return Return_Statement(exp)


@action
def param_list(_, __, args: Optional[List[Variable_Expression]] = None,
               kwargs: Optional[List[Assignment]] = None) -> Tuple[List[Variable_Expression], List[Assignment]]:
    """
    :param _:
    :param __:
    :param args: list of argument identifiers
    :param kwargs: list of keyword assignments
    :return: arguments and keyword assignments
    """
    if args is None:
        args = []
    if kwargs is None:
        kwargs = []
    return args, kwargs


@action
def function_declaration(_, __, func_name: Variable_Expression,
                         params: Optional[Tuple[List[Variable_Expression], List[Assignment]]],
                         block: Statement) -> Function_Declaration:
    """
    :param _:
    :param __:
    :param func_name: name of function
    :param params: list of variables for arguments, list of key word assignments
    :param block: body to execute
    :return: the function declaration
    """
    if params is None:
        params = [], []
    args = params[0]
    kwargs = params[1]
    return Function_Declaration(func_name.variable_name, args, kwargs, block)


@action
def expression(_, nodes: list) -> Expression:
    """
    :param _: ignored parglare context
    :param nodes: nodes to parse into expression
    :return: expression
    """
    if len(nodes) == 1:
        return nodes[0]
    if nodes[0] == "(":
        return nodes[1]
    else:
        return Operator_Expression(nodes[0], nodes[1], nodes[2])


@action
def negation(_, __, exp: Expression) -> Not_Expression:
    """
    :param _:
    :param __:
    :param exp: expression to negate
    :return: not expression
    """
    return Not_Expression(exp)


@action
def xfer_rack(_, __, is_across: Optional[str] = None, dist_exp: Optional[Expression] = None, side_id: Optional[Expression] = None) -> Xfer_Pass_Racking:
    """
    :param _:
    :param __:
    :param is_across: true if xfer is directly across beds
    :param dist_exp: the needle offset for xfer
    :param side_id: offset direction
    :return: xfer pass racking
    """
    return Xfer_Pass_Racking(is_across is not None, dist_exp, side_id)


@action
def xfer_pass(_, __, needles: List[Expression],
              rack_val: Xfer_Pass_Racking,
              bed: Optional[Expression] = None,
              slider: Optional[str] = None) -> Xfer_Pass_Statement:
    """

    :param _:
    :param __:
    :param rack_val: racking for xfers
    :param needles: needles to start xfer from
    :param bed: beds to land on. Exclude needles already on bed
    :param slider: True if transferring to sliders
    :return: xfer pass statement
    """
    return Xfer_Pass_Statement(rack_val, needles, bed, slider is not None)


@action
def accessor(_, __, exp: Expression, attribute: Expression) -> Attribute_Accessor_Expression:
    """
    :param _:
    :param __:
    :param exp: expression to get from
    :param attribute: attribute to collect
    :return: accessor
    """
    return Attribute_Accessor_Expression(exp, attribute)


@action
def exp_statement(_, __, exp: Expression) -> Expression_Statement:
    """
    :param _:
    :param __:
    :param exp: expression to execute
    :return: execution of expression
    """
    return Expression_Statement(exp)


@action
def cut_statement(_, __, exps: List[Expression]) -> Cut_Statement:
    """
    :param _:
    :param __:
    :param exps: carriers to cut
    :return: cut statement
    """
    return Cut_Statement(exps)


@action
def remove_statement(_, __, exps: List[Expression]) -> Remove_Statement:
    """
    :param _:
    :param __:
    :param exps: carriers to out
    :return: remove statement
    """
    return Remove_Statement(exps)


@action
def gauge_exp(_, __, sheet_exp: Expression, gauge: Expression) -> Gauge_Expression:
    """

    :param _:
    :param __:
    :param sheet_exp: sheet value
    :param gauge: gauge value
    :return: Gauge expression
    """
    return Gauge_Expression(sheet_exp, gauge)


@action
def drop_pass(_, __, needles: List[Expression]) -> Drop_Pass:
    """
    :param _:
    :param __:
    :param needles: needles to drop from
    :return: drop pass
    """
    return Drop_Pass(needles)


@action
def push_to(_, __, push_val: Union[str, list]) -> Union[str, Expression]:
    """
    :param _:
    :param __:
    :param push_val: front, back, or a specific layer value
    :return: identifying string or expression layer value
    """
    if isinstance(push_val, list):
        return push_val[1]
    return push_val


@action
def push_dir(_, __, amount: Expression, direction: str) -> Tuple[Expression, str]:
    """
    :param _:
    :param __:
    :param amount: value to push
    :param direction: direction to push
    :return: amount, direction
    """
    return amount, direction


@action
def push_statement(_, __, needles: List[Expression], push_val: Union[str, Expression, Tuple[Expression, str]]) -> Push_Statement:
    """

    :param _:
    :param __:
    :param needles: needles to push layer value
    :param push_val: specification of push value
    :return: Push statement
    """
    return Push_Statement(needles, push_val)


@action
def swap_statement(_, __, needles: List[Expression], swap_type: str, value: Expression) -> Swap_Statement:
    """
    :param _:
    :param __:
    :param needles: the needles to do this swap with
    :param swap_type: type of value to swap with
    :param value: the value to swap with
    :return: swap statement
    """
    return Swap_Statement(needles, swap_type, value)


@action
def pass_second(_, nodes: list):
    """
    :param _:
    :param nodes: nodes parsed
    :return: the second node in the list
    """
    return nodes[1]


@action
def import_statement(_, __, src: Expression, alias: Optional[Expression]) -> Import_Statement:
    """

    Parameters
    ----------
    _
    __
    src: source module
    alias: alias to assign in variable scope

    Returns
    -------
    The import statement holder
    """
    return Import_Statement(src, alias)
