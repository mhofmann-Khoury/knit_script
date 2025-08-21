"""Module containing the Gauged_Sheet_Record class and Sheet class.

This module provides functionality for managing sheet-based needle organization in knitting machines with gauged configurations.
The Gauged_Sheet_Record class maintains state tracking for multiple sheets at different layers and provides methods for organizing, peeling, and resetting needle positions across sheets.

The module handles complex operations like sheet peeling, layer management, and loop state tracking across multiple gauge configurations.
"""
from __future__ import annotations

from typing import cast

from knitout_interpreter.knitout_operations.Knitout_Line import (
    Knitout_Comment_Line,
    Knitout_Line,
)
from knitout_interpreter.knitout_operations.needle_instructions import Xfer_Instruction
from virtual_knitting_machine.Knitting_Machine import Knitting_Machine
from virtual_knitting_machine.machine_components.needles.Needle import Needle
from virtual_knitting_machine.machine_components.needles.Sheet_Needle import (
    Sheet_Needle,
    get_sheet_needle,
)
from virtual_knitting_machine.machine_components.needles.Slider_Needle import (
    Slider_Needle,
)

from knit_script.knit_script_exceptions.gauge_sheet_exceptions import (
    Lost_Sheet_Loops_Exception,
    Sheet_Peeling_Blocked_Loops_Exception,
    Sheet_Peeling_Stacked_Loops_Exception,
)
from knit_script.knit_script_interpreter.scope.gauged_sheet_schema.Sheet import Sheet


class Gauged_Sheet_Record:
    """Class for maintaining a record of loops on each sheet at the current gauging schema.

    The Gauged_Sheet_Record manages the organization of knitting machine needles across multiple sheets in a gauged configuration.
    It tracks loop states, handles sheet peeling operations, and manages layer positioning for complex knitting patterns that require multiple working levels.

    This class is essential for advanced knitting techniques that involve working with multiple sheets of fabric simultaneously, such as double-knit fabrics or complex color-work patterns.

    Attributes:
        knitting_machine (Knitting_Machine): The knitting machine being managed.
        gauge (int): The gauge value determining the number of sheets.
        sheets (list[Sheet]): List of Sheet objects, one for each gauge level.
    """

    def __init__(self, gauge: int, knitting_machine: Knitting_Machine) -> None:
        """Initialize the gauged sheet record with specified gauge and machine.

        Creates a new gauged sheet record that manages needle organization across multiple sheets based on the specified gauge value.
        Each sheet corresponds to a different layer in the gauge configuration.

        Args:
            gauge (int): The gauge value determining the number of sheets to create. Must be a positive integer representing the number of working levels.
            knitting_machine (Knitting_Machine): The knitting machine instance that this record will manage. The machine provides needle access and state information.
        """
        self.knitting_machine: Knitting_Machine = knitting_machine
        self.gauge: int = gauge
        self.sheets: list[Sheet] = [Sheet(s, self.gauge, self.knitting_machine) for s in range(0, gauge)]
        self._needle_pos_to_layer: dict[int, int] = {n: n % self.gauge for n in range(0, self.knitting_machine.needle_count)}

    def record_needle(self, needle: Needle) -> None:
        """Record the state of the given needle assuming it is not moved for sheets.

        Updates the internal record with the current state of the specified needle. If the needle is not already a Sheet_Needle, it will be converted to one based on the current gauge configuration.

        Args:
            needle (Needle): The needle to record the state of. Can be any type of needle, which will be converted to a Sheet_Needle if necessary.
        """
        if not isinstance(needle, Sheet_Needle):
            needle = get_sheet_needle(needle, self.gauge, needle.is_slider)
        self.sheets[needle.sheet].record_needle(needle)

    def peel_sheet_relative_to_active_sheet(self, active_sheet: int) -> tuple[list[Knitout_Line], list[int]]:
        """Move loops out of the way of the active sheet based on needle layer positions.

        This method implements sheet peeling by moving loops that would interfere with the active sheet to appropriate positions.
        Loops are moved based on their layer relationships - loops in front of the active sheet on the back bed are moved, and loops behind the active sheet on the front bed are moved.

        Args:
            active_sheet (int): The sheet to activate by peeling all other needles based on their relative layers. Must be a valid sheet index within the gauge range.

        Returns:
            tuple[list[Knitout_Line], list[int]]: A tuple containing:
                - list[Knitout_Line]: The knitout instructions that peel the layers, including transfer operations and comments.
                - list[int]: The needle positions that hold loops on the front or back beds in the same layer as the given active sheet.

        Note:
            This operation is essential for complex multi-sheet knitting where different sheets need to be worked at different times without interference from loops on other sheets.
        """
        peel_order_to_needles: dict[int, list[Needle]] = {i: [] for i in range(0, self.gauge)}
        same_layer_needles: list[int] = []

        for needle_pos, needle_layer in self._needle_pos_to_layer.items():
            back_needle = self.knitting_machine[Needle(False, needle_pos)]
            back_sheet_needle = get_sheet_needle(back_needle, self.gauge)
            front_needle = self.knitting_machine[Needle(True, needle_pos)]
            sheet_of_needle = back_sheet_needle.sheet
            sheet_pos = back_sheet_needle.sheet_pos
            if back_needle.has_loops or front_needle.has_loops:
                if sheet_of_needle != active_sheet:
                    active_sheet_needle = Sheet_Needle(True, sheet_pos, active_sheet, self.gauge)
                    active_sheet_layer = self._needle_pos_to_layer[active_sheet_needle.position]
                    if active_sheet_layer == needle_layer:
                        same_layer_needles.append(needle_pos)
                    if needle_layer < active_sheet_layer and back_needle.has_loops:  # needle is in front of the active sheet but has loops on the back.
                        peel_order_to_needles[sheet_of_needle].append(back_needle)
                    elif needle_layer > active_sheet_layer and front_needle.has_loops:  # needle is behind the active sheet but has loops on the front
                        peel_order_to_needles[sheet_of_needle].append(front_needle)

        xfers = []
        for sheet, peel_needles in peel_order_to_needles.items():
            if len(peel_needles) > 0:
                xfers.append(Knitout_Comment_Line(f"Peel sheet {sheet} relative to {active_sheet}"))
            for peel_needle in peel_needles:
                xfer_instruction = Xfer_Instruction.execute_xfer(self.knitting_machine, peel_needle, peel_needle.opposite())
                xfers.append(xfer_instruction)
        return xfers, same_layer_needles

    def reset_to_sheet(self, sheet_id: int) -> list[Knitout_Line]:
        """Return loops to a recorded location in a layer gauging schema.

        This method restores the needle configuration to a previously recorded state for the specified sheet.
        It handles complex loop management including detecting lost loops, stacked loop conflicts, and blocked loop situations.

        Args:
            sheet_id (int): The sheet to reset to. Must be a valid sheet index within the gauge range.

        Returns:
            list[Knitout_Line]: The knitout instructions needed to reset to that  sheet, including any necessary transfer operations and comments.

        Raises:
            Lost_Sheet_Loops_Exception: If loops that were recorded are no longer present on the expected needles.
            Sheet_Peeling_Stacked_Loops_Exception: If stacked loops cannot be properly separated during the reset operation.
            Sheet_Peeling_Blocked_Loops_Exception: If loops are blocked from returning to their expected positions due to conflicts.

        Note:
            This operation is crucial for maintaining consistency when switching between different sheet configurations during complex knitting patterns.
        """
        knitout, same_layer_needles = self.peel_sheet_relative_to_active_sheet(sheet_id)
        sheet = self.sheets[sheet_id]

        for f, b in zip(self.front_needles(sheet_id), self.back_needles(sheet_id)):
            sheet_needle = get_sheet_needle(f, self.gauge)
            front_had_loops, back_had_loops = sheet.loop_record[sheet_needle.position]
            had_loops = front_had_loops or back_had_loops
            has_loops = f.has_loops or b.has_loops
            if had_loops and not has_loops:
                if front_had_loops:
                    raise Lost_Sheet_Loops_Exception(f)
                if back_had_loops:
                    raise Lost_Sheet_Loops_Exception(b)
            if front_had_loops and back_had_loops:  # Loops must still be there or there is a peeling error.
                if not f.has_loops or not b.has_loops:
                    raise Sheet_Peeling_Stacked_Loops_Exception(f, b)
            elif front_had_loops:  # Loops must still be there or loops on back can be moved to front.
                if f.has_loops:  # Front loops are there. Raise an error if extra back loops are present.
                    if b.has_loops:
                        raise Sheet_Peeling_Blocked_Loops_Exception(f, b)
                else:  # front loops are not there, must have back loops to transfer.
                    knitout.append(Xfer_Instruction.execute_xfer(self.knitting_machine, b, f, f"return loops {b.held_loops}"))
            elif back_had_loops:  # Loops must still be there or loops on front can be moved back.
                if b.has_loops:  # Back loops are there. Raise an error if extra front loops are present.
                    if f.has_loops:
                        raise Sheet_Peeling_Blocked_Loops_Exception(b, f)
                else:  # Back loops are not there. Must have front loops to transfer.
                    knitout.append(Xfer_Instruction.execute_xfer(self.knitting_machine, f, b, f"return loops {f.held_loops}"))
        return knitout

    def get_layer_at_position(self, needle_pos: int | Needle) -> int:
        """Get the layer index of loops held on the needles at the given needle position.

        Returns the current layer assignment for the specified needle position.
        Layer indices range from 0 (front) to gauge-1 (back), representing the relative depth of the needle in the sheet configuration.

        Args:
            needle_pos (int | Needle): The position of a needle to find the layer value for. If a needle is given, the position is extracted from the needle.

        Returns:
            int: The layer index of loops held on the needles at the given needle position. Range is 0 to gauge-1.
        """
        if isinstance(needle_pos, Needle):
            needle_pos = needle_pos.position
        return self._needle_pos_to_layer[needle_pos]

    def sheet_needles_at_needle_position(self, needle_pos: int | Needle) -> list[Sheet_Needle]:
        """Get a list of sheet needles in the order of the sheets with needles at the same relative position as needle_pos.

        Returns all sheet needles that correspond to the same relative position across all sheets in the gauge configuration.
        This is useful for operations that need to work with corresponding needles across multiple sheets.

        Args:
            needle_pos (int | Needle): The position of the sheet needles needed. Accepts an integer in real needle positions, a needle, or a sheet needle.

        Returns:
            list[Sheet_Needle]: A list of sheet needles in the order of the sheets with needles at the same relative position as needle_pos.
        """
        if isinstance(needle_pos, Sheet_Needle):
            sheet_needle = needle_pos
        elif isinstance(needle_pos, Needle):
            sheet_needle = get_sheet_needle(needle_pos, self.gauge)
        else:
            sheet_needle = get_sheet_needle(Needle(True, needle_pos), self.gauge)
        return [s.get_matching_sheet_needle(sheet_needle) for s in self.sheets]

    def set_layer_position(self, needle_pos: int | Needle, layer_value: int, push_forward: bool = True, push_backward: bool = False, swap: bool = False) -> None:
        """Set the layer at the given needle position to the given layer value.

        Reorganizes needle layer assignments to place the specified needle at the target layer.
        Other needles at corresponding sheet positions are reorganized based on the specified method (forward rotation, backward rotation, or swapping).

        Args:
            needle_pos (int | Needle): The position of the needle to set the layer of. Accepts an integer or a needle.
            layer_value (int): The position to set the layer to. Lower values are  brought forward. Must be in range 0 to gauge-1.
            push_forward (bool, optional): If True, rotates sheet needle layers forward until this needle has the target layer value. Defaults to True.
            push_backward (bool, optional): If True, rotates sheet needle layers backward until this needle has the target layer value. Defaults to False.
            swap (bool, optional): If True, swap layer values with the needle that currently has the target layer value. Defaults to False.

        Note:
            Exactly one of push_forward, push_backward, or swap must be True. The method determines how other needles are reorganized when this needle is moved to the target layer.
        """
        if self.get_layer_at_position(needle_pos) == layer_value:
            return  # No-Op for no change.
        if isinstance(needle_pos, Sheet_Needle):
            sheet_needle = needle_pos
            needle_pos = needle_pos.position
        elif isinstance(needle_pos, Needle):
            sheet_needle = get_sheet_needle(needle_pos, self.gauge)
            needle_pos = needle_pos.position
        else:
            sheet_needle = get_sheet_needle(Needle(True, needle_pos), self.gauge)
        sheet_needles = self.sheet_needles_at_needle_position(needle_pos)
        sheet_needles_current_layers = {sn: self.get_layer_at_position(sn) for sn in sheet_needles}
        sheet_needle_with_target_layer = None
        for sn, cl in sheet_needles_current_layers.items():
            if cl == layer_value:
                sheet_needle_with_target_layer = sn
                break
        assert sheet_needle_with_target_layer is not None, f"Could not find a needle with the layer value {layer_value} at position {needle_pos}"
        assert sheet_needle_with_target_layer != sheet_needle
        if swap:
            self.swap_layer_at_positions(sheet_needle, sheet_needle_with_target_layer)
            return
        push_distance = sheet_needle_with_target_layer.sheet - sheet_needle.sheet
        if push_forward:
            self.push_layer_forward(needle_pos, self.gauge - push_distance)
            return
        elif push_backward:
            self.push_layer_backward(needle_pos, push_distance)
            return
        assert False, f"Needs a rule for setting the layer (forward, backward, or swap)"

    def swap_layer_at_positions(self, position_a: int | Needle, position_b: int | Needle) -> None:
        """Swap the layer values between two needle positions.

        Exchanges the layer assignments between two needle positions. This operation  is useful for reorganizing sheet layers without affecting other needles.

        Args:
            position_a (int | Needle): The needle position of the first needle in  the swap. Can be an integer position or a Needle object.
            position_b (int | Needle): The needle position of the second needle in the swap. Can be an integer position or a Needle object.

        Note:
            The order of the needle positions does not affect the outcome. Both positions must be valid needle positions within the machine range.
        """
        if isinstance(position_a, Needle):
            position_a = position_a.position
        if isinstance(position_b, Needle):
            position_b = position_b.position
        a_layer = self.get_layer_at_position(position_a)
        b_layer = self.get_layer_at_position(position_b)
        self._needle_pos_to_layer[position_a] = b_layer
        self._needle_pos_to_layer[position_b] = a_layer

    def push_layer_backward(self, needle_position: int | Needle, pushed_layers: int = 1) -> None:
        """Change the layer positions of needles at the sheet positions relative to the given needle position.

        Rotates the layer assignments at corresponding sheet positions by moving them backward by the specified number of layers.
        The rotation wraps around from the back layer (gauge-1) to the front layer (0).

        Args:
            needle_position (int | Needle): A needle position to rotate layer values from. Integers and Needles are considered in the actual machine space.
                Sheet needles will be relative to other sheets.
            pushed_layers (int, optional): Amount to move backward, circles around from 0 to back layer. Defaults to 1.

        Note:
            A pushed_layers value of 0 results in no operation. Negative values will effectively push forward.
        """
        if pushed_layers == 0:
            return  # no op because no change to layer order
        sheet_needles = self.sheet_needles_at_needle_position(needle_position)
        sheet_needles_current_layers = {sn: self.get_layer_at_position(sn) for sn in sheet_needles}
        for sheet_needle, current_layer in sheet_needles_current_layers.items():
            rotated_sheet_index = (sheet_needle.sheet + pushed_layers) % self.gauge
            rotated_sheet_needle = sheet_needles[rotated_sheet_index]
            self._needle_pos_to_layer[rotated_sheet_needle.position] = current_layer

    def push_layer_forward(self, needle_position: int, pushed_layers: int = 1) -> None:
        """Change the layer positions of needles at the sheet positions relative to the given needle position.

        Rotates the layer assignments at corresponding sheet positions by moving them forward by the specified number of layers. This is implemented as a backward push with negated distance.

        Args:
            needle_position (int): A needle position to rotate layer values from. Integers and Needles are considered in the actual machine space. Sheet needles will be relative to other sheets.
            pushed_layers (int, optional): Amount to move forward, circles around from back layer to front layer. Defaults to 1.

        Note:
            This method is equivalent to push_layer_backward with a negated pushed_layers value.
        """
        self.push_layer_backward(needle_position, -1 * pushed_layers)

    def set_layer_to_front(self, needle_position: int, push_forward: bool = True, push_backward: bool = False, swap: bool = False) -> None:
        """Set the layer as the front layer.

        Convenience method to set the specified needle position to layer 0 (front).
        This is equivalent to calling set_layer_position with layer_value=0.

        Args:
            needle_position (int): The needle to set the layer to the front layer.
            push_forward (bool, optional): If True, rotates sheet needle layers forward until this needle has the target layer value. Defaults to True.
            push_backward (bool, optional): If True, rotates sheet needle layers backward until this needle has the target layer value. Defaults to False.
            swap (bool, optional): If True, swap layer values with the needle that currently has the target layer value. Defaults to False.
        """
        self.set_layer_position(needle_position, 0, push_forward=push_forward, push_backward=push_backward, swap=swap)

    def set_layer_to_back(self, needle_position: int, push_forward: bool = True, push_backward: bool = False, swap: bool = False) -> None:
        """Set the layer as the back layer.

        Convenience method to set the specified needle position to the back layer (gauge-1). This is equivalent to calling set_layer_position with  layer_value=gauge-1.

        Args:
            needle_position (int): The needle to set the layer to back layer.
            push_forward (bool, optional): If True, rotates sheet needle layers forward until this needle has the target layer value. Defaults to True.
            push_backward (bool, optional): If True, rotates sheet needle layers  backward until this needle has the target layer value. Defaults to False.
            swap (bool, optional): If True, swap layer values with the needle that currently has the target layer value. Defaults to False.
        """
        self.set_layer_position(needle_position, self.gauge - 1, push_forward=push_forward, push_backward=push_backward, swap=swap)

    def front_needles(self, sheet: int) -> list[Needle]:
        """Get the set of front bed needles on the machine that belong to the given sheet.

        Args:
            sheet (int): The sheet number. Must be a valid sheet index within the gauge range (0 to gauge-1).

        Returns:
            list[Needle]: The set of front bed needles on the machine that belong  to the given sheet.
        """
        return cast(list[Needle], self.sheets[sheet].front_needles())

    def back_needles(self, sheet: int) -> list[Needle]:
        """Get the set of back bed needles on the machine that belong to the given sheet.

        Args:
            sheet (int): The sheet number. Must be a valid sheet index within  the gauge range (0 to gauge-1).

        Returns:
            list[Needle]: The set of back bed needles on the machine that belong to the given sheet.
        """
        return cast(list[Needle], self.sheets[sheet].back_needles())

    def front_sliders(self, sheet: int) -> list[Slider_Needle]:
        """Get the set of front bed slider needles on the machine that belong to the given sheet.

        Args:
            sheet (int): The sheet number. Must be a valid sheet index within  the gauge range (0 to gauge-1).

        Returns:
            list[Slider_Needle]: The set of front bed slider needles on the machine  that belong to the given sheet.
        """
        return cast(list[Slider_Needle], self.sheets[sheet].front_sliders())

    def back_sliders(self, sheet: int) -> list[Slider_Needle]:
        """Get the set of back bed slider needles on the machine that belong to the given sheet.

        Args:
            sheet (int): The sheet number. Must be a valid sheet index within  the gauge range (0 to gauge-1).

        Returns:
            list[Slider_Needle]: The set of back bed slider needles on the machine that belong to the given sheet.
        """
        return cast(list[Slider_Needle], self.sheets[sheet].back_sliders())

    def front_loops(self, sheet: int) -> list[Needle]:
        """Get the list of front bed needles that belong to this sheet and currently hold loops.

        Args:
            sheet (int): The sheet number. Must be a valid sheet index within  the gauge range (0 to gauge-1).

        Returns:
            list[Needle]: The list of front bed needles that belong to this sheet  and currently hold loops.
        """
        return cast(list[Needle], self.sheets[sheet].front_loops())

    def back_loops(self, sheet: int) -> list[Needle]:
        """Get the list of back bed needles that belong to this sheet and currently hold loops.

        Args:
            sheet (int): The sheet number. Must be a valid sheet index within the gauge range (0 to gauge-1).

        Returns:
            list[Needle]: The list of back bed needles that belong to this sheet and currently hold loops.
        """
        return cast(list[Needle], self.sheets[sheet].back_loops())

    def front_slider_loops(self, sheet: int) -> list[Slider_Needle]:
        """Get the list of front bed slider needles that belong to this sheet and currently hold loops.

        Args:
            sheet (int): The sheet number. Must be a valid sheet index within  the gauge range (0 to gauge-1).

        Returns:
            list[Slider_Needle]: The list of front bed slider needles that belong  to this sheet and currently hold loops.
        """
        return cast(list[Slider_Needle], self.sheets[sheet].front_slider_loops())

    def back_slider_loops(self, sheet: int) -> list[Slider_Needle]:
        """Get the list of back bed slider needles that belong to this sheet and currently hold loops.

        Args:
            sheet (int): The sheet number. Must be a valid sheet index within  the gauge range (0 to gauge-1).

        Returns:
            list[Slider_Needle]: The list of back bed slider needles that belong  to this sheet and currently hold loops.
        """
        return cast(list[Slider_Needle], self.sheets[sheet].back_slider_loops())

    def all_needles(self, sheet: int) -> list[Needle]:
        """Get list of all needles on the sheet with front bed needles given first.

        Args:
            sheet (int): The sheet number. Must be a valid sheet index within  the gauge range (0 to gauge-1).

        Returns:
            list[Needle]: List of all needles on the sheet with front bed needles  given first, followed by back bed needles.
        """
        return cast(list[Needle], self.sheets[sheet].all_needles())

    def all_sliders(self, sheet: int) -> list[Slider_Needle]:
        """Get list of all slider needles on the sheet with front bed sliders given first.

        Args:
            sheet (int): The sheet number. Must be a valid sheet index within the gauge range (0 to gauge-1).

        Returns:
            list[Slider_Needle]: List of all slider needles on the sheet with front  bed sliders given first, followed by back bed sliders.
        """
        return cast(list[Slider_Needle], self.sheets[sheet].all_sliders())

    def all_loops(self, sheet: int) -> list[Needle]:
        """Get list of all loop-holding needles on the sheet with front bed needles given first.

        Args:
            sheet (int): The sheet number. Must be a valid sheet index within the gauge range (0 to gauge-1).

        Returns:
            list[Needle]: List of all loop-holding needles on the sheet with front  bed needles given first, followed by back bed needles.
        """
        return cast(list[Needle], self.sheets[sheet].all_loops())

    def all_slider_loops(self, sheet: int) -> list[Slider_Needle]:
        """Get list of all loop-holding slider needles on the sheet with front bed sliders given first.

        Args:
            sheet (int): The sheet number. Must be a valid sheet index within  the gauge range (0 to gauge-1).

        Returns:
            list[Slider_Needle]: List of all loop-holding slider needles on the sheet with front bed sliders given first, followed by back bed sliders.
        """
        return cast(list[Slider_Needle], self.sheets[sheet].all_slider_loops())
