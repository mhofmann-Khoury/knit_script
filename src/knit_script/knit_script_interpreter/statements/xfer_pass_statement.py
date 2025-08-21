"""Statement for executing a transfer pass.

This module provides the Xfer_Pass_Statement class, which handles transfer operations between needle beds and to slider needles.
It manages the complex racking requirements and bed-specific processing needed for reliable stitch transfers.
"""
from typing import Iterable

from knitout_interpreter.knitout_operations.knitout_instruction import (
    Knitout_Instruction_Type,
)
from parglare.parser import LRStackNode
from virtual_knitting_machine.machine_components.needles.Needle import Needle

from knit_script.knit_script_exceptions.python_style_exceptions import (
    Knit_Script_TypeError,
)
from knit_script.knit_script_interpreter.expressions.expressions import Expression
from knit_script.knit_script_interpreter.knit_script_context import Knit_Script_Context
from knit_script.knit_script_interpreter.Machine_Specification import (
    Machine_Bed_Position,
)
from knit_script.knit_script_interpreter.statements.Carriage_Pass_Specification import (
    Carriage_Pass_Specification,
)
from knit_script.knit_script_interpreter.statements.Statement import Statement


class Xfer_Pass_Statement(Statement):
    """Executes transfer operations at specified racking with target needles.

    This statement manages the transfer of stitches between needle beds or to sliders,
     handling the complex racking requirements for different bed configurations and ensuring proper sequencing of operations.
     For non-zero racking, it separates front and back bed transfers since they require different racking values due to the mechanical constraints of the knitting machine.

    The transfer pass handles evaluation of needle expressions, racking calculations, bed filtering, and creation of appropriate carriage pass specifications for reliable stitch transfer operations.

    Attributes:
        _is_sliders (bool): True if transferring to sliders instead of regular needles.
        _bed (Expression | None): Expression that evaluates to the target bed position.
        _racking (Expression): Expression that evaluates to the racking position for transfers.
        _needles (list[Expression]): List of expressions that evaluate to needles to transfer from.
    """

    def __init__(self, parser_node: LRStackNode, racking: Expression, needles: list[Expression], bed: Expression | None, is_sliders: bool = False) -> None:
        """Initialize a transfer pass statement.

        Args:
            parser_node (LRStackNode): The parser node from the abstract syntax tree.
            racking (Expression): Expression that evaluates to the racking position for transfers.
            needles (list[Expression]): List of expressions that evaluate to needles to transfer from.
            bed (Expression | None): Expression that evaluates to the target bed position, or None to transfer to the opposite bed. Needles already on the target bed are excluded from the transfer.
            is_sliders (bool, optional): True if transferring to sliders instead of regular needles. Defaults to False.
        """
        super().__init__(parser_node)
        self._is_sliders: bool = is_sliders
        self._bed: Expression | None = bed
        self._racking: Expression = racking
        self._needles: list[Expression] = needles

    def __str__(self) -> str:
        """Return string representation of the transfer pass statement.

        Returns:
            str: A string showing the needles, racking, target bed, and slider flag.
        """
        s = ""
        if self._is_sliders:
            s = " on sliders"
        return f"Xfer({self._needles} to {self._racking} to {self._bed}{s})"

    def __repr__(self) -> str:
        """Return detailed string representation of the transfer pass statement.

        Returns:
            str: Same as __str__ for this class.
        """
        return str(self)

    def execute(self, context: Knit_Script_Context) -> None:
        """Execute transfer operations with proper racking and bed handling.

        Evaluates all needle expressions, determines the target bed, and creates appropriate carriage pass specifications.
        For non-zero racking, separates front and back bed transfers since they require different racking values due to mechanical constraints.

        Args:
            context (Knit_Script_Context): The current execution context of the knit script interpreter.

        Raises:
            TypeError: If needle expressions don't evaluate to Needle objects or if the bed expression doesn't evaluate to a Machine_Bed_Position.
        """
        needles: list[Needle] = []
        for needle in self._needles:
            n = needle.evaluate(context)
            if isinstance(n, Iterable):
                needles.extend(n)
            else:
                needles.append(n)
        for n in needles:
            if not isinstance(n, Needle):
                raise Knit_Script_TypeError(f"Expected xfer from needles but got {n}", self)

        target_bed = None
        if self._bed is not None:  # throw out needles that are on target bed already
            target_bed = self._bed.evaluate(context)
            if not isinstance(target_bed, Machine_Bed_Position):
                raise Knit_Script_TypeError(f"Expected xfer to Front or Back Bed but got {target_bed}", self)

        needles_to_instruction = {n: Knitout_Instruction_Type.Xfer for n in needles}

        racking = self._racking.evaluate(context)
        if racking != 0:  # rack for left or right transfers
            results = {}
            front_needles_to_instruction = {n: i for n, i in needles_to_instruction.items() if n.is_front}
            if len(front_needles_to_instruction) > 0:
                machine_pass = Carriage_Pass_Specification(self, front_needles_to_instruction, target_bed=target_bed, racking=racking, to_sliders=self._is_sliders)
                results.update(machine_pass.write_knitout(context))
            back_needles_to_instruction = {n: i for n, i in needles_to_instruction.items() if n.is_back}
            if len(back_needles_to_instruction) > 0:
                machine_pass = Carriage_Pass_Specification(self, back_needles_to_instruction, target_bed=target_bed, racking=racking * -1, to_sliders=self._is_sliders)
                # racking is reversed for back bed xfers
                results.update(machine_pass.write_knitout(context))
            context.last_carriage_pass_result = results
        else:
            machine_pass = Carriage_Pass_Specification(self, needles_to_instruction, target_bed=target_bed, racking=racking, to_sliders=self._is_sliders)
            context.last_carriage_pass_result = machine_pass.write_knitout(context)
