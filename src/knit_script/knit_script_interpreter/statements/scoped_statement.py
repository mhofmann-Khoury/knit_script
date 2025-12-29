"""Module containing the superclass of knitscript statements that create a subscope."""

from collections.abc import Iterable

from parglare.parser import LRStackNode

from knit_script.knit_script_interpreter.knit_script_context import Knit_Script_Context
from knit_script.knit_script_interpreter.statements.Statement import Statement


class Scoped_Statement(Statement):
    """
    A super class of knitscript statements that enter a subscope.
    """

    def __init__(self, parser_node: LRStackNode, subscope_statement: Statement | Iterable[Statement], collapse_scope_into_parent: bool = False) -> None:
        """
        Args:
            parser_node (LRStackNode): The parser node from the abstract syntax tree.
            subscope_statement (Statement | Iterable[Statement]): The statement or statements to execute at the subscope.
            collapse_scope_into_parent (bool, optional): If true, the variables created in the subscope will be drawn up into the parent subscope after execution.
        """
        super().__init__(parser_node)
        self._subscope_statements: Iterable[Statement] = [subscope_statement] if isinstance(subscope_statement, Statement) else subscope_statement
        self._collapse_scope_into_parent: bool = collapse_scope_into_parent

    def pre_scope_action(self, context: Knit_Script_Context) -> bool:
        """
        An action taken before execution of the subscope statement (e.g., assigning local variables).

        This method should be overridden by subclasses that take actions before executing the sub-scoped statement(s).

        Args:
            context (Knit_Script_Context): The current execution context of the knit script interpreter.

        Returns:
            bool: True if the statements should follow execution of the pre-amble, False otherwise.
        """
        return True

    def execute(self, context: Knit_Script_Context) -> None:
        """Execute any pre-scope actions and then executing the sub-scoped statement(s) within a new scope.
        If any statement triggers a return, execution stops early and the return value is preserved.

        Args:
            context (Knit_Script_Context): The current execution context of the knit script interpreter.
        """
        context.enter_sub_scope()  # make sub scope with variable changes
        execute_statements = self.pre_scope_action(context)
        if execute_statements:
            for statement in self._subscope_statements:
                statement.execute(context)
                if context.variable_scope.returned:  # executed statement updated scope with return value
                    break  # don't continue to execute block statements
        context.exit_current_scope(collapse_into_parent=self._collapse_scope_into_parent)
