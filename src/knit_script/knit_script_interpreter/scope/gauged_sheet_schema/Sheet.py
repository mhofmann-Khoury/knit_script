"""Module containing the Sheet class.

This module provides the Sheet class, which represents a single sheet in a gauged knitting configuration.
A sheet maintains records of loop positions and provides access to needles that belong to the sheet based on the gauge spacing.

The Sheet class is fundamental to multi-sheet knitting operations,
where different parts of the knitting process are organized across multiple virtual sheets that correspond to different needle positions in a gauged pattern.
"""
from __future__ import annotations

from typing import cast

from virtual_knitting_machine.Knitting_Machine import Knitting_Machine
from virtual_knitting_machine.machine_components.needles.Needle import Needle
from virtual_knitting_machine.machine_components.needles.Sheet_Needle import (
    Sheet_Needle,
    Slider_Sheet_Needle,
)
from virtual_knitting_machine.machine_components.needles.Slider_Needle import (
    Slider_Needle,
)

from knit_script.knit_script_exceptions.gauge_sheet_exceptions import (
    Sheet_Value_Exception,
)


class Sheet:
    """Record of the position of loops on a sheet defined by the current gauging schema.

    A Sheet represents one layer in a multi-sheet knitting configuration, where needles are organized according to a gauge pattern.
    Each sheet maintains a record of which needles currently hold loops and provides methods to access needles that belong to this particular sheet.

    The sheet system allows for complex knitting patterns where different operations are performed on different subsets of needles in a structured, repeating pattern based on the gauge value.

    Attributes:
        knitting_machine (Knitting_Machine): The knitting machine that this sheet operates on.
        gauge (int): The gauge value that determines needle spacing and sheet count.
        sheet_number (int): The index of this sheet within the gauge configuration.
        loop_record (dict[int, tuple[bool, bool]]): Dictionary mapping in-sheet needle positions to tuples indicating whether loops are recorded on the front and back needles at that position.
    """

    def __init__(self, sheet_number: int, gauge: int, knitting_machine: Knitting_Machine) -> None:
        """Initialize a sheet with the specified number, gauge, and knitting machine.

        Creates a new sheet that will manage a subset of needles on the knitting machine according to the gauge pattern. The sheet records the initial state of all needles that belong to it.

        Args:
            sheet_number (int): The index of this sheet within the gauge configuration. Must be non-negative and less than the gauge value.
            gauge (int): The gauge value that determines the spacing pattern for needle organization. Must be positive.
            knitting_machine (Knitting_Machine): The knitting machine instance that this sheet will manage needles for.

        Raises:
            Sheet_Value_Exception: If sheet_number is negative or greater than or equal to the gauge value.
        """
        self.knitting_machine = knitting_machine
        if sheet_number < 0 or sheet_number >= gauge:
            raise Sheet_Value_Exception(sheet_number, gauge)
        self.gauge = gauge
        self.sheet_number = sheet_number
        # in-sheet needle position -> Recorded loop on Front, Recorded loop on Back
        self.loop_record: dict[int, tuple[bool, bool]] = {f.position: (f.has_loops, b.has_loops) for f, b in zip(self.front_needles(), self.back_needles())}

    def record_needle(self, sheet_needle: Sheet_Needle) -> None:
        """Record the state of the given sheet needle and its opposite needle.

        Updates the loop record for the specified sheet needle position by recording the current loop state of both the front and back needles at that position.

        Args:
            sheet_needle (Sheet_Needle): The sheet needle to record the state of. Must be a valid sheet needle that belongs to this sheet.

        Note:
            This method records the state of both the specified needle and its opposite bed counterpart, maintaining consistency in the loop record.
        """
        actual_needle = self.knitting_machine[sheet_needle]
        opposite_needle = self.knitting_machine[actual_needle.opposite()]
        if actual_needle.is_front:
            self.loop_record[sheet_needle.position] = actual_needle.has_loops, opposite_needle.has_loops
        else:
            self.loop_record[sheet_needle.position] = opposite_needle.has_loops, actual_needle.has_loops

    def record_sheet(self) -> None:
        """Record the loop locations for needles in the sheet given the current state of the knitting machine.

        Updates the entire loop record for this sheet by examining the current state of all needles that belong to the sheet.
        This method provides a way to synchronize the sheet's record with the actual machine state.

        Note:
            This operation examines all needle positions in the sheet and updates the loop record accordingly.
            It's useful after operations that may have changed the loop distribution across the sheet.
        """
        new_record = {n: (self.knitting_machine[self.sheet_needle(True, n)].has_loops,
                          self.knitting_machine[self.sheet_needle(False, n)].has_loops)
                      for n in self.loop_record.keys()}
        self.loop_record = new_record

    def sheet_needle(self, is_front: bool, in_sheet_position: int, is_slider: bool = False) -> Sheet_Needle:
        """Get a Sheet_Needle from this sheet set with the given parameters.

        Creates a sheet needle object that belongs to this sheet with the specified characteristics. The needle will be positioned according to the sheet's gauge configuration.

        Args:
            is_front (bool): If True, return a needle on the front bed. Otherwise, return a back-bed needle.
            in_sheet_position (int): The position of the needle relative to the sheet (not the actual needle bed position). This is the index within this sheet's needle sequence.
            is_slider (bool, optional): If True, return a slider needle. Otherwise, return a standard needle. Defaults to False.

        Returns:
            Sheet_Needle: A Sheet_Needle from this sheet with the specified parameters, properly configured for the sheet's gauge and position.
        """
        if is_slider:
            return Slider_Sheet_Needle(is_front, in_sheet_position, self.sheet_number, self.gauge)
        return Sheet_Needle(is_front, in_sheet_position, self.sheet_number, self.gauge)

    def get_matching_sheet_needle(self, other_sheet_needle: Sheet_Needle) -> Sheet_Needle:
        """Get a sheet needle belonging to this sheet at the same sheet position as a given sheet needle.

        Creates a needle that belongs to this sheet but has the same relative position and characteristics as the provided needle from another sheet.
        This is useful for operations that need to work with corresponding needles across different sheets.

        Args:
            other_sheet_needle (Sheet_Needle): The sheet needle to find a match for in this sheet. The returned needle will have the same bed position, sheet position, and slider status.

        Returns:
            Sheet_Needle: A sheet needle belonging to this sheet at the same sheet position as the given sheet needle, with matching  characteristics.
        """
        return self.sheet_needle(other_sheet_needle.is_front, other_sheet_needle.sheet_pos, isinstance(other_sheet_needle, Slider_Sheet_Needle))

    def __eq__(self, other: Sheet | int) -> bool:
        """Check equality with another Sheet or integer.

        Args:
            other (Sheet | int): The object to compare with. Can be another Sheet or an integer representing a sheet number.

        Returns:
            bool: True if the objects are equal, False otherwise.

        Note:
            When comparing with another Sheet, both sheet_number and gauge must match.
            When comparing with an integer, only the sheet_number is compared.
        """
        if isinstance(other, Sheet):
            return self.sheet_number == other.sheet_number and self.gauge == other.gauge
        elif isinstance(other, int):
            return self.sheet_number == other
        assert False, f'Expected Sheet or integer but got {other}'

    def front_needles(self) -> list[Needle]:
        """Get the set of front bed needles on the machine that belong to this sheet.

        Returns all front bed needles that are part of this sheet according to the gauge configuration. Needles are selected using the gauge spacing pattern starting from this sheet's offset.

        Returns:
            list[Needle]: The set of front bed needles on the machine that belong to this sheet, ordered by position.
        """
        machine_needles = cast(list[Needle], self.knitting_machine.front_needles())
        return machine_needles[self.sheet_number::self.gauge]

    def back_needles(self) -> list[Needle]:
        """Get the set of back bed needles on the machine that belong to this sheet.

        Returns all back bed needles that are part of this sheet according to the gauge configuration. Needles are selected using the gauge spacing pattern starting from this sheet's offset.

        Returns:
            list[Needle]: The set of back bed needles on the machine that belong to this sheet, ordered by position.
        """
        machine_needles = cast(list[Needle], self.knitting_machine.back_needles())
        return machine_needles[self.sheet_number::self.gauge]

    def front_sliders(self) -> list[Slider_Needle]:
        """Get the set of front bed slider needles on the machine that belong to this sheet.

        Returns all front bed slider needles that are part of this sheet according to the gauge configuration.
        Slider needles are selected using the gauge  spacing pattern starting from this sheet's offset.

        Returns:
            list[Slider_Needle]: The set of front bed slider needles on the machine that belong to this sheet, ordered by position.
        """
        machine_needles = cast(list[Slider_Needle], self.knitting_machine.front_sliders())
        return machine_needles[self.sheet_number::self.gauge]

    def back_sliders(self) -> list[Slider_Needle]:
        """Get the set of back bed slider needles on the machine that belong to this sheet.

        Returns all back bed slider needles that are part of this sheet according to the gauge configuration.
        Slider needles are selected using the gauge spacing pattern starting from this sheet's offset.

        Returns:
            list[Slider_Needle]: The set of back bed slider needles on the machine that belong to this sheet, ordered by position.
        """
        machine_needles = cast(list[Slider_Needle], self.knitting_machine.back_sliders())
        return machine_needles[self.sheet_number::self.gauge]

    def front_loops(self) -> list[Needle]:
        """Get the list of front bed needles that belong to this sheet and currently hold loops.

        Filters the front bed needles of this sheet to return only those that currently have loops on them. This is useful for operations that need to work specifically with active needles.

        Returns:
            list[Needle]: The list of front bed needles that belong to this sheet and currently hold loops, ordered by position.
        """
        sheet_needles = self.front_needles()
        return [n for n in sheet_needles if n.has_loops]

    def back_loops(self) -> list[Needle]:
        """Get the list of back bed needles that belong to this sheet and currently hold loops.

        Filters the back bed needles of this sheet to return only those that currently have loops on them. This is useful for operations that need to work specifically with active needles.

        Returns:
            list[Needle]: The list of back bed needles that belong to this sheet and currently hold loops, ordered by position.
        """
        sheet_needles = self.back_needles()
        return [n for n in sheet_needles if n.has_loops]

    def front_slider_loops(self) -> list[Slider_Needle]:
        """Get the list of front bed slider needles that belong to this sheet and currently hold loops.

        Filters the front bed slider needles of this sheet to return only those that currently have loops on them.
        This is useful for operations that need to work specifically with active slider needles.

        Returns:
            list[Slider_Needle]: The list of front bed slider needles that belong to this sheet and currently hold loops, ordered by position.
        """
        sheet_needles = self.front_sliders()
        return [n for n in sheet_needles if n.has_loops]

    def back_slider_loops(self) -> list[Slider_Needle]:
        """Get the list of back bed slider needles that belong to this sheet and currently hold loops.

        Filters the back bed slider needles of this sheet to return only those that currently have loops on them.
        This is useful for operations that need to work specifically with active slider needles.

        Returns:
            list[Slider_Needle]: The list of back bed slider needles that belong to this sheet and currently hold loops, ordered by position.
        """
        sheet_needles = self.back_sliders()
        return [n for n in sheet_needles if n.has_loops]

    def all_needles(self) -> list[Needle]:
        """Get list of all needles on the sheet with front bed needles given first.

        Combines all needles (both front and back bed) that belong to this sheet into a single list. Front bed needles are listed first, followed by back bed needles.

        Returns:
            list[Needle]: List of all needles on the sheet with front bed needles given first, followed by back bed needles, all ordered by position within their respective beds.
        """
        return [*self.front_needles(), *self.back_needles()]

    def all_sliders(self) -> list[Slider_Needle]:
        """Get list of all slider needles on the sheet with front bed sliders given first.

        Combines all slider needles (both front and back bed) that belong to this  sheet into a single list. Front bed slider needles are listed first, followed by back bed slider needles.

        Returns:
            list[Slider_Needle]: List of all slider needles on the sheet with front bed sliders given first, followed by back bed sliders, all ordered by position within their respective beds.
        """
        return [*self.front_sliders(), *self.back_sliders()]

    def all_loops(self) -> list[Needle]:
        """Get list of all loop-holding needles on the sheet with front bed needles given first.

        Combines all needles (both front and back bed) that belong to this sheet and currently hold loops into a single list.
        Front bed needles with loops  are listed first, followed by back bed needles with loops.

        Returns:
            list[Needle]: List of all loop-holding needles on the sheet with front bed needles given first, followed by back bed needles, all ordered by position within their respective beds.
        """
        return [*self.front_loops(), *self.back_loops()]

    def all_slider_loops(self) -> list[Slider_Needle]:
        """Get list of all loop-holding slider needles on the sheet with front bed sliders given first.

        Combines all slider needles (both front and back bed) that belong to this sheet and currently hold loops into a single list.
        Front bed slider needles with loops are listed first, followed by back bed slider needles with loops.

        Returns:
            list[Slider_Needle]: List of all loop-holding slider needles on the sheet with front bed sliders given first, followed by back bed sliders,
             all ordered by position within their respective beds.
        """
        return [*self.front_slider_loops(), *self.back_slider_loops()]


class Sheet_Identifier:
    """
    Used to convert needles given a defined sheet
    ...

    Attributes
    ----------

    """

    def __init__(self, sheet: int, gauge: int):
        assert gauge > 0, f"Knit Pass Error: Cannot make sheets for gauge {gauge}"
        assert 0 <= sheet < gauge, f"Cannot identify sheet {sheet} at gauge {gauge}"
        self._sheet: int = sheet
        self._gauge: int = gauge

    @property
    def sheet(self) -> int:
        """
        :return: The position of the sheet in the gauge
        """
        return self._sheet

    @property
    def gauge(self) -> int:
        """
        :return: The number of active sheets
        """
        return self._gauge

    def get_needle(self, needle: Needle) -> Sheet_Needle:
        """
        :param needle: Needle to access from sheet. Maybe a sheet needle which will be retargeted to this sheet
        :return: the sheet needle at the given needle index and bed
        """
        pos = needle.position
        if isinstance(needle, Sheet_Needle):
            pos = needle.sheet_pos
        if isinstance(needle, Slider_Needle):
            return Slider_Sheet_Needle(needle.is_front, pos, self.sheet, self.gauge)
        else:
            return Sheet_Needle(needle.is_front, pos, self.sheet, self.gauge)

    def needle(self, is_front: bool, position: int) -> Sheet_Needle:
        """
        Gets a needle within the sheet with specified position
        :param is_front: True if needle is on front bed
        :param position: position within the sheet
        :return: the specified sheet needle
        """
        return Sheet_Needle(is_front, position, self.sheet, self.gauge)

    def __str__(self) -> str:
        return f"s{self.sheet}:g{self.gauge}"

    def __repr__(self) -> str:
        return str(self)

    def __int__(self) -> int:
        return self.sheet

    def __lt__(self, other: Sheet_Identifier | int) -> bool:
        return self.sheet < int(other)

    def __eq__(self, other: Sheet_Identifier | int) -> bool:
        if isinstance(other, Sheet_Identifier):
            return self.sheet == other.sheet and self.gauge == other.gauge
        else:
            return self.sheet == int(other)

    # def __add__(self, other: int | Needle | Sheet_Identifier):
    #     return self.sheet + int(other)
    #
    # def __radd__(self, other):
    #     return self + other
    #
    # def __sub__(self, other):
    #     return self.sheet - int(other)
