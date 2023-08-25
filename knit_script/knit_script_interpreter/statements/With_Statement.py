"""With statement for setting variables in temporary variable space"""
from typing import List

from knit_script.knit_script_interpreter.knit_script_context import Knit_Script_Context
from knit_script.knit_script_interpreter.scope.machine_scope import Machine_Variables
from knit_script.knit_script_interpreter.statements.Statement import Statement
from knit_script.knit_script_interpreter.statements.assignment import Assignment
from knit_script.knitout_interpreter.knitout_structures.knitout_instructions.knitout_instructions import rack


class With_Statement(Statement):
    """
        Statements that set variables for sub statement block
    """

    def __init__(self, parser_node, statement: Statement, assignments: List[Assignment]):
        """
        Instantiate
        :param parser_node:
        :param statement: statement to execute with variable space
        :param assignments: variables to assign in variable space
        """
        super().__init__(parser_node)
        self._statement = statement
        self._assignments = assignments

    def execute(self, context: Knit_Script_Context):
        """
        Sets variable values at new scope and executes in-context code
        :param context: The current context of the knit_script_interpreter
        """
        context.enter_sub_scope()  # make sub scope with variable changes
        reset_machine_scope = {}
        for assign in self._assignments:
            if Machine_Variables.in_machine_variables(assign.variable_name.lower()):
                reset_machine_scope[assign.variable_name] = context.variable_scope.machine_scope[assign.variable_name]
            assign.assign_value(context)
        self._statement.execute(context)
        # Reset the machine state to before the with statement assignments
        if Machine_Variables.Sheet.name in reset_machine_scope:  # reset sheet before gauge
            Machine_Variables.Sheet.set_value(context, reset_machine_scope[Machine_Variables.Sheet.name])
        if Machine_Variables.Gauge.name in reset_machine_scope:
            Machine_Variables.Gauge.set_value(context, reset_machine_scope[Machine_Variables.Gauge.name])
        if Machine_Variables.Rack.name in reset_machine_scope:
            Machine_Variables.Rack.set_value(context, reset_machine_scope[Machine_Variables.Rack.name])
            rack_instruction = rack(context.machine_state, context.racking)
            context.knitout.append(rack_instruction)
        if Machine_Variables.Carrier.name in reset_machine_scope:
            Machine_Variables.Carrier.set_value(context, reset_machine_scope[Machine_Variables.Carrier.name])
        context.exit_current_scope()  # exit scope with variable changes including prior racking and carrier

    def __str__(self):
        return f"With({self._assignments} -> {self._statement})"

    def __repr__(self):
        return str(self)
