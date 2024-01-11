"""Used to manage all instruction sets written for a single carriage pass in a given direction"""
from typing import Optional, Dict

from knit_script.Knit_Errors.knitting_errors import Incompatible_Carriage_Pass_Operations, Instructions_Require_Direction, Repeated_Needle_In_Pass, All_Needle_Operation_Error
from knit_script.knit_script_interpreter.knit_script_context import Knit_Script_Context
from knit_script.knitout_interpreter.knitout_structures.knitout_instructions.instruction import Instruction_Type
from knit_script.knitout_interpreter.knitout_structures.knitout_instructions.knitout_instructions import build_instruction, rack
from knit_script.knitting_machine.machine_components.machine_pass_direction import Pass_Direction
from knit_script.knitting_machine.machine_components.machine_position import Machine_Bed_Position
from knit_script.knitting_machine.machine_components.needles import Needle


class Carriage_Pass:
    """
        Manages actions on a collection of needles in a carriage pass
    """

    def __init__(self, needle_to_instruction: dict[Needle, Instruction_Type], direction: Optional[Pass_Direction] = None, target_bed: Optional[Machine_Bed_Position] = None,
                 racking: Optional[float] = None, to_sliders: bool = False, is_drop_pass=False):
        """
        Instantiate
        :param is_drop_pass:
        :param needle_to_instruction:  Needles keyed to instruction to do on them.
        :param direction: The direction of the carriage pass.
        :param target_bed: The only bed to do operations on
        :param racking: the racking of the pass
        :param to_sliders: true if transferring or splitting to sliders
        """
        self._to_sliders: bool = to_sliders
        self._racking: Optional[float] = racking
        self._target_bed: Optional[Machine_Bed_Position] = target_bed
        self._has_drops: bool = False
        self._drop_pass: Optional[Carriage_Pass] = None
        if not is_drop_pass:  # extract drop operations
            drop_pass = {}
            n_to_i = {}
            for needle, instruction_type in needle_to_instruction.items():
                if instruction_type is Instruction_Type.Drop:
                    drop_pass[needle] = Instruction_Type.Drop
                else:
                    n_to_i[needle] = instruction_type
            if len(drop_pass) > 0:
                self._has_drops = True
                self._drop_pass = Carriage_Pass(drop_pass, Pass_Direction.Rightward, is_drop_pass=True)
                needle_to_instruction = n_to_i
        self._needle_to_instruction: dict[Needle: Instruction_Type] = needle_to_instruction
        self._direction: Optional[Pass_Direction] = direction
        self._instruction_types: set[Instruction_Type] = set()
        first_instruction_type = None
        self._knitting_pass = False
        self._require_second = False

        for _, instruction_type in self._needle_to_instruction.items():
            self._instruction_types.add(instruction_type)
            if first_instruction_type is None:
                first_instruction_type = instruction_type
                if first_instruction_type.in_knitting_pass:
                    self._knitting_pass = True
                if first_instruction_type.requires_second_needle:
                    self._require_second = True
            else:
                if not first_instruction_type.compatible_pass(instruction_type):
                    raise Incompatible_Carriage_Pass_Operations(first_instruction_type, instruction_type)
            if instruction_type.directed_pass and self._direction is None:
                raise Instructions_Require_Direction(instruction_type)

    def _needs_released_hook(self, context: Knit_Script_Context) -> bool:
        requires_rack = self._racking is not None and self._racking != context.racking
        return requires_rack or self._require_second

    def write_knitout(self, context: Knit_Script_Context) -> Dict[Needle, Optional[Needle]]:
        """
        Executes machine pass instructions on the current context
        :param context: the knit_pass context to execute on
        """
        results = {}
        if self._direction is None:  # assume the next pass is reversed
            self._direction = context.direction.opposite()  # used as the implied direction but not set unless explicit
        else:
            if self._has_drops and context.direction is Pass_Direction.Leftward and self._direction is Pass_Direction.Leftward:  # needs to drop and can drop between repeat leftward passes
                results = self._drop_pass.write_knitout(context)
                self._has_drops = False
            context.direction = self._direction
        cur_rack = context.racking
        if self._racking is not None:
            context.racking = self._racking

        needles = [*self._needle_to_instruction.keys()]

        needles = self._keep_target_bed_needles(needles)  # ignore needles that are already on target bed

        needles_in_order = self._direction.sort_needles(needles, racking=context.racking)  # sort into the direction of machine pass

        # calculate all-needle racking condition
        needs_all_needle_rack = False
        for n, m in zip(needles_in_order[0:-1], needles_in_order[1:]):
            if n.racked_position_on_front(context.racking) == m.racked_position_on_front(context.racking):
                if n.is_front == m.is_front:
                    raise Repeated_Needle_In_Pass(n)
                n_instruction = self._needle_to_instruction[n]
                # todo: what did these do?
                # m_instruction = self._needle_to_instruction[n]
                # assert n_instruction is m_instruction, \
                #     f"Cannot {n_instruction} on {n} and {m_instruction} on same position {m}"
                if not n_instruction.all_needle_instruction:
                    raise All_Needle_Operation_Error(n, m, n_instruction)
                needs_all_needle_rack = True

        if needs_all_needle_rack:
            if context.racking >= 0:
                context.knitout.append(rack(context.machine_state, context.racking + .25, comment=f"All Needle racking {context.racking} to right"))
            else:
                context.knitout.append(rack(context.machine_state, context.racking - .25, comment=f"All Needle racking {context.racking} to left"))

        for needle in needles_in_order:
            instruction_type = self._needle_to_instruction[needle]
            if instruction_type.requires_second_needle:
                second_needle = context.machine_state.xfer_needle_at_racking(needle, slider=self._to_sliders)
            else:
                second_needle = None
            results[needle] = second_needle
            instruction = build_instruction(instruction_type, first_needle=needle, direction=context.direction, carrier_set=context.carrier, second_needle=second_needle)
            _ = instruction.execute(context.machine_state)
            context.knitout.append(instruction)
        if needs_all_needle_rack:
            context.knitout.append(rack(context.machine_state, cur_rack, comment=f"Reset rack from all_needle"))
        context.racking = cur_rack
        if self._has_drops:  # still has drops available
            results.update(self._drop_pass.write_knitout(context))
        return results

    def _keep_target_bed_needles(self, needles):
        if self._target_bed is not None:  # throw out needles that are on target bed already
            if not isinstance(self._target_bed, Machine_Bed_Position):
                raise TypeError(f"Expected xfer to Front or Back Bed but got {self._target_bed}")
            match_front = self._target_bed is Machine_Bed_Position.Back  # xfer from front to back
            match_needles = []
            for n in needles:
                if (match_front and n.is_front) or \
                        (not match_front and not n.is_front):
                    match_needles.append(n)
            needles = match_needles
        return needles
