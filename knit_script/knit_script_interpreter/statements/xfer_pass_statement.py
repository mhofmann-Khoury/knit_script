"""
Statement for executing a xfer pass
"""
from typing import List, Optional

from knit_script.knit_script_interpreter.expressions.expressions import Expression
from knit_script.knit_script_interpreter.expressions.instruction_expression import Needle_Instruction
from knit_script.knit_script_interpreter.knit_script_context import Knit_Script_Context
from knit_script.knit_script_interpreter.statements.Carriage_Pass import Carriage_Pass
from knit_script.knit_script_interpreter.statements.Statement import Statement
from knit_script.knitting_machine.machine_components.machine_position import Machine_Bed_Position
from knit_script.knitting_machine.machine_components.needles import Needle


class Xfer_Pass_Statement(Statement):
    """
        Executes transfers at specified racking with target needles
    """

    def __init__(self, racking: Expression,
                 needles: List[Expression],
                 bed: Optional[Expression],
                 is_sliders: bool = False):
        """
        Instantiate
        :param racking: racking for xfers
        :param needles: needles to start xfer from
        :param bed: beds to land on. Exclude needles already on bed
        :param is_sliders: True if transferring to sliders
        """
        super().__init__()
        self._is_sliders = is_sliders
        self._bed = bed
        self._racking = racking
        self._needles = needles

    def __str__(self):
        s = ""
        if self._is_sliders:
            s = " on sliders"
        return f"Xfer({self._needles} to {self._racking} to {self._bed}{s})"

    def __repr__(self):
        return str(self)

    def execute(self, context: Knit_Script_Context):
        """
        Execute xfer operations
        :param context: The current context of the knit_script_interpreter
        """
        needles = []
        for needle in self._needles:
            n = needle.evaluate(context)
            if isinstance(n, list):
                needles.extend(n)
            else:
                needles.append(n)
        for n in needles:
            assert isinstance(n, Needle), \
                f"Expected xfer from needles but got {n}"

        target_bed = None
        if self._bed is not None:  # throw out needles that are on target bed already
            target_bed = self._bed.evaluate(context)
            assert isinstance(target_bed, Machine_Bed_Position), \
                f"Expected xfer to Front or Back Bed but got {target_bed}"

        needles_to_instruction = {n: Needle_Instruction.xfer for n in needles}

        machine_pass = Carriage_Pass(needles_to_instruction, target_bed=target_bed, to_sliders=self._is_sliders)

        machine_pass.write_knitout(context)
