"""With statement for setting variables in temporary variable space"""
from typing import List

from knit_script.knit_script_interpreter.knit_script_context import Knit_Script_Context
from knit_script.knit_script_interpreter.statements.Statement import Statement
from knit_script.knit_script_interpreter.statements.assignment import Assignment
from knit_script.knitting_machine.knitout_instructions import rack


class With_Statement(Statement):
    """
        Statements that set variables for sub statement block
    """
    def __init__(self, statement: Statement, assignments: List[Assignment]):
        """
        Instantiate
        :param statement: statement to execute with variable space
        :param assignments: variables to assign in variable space
        """
        super().__init__()
        self._statement = statement
        self._assignments = assignments

    def execute(self, context: Knit_Script_Context):
        """
        Sets variable values at new scope and executes in-context code
        :param context: The current context of the knit_script_interpreter
        """
        reset_rack = False
        context.enter_sub_scope()  # make sub scope with variable changes
        for assign in self._assignments:
            assign.assign_value(context)
        self._statement.execute(context)
        context.exit_current_scope()  # exit scope with variable changes including prior racking and carrier
        # Note: resetting scope should revert carrier rack values which can be used for reset operations
        if reset_rack:
            rack_instruction = rack(context.machine_state, context.current_racking)
            context.knitout.append(rack_instruction)

    def __str__(self):
        return f"With({self._assignments} -> {self._statement})"

    def __repr__(self):
        return str(self)


