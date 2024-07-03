"""Module containing the Gauged_Sheet_Record class and Sheet class"""
from knitout_interpreter.knitout_operations.Knitout_Line import Knitout_Line, Knitout_Comment_Line
from virtual_knitting_machine.Knitting_Machine import Knitting_Machine
from virtual_knitting_machine.machine_components.needles.Needle import Needle
from virtual_knitting_machine.machine_components.needles.Sheet_Needle import Sheet_Needle, Slider_Sheet_Needle, get_sheet_needle
from virtual_knitting_machine.machine_components.needles.Slider_Needle import Slider_Needle

from knit_script.knit_script_exceptions.Knit_Script_Exception import Sheet_Value_Exception, Sheet_Peeling_Stacked_Loops_Exception, Sheet_Peeling_Blocked_Loops_Exception, Lost_Sheet_Loops_Exception
from knit_script.knitout_execution.knitout_execution import xfer


class Sheet:
    """
        Record of the position of loops on a sheet defined by the current gauging schema.
    """
    def __init__(self, sheet_number: int, gauge: int, knitting_machine: Knitting_Machine):
        self.knitting_machine = knitting_machine
        if sheet_number < 0 or sheet_number > gauge:
            raise Sheet_Value_Exception(sheet_number, gauge)
        self.gauge = gauge
        self.sheet_number = sheet_number
        # in-sheet needle position -> Recorded loop on Front, Recorded loop on Back
        self.loop_record: dict[int, tuple[bool, bool]] = {f.position: (f.has_loops, b.has_loops) for f, b in zip(self.front_needles(), self.back_needles())}
        # self.loop_record: dict[int, tuple[bool, bool]] = {n: (False, False) for n in range(0, int(self.knitting_machine.needle_count / self.gauge))}

    def record_needle(self, sheet_needle: Sheet_Needle):
        """
        Record the state of the given sheet needle and its opposite needle.
        :param sheet_needle: The sheet needle to record.
        """
        actual_needle = self.knitting_machine[sheet_needle]
        opposite_needle = self.knitting_machine[actual_needle.opposite()]
        if actual_needle.is_front:
            self.loop_record[sheet_needle.position] = actual_needle.has_loops, opposite_needle.has_loops
        else:
            self.loop_record[sheet_needle.position] = opposite_needle.has_loops, actual_needle.has_loops

    def record_sheet(self):
        """
            Records the loop locations for needles in the sheet given the current state of the knitting machine.
        """
        new_record = {n: (self.knitting_machine[self.sheet_needle(True, n)].has_loops,
                          self.knitting_machine[self.sheet_needle(False, n)].has_loops)
                      for n in self.loop_record.keys()}
        self.loop_record = new_record

    def sheet_needle(self, is_front: bool, in_sheet_position: int, is_slider: bool = False) -> Sheet_Needle:
        """
        :param is_slider: If True, return a slider needle. Otherwise, return a standard needle.
        :param is_front: If True, return a needle on the front bed. Otherwise, return a back-bed needle.
        :param in_sheet_position: The position of the needle relative to the sheet (not the actual needle bed).
        :return: A Sheet_Needle from this sheet set with the given parameters.
        """
        if is_slider:
            return Slider_Sheet_Needle(is_front, in_sheet_position, self.sheet_number, self.gauge)
        return Sheet_Needle(is_front, in_sheet_position, self.sheet_number, self.gauge)

    def get_matching_sheet_needle(self, other_sheet_needle: Sheet_Needle) -> Sheet_Needle:
        """
        :param other_sheet_needle: The sheet needle to find a match to in this sheet.
        :return: A sheet needle belonging to this sheet at the same sheet position as a given sheet needle.
        """
        return self.sheet_needle(other_sheet_needle.is_front, other_sheet_needle.sheet_pos, isinstance(other_sheet_needle, Slider_Sheet_Needle))

    def __eq__(self, other):
        if isinstance(other, Sheet):
            return self.sheet_number == other.sheet_number and self.gauge == other.gauge
        elif isinstance(other, int):
            return self.sheet_number == other
        assert False, f'Expected Sheet or integer but got {other}'

    def front_needles(self) -> list[Needle]:  # Todo: should these be Sheet Needles?
        """
        :return: The set of front bed needles on the machine that belong to the given sheet.
        """
        machine_needles = self.knitting_machine.front_needles()
        return machine_needles[self.sheet_number::self.gauge]

    def back_needles(self) -> list[Needle]:  # Todo: should these be Sheet Needles?
        """
        :return: The set of back bed needles on the machine that belong to the given sheet.
        """
        machine_needles = self.knitting_machine.back_needles()
        return machine_needles[self.sheet_number::self.gauge]

    def front_sliders(self) -> list[Slider_Needle]:  # Todo: should these be Sheet Needles?
        """
        :return: The set of front bed  slider needles on the machine that belong to the given sheet.
        """
        machine_needles = self.knitting_machine.front_sliders()
        return machine_needles[self.sheet_number::self.gauge]

    def back_sliders(self) -> list[Slider_Needle]:  # Todo: should these be Sheet Needles?
        """
        :return: The set of back bed slider needles on the machine that belong to the given sheet.
        """
        machine_needles = self.knitting_machine.back_sliders()
        return machine_needles[self.sheet_number::self.gauge]

    def front_loops(self) -> list[Needle]:
        """
        :return: The list of front bed needles that belong to this sheet and currently hold loops.
        """
        sheet_needles = self.front_needles()
        return [n for n in sheet_needles if n.has_loops]

    def back_loops(self) -> list[Needle]:
        """
        :return: The list of back bed needles that belong to this sheet and currently hold loops.
        """
        sheet_needles = self.back_needles()
        return [n for n in sheet_needles if n.has_loops]

    def front_slider_loops(self) -> list[Slider_Needle]:
        """
        :return: The list of front bed slider needles that belong to this sheet and currently hold loops.
        """
        sheet_needles = self.front_sliders()
        return [n for n in sheet_needles if n.has_loops]

    def back_slider_loops(self) -> list[Slider_Needle]:
        """
        :return: The list of back bed slider needles that belong to this sheet and currently hold loops.
        """
        sheet_needles = self.back_sliders()
        return [n for n in sheet_needles if n.has_loops]

    def all_needles(self) -> list[Needle]:
        """
        :return: List of all needles on the sheet with front bed needles given first.
        """
        return [*self.front_needles(), *self.back_needles()]

    def all_sliders(self) -> list[Slider_Needle]:
        """
        :return: List of all slider needles on the sheet with front bed sliders given first.
        """
        return [*self.front_sliders(), *self.back_sliders()]

    def all_loops(self) -> list[Needle]:
        """
        :return: List of all loop-holding needles on the sheet with front bed needles given first.
        """
        return [*self.front_loops(), *self.back_loops()]

    def all_slider_loops(self) -> list[Slider_Needle]:
        """
        :return: List of all loop-holding slider needles on the sheet with front bed sliders given first.
        """
        return [*self.front_slider_loops(), *self.back_slider_loops()]


class Gauged_Sheet_Record:
    """
        Class for maintaining a record of loops on each sheet at the current gauging schema.
    """
    def __init__(self, gauge: int, knitting_machine: Knitting_Machine):
        self.knitting_machine: Knitting_Machine = knitting_machine
        self.gauge: int = gauge
        self.sheets: list[Sheet] = [Sheet(s, self.gauge, self.knitting_machine) for s in range(0, gauge)]
        self._needle_pos_to_layer: dict[int, int] = {n: n % self.gauge for n in range(0, self.knitting_machine.needle_count)}

    def record_needle(self, needle: Needle):
        """
        Records the state of the given needle assuming it is not moved for sheets.
        :param needle: The needle to record the state of.
        """
        if not isinstance(needle, Sheet_Needle):
            needle = get_sheet_needle(needle, self.gauge, needle.is_slider)
        self.sheets[needle.sheet].record_needle(needle)

    def peel_sheet_relative_to_active_sheet(self, active_sheet: int) -> tuple[list[Knitout_Line], list[int]]:
        """
        Moves loops out of the way of the active sheet based on needle layer positions.
        :param active_sheet: The sheet to activate by peeling all other needles based on their relative layers.
        :return: The knitout instructions that peel the layers, the needle positions that are hold loops on the front or back beds in the layer of the given active sheet.
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
                    elif needle_layer > active_sheet_layer and front_needle.has_loops:  # needle is behidn the active sheet but has loops on the front
                        peel_order_to_needles[sheet_of_needle].append(front_needle)

        xfers = []
        for sheet, peel_needles in peel_order_to_needles.items():
            if len(peel_needles) > 0:
                xfers.append(Knitout_Comment_Line(f"Peel sheet {sheet} relative to {active_sheet}"))
            for peel_needle in peel_needles:
                xfer_instruction = xfer(self.knitting_machine, peel_needle, peel_needle.opposite())
                xfers.append(xfer_instruction)
        return xfers, same_layer_needles

    def reset_to_sheet(self, sheet_id: int) -> list[Knitout_Line]:
        """
        Returns loops to a recorded location in a layer gauging schema.
        :param sheet_id: The sheet to reset to.
        :return: The knitout of the xfers needed to reset to that sheet.
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
                    knitout.append(xfer(self.knitting_machine, b, f, f"return loops {b.held_loops}"))
            elif back_had_loops:  # Loops must still be there or loops on front can be moved back.
                if b.has_loops:  # Back loops are there. Raise an error if extra front loops are present.
                    if f.has_loops:
                        raise Sheet_Peeling_Blocked_Loops_Exception(b, f)
                else:  # Back loops are not there. Must have front loops to transfer.
                    knitout.append(xfer(self.knitting_machine, f, b, f"return loops {f.held_loops}"))
        return knitout

    def get_layer_at_position(self, needle_pos: int | Needle) -> int:
        """
        :param needle_pos: The position of a needle to find the layer value for. If a needle is given, the position is extracted from the needle.
        :return: The layer index of loops held on the needles at the given needle position.
        """
        if isinstance(needle_pos, Needle):
            needle_pos = needle_pos.position
        return self._needle_pos_to_layer[needle_pos]

    def sheet_needles_at_needle_position(self, needle_pos: int | Needle) -> list[Sheet_Needle]:
        """
        :param needle_pos: The position of the sheet needles needed. Accepts an integer in real needle positions, a needle, or a sheet needle.
        :return: A list of sheet needles in the order of the sheets with needles at the same relative position as needle_pos.
        """
        if isinstance(needle_pos, Sheet_Needle):
            sheet_needle = needle_pos
        elif isinstance(needle_pos, Needle):
            sheet_needle = get_sheet_needle(needle_pos, self.gauge)
        else:
            sheet_needle = get_sheet_needle(Needle(True, needle_pos), self.gauge)
        return [s.get_matching_sheet_needle(sheet_needle) for s in self.sheets]

    def set_layer_position(self, needle_pos: int | Needle, layer_value: int,
                           push_forward: bool = True, push_backward: bool = False, swap: bool = False):
        """
        Sets the layer at the given needle position to the given layer value.
            Reorganizes other needles at corresponding sheet positions based on forward, backward rotation between sheets
                or by swapping with the needle that currently has this value.
        :param swap: If True, swap layer values with the needle that currently has the target layer value.
        :param push_backward: If true, rotates sheet needle layers backward until this needle has the target layer value.
        :param push_forward: If True, rotates sheet needle layers forward until this needle has the target layer value.
        :param needle_pos: The position of the needle to set the layer of. Accepts an integer or a needle.
        :param layer_value: The position to set the layer to. Lower values are brought forward
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

    def swap_layer_at_positions(self, position_a: int | Needle, position_b: int | Needle):
        """
        Swaps the layer values between two needle positions
        :param position_a: The needle position of the first needle in the swap.
        :param position_b: The needle position of the second needle in the swap.
        Note that the order of the needle positions does not affect the outcome.
        """
        a_layer = self.get_layer_at_position(position_a)
        b_layer = self.get_layer_at_position(position_b)
        self._needle_pos_to_layer[position_a] = b_layer
        self._needle_pos_to_layer[position_b] = a_layer

    def push_layer_backward(self, needle_position: int | Needle, pushed_layers: int = 1):
        """
        Change the layer positions of needles at the sheet positions relative to the given needle position so that all layers
        :param needle_position: A needle position to rotate layer values from.
            Integers and Needles are considered in the actual machine space.
            Sheet needles will be relative to other sheets.
        :param pushed_layers: Amount to move backward, circles around from 0 to back layer
        """
        if pushed_layers == 0:
            return  # no op because no change to layer order
        sheet_needles = self.sheet_needles_at_needle_position(needle_position)
        sheet_needles_current_layers = {sn: self.get_layer_at_position(sn) for sn in sheet_needles}
        for sheet_needle, current_layer in sheet_needles_current_layers.items():
            rotated_sheet_index = (sheet_needle.sheet + pushed_layers) % self.gauge
            rotated_sheet_needle = sheet_needles[rotated_sheet_index]
            self._needle_pos_to_layer[rotated_sheet_needle.position] = current_layer

    def push_layer_forward(self, needle_position: int, pushed_layers: int = 1):
        """
        Change the layer positions of needles at the sheet positions relative to the given needle position so that all layers
        :param needle_position: A needle position to rotate layer values from.
            Integers and Needles are considered in the actual machine space.
            Sheet needles will be relative to other sheets.
        :param pushed_layers:Amount to move forward, circles around from 0 to back layer
        """
        self.push_layer_backward(needle_position, -1 * pushed_layers)

    def set_layer_to_front(self, needle_position: int,
                           push_forward: bool = True, push_backward: bool = False, swap: bool = False):
        """
        Sets the layer as the front layer.
        :param needle_position: The needle to set the layer to the front layer.
        :param swap: If True, swap layer values with the needle that currently has the target layer value.
        :param push_backward: If true, rotates sheet needle layers backward until this needle has the target layer value.
        :param push_forward: If True, rotates sheet needle layers forward until this needle has the target layer value.
        """
        self.set_layer_position(needle_position, 0, push_forward=push_forward, push_backward=push_backward, swap=swap)

    def set_layer_to_back(self, needle_position: int,
                          push_forward: bool = True, push_backward: bool = False, swap: bool = False):
        """
        Sets the layer as the back layer.
        :param needle_position: The needle to set the layer to back layer.
        :param swap: If True, swap layer values with the needle that currently has the target layer value.
        :param push_backward: If true, rotates sheet needle layers backward until this needle has the target layer value.
        :param push_forward: If True, rotates sheet needle layers forward until this needle has the target layer value.
        """
        self.set_layer_position(needle_position, self.gauge - 1, push_forward=push_forward, push_backward=push_backward, swap=swap)

    def front_needles(self, sheet: int) -> list[Needle]:
        """
        :return: The set of front bed needles on the machine that belong to the given sheet.
        """
        return self.sheets[sheet].front_needles()

    def back_needles(self, sheet: int) -> list[Needle]:
        """
        :return: The set of back bed needles on the machine that belong to the given sheet.
        """
        return self.sheets[sheet].back_needles()

    def front_sliders(self, sheet: int) -> list[Slider_Needle]:
        """
        :return: The set of front bed slider needles on the machine that belong to the given sheet.
        """
        return self.sheets[sheet].front_sliders()

    def back_sliders(self, sheet: int) -> list[Slider_Needle]:
        """
        :return: The set of back bed slider needles on the machine that belong to the given sheet.
        """
        return self.sheets[sheet].back_sliders()

    def front_loops(self, sheet: int) -> list[Needle]:
        """
        :return: The list of front bed needles that belong to this sheet and currently hold loops.
        """
        return self.sheets[sheet].front_loops()

    def back_loops(self, sheet: int) -> list[Needle]:
        """
        :return: The list of back bed needles that belong to this sheet and currently hold loops.
        """
        return self.sheets[sheet].back_loops()

    def front_slider_loops(self, sheet: int) -> list[Slider_Needle]:
        """
        :return: The list of front bed slider needles that belong to this sheet and currently hold loops.
        """
        return self.sheets[sheet].front_slider_loops()

    def back_slider_loops(self, sheet: int) -> list[Slider_Needle]:
        """
        :return: The list of back bed slider needles that belong to this sheet and currently hold loops.
        """
        return self.sheets[sheet].back_slider_loops()

    def all_needles(self, sheet: int) -> list[Needle]:
        """
        :return: List of all needles on the sheet with front bed needles given first.
        """
        return self.sheets[sheet].all_needles()

    def all_sliders(self, sheet: int) -> list[Slider_Needle]:
        """
        :return: List of all slider needles on the sheet with front bed sliders given first.
        """
        return self.sheets[sheet].all_sliders()

    def all_loops(self, sheet: int) -> list[Needle]:
        """
        :return: List of all loop-holding needles on the sheet with front bed needles given first.
        """
        return self.sheets[sheet].all_loops()

    def all_slider_loops(self, sheet: int) -> list[Slider_Needle]:
        """
        :return: List of all loop-holding slider needles on the sheet with front bed sliders given first.
        """
        return self.sheets[sheet].all_slider_loops()
