"""Collection of instructions in a shared carriage pass"""

from knit_script.knitout_interpreter.knitout_structures.knitout_instructions.Rack_Instruction import Rack_Instruction
from knit_script.knitout_interpreter.knitout_structures.knitout_instructions.instruction import Instruction_Type
from knit_script.knitout_interpreter.knitout_structures.knitout_instructions.needle_instructions import Knitout_Needle_Instruction
from knit_script.knitting_machine.machine_components.machine_pass_direction import Pass_Direction
from knit_script.knitting_machine.machine_components.needles import Needle


class Carriage_Pass_Instructions:
    """
        A collection of Knitout instructions associated with a carriage pass
    """

    def __init__(self, first_instruction: Knitout_Needle_Instruction, racking: float, index: int | None = None):
        self.index = index
        self.racking = racking
        self.direction: Pass_Direction = first_instruction.direction
        self.carrier_set = first_instruction.carrier_set
        self._needles_to_instruction: dict[Needle, Knitout_Needle_Instruction] = {}
        self._instruction_type_to_needles: dict[Instruction_Type: list[Needle]] = {}
        self.instructions: list[Knitout_Needle_Instruction] = []
        self.add_to_pass(first_instruction)

    @property
    def implied_direction(self) -> Pass_Direction:
        """
        :return: The implied carriage pass direction based on yarn direction or xfer order
        """
        if self.direction is not None:
            return self.direction
        if len(self.instructions) < 2:  # default to leftward pass
            return Pass_Direction.Leftward
        else:
            if self.instructions[0].needle < self.instructions[1].needle:  # increasing
                return Pass_Direction.Rightward
            else:
                return Pass_Direction.Leftward

    @property
    def is_xfer_pass(self) -> bool:
        """
        :return: True if this is a transfer pass
        """
        return Instruction_Type.Xfer in self._instruction_type_to_needles

    def rack_instruction(self) -> Rack_Instruction:
        """
        :return: Rack instruction to set racking for this carriage_pass
        """
        return Rack_Instruction(self.racking)

    def has_needle(self, needle: Needle):
        """
        :param needle:
        :return: An operation starts on the given needle
        """
        return needle in self._needles_to_instruction

    def can_add_to_pass(self, instruction: Knitout_Needle_Instruction) -> bool:
        """
        :param instruction:
        :return: True, if the instruction could come next in this carriage pass
        """
        if instruction.direction == self.direction and instruction.carrier_set == self.carrier_set:
            if self.is_xfer_pass:
                return True  # combine all xfers at same rack into same carriage pass
            else:  # carriage pass involves a yarn
                if self.has_needle(instruction.needle):  # multiple instructions on one needle triggers new pass
                    return False
                comp = self.instructions[-1].needle.at_racking_comparison(instruction.needle, self.racking)
                if self.direction is Pass_Direction.Leftward and comp > 0:  # decreasing pass, last needle should be greater than the next needle
                    return True
                elif self.direction is Pass_Direction.Rightward and comp < 0:  # increasing pass, the last needle should be less than the next needle
                    return True
                else:
                    return False
        else:
            return False

    def clean_xfer_pass(self, sort_direction):
        """
        Cleans this carriage pass of redundant and no-op xfers
        :return: None
        """
        if not self.is_xfer_pass:
            return
        start_needles_to_xfer = {}
        for xfer in self.instructions:
            if xfer.needle_2 in start_needles_to_xfer:  # cancels out transfer
                del start_needles_to_xfer[xfer.needle_2]
            else:
                start_needles_to_xfer[xfer.needle] = xfer

        self.direction = None
        self.carrier_set = None
        self._needles_to_instruction: dict[Needle, Knitout_Needle_Instruction] = start_needles_to_xfer
        self._instruction_type_to_needles: dict[Instruction_Type: list[Needle]] = {Instruction_Type.Xfer: [*start_needles_to_xfer.values()]}
        sorted_needles = sort_direction.sort_needles([*start_needles_to_xfer.keys()], self.racking)
        self.instructions: list[Knitout_Needle_Instruction] = [start_needles_to_xfer[n] for n in sorted_needles]

    def add_to_pass(self, instruction: Knitout_Needle_Instruction):
        """
        Adds the instruction into the carriage pass
        :param instruction:
        """
        instruction.carriage_pass = self
        self.instructions.append(instruction)
        self._needles_to_instruction[instruction.needle] = instruction
        if instruction.instruction_type not in self._instruction_type_to_needles:
            self._instruction_type_to_needles[instruction.instruction_type] = []
        self._instruction_type_to_needles[instruction.instruction_type].append(instruction.needle)

    def sort_instructions(self, new_direction: Pass_Direction):
        """
        Sorts the instructions by the given direction.
        :param new_direction:
        :return: The sorted carriage pass
        """
        sorted_needles = new_direction.sort_needles([*self._needles_to_instruction.keys()], self.racking)
        instructions = [self._needles_to_instruction[n] for n in sorted_needles]
        new_pass = Carriage_Pass_Instructions(instructions[0], self.racking)
        self.direction = new_direction
        for instruction in instructions[1:]:
            new_pass.add_to_pass(instruction)
        return new_pass

    def __str__(self):
        string = ""
        indent = ""
        if self.direction is not None:
            string = f"in {self.direction} direction:"
            if len(self._instruction_type_to_needles) > 1:
                indent = "\t"
                string += "\n"
        for instruction_type, needles in self._instruction_type_to_needles.items():
            string += f"{indent}{instruction_type.value} {needles} with {self.carrier_set}\n"
        return string

    def id_str(self) -> str:
        """
        :return: string with original line number added if present
        """

        if self.index is not None:
            return f"{self.index}:{self}"
        else:
            return str(self)

    def __repr__(self):
        return str(self.instructions)

    def __iter__(self):
        return iter(self.instructions)

    def __getitem__(self, subscript):
        return self.instructions.__getitem__(subscript)

    def __hash__(self):
        if self.index is not None:
            return self.index
        return hash(self[0])
