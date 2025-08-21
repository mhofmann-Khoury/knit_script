"""Manages blocks of code executed in a new scope.

This module provides the Code_Block statement class, which handles the execution of multiple statements within a new variable scope.
It manages scope creation, statement execution, and proper handling of return values and scope cleanup.
"""
from parglare.parser import LRStackNode

from knit_script.knit_script_exceptions.add_exception_information import (
    add_exception_to_statement,
)
from knit_script.knit_script_interpreter.knit_script_context import Knit_Script_Context
from knit_script.knit_script_interpreter.statements.Statement import Statement


class Code_Block(Statement):
    """Used for executing any block of code in a new scope.

    Creates a new variable scope, executes all statements in order, then restores the previous scope. Handles return statements properly by preserving return values across scope boundaries.
     This class is fundamental to knit script's scoping system, providing isolation for variables while allowing controlled inheritance of changes.

    The code block ensures that variables defined within the block don't interfere with the outer scope unless explicitly designed to do so.
     It supports early termination through return statements and properly propagates return values to the appropriate scope level.

    Attributes:
        _statements (list[Statement]): Ordered list of statements to execute within the new scope.
    """

    def __init__(self, parser_node: LRStackNode, statements: list[Statement]) -> None:
        """Initialize a code block.

        Args:
            parser_node (LRStackNode): The parser node from the abstract syntax tree.
            statements (list[Statement]): Ordered list of statements to execute within the new scope.
        """
        super().__init__(parser_node)
        self._statements: list[Statement] = statements

    def execute(self, context: Knit_Script_Context) -> None:
        """Execute all statements in a new scope.

        Creates a new variable scope, executes statements in order, then exits the scope.
        If any statement triggers a return, execution stops early and the return value is preserved. The scope is collapsed into the parent to preserve variable changes.

        Args:
            context (Knit_Script_Context): The current execution context of the knit script interpreter.
        """
        context.enter_sub_scope()
        for statement in self._statements:
            try:
                statement.execute(context)
            except Exception as e:
                raise add_exception_to_statement(e, statement)
            if context.variable_scope.returned:  # executed statement updated scope with return value
                break  # don't continue to execute block statements
        context.exit_current_scope(collapse_into_parent=True)  # Collapse change upward, let next level decide if value changes are passed on.

    def __str__(self) -> str:
        """Return string representation of the code block.

        Returns:
            str: A string showing all statements in the block separated by semicolons.
        """
        values = ""
        for stst in self._statements:
            values += f"{stst};\n"
        values = values[:-2]
        return f"[{values}]"

    def __repr__(self) -> str:
        """Return detailed string representation of the code block.

        Returns:
            str: Same as __str__ for this class.
        """
        return str(self)
