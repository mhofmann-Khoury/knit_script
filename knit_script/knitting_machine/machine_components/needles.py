"""File used to manage Needles and Slider Needles"""
import math
from typing import Set, Iterable

from knit_script.knit_graphs.Loop import Loop

NEEDLE_OFFSET = 1


def set_needle_offset(offset: int):
    """
    Sets the offset from 0 for actual needle values
    :param offset: a positive number greater than 0
    """
    global NEEDLE_OFFSET
    NEEDLE_OFFSET = offset


class Needle:
    """
    A Simple class structure for keeping track of needle locations
    ...

    Attributes
    ----------
    held_loops: Set[Loop]
        The set of loops currently held on the needle
    """

    def __init__(self, is_front: bool, position: int):
        """
        instantiate a new needle
        :param is_front: True if front bed needle, False otherwise
        :param position: the needle index of this needle
        """
        self._is_front: bool = is_front
        self._position: int = int(position)
        assert self.position is not None
        self.held_loops: list[Loop] = []

    @property
    def is_front(self) -> bool:
        """
        :return: True if needle is on front bed
        """
        return self._is_front

    @property
    def position(self) -> int:
        """
        :return: The index on the machine bed of the needle
        """
        return self._position

    @property
    def has_loops(self) -> bool:
        """
        :return: True if needle is holding loops
        """
        return len(self.held_loops) > 0

    def add_loop(self, loop: Loop):
        """
        puts the loop in the set of currently held loops
        :param loop:
        """
        self.held_loops.append(loop)

    def add_loops(self, loops: Iterable[Loop]):
        """
        Adds loops to the held set
        :param loops:
        """
        for l in loops:
            self.add_loop(l)
            l.put_on_needle(self)

    def drop(self):
        """
        releases all held loops by resetting the loop-set
        """
        for l in self.held_loops:
            l.drop_from_needle()
        self.held_loops = []

    @property
    def is_back(self) -> bool:
        """
        :return: True if a needle is a back needle
        """
        return not self.is_front

    def opposite(self, slider: bool = False):
        """
        Return the needle on the opposite bed
        :param slider: If true, creates a slider needle
        :return: the needle on the opposite bed at the same position
        """
        if slider:
            return Slider_Needle(is_front=not self.is_front, position=self.position)
        else:
            return Needle(is_front=not self.is_front, position=self.position)

    def offset(self, offset: int, slider: bool = False):
        """
        Return a needle by the offset value
        :param slider: If true, creates a slider needle
        :param offset: the amount to offset the needle from
        :return: the needle offset spaces away on the same bed
        """
        if slider:
            return Slider_Needle(is_front=self.is_front, position=self.position + offset)
        else:
            return Needle(is_front=self.is_front, position=self.position + offset)

    def racked_position_on_front(self, rack: float) -> float:
        """
        Get the position of the needle on the front bed at a given racking
        :param rack: the racking value
        :return: The front needle position the needle given a racking (no change for front bed needles)
        """
        if self.is_front:
            return self.position
        else:
            return math.floor(self.position + rack)

    def slider(self):
        """
        :return: The slider needle at this position
        """
        return Slider_Needle(is_front=self.is_front, position=self.position)

    def main_needle(self):
        """
        :return: The non-slider needle at this needle positions
        """
        return Needle(is_front=self.is_front, position=self.position)

    def __str__(self):
        if self.is_front:
            return f"f{self.position}"
        else:
            return f"b{self.position}"

    def __repr__(self):
        return str(self)

    def __hash__(self):
        return self.position

    def __lt__(self, other) -> bool:
        if isinstance(other, Needle):
            if self.position < other.position:  # self is left of other
                return True
            elif other.position < self.position:  # other is left of self
                return False
            elif self.is_front and not other.is_front:  # self.position == other.position, front followed by back
                return True
            else:  # same positions, back followed by front or same side
                return False
        elif isinstance(other, int) or isinstance(other, float):
            return self.position < other
        else:
            raise AttributeError

    def __int__(self):
        return self.position

    def at_racking_comparison(self, other, rack: float = 0.0) -> int:
        """
        a comparison value between self and another needle at a given racking.
        :param other: the other needle to compare positions
        :param rack: racking value to compare between
        :return: 1 if self > other, 0 if equal, -1 self < other
        """
        assert isinstance(other, Needle)
        self_pos = self.racked_position_on_front(rack)
        other_pos = other.racked_position_on_front(rack)
        if self_pos < other_pos:
            return -1
        elif self_pos > other_pos:
            return 1
        else:  # same position at racking
            if self.is_front == other.is_front:  # same needle
                return 0
            elif self.is_front:  # self = fn other =bn fn->bn
                return -1
            else:
                return 1

    def __add__(self, other):
        position = other
        if isinstance(other, Needle):
            position = other.position
        return Needle(self.is_front, self.position + position)

    def __radd__(self, other):
        position = other
        if isinstance(other, Needle):
            position = other.position
        return Needle(self.is_front, position + self.position)

    def __sub__(self, other):
        position = other
        if isinstance(other, Needle):
            position = other.position
        return Needle(self.is_front, self.position - position)

    def __rsub__(self, other):
        position = other
        if isinstance(other, Needle):
            position = other.position
        return Needle(self.is_front, position - self.position)

    def __mul__(self, other):
        position = other
        if isinstance(other, Needle):
            position = other.position
        return Needle(self.is_front, self.position * position)

    def __rmul__(self, other):
        position = other
        if isinstance(other, Needle):
            position = other.position
        return Needle(self.is_front, position * self.position)

    def __truediv__(self, other):
        position = other
        if isinstance(other, Needle):
            position = other.position
        return Needle(self.is_front, self.position / position)

    def __rtruediv__(self, other):
        position = other
        if isinstance(other, Needle):
            position = other.position
        return Needle(self.is_front, position / self.position)

    def __floordiv__(self, other):
        position = other
        if isinstance(other, Needle):
            position = other.position
        return Needle(self.is_front, self.position // position)

    def __rfloordiv__(self, other):
        position = other
        if isinstance(other, Needle):
            position = other.position
        return Needle(self.is_front, position // position)

    def __mod__(self, other):
        position = other
        if isinstance(other, Needle):
            position = other.position
        return Needle(self.is_front, self.position % position)

    def __rmod__(self, other):
        position = other
        if isinstance(other, Needle):
            position = other.position
        return Needle(self.is_front, position % self.position)

    def __pow__(self, power, modulo=None):
        position = power
        if isinstance(power, Needle):
            position = power.position
        return Needle(self.is_front, self.position ** position)

    def __rpow__(self, power, modulo=None):
        position = power
        if isinstance(power, Needle):
            position = power.position
        return Needle(self.is_front, position ** self.position)

    def __lshift__(self, other):
        return self - other

    def __rshift__(self, other):
        return self + other

    def __rlshift__(self, other):
        return other - self

    def __rrshift__(self, other):
        return other + self

    @staticmethod
    def needle_at_racking_cmp(x, y, racking: float = 0.0) -> int:
        """
        :param x:
        :param y:
        :param racking:
        :return:
        """
        assert isinstance(x, Needle)
        return x.at_racking_comparison(y, racking)

    def greater_than_racking(self, other, rack: float = 0.0) -> bool:
        """
        Return a comparison ff self and the other needle at a given racking
        :param other: other needle to compare positions
        :param rack: racking value to compare between
        :return: True if this needle follows the other needle at current racking
        """
        assert isinstance(other, Needle)
        self_pos = self.racked_position_on_front(rack)
        other_pos = other.racked_position_on_front(rack)
        if self_pos > other_pos:
            return True
        if self_pos == other_pos:  # front needles less than back at all needle racking
            if self.is_front != other.is_front:  # front vs back
                decimal = rack - math.floor(rack)
                if decimal != 0:  # all needle racking
                    if other.is_front:
                        return True  # other on front at same position as self on back
        return False

    def __eq__(self, other):
        assert isinstance(other, Needle), f"Cannot compare needle equality to other types: {type(other)}"
        return self.is_front == other.is_front and self.is_slider == other.is_slider and self.position == other.position

    @property
    def is_slider(self) -> bool:
        """
        :return: True if the needle is a slider
        """
        return False

    def is_clear(self, machine_state) -> bool:
        """
        a needle is clear if it is a sliding needle or if its associated slider needle is empty
        :param machine_state: used to get slider needle
        :return: True if needle is clear
        """
        slider = self.slider()
        slider_ = machine_state[slider]
        return not slider_.has_loops


class Slider_Needle(Needle):
    """
    A Needle subclass for slider needles which an only transfer loops, but not be knit through
    """

    def __init__(self, is_front: bool, position: int):
        super().__init__(is_front, position)

    def __str__(self):
        if self.is_front:
            return f"fs{self.position}"
        else:
            return f"bs{self.position}"

    @property
    def is_slider(self) -> bool:
        """
        :return: True if the needle is a slider
        """
        return True

    def is_clear(self, machine_state):
        """
        a needle is clear if it is a sliding needle or if its associated slider needle is empty
        :param machine_state: not used by slider
        :return: True if needle is clear
        """
        return True

    def __add__(self, other):
        position = other
        if isinstance(other, Needle):
            position = other.position
        return Slider_Needle(self.is_front, self.position + position)

    def __radd__(self, other):
        position = other
        if isinstance(other, Needle):
            position = other.position
        return Slider_Needle(self.is_front, position + self.position)

    def __sub__(self, other):
        position = other
        if isinstance(other, Needle):
            position = other.position
        return Slider_Needle(self.is_front, self.position - position)

    def __rsub__(self, other):
        position = other
        if isinstance(other, Needle):
            position = other.position
        return Slider_Needle(self.is_front, position - self.position)

    def __mul__(self, other):
        position = other
        if isinstance(other, Needle):
            position = other.position
        return Slider_Needle(self.is_front, self.position * position)

    def __rmul__(self, other):
        position = other
        if isinstance(other, Needle):
            position = other.position
        return Slider_Needle(self.is_front, position * self.position)

    def __truediv__(self, other):
        position = other
        if isinstance(other, Needle):
            position = other.position
        return Slider_Needle(self.is_front, self.position / position)

    def __rtruediv__(self, other):
        position = other
        if isinstance(other, Needle):
            position = other.position
        return Slider_Needle(self.is_front, position / self.position)

    def __floordiv__(self, other):
        position = other
        if isinstance(other, Needle):
            position = other.position
        return Slider_Needle(self.is_front, self.position // position)

    def __rfloordiv__(self, other):
        position = other
        if isinstance(other, Needle):
            position = other.position
        return Slider_Needle(self.is_front, position // position)

    def __mod__(self, other):
        position = other
        if isinstance(other, Needle):
            position = other.position
        return Slider_Needle(self.is_front, self.position % position)

    def __rmod__(self, other):
        position = other
        if isinstance(other, Needle):
            position = other.position
        return Slider_Needle(self.is_front, position % self.position)

    def __pow__(self, power, modulo=None):
        position = power
        if isinstance(power, Needle):
            position = power.position
        return Slider_Needle(self.is_front, self.position ** position)

    def __rpow__(self, power, modulo=None):
        position = power
        if isinstance(power, Needle):
            position = power.position
        return Slider_Needle(self.is_front, position ** self.position)
