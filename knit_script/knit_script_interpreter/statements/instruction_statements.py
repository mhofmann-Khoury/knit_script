"""Statements that produce knitout for machine level instructions"""

import os

from knit_script.knit_script_interpreter.knit_script_context import Knit_Script_Context
from knit_script.knit_script_interpreter.statements.Statement import Statement


class Pause_Statement(Statement):
    """
    An instruction execution that pauses the knitting machine
    """

    def __init__(self):
        super().__init__()

    def execute(self, context: Knit_Script_Context):
        """
        Writes a pause instruction into the knitout at current context
        :param context:  The current context of the knit_script_interpreter
        """
        context.knitout.append(f"pause;{os.linesep}")

    def __str__(self):
        return "Pause"

    def __repr__(self):
        return str(self)
