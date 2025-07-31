"""Module containing the Sheet class"""
from __future__ import annotations

from typing import cast

from virtual_knitting_machine.Knitting_Machine import Knitting_Machine
from virtual_knitting_machine.machine_components.needles.Needle import Needle
from virtual_knitting_machine.machine_components.needles.Sheet_Needle import Sheet_Needle, Slider_Sheet_Needle
from virtual_knitting_machine.machine_components.needles.Slider_Needle import Slider_Needle

from knit_script.knit_script_exceptions import Sheet_Value_Exception


class Sheet:
    """Record of the position of loops on a sheet defined by the current gauging schema."""

    def __init__(self, sheet_number: int, gauge: int, knitting_machine: Knitting_Machine):
        self.knitting_machine = knitting_machine
        if sheet_number < 0 or sheet_number > gauge:
            raise Sheet_Value_Exception(sheet_number, gauge)
        self.gauge = gauge
        self.sheet_number = sheet_number
        # in-sheet needle position -> Recorded loop on Front, Recorded loop on Back
        self.loop_record: dict[int, tuple[bool, bool]] = {f.position: (f.has_loops, b.has_loops) for f, b in zip(self.front_needles(), self.back_needles())}
        # self.loop_record: dict[int, tuple[bool, bool]] = {n: (False, False) for n in range(0, int(self.knitting_machine.needle_count / self.gauge))}

    def record_needle(self, sheet_needle: Sheet_Needle) -> None:
        """Record the state of the given sheet needle and its opposite needle.

        Args:
            sheet_needle (Sheet_Needle): The sheet needle to record.
        """
        actual_needle = self.knitting_machine[sheet_needle]
        opposite_needle = self.knitting_machine[actual_needle.opposite()]
        if actual_needle.is_front:
            self.loop_record[sheet_needle.position] = actual_needle.has_loops, opposite_needle.has_loops
        else:
            self.loop_record[sheet_needle.position] = opposite_needle.has_loops, actual_needle.has_loops

    def record_sheet(self) -> None:
        """Record the loop locations for needles in the sheet given the current state of the knitting machine."""
        new_record = {n: (self.knitting_machine[self.sheet_needle(True, n)].has_loops,
                          self.knitting_machine[self.sheet_needle(False, n)].has_loops)
                      for n in self.loop_record.keys()}
        self.loop_record = new_record

    def sheet_needle(self, is_front: bool, in_sheet_position: int, is_slider: bool = False) -> Sheet_Needle:
        """Get a Sheet_Needle from this sheet set with the given parameters.

        Args:
            is_front (bool): If True, return a needle on the front bed. Otherwise, return a back-bed needle.
            in_sheet_position (int): The position of the needle relative to the sheet (not the actual needle bed).
            is_slider (bool, optional): If True, return a slider needle. Otherwise, return a standard needle.

        Returns:
            Sheet_Needle: A Sheet_Needle from this sheet set with the given parameters.
        """
        if is_slider:
            return Slider_Sheet_Needle(is_front, in_sheet_position, self.sheet_number, self.gauge)
        return Sheet_Needle(is_front, in_sheet_position, self.sheet_number, self.gauge)

    def get_matching_sheet_needle(self, other_sheet_needle: Sheet_Needle) -> Sheet_Needle:
        """Get a sheet needle belonging to this sheet at the same sheet position as a given sheet needle.

        Args:
            other_sheet_needle (Sheet_Needle): The sheet needle to find a match to in this sheet.

        Returns:
            Sheet_Needle: A sheet needle belonging to this sheet at the same sheet position as a given sheet needle.
        """
        return self.sheet_needle(other_sheet_needle.is_front, other_sheet_needle.sheet_pos, isinstance(other_sheet_needle, Slider_Sheet_Needle))

    def __eq__(self, other: Sheet | int) -> bool:
        if isinstance(other, Sheet):
            return self.sheet_number == other.sheet_number and self.gauge == other.gauge
        elif isinstance(other, int):
            return self.sheet_number == other
        assert False, f'Expected Sheet or integer but got {other}'

    def front_needles(self) -> list[Needle]:
        """Get the set of front bed needles on the machine that belong to the given sheet.

        Returns:
            list[Needle]: The set of front bed needles on the machine that belong to the given sheet.
        """
        machine_needles = cast(list[Needle], self.knitting_machine.front_needles())
        return machine_needles[self.sheet_number::self.gauge]

    def back_needles(self) -> list[Needle]:
        """Get the set of back bed needles on the machine that belong to the given sheet.

        Returns:
            list[Needle]: The set of back bed needles on the machine that belong to the given sheet.
        """
        machine_needles = cast(list[Needle], self.knitting_machine.back_needles())
        return machine_needles[self.sheet_number::self.gauge]

    def front_sliders(self) -> list[Slider_Needle]:
        """Get the set of front bed slider needles on the machine that belong to the given sheet.

        Returns:
            list[Slider_Needle]: The set of front bed slider needles on the machine that belong to the given sheet.
        """
        machine_needles = cast(list[Slider_Needle], self.knitting_machine.front_sliders())
        return machine_needles[self.sheet_number::self.gauge]

    def back_sliders(self) -> list[Slider_Needle]:
        """Get the set of back bed slider needles on the machine that belong to the given sheet.

        Returns:
            list[Slider_Needle]: The set of back bed slider needles on the machine that belong to the given sheet.
        """
        machine_needles = cast(list[Slider_Needle], self.knitting_machine.back_sliders())
        return machine_needles[self.sheet_number::self.gauge]

    def front_loops(self) -> list[Needle]:
        """Get the list of front bed needles that belong to this sheet and currently hold loops.

        Returns:
            list[Needle]: The list of front bed needles that belong to this sheet and currently hold loops.
        """
        sheet_needles = self.front_needles()
        return [n for n in sheet_needles if n.has_loops]

    def back_loops(self) -> list[Needle]:
        """Get the list of back bed needles that belong to this sheet and currently hold loops.

        Returns:
            list[Needle]: The list of back bed needles that belong to this sheet and currently hold loops.
        """
        sheet_needles = self.back_needles()
        return [n for n in sheet_needles if n.has_loops]

    def front_slider_loops(self) -> list[Slider_Needle]:
        """Get the list of front bed slider needles that belong to this sheet and currently hold loops.

        Returns:
            list[Slider_Needle]: The list of front bed slider needles that belong to this sheet and currently hold loops.
        """
        sheet_needles = self.front_sliders()
        return [n for n in sheet_needles if n.has_loops]

    def back_slider_loops(self) -> list[Slider_Needle]:
        """Get the list of back bed slider needles that belong to this sheet and currently hold loops.

        Returns:
            list[Slider_Needle]: The list of back bed slider needles that belong to this sheet and currently hold loops.
        """
        sheet_needles = self.back_sliders()
        return [n for n in sheet_needles if n.has_loops]

    def all_needles(self) -> list[Needle]:
        """Get list of all needles on the sheet with front bed needles given first.

        Returns:
            list[Needle]: List of all needles on the sheet with front bed needles given first.
        """
        return [*self.front_needles(), *self.back_needles()]

    def all_sliders(self) -> list[Slider_Needle]:
        """Get list of all slider needles on the sheet with front bed sliders given first.

        Returns:
            list[Slider_Needle]: List of all slider needles on the sheet with front bed sliders given first.
        """
        return [*self.front_sliders(), *self.back_sliders()]

    def all_loops(self) -> list[Needle]:
        """Get list of all loop-holding needles on the sheet with front bed needles given first.

        Returns:
            list[Needle]: List of all loop-holding needles on the sheet with front bed needles given first.
        """
        return [*self.front_loops(), *self.back_loops()]

    def all_slider_loops(self) -> list[Slider_Needle]:
        """Get list of all loop-holding slider needles on the sheet with front bed sliders given first.

        Returns:
            list[Slider_Needle]: List of all loop-holding slider needles on the sheet with front bed sliders given first.
        """
        return [*self.front_slider_loops(), *self.back_slider_loops()]
