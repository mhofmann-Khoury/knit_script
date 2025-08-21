"""Loop control structures.

This module provides statement classes for implementing loop control flow in knit script programs.
It includes while loops for condition-based iteration and for-each loops for iterating over collections, both essential for repetitive knitting operations and pattern generation.
"""
from typing import Iterable

from parglare.parser import LRStackNode

from knit_script.knit_script_exceptions.python_style_exceptions import (
    Knit_Script_TypeError,
    Knit_Script_ValueError,
)
from knit_script.knit_script_interpreter.expressions.expressions import Expression
from knit_script.knit_script_interpreter.expressions.variables import (
    Variable_Expression,
)
from knit_script.knit_script_interpreter.knit_script_context import Knit_Script_Context
from knit_script.knit_script_interpreter.statements.Statement import Statement


class While_Statement(Statement):
    """While loop execution structure.

    Repeatedly evaluates a condition and executes a statement while the condition remains true.
    This provides the fundamental loop control structure for condition-based iteration in knit script programs, enabling repetitive operations based on dynamic conditions.

    The while loop follows Python's truthiness conventions for condition evaluation and provides proper scope management for loop variables and state.

    Attributes:
        _condition (Expression): The boolean expression to evaluate before each iteration.
        _statement (Statement): The statement to execute with each iteration.
    """

    def __init__(self, parser_node: LRStackNode, condition: Expression, statement: Statement) -> None:
        """Initialize a while loop.

        Args:
            parser_node (LRStackNode): The parser node from the abstract syntax tree.
            condition (Expression): The boolean expression to evaluate before each iteration. Loop continues while this evaluates to a truthy value.
            statement (Statement): The statement to execute with each iteration of the loop.
        """
        super().__init__(parser_node)
        self._condition: Expression = condition
        self._statement: Statement = statement

    def execute(self, context: Knit_Script_Context) -> None:
        """Execute the while loop.

        Evaluates the condition and executes the statement repeatedly until the condition becomes false. The condition is re-evaluated before each iteration.

        Args:
            context (Knit_Script_Context): The current execution context of the knit script interpreter.
        """
        condition = self._condition.evaluate(context)
        while condition:
            self._statement.execute(context)
            condition = self._condition.evaluate(context)

    def __str__(self) -> str:
        """Return string representation of the while loop.

        Returns:
            str: A string showing the condition and statement.
        """
        return f"While({self._condition} -> {self._statement})"

    def __repr__(self) -> str:
        """Return detailed string representation of the while loop.

        Returns:
            str: Same as __str__ for this class.
        """
        return str(self)


class For_Each_Statement(Statement):
    """For-each loop that iterates over iterable elements.

    Provides access to iterable variables over lists or other iterable objects. Supports both single variable and multiple variable unpacking for complex iteration patterns.
    This is the primary iteration mechanism for processing collections in knit script programs.

    The for-each loop creates a new scope for iteration variables, ensuring proper variable isolation while allowing access to outer scope variables.
    It supports unpacking for tuple iteration and provides comprehensive error handling for iteration issues.

    Attributes:
        _variables (list[Variable_Expression]): List of variables to assign on each iteration.
        var_name (str | None): Single variable name for simple iterations.
        _iter_expression (Expression | list[Expression]): Expression that evaluates to an iterable.
        _statement (Statement): Statement to execute with each iteration.
    """

    def __init__(self, parser_node: LRStackNode, variables: list[Variable_Expression], iter_expression: Expression | list[Expression], statement: Statement) -> None:
        """Initialize a for-each loop.

        Args:
            parser_node (LRStackNode): The parser node from the abstract syntax tree.
            variables (list[Variable_Expression]): List of variables to assign on each iteration. If single variable, assigns the iterated value directly.
            If multiple variables, unpacks each iterated value.
            iter_expression (Expression | list[Expression]): Expression that evaluates to an iterable, or list of expressions to iterate over.
            statement (Statement): Statement to execute with each iteration of the loop.
        """
        super().__init__(parser_node)
        self._variables: list[Variable_Expression] = variables
        if len(self._variables) == 1:
            self.var_name: str | None = self._variables[0].variable_name
        else:
            self.var_name: str | None = None  # multiple variables require unpacking
        self._iter_expression: Expression | list[Expression] = iter_expression
        self._statement = statement

    def execute(self, context: Knit_Script_Context) -> None:
        """Execute the for-each loop.

        Creates a new scope for the loop variables, then iterates over the iterable expression, assigning values and executing the statement for each iteration.
        Handles both single variable assignment and multiple variable unpacking.

        Args:
            context (Knit_Script_Context): The current execution context of the knit script interpreter.

        Raises:
            TypeError: If the expression does not evaluate to an iterable.
            ValueError: If unpacking multiple variables and the number of values doesn't match the number of variables.
        """
        if isinstance(self._iter_expression, list):
            iterable = [e.evalute(context) for e in self._iter_expression]
        else:
            iterable = self._iter_expression.evaluate(context)
        if not isinstance(iterable, Iterable):
            raise Knit_Script_TypeError(f'Cannot iterate over non-iterable value {iterable}', self)
        context.enter_sub_scope()  # create new scope that holds iterator variable
        for var in iterable:
            if self.var_name is not None:
                context.variable_scope[self.var_name] = var  # update iterator variable in scope
            else:  # multiple vars to unpack
                iterated_var = [*var]
                if len(iterated_var) > len(self._variables):
                    raise Knit_Script_ValueError(f"Too many values to unpack, expected {len(self._variables)} but got {len(iterated_var)}: {iterated_var}.", self)
                elif len(iterated_var) < len(self._variables):
                    raise Knit_Script_ValueError(f"Too few values to unpack, expected {len(self._variables)} but got {len(iterated_var)}: {iterated_var}.",self)

                for var_name, var_val in zip(self._variables, iterated_var):
                    context.variable_scope[var_name.variable_name] = var_val

            self._statement.execute(context)
        context.exit_current_scope()  # exit scope, removing access to iterator variable

    def __str__(self) -> str:
        """Return string representation of the for-each loop.

        Returns:
            str: A string showing the variables, iterable, and statement.
        """
        return f"for {self.var_name} in {self._iter_expression} -> {self._statement}"

    def __repr__(self) -> str:
        """Return detailed string representation of the for-each loop.

        Returns:
            str: Same as __str__ for this class.
        """
        return str(self)
