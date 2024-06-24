"""Instructions Expressions"""
from knitout_interpreter.knitout_operations.knitout_instruction import Knitout_Instruction_Type
from virtual_knitting_machine.machine_components.needles.Needle import Needle

from knit_script.knit_script_interpreter.expressions.expressions import Expression
from knit_script.knit_script_interpreter.knit_script_context import Knit_Script_Context
from knit_script.knit_script_exceptions.Knit_Script_Exception import Needle_Instruction_Type_Exception


class Needle_Instruction_Exp(Expression):
    """
        Instructions that happen on a needle
    """

    def __init__(self, parser_node, instruction: Expression | Knitout_Instruction_Type, needles: list[Expression] | Expression):
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
        self._instruction_type: Expression | Knitout_Instruction_Type = instruction

    def evaluate(self, context: Knit_Script_Context) -> tuple[Knitout_Instruction_Type, list[Needle]]:
        """
        Evaluate the expression
        :param context: The current context of the knit_script_interpreter
        :return: The needle instruction of the expression
        """
        if isinstance(self._instruction_type, Knitout_Instruction_Type):
            instruction_type = self._instruction_type
        else:
            instruction_type = self._instruction_type.evaluate(context)
            if not isinstance(instruction_type, Knitout_Instruction_Type):
                raise TypeError(f"Expected Knitout_Instruction_Type but got {instruction_type}")
            if not instruction_type.is_needle_instruction:
                raise Needle_Instruction_Type_Exception(instruction_type)
        needles = []
        for exp in self._needles:
            value = exp.evaluate(context)
            if isinstance(value, list):
                needles.extend(value)
            else:
                needles.append(value)
        for needle in needles:
            if not isinstance(needle, Needle):
                raise TypeError(f"Expected List of needles, but got {needle} in {needles}")

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

    def evaluate(self, context: Knit_Script_Context) -> Knitout_Instruction_Type:
        """
        :param context:
        :return: The carrier instruction of the expression
        """
        return Knitout_Instruction_Type.get_instruction(self.inst_str)
