"""Expressions with operators between left and right hand side.

This module provides classes for handling binary operator expressions in knit script programs.
It includes the Operator enumeration that defines available operators and their behavior, and the Operator_Expression class that evaluates binary operations between two expressions.
"""
from __future__ import annotations

from enum import Enum
from typing import Any

from parglare.parser import LRStackNode

from knit_script.knit_script_interpreter.expressions.expressions import Expression
from knit_script.knit_script_interpreter.knit_script_context import Knit_Script_Context


class Operator(Enum):
    """Enumeration of different standard operators.

    The Operator enumeration defines all the binary operators supported in knit script expressions.
    It includes arithmetic operators, comparison operators, logical operators, and membership operators, following Python's operator conventions and behavior.

    Each operator enum value provides both the string representation and the operation implementation, ensuring consistent behavior across all operator expressions.
    """
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
        """Get the enumerated operator value from string.

        Args:
            op_str (str): String representation of the operator.

        Returns:
            Operator: The corresponding operator enumeration value.
        """
        return Operator(op_str)

    def operate(self, lhs: Any, rhs: Any) -> Any:
        """Execute the operation on the left and right operands.

        Performs the operation represented by this operator enum value on the provided operands, following Python's standard operator behavior and type coercion rules.

        Args:
            lhs (Any): Left-hand side operand (first value).
            rhs (Any): Right-hand side operand (second value).

        Returns:
            Any: Result of applying this operation to lhs and rhs, with return type depending on the operator and operand types.

        Note:
            Arithmetic operators return numeric results, comparison operators return booleans, logical operators follow Python's short-circuit evaluation, and membership operators return booleans.
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
    """Expression for managing operations between two expressions.

    The Operator_Expression class handles binary operator expressions in knit script programs.
    It takes two operand expressions and an operator, evaluates the operands in the current context, and applies the specified operation to produce a result.

    This expression type is fundamental to knit script programs, enabling arithmetic calculations, logical operations, comparisons, and other binary operations between any types of expressions.

    Attributes:
        _lhs (Expression): The left-hand side expression operand.
        op_str (str): The string representation of the operator.
        _rhs (Expression): The right-hand side expression operand.
    """

    def __init__(self, parser_node: LRStackNode, lhs: Expression, op_str: str, rhs: Expression) -> None:
        """Initialize the Operator_Expression.

        Args:
            parser_node (LRStackNode): The parser node from the parse tree.
            lhs (Expression): Left-hand side expression operand.
            op_str (str): String representation of the operator to apply.
            rhs (Expression): Right-hand side expression operand.
        """
        super().__init__(parser_node)
        self._rhs: Expression = rhs
        self.op_str: str = op_str
        self._lhs: Expression = lhs

    def evaluate(self, context: Knit_Script_Context) -> Any:
        """Evaluate the expression to perform the binary operation.

        Evaluates both operand expressions in the current context, retrieves the corresponding operator, and applies the operation to the evaluated operands.

        Args:
            context (Knit_Script_Context): The current context of the knit_script_interpreter.

        Returns:
            Any: The result of applying the operator to the evaluated operands, with type depending on the operator and operand types.
        """
        first_num = self._lhs.evaluate(context)
        op = Operator.get_op(self.op_str)
        second_num = self._rhs.evaluate(context)
        return op.operate(first_num, second_num)

    def __str__(self) -> str:
        return f"({self._lhs} {self.op_str} {self._rhs})"

    def __repr__(self) -> str:
        return str(self)
