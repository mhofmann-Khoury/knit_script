"""Used to manage all instruction sets written for a single carriage pass in a given direction"""
from knitout_interpreter.knitout_operations.Rack_Instruction import Rack_Instruction
from knitout_interpreter.knitout_operations.knitout_instruction import Knitout_Instruction_Type
from knitout_interpreter.knitout_operations.needle_instructions import Needle_Instruction
from virtual_knitting_machine.machine_components.carriage_system.Carriage_Pass_Direction import Carriage_Pass_Direction
from virtual_knitting_machine.machine_components.needles.Needle import Needle

from knit_script.knit_script_exceptions.Knit_Script_Exception import Incompatible_In_Carriage_Pass_Exception, Required_Direction_Exception, Repeated_Needle_Exception, All_Needle_Operation_Exception
from knit_script.knit_script_interpreter.knit_script_context import Knit_Script_Context
from knit_script.knit_script_interpreter.knit_script_values.Machine_Specification import Machine_Bed_Position
from knit_script.knitout_execution.knitout_execution import build_instruction


class Carriage_Pass_Specification:
    """
        Manages actions on a collection of needles in a carriage pass
    """

    def __init__(self, needle_to_instruction: dict[Needle, Knitout_Instruction_Type], direction: Carriage_Pass_Direction | None = None, target_bed: Machine_Bed_Position | None = None,
                 racking: float | None = None, to_sliders: bool = False, is_drop_pass=False):
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
        self._racking: float | None = racking
        self._target_bed: Machine_Bed_Position | None = target_bed
        self._has_drops: bool = False
        self._drop_pass: Carriage_Pass_Specification | None = None
        if not is_drop_pass:  # extract drop operations
            drop_pass = {}
            n_to_i = {}
            for needle, instruction_type in needle_to_instruction.items():
                if instruction_type is Knitout_Instruction_Type.Drop:
                    drop_pass[needle] = Knitout_Instruction_Type.Drop
                else:
                    n_to_i[needle] = instruction_type
            if len(drop_pass) > 0:
                self._has_drops = True
                self._drop_pass = Carriage_Pass_Specification(drop_pass, Carriage_Pass_Direction.Rightward, is_drop_pass=True)
                needle_to_instruction = n_to_i
        self._needle_to_instruction: dict[Needle: Knitout_Instruction_Type] = needle_to_instruction
        self._direction: Carriage_Pass_Direction | None = direction
        self._instruction_types: set[Knitout_Instruction_Type] = set()
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
                    raise Incompatible_In_Carriage_Pass_Exception(first_instruction_type, instruction_type)
            if instruction_type.directed_pass and self._direction is None:
                raise Required_Direction_Exception(instruction_type)

    def _needs_released_hook(self, context: Knit_Script_Context) -> bool:
        requires_rack = self._racking is not None and self._racking != context.racking
        return requires_rack or self._require_second

    def write_knitout(self, context: Knit_Script_Context) -> dict[Needle, Needle | None]:
        """
        Executes machine pass instructions on the current context
        :param context: the knit_pass context to execute on
        """
        results = {}
        if self._direction is None:  # assume the next pass is reversed
            self._direction = context.direction.opposite()  # used as the implied direction but not set unless explicit
        else:
            if self._has_drops and context.direction is Carriage_Pass_Direction.Leftward and self._direction is Carriage_Pass_Direction.Leftward:
                # needs to drop and can drop between repeat leftward passes
                results = self._drop_pass.write_knitout(context)
                self._has_drops = False
            context.direction = self._direction
        cur_rack = context.racking
        if self._racking is not None:
            context.racking = self._racking

        needles = [*self._needle_to_instruction.keys()]

        needles = self._keep_target_bed_needles(needles)  # ignore needles that are already on target bed

        needles_in_order = self._direction.sort_needles(needles, racking=int(context.racking))
        # sort into the direction of machine pass #Todo: update context to give rack value and all_needle separately.

        # calculate all-needle racking condition
        needs_all_needle_rack = False
        for n, m in zip(needles_in_order[0:-1], needles_in_order[1:]):
            if n.racked_position_on_front(context.racking) == m.racked_position_on_front(context.racking):
                if n.is_front == m.is_front:
                    raise Repeated_Needle_Exception(n)
                n_instruction = self._needle_to_instruction[n]
                # todo: what did these do?
                # m_instruction = self._needle_to_instruction[n]
                # assert n_instruction is m_instruction, \
                #     f"Cannot {n_instruction} on {n} and {m_instruction} on same position {m}"
                if not n_instruction.all_needle_instruction:
                    raise All_Needle_Operation_Exception(n, m, n_instruction)
                needs_all_needle_rack = True

        if needs_all_needle_rack:
            if context.racking >= 0:
                context.knitout.append(Rack_Instruction.execute_rack(context.machine_state, context.racking + .25, comment=f"All Needle racking {context.racking} to right"))
            else:
                context.knitout.append(Rack_Instruction.execute_rack(context.machine_state, context.racking - .25, comment=f"All Needle racking {context.racking} to left"))

        for needle in needles_in_order:
            instruction_type = self._needle_to_instruction[needle]
            if instruction_type.requires_second_needle:
                second_needle = context.machine_state.get_aligned_needle(needle, aligned_slider=self._to_sliders)
            else:
                second_needle = None
            results[needle] = second_needle
            instruction = build_instruction(instruction_type, first_needle=needle, direction=context.direction, carrier_set=context.carrier, second_needle=second_needle)
            _ = instruction.execute(context.machine_state)
            if isinstance(instruction, Needle_Instruction):
                context.gauged_sheet_record.record_needle(instruction.needle)
                if instruction.has_second_needle and instruction.needle_2.position != instruction.needle.position:
                    context.gauged_sheet_record.record_needle(instruction.needle_2)
            context.knitout.append(instruction)
        if needs_all_needle_rack:
            context.knitout.append(Rack_Instruction.execute_rack(context.machine_state, cur_rack, comment=f"Reset rack from all_needle"))
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
