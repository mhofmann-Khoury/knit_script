"""Instructions Expressions.

This module provides expression classes for handling knitting machine instructions in knit script programs.
 It includes classes for needle-specific instructions and general machine instructions, with proper type checking and validation.
"""
from typing import Iterable

from knitout_interpreter.knitout_operations.knitout_instruction import (
    Knitout_Instruction_Type,
)
from parglare.parser import LRStackNode
from virtual_knitting_machine.machine_components.needles.Needle import Needle

from knit_script.knit_script_exceptions.ks_exceptions import (
    Needle_Instruction_Type_Exception,
)
from knit_script.knit_script_exceptions.python_style_exceptions import (
    Knit_Script_TypeError,
)
from knit_script.knit_script_interpreter.expressions.expressions import Expression
from knit_script.knit_script_interpreter.knit_script_context import Knit_Script_Context


class Needle_Instruction_Exp(Expression):
    """Instructions that happen on a needle.

    The Needle_Instruction_Exp class represents instructions that are applied to specific needles on the knitting machine.
     It combines an instruction type with a set of target needles, ensuring that the instruction is valid for needle operations and that all targets are proper Needle objects.

    This class is essential for carriage pass operations where specific instructions (like knit, tuck, miss, etc.) need to be applied to particular needles.
    It provides validation to ensure instruction types are appropriate for needle operations.

    Attributes:
        _needles (list[Expression]): List of expressions that evaluate to needles.
        _instruction_type (Expression | Knitout_Instruction_Type): The instruction type to apply to the needles.
    """

    def __init__(self, parser_node: LRStackNode, instruction: Expression | Knitout_Instruction_Type, needles: list[Expression] | Expression) -> None:
        """Initialize the Needle_Instruction_Exp.

        Args:
            parser_node (LRStackNode): The parser node from the parse tree.
            instruction (Expression | Knitout_Instruction_Type): The instruction to apply to the needle set, either as a direct instruction type or an expression that evaluates to one.
            needles (list[Expression] | Expression): The needles to apply the instruction to, either as a list of expressions or a single expression that may evaluate to multiple needles.
        """
        super().__init__(parser_node)
        if not isinstance(needles, list):
            needles = [needles]
        self._needles = needles
        self._instruction_type: Expression | Knitout_Instruction_Type = instruction

    def evaluate(self, context: Knit_Script_Context) -> tuple[Knitout_Instruction_Type, list[Needle]]:
        """Evaluate the expression to get the instruction and target needles.

        Evaluates the instruction type and needle expressions, validates that the instruction is appropriate for needle operations, and ensures all targets are valid Needle objects.

        Args:
            context (Knit_Script_Context): The current context of the knit_script_interpreter.

        Returns:
            tuple[Knitout_Instruction_Type, list[Needle]]: A tuple containing the validated instruction type and the list of target needles.

        Raises:
            TypeError: If the instruction type is not a Knitout_Instruction_Type or if any needle is not a Needle object.
            Needle_Instruction_Type_Exception: If the instruction type is not valid for needle operations.
        """
        if isinstance(self._instruction_type, Knitout_Instruction_Type):
            instruction_type = self._instruction_type
        else:
            instruction_type = self._instruction_type.evaluate(context)
            if not isinstance(instruction_type, Knitout_Instruction_Type):
                raise Knit_Script_TypeError(f"Expected Knitout_Instruction_Type but got {instruction_type}", self)
            if not instruction_type.is_needle_instruction:
                raise Needle_Instruction_Type_Exception(self, instruction_type)
        needles: list[Needle] = []
        for exp in self._needles:
            value = exp.evaluate(context)
            if isinstance(value, Iterable):
                needles.extend(value)
            else:
                needles.append(value)
        for needle in needles:
            if not isinstance(needle, Needle):
                raise Knit_Script_TypeError(f"Expected List of needles, but got {needle} in {needles}", self)

        return instruction_type, needles

    def __str__(self) -> str:
        return f"N_Inst({self._instruction_type} -> {self._needles})"

    def __repr__(self) -> str:
        return str(self)


class Machine_Instruction_Exp(Expression):
    """Expression evaluates to machine instructions.

    The Machine_Instruction_Exp class represents general machine instruction expressions that are not specific to individual needles.
     It converts instruction string identifiers into the corresponding Knitout_Instruction_Type objects.

    This class is used for machine-level operations that don't target specific needles but rather control overall machine behavior or state.

    Attributes:
        inst_str (str): The instruction string identifier.
    """

    def __init__(self, parser_node: LRStackNode, inst_str: str) -> None:
        """Initialize the Machine_Instruction_Exp.

        Args:
            parser_node (LRStackNode): The parser node from the parse tree.
            inst_str (str): The instruction string identifier to convert to an instruction type.
        """
        super().__init__(parser_node)
        self.inst_str = inst_str

    def evaluate(self, context: Knit_Script_Context) -> Knitout_Instruction_Type:
        """Evaluate the expression to get the machine instruction type.

        Converts the instruction string identifier into the corresponding Knitout_Instruction_Type object.

        Args:
            context (Knit_Script_Context): The current context of the knit_script_interpreter.

        Returns:
            Knitout_Instruction_Type: The instruction type matching the string identifier.
        """
        return Knitout_Instruction_Type.get_instruction(self.inst_str)
