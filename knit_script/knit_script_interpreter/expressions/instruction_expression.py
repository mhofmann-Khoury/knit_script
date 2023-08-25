"""Instructions Expressions"""
from typing import Union

from knit_script.knit_script_interpreter.expressions.expressions import Expression
from knit_script.knit_script_interpreter.knit_script_context import Knit_Script_Context
from knit_script.knitout_interpreter.knitout_structures.knitout_instructions.instruction import Instruction_Type
from knit_script.knitting_machine.machine_components.needles import Needle


class Needle_Instruction_Exp(Expression):
    """
        Instructions that happen on a needle
    """

    def __init__(self, parser_node, instruction: Union[Expression, Instruction_Type], needles: Union[list[Expression], Expression]):
        """
        Instantiate
        :param parser_node:
        :param instruction: The instruction to do to a needle set
        :param needles: the needles to do the instruction on
        """
        super().__init__(parser_node)
        if not isinstance(needles, list):
            needles = [needles]
        self._needles = needles
        self._instruction_type: Union[Expression, Instruction_Type] = instruction

    def evaluate(self, context: Knit_Script_Context) -> tuple[Instruction_Type, list[Needle]]:
        """
        Evaluate the expression
        :param context: The current context of the knit_script_interpreter
        :return: The needle instruction of the expression
        """
        if isinstance(self._instruction_type, Instruction_Type):
            instruction_type = self._instruction_type
        else:
            instruction_type = self._instruction_type.evaluate(context)
            assert isinstance(instruction_type, Instruction_Type), f"Expected needle instruction (knit, tuck, miss, split, xfer, drop) but got {instruction_type}"
            assert instruction_type.is_needle_instruction, f"Expected needle instruction (knit, tuck, miss, split, xfer, drop) but got {instruction_type}"
        needles = []
        for exp in self._needles:
            value = exp.evaluate(context)
            if isinstance(value, list):
                needles.extend(value)
            else:
                needles.append(value)
        for needle in needles:
            assert isinstance(needle, Needle), f"Expected List of needles, but got {needle} in {needles}"

        return instruction_type, needles

    def __str__(self):
        return f"N_Inst({self._instruction_type} -> {self._needles})"

    def __repr__(self):
        return str(self)


class Machine_Instruction_Exp(Expression):
    """
        Expression evaluates to machine instructions
    """

    def __init__(self, parser_node, inst_str: str):
        super().__init__(parser_node)
        self.inst_str = inst_str

    def evaluate(self, context: Knit_Script_Context) -> Instruction_Type:
        """
        :param context:
        :return: The carrier instruction of the expression
        """
        return Instruction_Type.get_instruction(self.inst_str)
