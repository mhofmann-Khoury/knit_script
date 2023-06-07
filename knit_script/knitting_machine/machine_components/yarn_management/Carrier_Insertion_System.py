"""Representation of the carrier managing components of the machine"""
from typing import Dict, Optional, List

from knit_script.knit_graphs.Yarn import Yarn
from knit_script.knitting_machine.machine_components.machine_pass_direction import Pass_Direction
from knit_script.knitting_machine.machine_components.needles import Needle
from knit_script.knitting_machine.machine_components.yarn_management.Carrier import Carrier
from knit_script.knitting_machine.machine_components.yarn_management.Carrier_Set import Carrier_Set


class Carrier_Insertion_System:
    """
    Manages the Yarn inserting hook system and the yarn carriers
    ...

    Attributes
    ----------
    hook_position: Optional[int]
        the needle position of the yarn inserting hook. None if the hook is not active
    hooked_carriers: Carrier_Set
        The yarn carrier that is on the yarn inserting hook. None, if the hook is not active
    passes_since_releasehook: int
        The number of machine passes with carrier operations since the last releasehook operation.
        Will not tick up if the hook is not active

    """

    def __init__(self, carrier_count: int = 10, hook_size: int = 5):
        """
        :param carrier_count: The number of carriers on a machine, defaults to 10
        :param hook_size: the number of needles blocked by a yarn inserting hook.
            Todo, figure hook_size default empirically
        """
        self.carriers: Dict[int, Carrier] = {i: Carrier(i, Yarn(str(i))) for i in range(1, carrier_count + 1)}
        self.hook_position: Optional[int] = None
        self._searching_for_position: bool = False
        self.hooked_carriers: Optional[Carrier_Set] = None
        self._hook_size: int = hook_size
        self.passes_since_releasehook: int = 0

    @property
    def hook_size(self) -> int:
        """
        :return: The number of needles blocked to the right of the yarn inserting hook position
        """
        return self._hook_size

    def count_machine_pass(self):
        """
        Records a machine pass with yarn inserting hook still active.
        """
        if not self.inserting_hook_available:
            self.passes_since_releasehook += 1

    @property
    def inserting_hook_available(self) -> bool:
        """
        :return: True if the yarn inserting hook can be used
        """
        return self.hooked_carriers is None

    @property
    def active_carriers(self) -> List[int]:
        """
        :return: List of carrier id of carriers that are currently active (off the grippers)
        """
        return [cid for cid, c in self.carriers.items() if c.is_active]

    def conflicts_with_inserting_hook(self, needle: Needle, direction: Pass_Direction) -> bool:
        """
        :param direction:
        :param needle: the needle to check for compliance
        :return: True if inserting hook is conflicting with needle
        """
        if self.hook_position is not None:  # reserve positions to right of needle
            if direction is Pass_Direction.Leftward:
                inserting_hook_range = range(self.hook_position + 1, self.hook_position + self.hook_size)
            else:
                inserting_hook_range = range(self.hook_position - 1, self.hook_position - self.hook_size)
            return needle.position in inserting_hook_range
        else:  # no conflicts if hook is not active
            return False

    def on_grippers(self, carrier: Carrier_Set) -> bool:
        """
        :param carrier: carrier set to check for grippers
        :return: true if any carrier in carrier set is on the grippers
        """
        for cid in carrier.carrier_ids:
            if self[cid].on_gripper:
                return True
        return False

    def is_active(self, carrier: Carrier_Set) -> bool:
        """
        :param carrier:
        :return: True if the carrier (all carriers in set) are active (not-on the gripper)
        """
        return not self.on_grippers(carrier)

    def yarn_is_loose(self, carrier: Carrier_Set) -> bool:
        """
        :param carrier:
        :return: True if any yarn in yarn carrier set is loose (not on the inserting hook or tuck/knit on bed)
        """
        for cid in carrier.carrier_ids:
            if not self.carriers[cid].is_hooked and self.carriers[cid].yarn.last_needle() is None:
                return True  # yarn is not on inserting hook and has no needles for its loops
        return False

    def bring_in(self, carrier: Carrier_Set):
        """
        Brings in a yarn carrier without insertion hook (tail to gripper). Yarn is considered loose until knit
        :param carrier:
        """
        for cid in carrier.carrier_ids:
            if self[cid].yarn.last_needle() is None:
                print(f"Knit Script Warning: yarn {cid} is loose and may not knit correctly. Suggestion: Use inhook {cid}")
            self[cid].bring_in()

    def inhook(self, carrier: Carrier_Set):
        """
        Brings a yarn in with insertion hook. Yarn is not loose
        :param carrier:
        """
        assert self.inserting_hook_available, \
            f"Cannot inhook {carrier} while {self.hooked_carriers} is on yarn inserting hook"
        self.hooked_carriers = carrier
        self._searching_for_position = True
        self.hook_position = None
        self.bring_in(carrier)

    def releasehook(self):
        """
        Releases the yarn inserting hook of what ever is on it.
        """
        if self.hooked_carriers is not None:
            self.hooked_carriers.release_carriers(self)
        self.hooked_carriers = None
        self._searching_for_position = False
        self.hook_position = None
        self.passes_since_releasehook = 0

    def try_releasehook(self, recommended_passes_since_inhook: int = 2,
                        recommended_loops_since_release: int = 10) -> bool:
        """
        Checks if held yarns are ready to be released to bed needles, then releases insertion hook if criteria is met
        :param recommended_loops_since_release:
        :param recommended_passes_since_inhook: Number of knitting passes since inhook operation recommended for holding yarn
        :return:  True, if releasehook is recommended
        """
        if self.hooked_carriers is None:
            return False
        elif self.passes_since_releasehook >= recommended_passes_since_inhook:
            return True
        else:
            for carrier in self.hooked_carriers.get_carriers(self):
                if carrier.loops_since_release < recommended_loops_since_release:
                    return False
            return True

    def out(self, carrier: Carrier_Set):
        """
        Moves carrier to gripper, removing it from action but does not cut it loose
        :param carrier:
        """
        for cid in carrier.carrier_ids:
            self[cid].out()

    def outhook(self, carrier: Carrier_Set):
        """
        Cuts carrier yarn, moves it to grippers with insertion hook. Carrier will no longer be active and is now loose
        :param carrier:
        """
        assert self.inserting_hook_available, f"Cannot outhook {carrier} because inserting hook is holding {self.hooked_carriers}"
        for cid in carrier.carrier_ids:
            self[cid].outhook()

    def cut_all_yarns(self) -> List[str]:
        """
            Out hooks all active yarns, disconnecting piece from yarn carriers
        """
        carrier_operations = []
        if not self.inserting_hook_available:
            carrier_operations.append(f"releasehook {self.hooked_carriers}; Release inserting hook before outhooks\n")  # todo, unify knitout operation writing
            self.releasehook()
        for cid, carrier in self.carriers.items():
            if carrier.is_active:
                carrier.outhook()
                carrier_operations.append(f"outhook {cid}; Cut yarn {cid}, disconnecting knitted piece\n")  # todo, unify knitout operations
        return carrier_operations

    def make_loop(self, carrier: Carrier_Set, needle: Needle):
        """
        Establishes that yarn carrier has been used to make a loop at a given needle
        :param carrier:
        :param needle:
        """
        if self._searching_for_position:  # mark inserting hook position
            self.hook_position = needle.position
            self._searching_for_position = False
        for cid in carrier.carrier_ids:
            loop_id, loop = self[cid].yarn.add_loop_to_end()
            loop.put_on_needle(needle)

    def __getitem__(self, item: int) -> Carrier:
        return self.carriers[item]
