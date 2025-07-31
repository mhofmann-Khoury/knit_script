"""Expressions with operators between left and right hand side"""
from __future__ import annotations
from enum import Enum
from typing import Any

from parglare.parser import LRStackNode

from knit_script.knit_script_interpreter.expressions.expressions import Expression
from knit_script.knit_script_interpreter.knit_script_context import Knit_Script_Context


class Operator(Enum):
    """Enumeration of different standard operators."""
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
    def get_op(op_str: str) -> Operator:
        """Get the enumerated value.

        Args:
            op_str (str): String of operator.

        Returns:
            Operator: Operation Enum.
        """
        return Operator(op_str)

    def operate(self, lhs: Any, rhs: Any) -> Any:
        """Execute the operation on a and b.

        Args:
            lhs (Any): First value.
            rhs (Any): Second value.

        Returns:
            Any: Result of operation on lhs onto rhs.
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
    """Expression for managing operations of expressions."""

    def __init__(self, parser_node: LRStackNode, lhs: Expression, op_str: str, rhs: Expression) -> None:
        """Initialize the Operator_Expression.

        Args:
            parser_node (LRStackNode): The parser node from the parse tree.
            lhs (Expression): Left expression.
            op_str (str): Operation.
            rhs (Expression): Right expression.
        """
        super().__init__(parser_node)
        self._rhs: Expression = rhs
        self.op_str: str = op_str
        self._lhs: Expression = lhs

    def evaluate(self, context: Knit_Script_Context) -> Any:
        """Evaluate the expression.

        Args:
            context (Knit_Script_Context): The current context of the knit_script_interpreter.

        Returns:
            Any: Integer resulting from evaluation.
        """
        first_num = self._lhs.evaluate(context)
        op = Operator.get_op(self.op_str)
        second_num = self._rhs.evaluate(context)
        return op.operate(first_num, second_num)

    def __str__(self) -> str:
        return f"({self._lhs} {self.op_str} {self._rhs})"

    def __repr__(self) -> str:
        return str(self)
