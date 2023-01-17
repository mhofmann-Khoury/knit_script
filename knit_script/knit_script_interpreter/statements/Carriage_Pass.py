"""Used to manage all instruction sets written for a single carriage pass in a given direction"""
from typing import Optional, Dict, Set

from knit_script.knit_script_interpreter.expressions.instruction_expression import Needle_Instruction
from knit_script.knit_script_interpreter.knit_script_context import Knit_Script_Context
from knit_script.knitting_machine.knitout_instructions import releasehook
from knit_script.knitting_machine.machine_components.machine_pass_direction import Pass_Direction
from knit_script.knitting_machine.machine_components.machine_position import Machine_Bed_Position
from knit_script.knitting_machine.machine_components.needles import Needle


class Carriage_Pass:
    """
        Manages actions on collection of needles in a carriage pass
    """
    def __init__(self, needle_to_instruction: Dict[Needle, Needle_Instruction],
                 direction: Optional[Pass_Direction] = None, target_bed: Optional[Machine_Bed_Position] = None,
                 rack: Optional[float] = None,
                 to_sliders: bool = False):
        """
        Instantiate
        :param needle_to_instruction:  needles keyed to instruction to do on them
        :param direction: direction of the carriage pass
        :param target_bed: The only bed to do operations on
        :param rack: the racking of the pass
        :param to_sliders: true if transferring or splitting to sliders
        """
        self._to_sliders: bool = to_sliders
        self._rack: Optional[float] = rack
        self._target_bed: Optional[Machine_Bed_Position] = target_bed
        self._needle_to_instruction: Dict[Needle: Needle_Instruction] = needle_to_instruction
        self._direction: Optional[Pass_Direction] = direction
        self._instruction_types: Set[Needle_Instruction] = set()
        first = None
        self._knitting_pass = False
        self._require_second = False
        for _, ni in self._needle_to_instruction.items():
            self._instruction_types.add(ni)
            if first is None:
                first = ni
                if first.in_knitting_pass:
                    self._knitting_pass = True
                if first.requires_second_needle:
                    self._require_second = True
                if first is Needle_Instruction.drop:
                    assert self._direction is None or self._direction is Pass_Direction.Rightward, \
                        f"Cannot drop in {self._direction} direction"
                    self._direction = Pass_Direction.Rightward
            else:
                assert first.compatible_pass(ni), f" Cannot {first} and {ni} in same machine pass"
            if ni.directed_pass:
                assert self._direction is not None, f"Cannot {ni} without a direction"

    def _needs_released_hook(self, context: Knit_Script_Context) -> bool:
        requires_rack = self._rack is not None and self._rack != context.racking
        return requires_rack or self._require_second

    def write_knitout(self, context: Knit_Script_Context):
        """
        Executes machine pass instructions on the current context
        :param context: the knit_pass context to execute on
        """

        # Force a releasehook before racking or xfers
        if not context.machine_state.yarn_manager.inserting_hook_available:  # check for release hook
            if self._needs_released_hook(context):
                cmd = releasehook(context.machine_state)
                context.knitout.append(cmd)

        if self._direction is None:  # assume next pass is reversed
            self._direction = context.direction.opposite()  # used as implied direction but not set unless explicit
        else:
            context.direction = self._direction
        cur_rack = context.racking
        if self._rack is not None:
            context.racking = self._rack

        needles = [*self._needle_to_instruction.keys()]

        needles = self._keep_target_bed_needles(needles)  # ignore needles that are already on target bed

        needles_in_order = self._direction.sort_needles(needles, racking=context.racking)
        # sort into direction of machine pass

        # calculate all-needle racking condition
        needs_all_needle_rack = False
        for n, m in zip(needles_in_order[0:-1], needles_in_order[1:]):
            if n.racked_position_on_front(context.racking) == m.racked_position_on_front(context.racking):
                assert n.is_front != m.is_front, \
                    f"Cannot repeat {self._needle_to_instruction[n]} on {n} in same carriage pass"
                n_instruction = self._needle_to_instruction[n]
                m_instruction = self._needle_to_instruction[n]
                assert n_instruction is m_instruction, \
                    f"Cannot {n_instruction} on {n} and {m_instruction} on same position {m}"
                assert n_instruction.all_needle_instruction, f"Cannot all-needle {n_instruction} at {n} and {m}"
                needs_all_needle_rack = True

        if needs_all_needle_rack:
            if context.racking >= 0:
                context.knitout.extend(f"rack {context.racking + .25}; All Needle racking {context.racking} to right\n")
            else:
                context.knitout.extend(f"rack {context.racking - .25}; All needle racking {context.racking} to left\n")

        for needle in needles_in_order:
            instruction = self._needle_to_instruction[needle]
            if instruction.requires_second_needle:
                second_needle = context.machine_state.xfer_needle_at_racking(needle, slider=self._to_sliders)
            else:
                second_needle = None
            executed_instruction = instruction.execute(context.machine_state, needle,
                                                       context.direction, context.carrier,
                                                       second_needle)
            context.knitout.append(executed_instruction)
        context.racking = cur_rack

        if self._knitting_pass:  # only counts towards release hook if new loops are created
            context.machine_state.yarn_manager.count_machine_pass()
        # tries to releasehook before next pass
        self._attempt_releasehook(context, needles_in_order)

    def _attempt_releasehook(self, context, needles_in_order):
        # manage a preemptive releasehook operation
        if context.machine_state.yarn_manager.inserting_hook_available:  # nothing to release
            return

        has_conflicting_needle = False  # requires a pre-emptive releasehook operation
        for needle in needles_in_order:
            if context.machine_state.yarn_manager.conflicts_with_inserting_hook(needle, self._direction):
                has_conflicting_needle = True
                break
        # Attempt release hooks at end of each pass. Often results in no actions
        release = context.machine_state.yarn_manager.try_releasehook()  # true if enough knits or needed to prevent conflict
        if release or has_conflicting_needle:
            cmd = releasehook(context.machine_state)
            context.knitout.append(cmd)

    def _keep_target_bed_needles(self, needles):
        if self._target_bed is not None:  # throw out needles that are on target bed already
            assert isinstance(self._target_bed, Machine_Bed_Position), \
                f"Expected xfer to Front or Back Bed but got {self._target_bed}"
            match_front = self._target_bed is Machine_Bed_Position.Back  # xfer from front to back
            match_needles = []
            for n in needles:
                if (match_front and n.is_front) or \
                        (not match_front and not n.is_front):
                    match_needles.append(n)
            needles = match_needles
        return needles
