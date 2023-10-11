from knit_script.knitout_interpreter.DAT_Compiler.Knitting_Operation import Knitting_Operation
from knit_script.knitout_interpreter.DAT_Compiler.OP_Line import OP_Line
from knit_script.knitout_interpreter.knitout_structures.knitout_instructions.Pass_Setting_Instruction import Pass_Setting_Instruction
from knit_script.knitout_interpreter.knitout_structures.knitout_instructions.Rack_Instruction import Rack_Instruction
from knit_script.knitout_interpreter.knitout_structures.knitout_instructions.carrier_instructions import Carrier_Instruction
from knit_script.knitout_interpreter.knitout_structures.knitout_instructions.knitout_instruction import Knitout_Instruction
from knit_script.knitout_interpreter.knitout_structures.knitout_instructions.needle_instructions import Knitout_Needle_Instruction, Drop_Instruction, Knit_Instruction, Tuck_Instruction
from knit_script.knitting_machine.machine_components.machine_pass_direction import Pass_Direction


class DAT_Carriage_Pass:
    """
    Keeps track of one line of a DAT file representing a carriage pass
    """
    Program_Spacing = 4
    Side_Spacing = 8

    def __init__(self, needles_to_operation: dict[int, Knitting_Operation] | None = None, settings: dict[OP_Line, int] | None = None):
        if needles_to_operation is None:
            needles_to_operation = {}
        if settings is None:
            settings = {}
        self.needles_to_operation: dict[int, Knitting_Operation] = needles_to_operation
        self.settings: dict[OP_Line, int] = settings

    @property
    def carrier_was_set(self) -> bool:
        """
        :return: True if the carrier was set for this pass
        """
        return OP_Line.Carrier_Combination in self.settings

    @property
    def carrier_set(self) -> int:
        """
        :return: carrier set number for the pass. Defaults to 0
        """
        if self.carrier_was_set:
            return self.settings[OP_Line.Carrier_Combination]
        else:
            return 0

    @carrier_set.setter
    def carrier_set(self, carrier_number: int):
        if not self.carrier_was_set:
            self.settings[OP_Line.Carrier_Combination] = carrier_number
        else:
            assert self.carrier_set == carrier_number, \
                f"Cannot use carriers sets {self.carrier_set} and {carrier_number} in same pass"

    @property
    def direction_was_set(self) -> bool:
        """
        :return: True if direction was set for this pass
        """
        return OP_Line.Direction_Line_Left in self.settings

    @property
    def direction(self) -> int:
        """
        :return: direction value defaults to 1 for no specified direction
        """
        if not self.direction_was_set:
            return 1
        else:
            return self.settings[OP_Line.Direction_Line_Left]

    @direction.setter
    def direction(self, value: Pass_Direction | None):
        if value is None:
            value = 1
        elif value is Pass_Direction.Leftward:
            value = 7
        else:
            value = 6
        if self.direction_was_set:
            assert self.direction == value, f"Cannot go both {self.direction} and {value} directions in same pass"
        self.settings[OP_Line.Direction_Line_Left] = value
        self.settings[OP_Line.Direction_Line_Right] = value

    @property
    def racking(self) -> float:
        """
        :return: racking implied by current racking settings
        """
        if OP_Line.Racking_Offset in self.settings:
            rack = self.settings[OP_Line.Racking_Offset]
        else:
            rack = 0
        if OP_Line.Racking_Pitch in self.settings:
            rack += .25 * self.settings[OP_Line.Racking_Pitch]
        if (OP_Line.Racking_Left_Right in self.settings
                and self.settings[OP_Line.Racking_Left_Right] == Rack_Instruction.LEFT_RACK):
            rack *= -1
        return rack

    def add_knitout_operation(self, knitout_line: Knitout_Instruction):
        """
        Update carriage pass by knitout instruction.
        Assumes operations happen in this pass without overriding prior knitting operations
        :param knitout_line:
        """
        if isinstance(knitout_line, Knitout_Needle_Instruction):
            # set operation lines
            if knitout_line.carrier_set is not None:
                self.carrier_set = knitout_line.carrier_number()
            self.direction = knitout_line.direction
            if isinstance(knitout_line, Drop_Instruction):
                self.settings[OP_Line.Drop_Failure] = 11
            first_needle_front_position = knitout_line.needle.racked_position_on_front(self.racking)
            if knitout_line.needle_2 is not None:
                assert first_needle_front_position == knitout_line.needle_2.racked_position_on_front(self.racking), \
                    f"Racking {self.racking} does not support operations from {knitout_line.needle} to {knitout_line.needle_2}"
            operation = knitout_line.needle_operation_value
            if first_needle_front_position in self.needles_to_operation:  # already used this position
                current_op = self.needles_to_operation[first_needle_front_position]
            else:
                if isinstance(knitout_line, Knit_Instruction):
                    if knitout_line.needle.is_front:
                        self.needles_to_operation[first_needle_front_position] = Knitting_Operation.Knit_Front
                    else:
                        self.needles_to_operation[first_needle_front_position] = Knitting_Operation.Knit_Back
                elif isinstance(knitout_line, Tuck_Instruction):
                    if knitout_line.needle.is_front:
                        self.needles_to_operation[first_needle_front_position] = Knitting_Operation.Tuck_Front
                    else:
                        self.needles_to_operation[first_needle_front_position] = Knitting_Operation.Tuck_Back
                elif isinstance(knitout_line, Drop_Instruction):
                    if knitout_line.needle.is_front:
                        self.needles_to_operation[first_needle_front_position] = Knitting_Operation.Drop_Front
                    else:
                        self.needles_to_operation[first_needle_front_position] = Knitting_Operation.Drop_Back
                elif isinstance(knitout_line, Drop_Instruction):
                    if knitout_line.needle.is_front:
                        self.needles_to_operation[first_needle_front_position] = Knitting_Operation.Drop_Front
                    else:
                        self.needles_to_operation[first_needle_front_position] = Knitting_Operation.Drop_Back

            pass  # set by racking, operations at position
        elif isinstance(knitout_line, Carrier_Instruction):
            self.settings[OP_Line.Carrier_Combination] = knitout_line.carrier_number()
            self.settings[OP_Line.Yarn_IN_Out] = knitout_line.yarn_in_out_value()
            self.settings[OP_Line.Yarn_Holding_Hook] = knitout_line.yarn_holding_value()
            self.settings[OP_Line.Yarn_Inserting_Hook] = knitout_line.yarn_inserting_hook_value()
        elif isinstance(knitout_line, Pass_Setting_Instruction):
            self.settings[knitout_line.op_line] = knitout_line.op_code_value()
        elif isinstance(knitout_line, Rack_Instruction):
            self.settings[OP_Line.Racking_Offset] = knitout_line.racking_offset()
            self.settings[OP_Line.Racking_Pitch] = knitout_line.racking_alignment()
            self.settings[OP_Line.Racking_Left_Right] = knitout_line.racking_direction()

    def dat_image_line(self, program_width: int, first_needle_pos: int = 0,
                       left_spacing: int = 8, right_spacing: int = 8, program_padding: int = 4) -> tuple[list[int], int, int, int]:
        """

        :param program_width: width of overall program to add additional padding to.
        :param first_needle_pos: The first needle position to compare this program to.
        :param left_spacing: Spacing of empty information on the left side of the whole program.
        :param right_spacing: Spacing of empty information on the right side of the whole program.
        :param program_padding: Spacing of empty information between operation lines and needle operations.
        :return: A list of integers representing this line in the DAT program, the index where left side operations start, the index where body operations start, the index where right side operations start
        """
        image = [0 for _ in range(0, left_spacing)]
        left_op_start = len(image)
        image.extend(self._operations(is_left=True))
        body_op_start = len(image)
        image.extend([0 for _ in range(0, program_padding)])
        image.extend(self._body_operations(program_width, first_needle_pos))
        image.extend([0 for _ in range(0, program_padding)])
        right_op_start = len(image)
        image.extend(self._operations(is_left=False))
        image.extend([0 for _ in range(0, right_spacing)])
        return image, left_op_start, body_op_start, right_op_start

    def _operations(self, is_left=True) -> list[int]:
        ops = []
        if is_left:
            op_range = range(-20, 0)
        else:
            op_range = range(1, 21)
        for op_code in op_range:
            ops.append(op_code)
            op_type = OP_Line.get_enum(op_code)
            if op_type in self.settings:
                ops.append(self.settings[op_type])
            else:
                ops.append(0)
        return ops

    def _body_operations(self, width: int, first_needle_pos: int = 0, add_misses=True) -> list[int]:
        needles: list[int] = self.sorted_needles()
        assert needles[0] >= first_needle_pos, f"Program should start at f{first_needle_pos} on left but first needle with operation is {needles[0]}"
        ops = [0 for _ in range(first_needle_pos, needles[0] - 1)]  # left program padding
        ops.append(Knitting_Operation.Boundary.value)  # left boundary
        for needle in range(needles[0], needles[-1]):
            if needle in self.needles_to_operation:
                ops.append(int(self.needles_to_operation[needle]))
            elif add_misses:
                ops.append(int(Knitting_Operation.Miss))
            else:
                ops.append(0)
        ops.append(Knitting_Operation.Boundary.value)  # right boundary
        assert len(ops) <= width, f"Program ({len(ops)} is greater than given width {width}"
        while len(ops) < width:  # right padding
            ops.append(0)
        return ops

    def sorted_needles(self) -> list[int]:
        """
        :return: list of needles to operate on sorted from lowest to highest position
        """
        return sorted(*self.needles_to_operation.keys())

    @property
    def needle_count(self) -> int:
        """
        :return: Number of needles included in the carriage pass
        """
        return len(self.needles_to_operation)
