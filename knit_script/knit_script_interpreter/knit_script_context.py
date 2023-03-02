"""Manages variable scope and machine state of knit pass during execution"""
from typing import Optional, List, Union

from knit_script.knit_script_interpreter.header_structure import Header
from knit_script.knit_script_interpreter.scope.local_scope import Knit_Script_Scope
from knit_script.knitting_machine.Machine_State import Machine_State
from knit_script.knitting_machine.knitout_instructions import inhook, bring_in, rack, releasehook
from knit_script.knitting_machine.machine_components.Sheet_Needle import Sheet_Needle, Slider_Sheet_Needle, Sheet_Identifier
from knit_script.knitting_machine.machine_components.machine_pass_direction import Pass_Direction
from knit_script.knitting_machine.machine_components.machine_position import Machine_Position
from knit_script.knitting_machine.machine_components.needles import Needle, Slider_Needle
from knit_script.knitting_machine.machine_components.yarn_carrier import Yarn_Carrier


class Knit_Script_Context:
    """Manages state of the Knitting machine during program execution"""

    def __init__(self, parent_scope: Optional[Knit_Script_Scope] = None,
                 bed_width: int = 250, machine_position: Machine_Position = Machine_Position.Center,
                 ks_file=None, parser=None):
        self.variable_scope: Knit_Script_Scope = Knit_Script_Scope(self, parent_scope)
        self._header: Header = Header(bed_width, machine_position)
        self.machine_state: Machine_State = self._header.machine_state()
        self.knitout: List[str] = self._header.header_lines()
        self.ks_file: Optional[str] = ks_file
        self.parser = parser

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

    def enter_sub_scope(self, function_name: Optional[str] = None, module_name: Optional[str] = None, module_scope: Optional[Knit_Script_Scope] = None) -> Knit_Script_Scope:
        """
            Creates a child scope and sets it as the current variable scope
            :param module_name: the name of the module owning this scope
            :param function_name: the name of the function owning this scope
            :param module_scope: the scope of the function declaration
            :return: Return the scope that was entered
        """
        if function_name is not None:
            self.variable_scope = self.variable_scope.enter_new_scope(function_name, is_function=True, module_scope=module_scope)
        elif module_name is not None:
            self.variable_scope = self.variable_scope.enter_new_scope(module_name, is_module=True, module_scope=module_scope)
        else:
            self.variable_scope = self.variable_scope.enter_new_scope(module_scope=module_scope)
        return self.variable_scope

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
    def direction(self) -> Pass_Direction:
        """
        :return: Carriage Pass direction at scope
        """
        return self.variable_scope.direction

    @direction.setter
    def direction(self, value: Pass_Direction):
        self.variable_scope.direction = value

    @property
    def carrier(self) -> Optional[Yarn_Carrier]:
        """
        :return: Carrier in use at scope
        """
        return self.variable_scope.carrier

    @carrier.setter
    def carrier(self, carrier: Optional[Yarn_Carrier]):
        if self.carrier != carrier:
            self.variable_scope.carrier = carrier
            if self.carrier is not None \
                    and not self.machine_state.yarn_manager.is_active(self.carrier):  # if yarn is not active, bring it in by inhook operation
                if self.machine_state.yarn_manager.yarn_is_loose(self.carrier):  # inhook loose yarns
                    if not self.machine_state.yarn_manager.inserting_hook_available:
                        releasehook_op = releasehook(self.machine_state, f"Releasehook to activate carrier {self.carrier}")
                        self.knitout.append(releasehook_op)
                    inhook_op = inhook(self.machine_state, self.carrier, f"Activating carrier {self.carrier}")
                    self.knitout.append(inhook_op)
                else:  # bring connected yarns out from grippers
                    in_op = bring_in(self.machine_state, self.carrier, f"Bring in {self.carrier} that is not loose")
                    self.knitout.append(in_op)

    @property
    def racking(self) -> float:
        """
        :return: Racking at current scope
        """
        return self.variable_scope.racking

    @racking.setter
    def racking(self, value: float):
        update = value != self.racking
        if update:
            self.variable_scope.racking = value
            gauge_adjusted_racking = self.gauge * self.racking
            rack_instruction = rack(self.machine_state, gauge_adjusted_racking, comment=f"Rack to {self.racking} at {self.gauge} gauge")
            self.knitout.append(rack_instruction)

    @property
    def sheet(self) -> Sheet_Identifier:
        """
        :return: Racking at current scope
        """
        return self.variable_scope.sheet

    @sheet.setter
    def sheet(self, value: Optional[Union[Sheet_Identifier, int]]):
        self.variable_scope.sheet = value
        self.knitout.append(f";Resetting to sheet {self.sheet} of {self.gauge}\n")
        self.knitout.extend(self.machine_state.reset_sheet(self.sheet.sheet))
        self.machine_state.sheet = value
        # Resets machine to the needed sheet, peeling other layers out of the way

    @property
    def gauge(self) -> int:
        """
        Resetting gauge will cause the machine state to forget all current layer records
        :return: The gauge (number of layers) that is being worked
        """
        return self.variable_scope.gauge

    @gauge.setter
    def gauge(self, value: Optional[int]):
        self.variable_scope.gauge = value

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
            sheet = self.sheet.sheet
        if gauge is None:
            gauge = self.gauge
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

    def execute_header(self, header: list):
        """
        Executes the header operations
        :param header: the list of header statements to execute
        """
        for header_line in header:
            header_line.execute(self)

        self.knitout = self._header.header_lines()

    def execute_statements(self, statements: list):
        """
        Execute the list of statements on current context
        :param statements: statements to execute
        """
        for statement in statements:
            statement.execute(self)
