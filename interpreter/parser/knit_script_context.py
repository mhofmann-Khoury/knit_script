"""Manages variable scope and machine state of knit pass during execution"""
from typing import Optional, List, Union

from interpreter.parser.variable_scope import Variable_Scope
from interpreter.statements.header_statement import Header
from knitting_machine.Machine_State import Machine_State
from knitting_machine.knitout_instructions import inhook, bring_in, rack, releasehook
from knitting_machine.machine_components.Sheet_Needle import Sheet_Needle, Slider_Sheet_Needle, Sheet_Identifier
from knitting_machine.machine_components.machine_pass_direction import Pass_Direction
from knitting_machine.machine_components.machine_position import Machine_Position
from knitting_machine.machine_components.needles import Needle, Slider_Needle
from knitting_machine.machine_components.yarn_carrier import Yarn_Carrier

class Knit_Script_Context:
    """Manages state of the Knitting machine during program execution"""
    def __init__(self, parent_scope: Optional[Variable_Scope] = None,
                 bed_width: int = 250, machine_position: Machine_Position = Machine_Position.Center):
        self.variable_scope = Variable_Scope(parent_scope)
        self._header: Header = Header(bed_width, machine_position)
        self.machine_state: Machine_State = self._header.machine_state()
        self.knitout: List[str] = self._header.header_lines()

    @property
    def header(self) -> Header:
        """
        :return: The header used to define the machine state
        """
        return self._header

    @header.setter
    def header(self, value: Header):
        self._header = value
        self.machine_state = self._header.machine_state()

    def enter_sub_scope(self, function_name: Optional[str] = None):
        """
            Creates a child scope and sets it as the current variable scope
        """
        self.variable_scope = self.variable_scope.enter_new_scope(function_name=function_name)

    def exit_current_scope(self):
        """
            Exits the lowest level variable scope and resets the current variable scope up a level
        """
        self.variable_scope = self.variable_scope.exit_current_scope()

    @property
    def sheet_needle_count(self, gauge: Optional[int] = None) -> int:
        """
        :return: The needle count of the bed broken up by current gauge
        """
        return self.machine_state.sheet_needle_count(gauge)

    @property
    def current_direction(self) -> Pass_Direction:
        """
        :return: Carriage Pass direction at scope
        """
        return self.variable_scope.current_direction

    @current_direction.setter
    def current_direction(self, value: Pass_Direction):
        self.variable_scope.current_direction = value

    @property
    def current_carrier(self) -> Optional[Yarn_Carrier]:
        """
        :return: Carrier in use at scope
        """
        return self.variable_scope.current_carrier

    @current_carrier.setter
    def current_carrier(self, carrier: Optional[Yarn_Carrier]):
        if self.current_carrier != carrier:
            self.variable_scope.current_carrier = carrier
            if self.current_carrier is not None \
                    and not self.machine_state.yarn_manager.is_active(self.current_carrier):  # if yarn is not active, bring it in by inhook operation
                if self.machine_state.yarn_manager.yarn_is_loose(self.current_carrier):  # inhook loose yarns
                    if not self.machine_state.yarn_manager.inserting_hook_available:
                        releasehook_op = releasehook(self.machine_state, f"Releasehook to activate carrier {self.current_carrier}")
                        self.knitout.append(releasehook_op)
                    inhook_op = inhook(self.machine_state, self.current_carrier, f"Activating carrier {self.current_carrier}")
                    self.knitout.append(inhook_op)
                else:  # bring connected yarns out from grippers
                    in_op = bring_in(self.machine_state, self.current_carrier, f"Bring in {self.current_carrier} that is not loose")
                    self.knitout.append(in_op)

    @property
    def current_racking(self) -> int:
        """
        :return: Racking at current scope
        """
        return self.variable_scope.current_racking

    @current_racking.setter
    def current_racking(self, value: int):
        update = value != self.current_racking
        if update:
            self.variable_scope.current_racking = value
            gauge_adjusted_racking = self.current_gauge * self.current_racking
            rack_instruction = rack(self.machine_state, gauge_adjusted_racking, comment=f"Rack to {self.current_racking} at {self.current_gauge} gauge")
            self.knitout.append(rack_instruction)

    @property
    def current_sheet(self) -> Sheet_Identifier:
        """
        :return: Racking at current scope
        """
        return self.variable_scope.current_sheet

    @current_sheet.setter
    def current_sheet(self, value: Optional[Union[Sheet_Identifier, int]]):
        self.variable_scope.current_sheet = value
        sheet = self.current_sheet
        self.machine_state.sheet = sheet.sheet
        self.knitout.append(f";Resetting to sheet {sheet} of {self.current_gauge}\n")
        self.knitout.extend(self.machine_state.reset_sheet(sheet.sheet))
        # Resets machine to the needed sheet, peeling other layers out of the way

    @property
    def current_gauge(self) -> int:
        """
        Resetting gauge will cause the machine state to forget all current layer records
        :return: The gauge (number of layers) that is being worked
        """
        return self.variable_scope.current_gauge

    @current_gauge.setter
    def current_gauge(self, value: Optional[int]):
        self.variable_scope.current_gauge = value
        gauge = self.current_gauge
        self.machine_state.gauge = gauge

    def get_needle(self, is_front: bool, pos: int, is_slider: bool = False,
                   global_needle: bool = False, sheet: Optional[int] = None, gauge: Optional[int] = None) -> Needle:
        """
        :param gauge: specifies gauging to get needles from, defaults to current gauge
        :param sheet: specifies the sheet to get needles from, defaults to current sheet
        :param global_needle: If true, ignore gauging scheme
        :param is_front:
        :param pos: position within current layer
        :param is_slider:
        :return: Needle based on current gauging
        """
        if sheet is None:
            sheet = self.current_sheet
        if gauge is None:
            gauge = self.current_gauge
        if global_needle or gauge == 1:
            if is_slider:
                return Slider_Needle(is_front, pos)
            else:
                return Needle(is_front, pos)
        else:
            if is_slider:
                return Slider_Sheet_Needle(is_front, pos, sheet, gauge)
            else:
                return Sheet_Needle(is_front, pos, sheet, gauge)

    def get_machine_needle(self, is_front: bool, pos: int, is_slider: bool = False,
                           global_needle: bool = False, sheet: Optional[int] = None, gauge: Optional[int] = None) -> Needle:
        """
        :param gauge:
        :param sheet:
        :param global_needle:
        :param is_front:
        :param pos: in current layer position
        :param is_slider:
        :return: Get the exact needle instance that is in use on the machine state
        """
        return self.machine_state[self.get_needle(is_front, pos, is_slider, global_needle, sheet, gauge)]
