"""Loop control structures"""
from typing import Iterable

from parglare.parser import LRStackNode

from knit_script.knit_script_interpreter.expressions.expressions import Expression
from knit_script.knit_script_interpreter.expressions.variables import Variable_Expression
from knit_script.knit_script_interpreter.knit_script_context import Knit_Script_Context
from knit_script.knit_script_interpreter.statements.Statement import Statement


class While_Statement(Statement):
    """While loop execution structure.

    Repeatedly evaluates a condition and executes a statement while
    the condition remains true.
    """

    def __init__(self, parser_node: LRStackNode, condition: Expression, statement: Statement) -> None:
        """Initialize a while loop.

        Args:
            parser_node: The parser node from the abstract syntax tree.
            condition: The boolean expression to evaluate before each iteration.
            statement: The statement to execute with each iteration.
        """
        super().__init__(parser_node)
        self._condition: Expression = condition
        self._statement: Statement = statement

    def execute(self, context: Knit_Script_Context) -> None:
        """Execute the while loop.

        Evaluates the condition and executes the statement repeatedly
        until the condition becomes false.

        Args:
            context: The current execution context of the knit script interpreter.
        """
        condition = self._condition.evaluate(context)
        while condition:
            self._statement.execute(context)
            condition = self._condition.evaluate(context)

    def __str__(self) -> str:
        """Return string representation of the while loop.

        Returns:
            A string showing the condition and statement.
        """
        return f"While({self._condition} -> {self._statement})"

    def __repr__(self) -> str:
        """Return detailed string representation of the while loop.

        Returns:
            Same as __str__ for this class.
        """
        return str(self)


class For_Each_Statement(Statement):
    """For-each loop that iterates over iterable elements.

    Provides access to iterable variables over lists or other iterable objects.
    Supports both single variable and multiple variable unpacking.
    """

    def __init__(self, parser_node: LRStackNode, variables: list[Variable_Expression], iter_expression: Expression | list[Expression], statement: Statement) -> None:
        """Initialize a for-each loop.

        Args:
            parser_node: The parser node from the abstract syntax tree.
            variables: List of variables to assign on each iteration. If single variable,
                assigns the iterated value directly. If multiple variables, unpacks
                each iterated value.
            iter_expression: Expression that evaluates to an iterable, or list of
                expressions to iterate over.
            statement: Statement to execute with each iteration.
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

        Creates a new scope for the loop variables, then iterates over the
        iterable expression, assigning values and executing the statement
        for each iteration.

        Args:
            context: The current execution context of the knit script interpreter.

        Raises:
            TypeError: If the expression does not evaluate to an iterable.
            ValueError: If unpacking multiple variables and the number of values
                doesn't match the number of variables.
        """
        if isinstance(self._iter_expression, list):
            iterable = [e.evalute(context) for e in self._iter_expression]
        else:
            iterable = self._iter_expression.evaluate(context)
        if not isinstance(iterable, Iterable):
            raise TypeError(f'Cannot iterate over non-iterable value {iterable}')
        context.enter_sub_scope()  # create new scope that holds iterator variable
        for var in iterable:
            if self.var_name is not None:
                context.variable_scope[self.var_name] = var  # update iterator variable in scope
            else:  # multiple vars to unpack
                iterated_var = [*var]
                if len(iterated_var) > len(self._variables):
                    raise ValueError(f"Too many values to unpack, expected {len(self._variables)} but got {len(iterated_var)}: {iterated_var}.")
                elif len(iterated_var) < len(self._variables):
                    raise ValueError(f"Too few values to unpack, expected {len(self._variables)} but got {len(iterated_var)}: {iterated_var}.")

                for var_name, var_val in zip(self._variables, iterated_var):
                    context.variable_scope[var_name.variable_name] = var_val

            self._statement.execute(context)
        context.exit_current_scope()  # exit scope, removing access to iterator variable

    def __str__(self) -> str:
        """Return string representation of the for-each loop.

        Returns:
            A string showing the variables, iterable, and statement.
        """
        return f"for {self.var_name} in {self._iter_expression} -> {self._statement}"

    def __repr__(self) -> str:
        """Return detailed string representation of the for-each loop.

        Returns:
            Same as __str__ for this class.
        """
        return str(self)
