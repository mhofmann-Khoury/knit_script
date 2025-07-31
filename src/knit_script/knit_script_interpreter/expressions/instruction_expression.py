"""Instructions Expressions"""
from typing import Iterable

from knitout_interpreter.knitout_operations.knitout_instruction import Knitout_Instruction_Type
from parglare.parser import LRStackNode
from virtual_knitting_machine.machine_components.needles.Needle import Needle

from knit_script.knit_script_interpreter.expressions.expressions import Expression
from knit_script.knit_script_exceptions.ks_exceptions import Needle_Instruction_Type_Exception
from knit_script.knit_script_interpreter.knit_script_context import Knit_Script_Context


class Needle_Instruction_Exp(Expression):
    """Instructions that happen on a needle."""

    def __init__(self, parser_node: LRStackNode, instruction: Expression | Knitout_Instruction_Type, needles: list[Expression] | Expression) -> None:
        """Initialize the Needle_Instruction_Exp.

        Args:
            parser_node (LRStackNode): The parser node from the parse tree.
            instruction (Expression | Knitout_Instruction_Type): The instruction to do to a needle set.
            needles (list[Expression] | Expression): The needles to do the instruction on.
        """
        super().__init__(parser_node)
        if not isinstance(needles, list):
            needles = [needles]
        self._needles = needles
        self._instruction_type: Expression | Knitout_Instruction_Type = instruction

    def evaluate(self, context: Knit_Script_Context) -> tuple[Knitout_Instruction_Type, list[Needle]]:
        """Evaluate the expression.

        Args:
            context (Knit_Script_Context): The current context of the knit_script_interpreter.

        Returns:
            tuple[Knitout_Instruction_Type, list[Needle]]: The needle instruction of the expression.
        """
        if isinstance(self._instruction_type, Knitout_Instruction_Type):
            instruction_type = self._instruction_type
        else:
            instruction_type = self._instruction_type.evaluate(context)
            if not isinstance(instruction_type, Knitout_Instruction_Type):
                raise TypeError(f"Expected Knitout_Instruction_Type but got {instruction_type}")
            if not instruction_type.is_needle_instruction:
                raise Needle_Instruction_Type_Exception(instruction_type)
        needles: list[Needle] = []
        for exp in self._needles:
            value = exp.evaluate(context)
            if isinstance(value, Iterable):
                needles.extend(value)
            else:
                needles.append(value)
        for needle in needles:
            if not isinstance(needle, Needle):
                raise TypeError(f"Expected List of needles, but got {needle} in {needles}")

        return instruction_type, needles

    def __str__(self) -> str:
        return f"N_Inst({self._instruction_type} -> {self._needles})"

    def __repr__(self) -> str:
        return str(self)


class Machine_Instruction_Exp(Expression):
    """Expression evaluates to machine instructions."""

    def __init__(self, parser_node: LRStackNode, inst_str: str) -> None:
        super().__init__(parser_node)
        self.inst_str = inst_str

    def evaluate(self, context: Knit_Script_Context) -> Knitout_Instruction_Type:
        """Evaluate the expression.

        Args:
            context (Knit_Script_Context): The current context of the knit_script_interpreter.

        Returns:
            Knitout_Instruction_Type: The carrier instruction of the expression.
        """
        return Knitout_Instruction_Type.get_instruction(self.inst_str)
