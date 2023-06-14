from typing import List, Dict

from knit_script.knitout_interpreter.knitout_structures.knitout_instructions.needle_instructions import Knitout_Needle_Instruction
from knit_script.knitting_machine.machine_components.machine_pass_direction import Pass_Direction
from knit_script.knitting_machine.machine_components.needles import Needle


class Carriage_Pass_Collection:

    def __init__(self, first_instruction: Knitout_Needle_Instruction, racking: float):
        self.racking = racking
        self.direction = first_instruction.direction
        self.carrier_set = first_instruction.carrier_set
        self._needles_to_instruction: Dict[Needle, Knitout_Needle_Instruction] = {}
        self.instructions: List[Knitout_Needle_Instruction] = []
        self.add_to_pass(first_instruction)

    def has_needle(self, needle: Needle):
        return needle in self._needles_to_instruction

    @property
    def last_instruction(self) -> Knitout_Needle_Instruction:
        return self.instructions[-1]

    def can_add_to_pass(self, instruction: Knitout_Needle_Instruction) -> bool:
        if instruction.direction == self.direction and instruction.carrier_set == self.carrier_set:
            if self.has_needle(instruction.needle):  # multiple instructions on one needle triggers new pass
                return False
            if self.direction is not None:
                comp = self.last_instruction.needle.at_racking_comparison(instruction.needle, self.racking)
                if self.direction is Pass_Direction.Leftward and comp > 0:  # decreasing pass, last needle should be greater than the next needle
                    return True
                elif self.direction is Pass_Direction.Rightward and comp < 0:  # increasing pass, the last needle should be less than the next needle
                    return True
                else:
                    return False
            else:  # no direction for xfer pass so any assignment can be done as long as the needle is not in a list
                return True
        else:
            return False

    def add_to_pass(self, instruction: Knitout_Needle_Instruction):
        instruction.carriage_pass = self
        self.instructions.append(instruction)
        self._needles_to_instruction[instruction.needle] = instruction

    def sort_instructions(self, new_direction: Pass_Direction):
        sorted_needles = new_direction.sort_needles([*self._needles_to_instruction.keys()], self.racking)
        instructions = [self._needles_to_instruction[n] for n in sorted_needles]
        new_pass = Carriage_Pass_Collection(instructions[0], self.racking)
        self.direction = new_direction
        for instruction in instructions[1:]:
            new_pass.add_to_pass(instruction)
        return new_pass

    def __str__(self):
        string = ""
        for instruction in self.instructions:
            string += f"{instruction}\n"
        return string

    def __repr__(self):
        return str(self.instructions)

    def __iter__(self):
        return self.instructions

    def __getitem__(self, subscript):
        return self.instructions.__getitem__(subscript)

    def __hash__(self):
        return hash(self[0])
