"""Instructions Expressions"""
from enum import Enum
from typing import Optional, Tuple, List, Union

from knit_script.knit_script_interpreter.expressions.expressions import Expression
from knit_script.knit_script_interpreter.knit_script_context import Knit_Script_Context
from knit_script.knitting_machine.Machine_State import Machine_State
from knit_script.knitting_machine.knitout_instructions import knit, tuck, xfer, split, miss, drop
from knit_script.knitting_machine.machine_components.machine_pass_direction import Pass_Direction
from knit_script.knitting_machine.machine_components.needles import Needle
from knit_script.knitting_machine.machine_components.yarn_carrier import Yarn_Carrier


class Needle_Instruction(Enum):
    """Instructions that operate on needles"""
    knit = "knit"
    xfer = "xfer"
    split = "split"
    miss = "miss"
    tuck = "tuck"
    drop = "drop"

    @staticmethod
    def get_instruction(inst_str: str):
        """
        Get the instruction from a string
        :param inst_str: instruction string to pull from
        :return: Needle_Instruction Object of that type
        """
        return Needle_Instruction[inst_str.lower()]

    @property
    def in_knitting_pass(self) -> bool:
        """
        :return: True if instruction can be done in a knit pass
        """
        return self in [Needle_Instruction.knit, Needle_Instruction.tuck]  # Todo: test miss and drop operations

    @property
    def all_needle_instruction(self) -> bool:
        """
        :return: True if instruction is compatible with all-needle knitting
        """
        return self.in_knitting_pass

    def compatible_pass(self, other_instruction):
        """
        Determine if instruction can share a machine pass
        :param other_instruction: Needle_Instruction to see if they match the pass type
        :return: True if both instructions could be executed in a pass
        """
        if self.in_knitting_pass and other_instruction.in_knitting_pass:
            return True
        else:
            return self is other_instruction

    @property
    def directed_pass(self) -> bool:
        """
        :return: True if instruction requires a direction
        """
        return self in [Needle_Instruction.knit, Needle_Instruction.tuck, Needle_Instruction.miss, Needle_Instruction.split]

    @property
    def requires_carrier(self) -> bool:
        """
        :return: True if instruction requires a direction
        """
        return self.directed_pass

    @property
    def requires_second_needle(self) -> bool:
        """
        :return: True if instruction requires second needle
        """
        return self in [Needle_Instruction.xfer, Needle_Instruction.split]

    @property
    def allow_sliders(self) -> bool:
        """
        :return: True if a xfer instruction that can operate on sliders
        """
        return self is Needle_Instruction.xfer

    def execute(self, machine_state: Machine_State, first_needle: Needle,
                direction: Optional[Pass_Direction] = None, carrier: Optional[Yarn_Carrier] = None,
                second_needle: Optional[Needle] = None) -> str:
        """
        Update machine state with knitout instruction with given parameters
        :param machine_state: current machine state to modify
        :param first_needle: the needle to operate on
        :param direction: optional direction for current pass
        :param carrier: optional carrier for instruction
        :param second_needle: optional second needle for xfers and splits
        :return: Knitout instruction
        """
        if first_needle.is_slider:
            assert self.allow_sliders, f"Cannot {self} on slider needle {first_needle}"
        if self.directed_pass:
            assert direction is not None, f"Cannot make {self} without a direction"
            assert carrier is not None, f"Cannot make {self} without a yarn carrier"
        if self.requires_second_needle:
            assert second_needle is not None, f"Cannot make {self} without destination needle"
        if self is Needle_Instruction.knit:
            return knit(machine_state, direction, first_needle, carrier)
        elif self is Needle_Instruction.tuck:
            return tuck(machine_state, direction, first_needle, carrier)
        elif self is Needle_Instruction.xfer:
            return xfer(machine_state, first_needle, second_needle)
        elif self is Needle_Instruction.split:
            return split(machine_state, direction, first_needle, second_needle, carrier)
        elif self is Needle_Instruction.miss:
            return miss(machine_state, direction, first_needle, carrier)
        elif self is Needle_Instruction.drop:
            assert direction is Pass_Direction.Left_to_Right_Increasing, "Cannot drop in decreasing pass"
            return drop(machine_state, first_needle)
        else:
            return ""


class Needle_Instruction_Exp(Expression):
    """
        Instructions that happen on a needle
    """

    def __init__(self, instruction: Union[Expression, Needle_Instruction], needles: Union[List[Expression], Expression]):
        """
        Instantiate
        :param instruction: the instruction to do to a needle set
        :param needles: the needles to do the instruction on
        """
        super().__init__()
        if not isinstance(needles, list):
            needles = [needles]
        self._needles = needles
        self._instruction = instruction

    def evaluate(self, context: Knit_Script_Context) -> Tuple[Needle_Instruction, List[Needle]]:
        """
        Evaluate the expression
        :param context: The current context of the knit_script_interpreter
        :return: The needle instruction of the expression
        """
        if isinstance(self._instruction, Needle_Instruction):
            instruction = self._instruction
        else:
            instruction = self._instruction.evaluate(context)
            assert isinstance(instruction, Needle_Instruction), f"Expected needle instruction (knit, tuck, miss, split, xfer, drop) but got {instruction}"
        needles = []
        for exp in self._needles:
            value = exp.evaluate(context)
            if isinstance(value, list):
                needles.extend(value)
            else:
                needles.append(value)
        for needle in needles:
            assert isinstance(needle, Needle), f"Expected List of needles, but got {needle} in {needles}"

        # Sort needles in current direction, warning if not correctly sorted
        # sorted_needles = context.current_direction.sort_needles(needles)
        return instruction, needles

    def __str__(self):
        return f"N_Inst({self._instruction} -> {self._needles})"

    def __repr__(self):
        return str(self)

class Machine_Instruction(Enum):
    """Enumerate of machine instructions"""
    pause = "pause"

    def allowed_mid_pass(self) -> bool:
        """
        :return: true if pause instruction which can be done without interrupting a machine pass
        """
        return self is Machine_Instruction.pause

    @staticmethod
    def get_instruction(inst_str: str):
        """
        Gets the machine instruction from a string
        :param inst_str: instruction string to pull from
        :return: Needle_Instruction Object of that type
        """
        return Machine_Instruction[inst_str.lower()]


class Machine_Instruction_Exp(Expression):
    """
        Expression evaluates to machine instructions
    """

    def __init__(self, inst_str: str):
        super().__init__()
        self.inst_str = inst_str

    def evaluate(self, context: Knit_Script_Context) -> Machine_Instruction:
        """
        :param context:
        :return: The carrier instruction of the expression
        """
        return Machine_Instruction.get_instruction(self.inst_str)
