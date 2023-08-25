from typing import Optional

from knit_script.knit_graphs.Yarn import Yarn
from knit_script.knitting_machine.machine_components.needles import Needle


class Carrier:
    """
        Carrier on a knitting machine
    """

    def __init__(self, carrier_id: int, yarn: Optional[Yarn]):
        self._carrier_id: int = carrier_id
        if yarn is None:
            self.yarn: Yarn = Yarn(str(self._carrier_id))
        else:
            self.yarn: Yarn = yarn
        self._is_active: bool = False
        self._is_hooked: bool = False
        self._position: Optional[int] = None
        self._loops_since_release: int = 0

    @property
    def position(self) -> Optional[int]:
        """
        :return: The needle position that the carrier sits at or None if the carrier is not active
        """
        return self._position

    @position.setter
    def position(self, new_position: Optional[Needle | int]):
        if new_position is None:
            self._position = None
        else:
            self._position = int(new_position)

    @property
    def loops_since_release(self) -> int:
        """
        :return: Loops made since release from yarn inserting hook
        """
        return self._loops_since_release

    def count_loop(self):
        self._loops_since_release += 1

    @property
    def is_active(self) -> bool:
        """
        :return: True if active
        """
        return self._is_active

    @is_active.setter
    def is_active(self, active_state: bool):
        if active_state is True:
            self._is_active = True
        else:
            self._is_active = False
            self.is_hooked = False
            self.position = None
            self._loops_since_release = 0

    @property
    def on_gripper(self) -> bool:
        """
        :return: True if carrier is held on grippers
        """
        return not self.is_active

    @property
    def is_hooked(self) -> bool:
        """
        :return: True if connected to inserting hook
        """
        return self._is_hooked

    @is_hooked.setter
    def is_hooked(self, hook_state: bool):
        if self.is_hooked != hook_state:  # change hook state
            self._loops_since_release = 0
        if hook_state is True:
            self._is_hooked = True
        else:
            self._is_hooked = False

    def bring_in(self):
        """
            Record in operation
        """
        self.is_active = True

    def inhook(self):
        """
            Record inhook operation
        """
        self.is_active = True
        self.is_hooked = True

    def releasehook(self):
        """
            Record release hook operation
        """
        self.is_hooked = False

    def out(self):
        """
            Record out operation
        """
        self.is_active = False

    def outhook(self):
        """
            Record outhook operation
        """
        self.is_active = False
        self.yarn = self.yarn.cut_yarn()

    @property
    def carrier_id(self) -> int:
        """
        :return: id of carrier, corresponds to order in machine
        """
        return self._carrier_id

    def __lt__(self, other):
        return hash(self) < hash(other)

    def __hash__(self):
        return self.carrier_id

    def __str__(self):
        if self.yarn.yarn_id == str(self._carrier_id):
            return str(self.carrier_id)
        else:
            return f"{self.carrier_id}:{self.yarn}"

    def __repr__(self):
        return str(self)
