"""Manages blocks of code executed in a new scope.

This module provides the Code_Block statement class, which handles the execution of multiple statements within a new variable scope.
It manages scope creation, statement execution, and proper handling of return values and scope cleanup.
"""

from parglare.parser import LRStackNode

from knit_script.knit_script_interpreter.statements.scoped_statement import Scoped_Statement
from knit_script.knit_script_interpreter.statements.Statement import Statement


class Code_Block(Scoped_Statement):
    """Used for executing any block of code in a new scope.

    Creates a new variable scope, executes all statements in order, then restores the previous scope. Handles return statements properly by preserving return values across scope boundaries.
     This class is fundamental to knit script's scoping system, providing isolation for variables while allowing controlled inheritance of changes.

    The code block ensures that variables defined within the block don't interfere with the outer scope unless explicitly designed to do so.
     It supports early termination through return statements and properly propagates return values to the appropriate scope level.
    """

    def __init__(self, parser_node: LRStackNode, statements: list[Statement]) -> None:
        """Initialize a code block.

        Args:
            parser_node (LRStackNode): The parser node from the abstract syntax tree.
            statements (list[Statement]): Ordered list of statements to execute within the new scope.
        """
        super().__init__(parser_node, statements, collapse_scope_into_parent=True)
        self._statements: list[Statement] = statements
