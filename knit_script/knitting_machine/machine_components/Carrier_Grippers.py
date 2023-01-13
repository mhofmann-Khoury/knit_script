"""Representation of the carrier managing components of the machine"""
from typing import Dict, Optional, List

from knit_script.knitting_machine.machine_components.machine_pass_direction import Pass_Direction
from knit_script.knitting_machine.machine_components.needles import Needle
from knit_script.knitting_machine.machine_components.yarn_carrier import Yarn_Carrier


class Carrier_Insertion_System:
    """
    Manages the Yarn inserting hook system and the yarn carriers
    ...

    Attributes
    ----------
    carriers_on_grippers: Dict[int, bool]
        Represents which carriers (1-10) are on the grippers. The grippers prevent a yarn from being used
    loose_yarns: Dict[int, bool]
        Loose yarns are yarns that are not currently connected to a needle or the inserting hook.
        indexes of carriers -> boolean representing if carrier is loose
    yarns_last_needle: Dict[int, Optional[Needle]]
        index of carriers -> needle that last held this yarn. Will be None if the yarn has no connected needle
    yarns_to_loop_count: Dict[int, int]
        index of carriers -> number of loops that have been made on this yarn since last cut
    hook_position: Optional[int]
        the needle position of the yarn inserting hook. None if the hook is not active
    hooked_carrier: Yarn_Carrier
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
        self.carriers_on_grippers: Dict[int, bool] = {i: True for i in range(1, carrier_count + 1)}
        self.loose_yarns: Dict[int, bool] = {i: False for i in range(1, carrier_count + 1)}
        self.yarns_last_needle: Dict[int, Optional[Needle]] = {i: None for i in range(1, carrier_count + 1)}
        self.yarns_to_loop_count: Dict[int, int] = {i: 0 for i in range(1, carrier_count + 1)}
        self.hook_position: Optional[int] = None
        self._searching_for_position: bool = False
        self.hooked_carrier: Optional[Yarn_Carrier] = None
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
        return self.hooked_carrier is None

    @property
    def active_carriers(self) -> List[int]:
        return [c for c, is_active in self.carriers_on_grippers if is_active]

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

    def on_grippers(self, carrier: Yarn_Carrier) -> bool:
        """
        :param carrier: carrier set to check for grippers
        :return: true if any carrier in carrier set is on the grippers
        """
        for yid in carrier.carrier_ids:
            if self.carriers_on_grippers[yid]:
                return True
        return False

    def is_active(self, carrier: Yarn_Carrier) -> bool:
        """
        :param carrier:
        :return: True if the carrier (all carriers in set) are active (not-on the gripper)
        """
        return not self.on_grippers(carrier)

    def yarn_is_loose(self, carrier: Yarn_Carrier) -> bool:
        """
        :param carrier:
        :return: True if any yarn in yarn carrier set is loose (not on the inserting hook or tuck/knit on bed)
        """
        for yid in carrier.carrier_ids:
            if self.yarns_last_needle[yid] is None:
                if self.hooked_carrier is None or yid not in self.hooked_carrier.carrier_ids:
                    # yarn isn't loose if it's on the hooked carrier
                    return True
        return False

    def bring_in(self, carrier: Yarn_Carrier):
        """
        Brings in a yarn carrier without insertion hook (tail to gripper). Yarn is considered loose until knit
        :param carrier:
        """
        for yid in carrier.carrier_ids:
            if self.loose_yarns[yid]:
                print(f"Knit Script Warning: yarn {yid} is loose and may not knit correctly. Suggestion: Use inhook {yid}")
            self.carriers_on_grippers[yid] = False

    def inhook(self, carrier: Yarn_Carrier):
        """
        Brings a yarn in with insertion hook. Yarn is not loose
        :param carrier:
        """
        assert self.inserting_hook_available, \
            f"Cannot inhook {carrier} while {self.hooked_carrier} is on yarn inserting hook"
        self.hooked_carrier = carrier
        self._searching_for_position = True
        self.hook_position = None
        self.bring_in(carrier)

    def releasehook(self):
        """
        Releases the yarn inserting hook of what ever is on it.
        """
        if self.hooked_carrier is not None:
            self.hooked_carrier.release_carrier()
        self.hooked_carrier = None
        self._searching_for_position = False
        self.hook_position = None
        self.passes_since_releasehook = 0

    def try_releasehook(self, recommended_passes_since_inhook: int = 2,
                        recommended_loops_since_release: int = 10) -> bool:
        """
        Checks if held yarns are ready to be released to bed needles, then releases insertion hook if criteria is met
        :param recommended_loops_since_release:
        :param recommended_passes_since_inhook: number of knitting passes since inhook operation recommended for holding yarn
        :return:  True, if releasehook is recommended
        """
        if self.hooked_carrier is None:
            return False
        elif self.passes_since_releasehook >= recommended_passes_since_inhook:
            return True
        elif self.hooked_carrier.loops_since_release >= recommended_loops_since_release:
            return True
        return False

    def out(self, carrier: Yarn_Carrier):
        """
        Moves carrier to gripper, removing it from action but does not cut it loose
        :param carrier:
        """
        assert self.is_active(carrier), f"Cannot bring {carrier} out of action because it is not in action"
        for yid in carrier.carrier_ids:
            self.carriers_on_grippers[yid] = True

    def outhook(self, carrier: Yarn_Carrier):
        """
        Cuts carrier yarn, moves it to grippers with insertion hook. Carrier will no longer be active and is now loose
        :param carrier:
        """
        assert self.inserting_hook_available, f"Cannot outhook {carrier} because inserting hook is holding {self.hooked_carrier}"
        assert self.is_active(carrier), f'Cannot cut inactive yarn carrier {carrier}'
        self.out(carrier)
        self.releasehook()  # will use hook then release it after out operations, removing any prior state
        for yid in carrier.carrier_ids:  # Cut yarns have not last_needle position and are considered loose
            self.yarns_last_needle[yid] = None
            self.yarns_to_loop_count[yid] = 0  # cut yarns restart their loop count

    def cut_all_yarns(self) -> List[str]:
        """
            Out hooks all active yarns, disconnecting piece from yarn carriers
        """
        outhooks = []
        if not self.inserting_hook_available:
            outhooks.append(f"releasehook {self.hooked_carrier}; Release inserting hook before outhooks\n")
            self.releasehook()
        for i, on_gripper in self.carriers_on_grippers.items():
            if not on_gripper:
                self.outhook(Yarn_Carrier(i))
                outhooks.append(f"outhook {i}; Cut yarn {i}, disconnecting knitted piece\n")
        return outhooks

    def make_loop(self, carrier: Yarn_Carrier, needle: Needle):
        """
        Establishes that yarn carrier has been used to make a loop at a given needle
        :param carrier:
        :param needle:
        """
        if self._searching_for_position:  # mark inserting hook position
            self.hook_position = needle.position
            self._searching_for_position = False
        for yid in carrier.carrier_ids:
            self.yarns_to_loop_count[yid] += 1
