"""Expressions with operators between left and right hand side"""
from enum import Enum

from knit_script.knit_script_interpreter.expressions.expressions import Expression
from knit_script.knit_script_interpreter.knit_script_context import Knit_Script_Context


class Operator(Enum):
    """ Enumeration of different standard operators"""
    Add = "+"
    Sub = "-"
    Div = "/"
    Mod = "%"
    Mul = "*"
    Exp = "^"
    LT = "<"
    LTE = "<="
    GT = ">"
    GTE = ">="
    Equal = "=="
    NE = "!="
    Is = "is"
    In = "in"
    And = "and"
    Or = "or"

    @staticmethod
    def get_op(op_str: str):
        """
        Get the enumerated value
        :param op_str: string of operator
        :return: Operation Enum
        """
        return Operator(op_str)

    def operate(self, lhs, rhs):
        """
        Execute the operation on a and b
        :param lhs: first value
        :param rhs: second value
        :return: result of operation on lhs onto rhs
        """
        if self is Operator.Add:
            return lhs + rhs
        elif self is Operator.Sub:
            return lhs - rhs
        elif self is Operator.Div:
            return lhs / rhs
        elif self is Operator.Mod:
            return lhs % rhs
        elif self is Operator.Mul:
            return lhs * rhs
        elif self is Operator.Exp:
            return lhs ** rhs
        elif self is Operator.LT:
            return lhs < rhs
        elif self is Operator.LTE:
            return lhs <= rhs
        elif self is Operator.GT:
            return lhs > rhs
        elif self is Operator.GTE:
            return lhs >= rhs
        elif self is Operator.Equal:
            return lhs == rhs
        elif self is Operator.NE:
            return lhs != rhs
        elif self is Operator.Is:
            return lhs is rhs
        elif self is Operator.In:
            return lhs in rhs
        elif self is Operator.And:
            return lhs and rhs
        elif self is Operator.Or:
            return lhs or rhs


class Operator_Expression(Expression):
    """Expression for managing operations of expressions"""
    def __init__(self, parser_node, lhs: Expression, op_str: str, rhs: Expression):
        """
        Instantiate
        :param parser_node:
        :param lhs: left expression
        :param op_str:  operation
        :param rhs: right expression
        """
        super().__init__(parser_node)
        self._rhs: Expression = rhs
        self.op_str: str = op_str
        self._lhs: Expression = lhs

    def evaluate(self, context: Knit_Script_Context) -> int:
        """
        Evaluate the expression
        :param context: The current context of the knit_script_interpreter
        :return: integer resulting from evaluation
        """
        first_num = self._lhs.evaluate(context)
        op = Operator.get_op(self.op_str)
        second_num = self._rhs.evaluate(context)
        return op.operate(first_num, second_num)

    def __str__(self):
        return f"({self._lhs} {self.op_str} {self._rhs})"

    def __repr__(self):
        return str(self)
