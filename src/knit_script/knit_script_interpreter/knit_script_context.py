"""Manages variable scope and machine state of knit pass during execution"""
from __future__ import annotations

from typing import Any

from knitout_interpreter.knitout_operations.Header_Line import Knitout_Header_Line, Knitout_Header_Line_Type, get_machine_header
from knitout_interpreter.knitout_operations.Knitout_Line import Knitout_Line, Knitout_Comment_Line
from knitout_interpreter.knitout_operations.Rack_Instruction import Rack_Instruction
from knitout_interpreter.knitout_operations.carrier_instructions import In_Instruction, Inhook_Instruction
from virtual_knitting_machine.Knitting_Machine import Knitting_Machine
from virtual_knitting_machine.Knitting_Machine_Specification import Knitting_Machine_Specification, Knitting_Machine_Type
from virtual_knitting_machine.machine_components.carriage_system.Carriage_Pass_Direction import Carriage_Pass_Direction
from virtual_knitting_machine.machine_components.needles.Needle import Needle
from virtual_knitting_machine.machine_components.needles.Sheet_Needle import Sheet_Identifier, Slider_Sheet_Needle, Sheet_Needle
from virtual_knitting_machine.machine_components.needles.Slider_Needle import Slider_Needle
from virtual_knitting_machine.machine_components.yarn_management.Yarn_Carrier_Set import Yarn_Carrier_Set

from knit_script.knit_script_interpreter.scope.gauged_sheet_schema import Gauged_Sheet_Record
from knit_script.knit_script_interpreter._parser_base import _Parser_Base
from knit_script.knit_script_interpreter.scope.local_scope import Knit_Script_Scope


class _Carriers_Header_Line(Knitout_Header_Line):
    """Header line for carrier information in knitout format."""

    def __init__(self, carrier_ids: list[int], comment: str | None = None) -> None:
        """Initializes carrier header line.

        Args:
            carrier_ids: List of carrier IDs
            comment: Optional comment string
        """
        self._carrier_ids = carrier_ids
        super().__init__(Knitout_Header_Line_Type.Carriers, carrier_ids, comment)

    def __str__(self) -> str:
        """Returns string representation of carrier header.

        Returns:
            Formatted carrier header string
        """
        carrier_str = ""
        for cid in self._carrier_ids:
            carrier_str += f"{cid} "
        carrier_str = carrier_str[:-1]  # removing the space.
        return f";;{self.header_type}: {carrier_str}{self.comment_str}"

    def execute(self, machine_state: Knitting_Machine) -> bool:
        """Executes the carrier header on the machine state.

        Args:
            machine_state: The knitting machine to configure

        Returns:
            True if execution was successful
        """
        carrier_count = len(self.header_value)
        machine_state.carrier_system = carrier_count
        return True


class Knit_Script_Context:
    """Manages the state of the Knitting machine during program execution."""

    def __init__(self, parent_scope: Knit_Script_Scope | None = None, machine_specification: Knitting_Machine_Specification = Knitting_Machine_Specification(),
                 ks_file: str | None = None, parser: _Parser_Base | None = None):
        """Initializes the knit script context.

        Args:
            parent_scope: Parent scope for variable management
            machine_specification: Specification for the knitting machine
            ks_file: Path to the knit script file
            parser: Parser instance for processing scripts
        """
        self.machine_state: Knitting_Machine = Knitting_Machine(machine_specification=machine_specification)
        self.variable_scope: Knit_Script_Scope = Knit_Script_Scope(self.machine_state, parent_scope)
        self.ks_file: str | None = ks_file
        self.parser: _Parser_Base | None = parser
        self.last_carriage_pass_result: list[Needle] | dict[Needle, Needle | None] = {}
        self._version = 2
        self._machine_gauge = 15
        self.knitout: list[Knitout_Line] = get_machine_header(self.machine_state, self.version)

    @property
    def gauged_sheet_record(self) -> Gauged_Sheet_Record:
        """
        Returns:
            The current record of loops stored on each sheet in the current gauge
        """
        return self.variable_scope.machine_scope.gauged_sheet_record

    @property
    def version(self) -> int:
        """The knitout version being written.

        Returns:
            The knitout version number
        """
        return self._version

    @version.setter
    def version(self, version: int) -> None:
        """Sets the knitout version.

        Args:
            version: The version number to set
        """
        self._version = version

    @property
    def machine_type(self) -> Knitting_Machine_Type:
        """The type of machine to generate the knitout for.

        Returns:
            The machine type
        """
        return self.machine_state.machine_specification.machine

    @property
    def machine_gauge(self) -> int:
        """The needle/inch gauge of the machine being knit on.

        Returns:
            The machine gauge value
        """
        return self._machine_gauge

    @machine_gauge.setter
    def machine_gauge(self, machine_gauge: int) -> None:
        """Sets the machine gauge.

        Args:
            machine_gauge: The gauge value to set
        """
        self._machine_gauge = machine_gauge

    def add_variable(self, key: str, value: Any) -> None:
        """Adds a variable to the variable scope by the name of key.

        Args:
            key: Name of variable to be used in the knit script
            value: Value of variable
        """
        self.variable_scope.__setattr__(key, value)

    def enter_sub_scope(self, function_name: str | None = None, module_name: str | None = None, module_scope: Knit_Script_Scope | None = None) -> Knit_Script_Scope:
        """Creates a child scope and sets it as the current variable scope.

        Args:
            function_name: The name of the function owning this scope
            module_name: The name of the module owning this scope
            module_scope: The scope of the function declaration

        Returns:
            The scope that was entered
        """
        if function_name is not None:
            self.variable_scope = self.variable_scope.enter_new_scope(function_name, is_function=True, module_scope=module_scope)
        elif module_name is not None:
            self.variable_scope = self.variable_scope.enter_new_scope(module_name, is_module=True, module_scope=module_scope)
        else:
            self.variable_scope = self.variable_scope.enter_new_scope(module_scope=module_scope)
        return self.variable_scope

    def exit_current_scope(self) -> None:
        """Exits the lowest level variable scope and resets the current variable scope up a level."""
        self.variable_scope = self.variable_scope.exit_current_scope()

    @property
    def sheet_needle_count(self, gauge: int | None = None) -> int:
        """The needle count of the bed broken up by current gauge.

        Args:
            gauge: The gauge to calculate needle count for

        Returns:
            The needle count
        """
        return int(self.machine_state.needle_count / gauge)

    @property
    def direction(self) -> Carriage_Pass_Direction:
        """Carriage Pass direction at scope.

        Returns:
            The current carriage pass direction
        """
        return self.variable_scope.direction

    @direction.setter
    def direction(self, value: Carriage_Pass_Direction) -> None:
        """Sets the carriage pass direction.

        Args:
            value: The direction to set
        """
        self.variable_scope.direction = value

    @property
    def carrier(self) -> Yarn_Carrier_Set | None:
        """Carrier in use at scope.

        Returns:
            The current carrier or None
        """
        return self.variable_scope.carrier

    @carrier.setter
    def carrier(self, carrier: Yarn_Carrier_Set | None | int | list[int]) -> None:
        """Sets the active carrier.

        Args:
            carrier: The carrier to set (can be Yarn_Carrier_Set, int, list of ints, or None)
        """
        if isinstance(carrier, int):
            carrier = Yarn_Carrier_Set([carrier])
        elif isinstance(carrier, list):
            carrier = Yarn_Carrier_Set(carrier)
        if self.carrier != carrier:
            self.variable_scope.carrier = carrier
            if self.carrier is not None and not self.machine_state.carrier_system.is_active(self.carrier.carrier_ids):  # if yarn is not active, bring it in by inhook operation
                for carrier in self.carrier:
                    if self.machine_state.carrier_system.yarn_is_loose(carrier):  # inhook loose yarns
                        inhook_op = Inhook_Instruction.execute_inhook(self.machine_state, carrier, f"Activating carrier {carrier}")
                        self.knitout.append(inhook_op)
                    else:  # bring connected yarns out from grippers
                        in_op = In_Instruction.execute_in(self.machine_state, carrier, f"Bring in {carrier} that is not loose")
                        self.knitout.append(in_op)

    @property
    def racking(self) -> float:
        """Racking at current scope.

        Returns:
            The current racking value
        """
        return float(self.variable_scope.racking)

    @racking.setter
    def racking(self, value: float) -> None:
        """Sets the racking value.

        Args:
            value: The racking value to set
        """
        update = value != self.racking
        if update:
            self.variable_scope.racking = value
            gauge_adjusted_racking = self.gauge * self.racking
            rack_instruction = Rack_Instruction.execute_rack(self.machine_state, gauge_adjusted_racking, comment=f"Rack to {self.racking} at {self.gauge} gauge")
            self.knitout.append(rack_instruction)

    @property
    def sheet(self) -> Sheet_Identifier:
        """Racking at current scope.

        Returns:
            The current sheet identifier
        """
        return self.variable_scope.sheet

    @sheet.setter
    def sheet(self, value: Sheet_Identifier | int | None) -> None:
        """Sets the current sheet.

        Args:
            value: The sheet value to set
        """
        self.variable_scope.sheet = value
        self.knitout.append(Knitout_Comment_Line(f"Resetting to sheet {self.sheet} of {self.gauge}"))
        self.knitout.extend(self.gauged_sheet_record.reset_to_sheet(self.sheet.sheet))
        self.machine_state.sheet = value
        # Resets machine to the needed sheet, peeling other layers out of the way

    @property
    def gauge(self) -> int:
        """The gauge (number of layers) that is being worked.

        Note:
            Resetting gauge will cause the machine state to forget all current layer records

        Returns:
            The current gauge value
        """
        return int(self.variable_scope.gauge)

    @gauge.setter
    def gauge(self, value: int | None) -> None:
        """Sets the gauge value.

        Args:
            value: The gauge value to set
        """
        self.variable_scope.gauge = value

    def get_needle(self, is_front: bool, pos: int, is_slider: bool = False,
                   global_needle: bool = False, sheet: int | None = None, gauge: int | None = None) -> Needle:
        """Gets a needle based on current gauging.

        Args:
            is_front: Whether this is a front needle
            pos: Position within the current layer
            is_slider: Whether this is a slider needle
            global_needle: If true, ignore the gauging scheme
            sheet: Specify the sheet to get needles from, defaults to the current sheet
            gauge: Specifies gauging to get needles from, defaults to current gauge

        Returns:
            Needle based on current gauging
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
        """Gets the exact needle instance in use on the machine state.

        Args:
            is_front: Whether this is a front needle
            pos: Position in current layer
            is_slider: Whether this is a slider needle
            global_needle: If true, ignore the gauging scheme
            sheet: Specify the sheet to get needles from, defaults to the current sheet
            gauge: Specifies gauging to get needles from, defaults to current gauge

        Returns:
            The exact needle instance in use on the machine state
        """
        return self.machine_state[self.get_needle(is_front, pos, is_slider, global_needle, sheet, gauge)]

    def execute_statements(self, statements: list) -> None:
        """Execute the list of statements on current context.

        Args:
            statements: Statements to execute
        """
        for statement in statements:
            statement.execute(self)
