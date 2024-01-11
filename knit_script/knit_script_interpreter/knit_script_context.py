"""Manages variable scope and machine state of knit pass during execution"""

from knit_script.knit_script_interpreter.scope.local_scope import Knit_Script_Scope
from knit_script.knitout_interpreter.knitout_structures.Knitout_Line import Knitout_Line, Comment_Line
from knit_script.knitout_interpreter.knitout_structures.knitout_instructions.knitout_instructions import inhook, bring_in, rack, releasehook
from knit_script.knitting_machine.Machine_State import Machine_State
from knit_script.knitting_machine.machine_components.Sheet_Needle import Sheet_Needle, Slider_Sheet_Needle, Sheet_Identifier
from knit_script.knitting_machine.machine_components.machine_pass_direction import Pass_Direction
from knit_script.knitting_machine.machine_components.machine_position import Machine_Position
from knit_script.knitting_machine.machine_components.needles import Needle, Slider_Needle
from knit_script.knitting_machine.machine_components.yarn_management.Carrier_Set import Carrier_Set
from knit_script.knitting_machine.machine_specification.Header import Header


class Knit_Script_Context:
    """Manages the state of the Knitting machine during program execution"""

    def __init__(self, parent_scope: Knit_Script_Scope | None = None,
                 bed_width: int = 540, machine_position: Machine_Position = Machine_Position.Right,
                 ks_file=None, parser=None):
        self.variable_scope: Knit_Script_Scope = Knit_Script_Scope(self, parent_scope)
        self._header: Header = Header(bed_width, machine_position)
        self.machine_state: Machine_State = self._header.machine_state()
        self.knitout: list[Knitout_Line] = self._header.header_lines()
        self.ks_file: str | None = ks_file
        self.parser = parser
        self.last_carriage_pass_result: list[Needle] | dict[Needle, Needle | None] = {}

    def add_variable(self, key, value):
        """
        Adds a variable to the variable scope by the name of key.
        :param key: Name of variable to be used in the knit script.
        :param value: Value of variable
        """
        self.variable_scope.__setattr__(key, value)

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

    def enter_sub_scope(self, function_name: str | None = None, module_name: str | None = None, module_scope: Knit_Script_Scope | None = None) -> Knit_Script_Scope:
        """
            Creates a child scope and sets it as the current variable scope
            :param module_name: the name of the module owning this scope
            :param function_name: the name of the function owning this scope.
            :param module_scope: The scope of the function declaration.
            :return: Return the scope that was entered.
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
    def sheet_needle_count(self, gauge: int | None = None) -> int:
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
    def carrier(self) -> Carrier_Set | None:
        """
        :return: Carrier in use at scope
        """
        return self.variable_scope.carrier

    @carrier.setter
    def carrier(self, carrier: Carrier_Set | None):
        if self.carrier != carrier:
            self.variable_scope.carrier = carrier
            if self.carrier is not None \
                    and not self.machine_state.carrier_system.is_active(self.carrier):  # if yarn is not active, bring it in by inhook operation
                if self.machine_state.carrier_system.yarn_is_loose(self.carrier):  # inhook loose yarns
                    inhook_op = inhook(self.machine_state, self.carrier, f"Activating carrier {self.carrier}")
                    self.knitout.append(inhook_op)
                    # releasehook_op = releasehook(self.machine_state, "Release after inhook must be optimized")
                    # self.knitout.append(releasehook_op)
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
    def sheet(self, value: Sheet_Identifier | int | None):
        self.variable_scope.sheet = value
        self.knitout.append(Comment_Line(f"Resetting to sheet {self.sheet} of {self.gauge}"))
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
    def gauge(self, value: int | None):
        self.variable_scope.gauge = value

    def get_needle(self, is_front: bool, pos: int, is_slider: bool = False,
                   global_needle: bool = False, sheet: int | None = None, gauge: int | None = None) -> Needle:
        """
        :param gauge: specifies gauging to get needles from, defaults to current gauge.
        :param sheet: Specify the sheet to get needles from, defaults to the current sheet.
        :param global_needle: If true, ignore the gauging scheme.
        :param is_front:
        :param pos: Position within the current layer.
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
                           global_needle: bool = False, sheet: int | None = None, gauge: int | None = None) -> Needle:
        """
        :param gauge:
        :param sheet:
        :param global_needle:
        :param is_front:
        :param pos: in current layer position
        :param is_slider:
        :return: Get the exact needle instance in use on the machine state
        """
        return self.machine_state[self.get_needle(is_front, pos, is_slider, global_needle, sheet, gauge)]

    def execute_statements(self, statements: list):
        """
        Execute the list of statements on current context
        :param statements: statements to execute
        """
        for statement in statements:
            statement.execute(self)
