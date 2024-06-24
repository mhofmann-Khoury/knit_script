"""
Statement for executing a xfer pass
"""
from knitout_interpreter.knitout_operations.knitout_instruction import Knitout_Instruction_Type
from virtual_knitting_machine.machine_components.needles.Needle import Needle

from knit_script.knit_script_interpreter.expressions.expressions import Expression
from knit_script.knit_script_interpreter.knit_script_context import Knit_Script_Context
from knit_script.knit_script_interpreter.knit_script_values.Machine_Specification import Machine_Bed_Position
from knit_script.knit_script_interpreter.statements.Carriage_Pass_Specification import Carriage_Pass_Specification
from knit_script.knit_script_interpreter.statements.Statement import Statement


class Xfer_Pass_Statement(Statement):
    """
        Executes transfers at specified racking with target needles
    """

    def __init__(self, parser_node, racking: Expression, needles: list[Expression], bed: Expression | None, is_sliders: bool = False):
        """
        Instantiate
        :param parser_node:
        :param racking: Racking for xfers
        :param needles: needles to start xfer from
        :param bed: beds to land on. Exclude needles already on bed
        :param is_sliders: True if transferred to sliders
        """
        super().__init__(parser_node)
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
            if not isinstance(n, Needle):
                raise TypeError(f"Expected xfer from needles but got {n}")

        target_bed = None
        if self._bed is not None:  # throw out needles that are on target bed already
            target_bed = self._bed.evaluate(context)
            if not isinstance(target_bed, Machine_Bed_Position):
                raise TypeError(f"Expected xfer to Front or Back Bed but got {target_bed}")

        needles_to_instruction = {n: Knitout_Instruction_Type.Xfer for n in needles}

        racking = self._racking.evaluate(context)
        if racking != 0:  # rack for left or right transfers
            results = {}
            front_needles_to_instruction = {n: i for n, i in needles_to_instruction.items() if n.is_front}
            if len(front_needles_to_instruction) > 0:
                machine_pass = Carriage_Pass_Specification(front_needles_to_instruction, target_bed=target_bed, racking=racking, to_sliders=self._is_sliders)
                results.update(machine_pass.write_knitout(context))
            back_needles_to_instruction = {n: i for n, i in needles_to_instruction.items() if n.is_back}
            if len(back_needles_to_instruction) > 0:
                machine_pass = Carriage_Pass_Specification(back_needles_to_instruction, target_bed=target_bed, racking=racking * -1, to_sliders=self._is_sliders)  # racking is reversed for back bed xfers
                results.update(machine_pass.write_knitout(context))
            context.last_carriage_pass_result = results
        else:
            machine_pass = Carriage_Pass_Specification(needles_to_instruction, target_bed=target_bed, racking=racking, to_sliders=self._is_sliders)
            context.last_carriage_pass_result = machine_pass.write_knitout(context)
