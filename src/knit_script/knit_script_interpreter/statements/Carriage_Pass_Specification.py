"""Used to manage all instruction sets written for a single carriage pass in a given direction.

This module provides the Carriage_Pass_Specification class, which coordinates the execution of multiple knitting operations that occur during a single pass of the carriage across the needle bed.
It ensures proper sequencing, compatibility checking, and execution of operations while handling complex scenarios like all-needle operations and drop pass separation.
"""
from knitout_interpreter.knitout_operations.knitout_instruction import (
    Knitout_Instruction_Type,
)
from knitout_interpreter.knitout_operations.knitout_instruction_factory import (
    build_instruction,
)
from knitout_interpreter.knitout_operations.needle_instructions import (
    Needle_Instruction,
)
from knitout_interpreter.knitout_operations.Rack_Instruction import Rack_Instruction
from virtual_knitting_machine.machine_components.carriage_system.Carriage_Pass_Direction import (
    Carriage_Pass_Direction,
)
from virtual_knitting_machine.machine_components.needles.Needle import Needle

from knit_script.knit_script_exceptions.ks_exceptions import (
    All_Needle_Operation_Exception,
    Incompatible_In_Carriage_Pass_Exception,
    Repeated_Needle_Exception,
    Required_Direction_Exception,
)
from knit_script.knit_script_exceptions.python_style_exceptions import (
    Knit_Script_TypeError,
)
from knit_script.knit_script_interpreter.knit_script_context import Knit_Script_Context
from knit_script.knit_script_interpreter.ks_element import KS_Element
from knit_script.knit_script_interpreter.Machine_Specification import (
    Machine_Bed_Position,
)


class Carriage_Pass_Specification:
    """Manages actions on a collection of needles in a carriage pass.

    This class coordinates the execution of multiple knitting operations that occur during a single pass of the carriage across the needle bed,
    ensuring proper sequencing and compatibility of operations.
    It handles complex scenarios including instruction compatibility checking, needle ordering, all-needle racking requirements, and drop operation separation.

    The carriage pass specification ensures that all operations within a single pass are physically possible on the knitting machine
     and executes them in the correct order based on the carriage direction and machine racking configuration.

    Attributes:
        _source_statement (KS_Element): The source statement that generates this specification.
        _to_sliders (bool): True if transferring or splitting operations target sliders.
        _racking (float | None): The racking position for this pass.
        _target_bed (Machine_Bed_Position | None): Target bed filter for operations.
        _has_drops (bool): True if this pass contains drop operations.
        _drop_pass (Carriage_Pass_Specification | None): Separate drop pass specification.
        _needle_to_instruction (dict[Needle, Knitout_Instruction_Type]): Mapping of needles to instructions.
        _direction (Carriage_Pass_Direction | None): Direction of the carriage pass.
        _instruction_types (set[Knitout_Instruction_Type]): Set of all instruction types in this pass.
        _knitting_pass (bool): True if this pass includes knitting operations.
        _require_second (bool): True if any instruction requires a second needle.
    """

    def __init__(self, source_statement: KS_Element, needle_to_instruction: dict[Needle, Knitout_Instruction_Type], direction: Carriage_Pass_Direction | None = None,
                 target_bed: Machine_Bed_Position | None = None, racking: float | None = None, to_sliders: bool = False, is_drop_pass: bool = False) -> None:
        """Initialize a carriage pass specification.

        Creates a carriage pass specification with the given instructions and validates compatibility between all operations.
        Automatically separates drop operations into a dedicated drop pass if other operations are present.

        Args:
            source_statement (KS_Element): The source statement that generates this specification for error reporting.
            needle_to_instruction (dict[Needle, Knitout_Instruction_Type]): Dictionary mapping needles to the instructions to perform on them during this pass.
            direction (Carriage_Pass_Direction | None, optional): The direction of the carriage pass. If None, will be determined automatically based on context. Defaults to None.
            target_bed (Machine_Bed_Position | None, optional): If specified, only operations on this bed will be performed. Defaults to None.
            racking (float | None, optional): The racking position for this pass. If None, uses current racking from context. Defaults to None.
            to_sliders (bool, optional): True if transferring or splitting operations target slider needles. Defaults to False.
            is_drop_pass (bool, optional): True if this is a specialized drop-only pass. Defaults to False.

        Raises:
            Incompatible_In_Carriage_Pass_Exception: If incompatible instruction types are specified for the same pass.
            Required_Direction_Exception: If a direction-dependent instruction is specified without providing a direction.
        """
        self._source_statement: KS_Element = source_statement
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
                self._drop_pass = Carriage_Pass_Specification(self._source_statement, drop_pass, Carriage_Pass_Direction.Rightward, is_drop_pass=True)
                needle_to_instruction = n_to_i

        self._needle_to_instruction: dict[Needle, Knitout_Instruction_Type] = needle_to_instruction
        self._direction: Carriage_Pass_Direction | None = direction
        self._instruction_types: set[Knitout_Instruction_Type] = set()
        first_instruction_type = None
        self._knitting_pass: bool = False
        self._require_second: bool = False

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
                    raise Incompatible_In_Carriage_Pass_Exception(self._source_statement, first_instruction_type, instruction_type)
            if instruction_type.directed_pass and self._direction is None:
                raise Required_Direction_Exception(self._source_statement, instruction_type)

    def _needs_released_hook(self, context: Knit_Script_Context) -> bool:
        """Check if the yarn hook needs to be released for this pass.

        Determines whether the yarn inserting hook needs to be released before executing this carriage pass, typically due to racking changes or operations requiring multiple needles.

        Args:
            context (Knit_Script_Context): The current execution context.

        Returns:
            bool: True if the hook needs to be released before executing this pass.
        """
        requires_rack = self._racking is not None and self._racking != context.racking
        return requires_rack or self._require_second

    def write_knitout(self, context: Knit_Script_Context) -> dict[Needle, Needle | None]:
        """Execute machine pass instructions and write to knitout.

        Executes all operations in the carriage pass, handling proper needle ordering, racking adjustments, all-needle operations, and drop pass coordination.
        Generates the appropriate knitout instructions and updates the machine state accordingly.

        Args:
            context (Knit_Script_Context): The knit pass context to execute operations on.

        Returns:
            dict[Needle, Needle | None]: Dictionary mapping each needle to its target needle (for transfers/splits) or None for other operations.

        Raises:
            Repeated_Needle_Exception: If the same needle position is used multiple times in incompatible ways during the pass.
            All_Needle_Operation_Exception: If all-needle operations are attempted on overlapping needles without proper racking configuration.
        """
        results: dict[Needle, Needle | None] = {}
        if self._direction is None:  # assume the next pass is reversed
            self._direction = context.direction.opposite()  # used as the implied direction but not set unless explicit
        else:
            if self._has_drops and context.direction is Carriage_Pass_Direction.Leftward and self._direction is Carriage_Pass_Direction.Leftward:
                # needs to drop and can drop between repeat leftward passes
                assert isinstance(self._drop_pass, Carriage_Pass_Specification)
                results = self._drop_pass.write_knitout(context)
                self._has_drops = False
            context.direction = self._direction
        cur_rack = context.racking
        if self._racking is not None:
            context.racking = self._racking

        needles = [*self._needle_to_instruction.keys()]

        needles = self._keep_target_bed_needles(needles)  # ignore needles that are already on target bed

        needles_in_order = self._direction.sort_needles(needles, racking=int(context.racking))
        # sort into the direction of machine pass

        # calculate all-needle racking condition
        needs_all_needle_rack = False
        for n, m in zip(needles_in_order[0:-1], needles_in_order[1:]):
            if n.racked_position_on_front(context.racking) == m.racked_position_on_front(context.racking):
                if n.is_front == m.is_front:
                    raise Repeated_Needle_Exception(self._source_statement, n)
                n_instruction = self._needle_to_instruction[n]
                if not n_instruction.all_needle_instruction:
                    raise All_Needle_Operation_Exception(self._source_statement, n, m, context.machine_state.rack, n_instruction)
                needs_all_needle_rack = True

        if needs_all_needle_rack:
            context.knitout.append(Rack_Instruction.execute_rack(context.machine_state, context.racking + .25, comment=f"All Needle racking {context.racking}"))

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
            assert isinstance(self._drop_pass, Carriage_Pass_Specification)
            results.update(self._drop_pass.write_knitout(context))
        return results

    def _keep_target_bed_needles(self, needles: list[Needle]) -> list[Needle]:
        """Filter needles to only include those not already on the target bed.

        When a target bed is specified, filters the needle list to include only needles that need to be processed (i.e., those not already on the target bed).

        Args:
            needles (list[Needle]): List of needles to filter based on target bed requirements.

        Returns:
            list[Needle]: Filtered list of needles that need to be processed for the target bed.

        Raises:
            TypeError: If target_bed is not a valid Machine_Bed_Position.
        """
        if self._target_bed is not None:  # throw out needles that are on target bed already
            if not isinstance(self._target_bed, Machine_Bed_Position):
                raise Knit_Script_TypeError(f"Expected xfer to Front or Back Bed but got {self._target_bed}", self._source_statement)
            if self._target_bed is Machine_Bed_Position.Front:
                return [n for n in needles if n.is_back]
            else:
                return [n for n in needles if n.is_front]
        else:
            return needles
