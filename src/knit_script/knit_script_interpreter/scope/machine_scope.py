"""Scope of machine variables"""
from __future__ import annotations

import warnings

from knitout_interpreter.knitout_operations.Knitout_Line import Knitout_Comment_Line
from knitout_interpreter.knitout_operations.Rack_Instruction import Rack_Instruction
from knitout_interpreter.knitout_operations.carrier_instructions import In_Instruction, Inhook_Instruction
from virtual_knitting_machine.Knitting_Machine import Knitting_Machine
from virtual_knitting_machine.machine_components.carriage_system.Carriage_Pass_Direction import Carriage_Pass_Direction
from virtual_knitting_machine.machine_components.needles.Sheet_Needle import Sheet_Identifier
from virtual_knitting_machine.machine_components.yarn_management.Yarn_Carrier import Yarn_Carrier
from virtual_knitting_machine.machine_components.yarn_management.Yarn_Carrier_Set import Yarn_Carrier_Set

from knit_script.knit_script_exceptions.ks_exceptions import Gauge_Value_Exception, Sheet_Value_Exception
from knit_script.knit_script_interpreter import _Context_Base
from knit_script.knit_script_interpreter.scope.gauged_sheet_schema import Gauged_Sheet_Record
from knit_script.knit_script_warnings.Knit_Script_Warning import Sheet_Beyond_Gauge_Warning


class Machine_Scope:
    """Keeps track of the machine state within different scopes."""

    def __init__(self, context: _Context_Base, prior_settings: Machine_Scope | None = None) -> None:
        self._context: _Context_Base = context
        self._direction: Carriage_Pass_Direction = Carriage_Pass_Direction.Leftward
        self._working_carrier: Yarn_Carrier_Set | None = None
        self._working_racking: float = 0.0
        self._gauge: int = 1
        self._sheet: Sheet_Identifier = Sheet_Identifier(0, self._gauge)
        self._gauged_sheet_record: Gauged_Sheet_Record = Gauged_Sheet_Record(self.Gauge, self.machine_state)
        if prior_settings is not None:
            self.inherit_from_scope(prior_settings)

    def inherit_from_scope(self, scope: Machine_Scope) -> None:
        """
        Set the machine scope values based on the given scope.
        Args:
            scope: The machine scope to inherit the values from.
        """
        self.direction = scope.direction
        self.Carrier = scope.Carrier
        self.Racking = scope.Racking
        self.Gauge = scope.Gauge
        self.Sheet = scope.Sheet
        self._gauged_sheet_record = scope._gauged_sheet_record

    @property
    def machine_state(self) -> Knitting_Machine:
        """

        Returns:
            The current machine state in the current context.
        """
        return self._context.machine_state

    @property
    def direction(self) -> Carriage_Pass_Direction:
        """Get the current direction the carriage will take.

        Returns:
            Carriage_Pass_Direction: The current direction the carriage will take.
        """
        return self._direction

    @direction.setter
    def direction(self, value: Carriage_Pass_Direction) -> None:
        if not isinstance(value, Carriage_Pass_Direction):
            raise TypeError(f"Direction cannot be set to to non-direction {value}")
        self._direction = value

    @property
    def Carrier(self) -> Yarn_Carrier_Set | None:
        """Get the current carrier being used by the machine.

        Returns:
            Yarn_Carrier_Set | None: The current carrier being used by the machine.
        """
        return self._working_carrier

    @Carrier.setter
    def Carrier(self, carrier: int | float | list[int | Yarn_Carrier] | Yarn_Carrier_Set | Yarn_Carrier | None) -> None:
        """
        Set the working carrier.
        Adds inhook/in operations as needed to work with inactive carriers.
        Args:
            carrier: The value to interpret into a new working yarn carrier set.
        """
        if isinstance(carrier, int):
            carrier = Yarn_Carrier_Set([carrier])
        elif isinstance(carrier, float):
            carrier = Yarn_Carrier_Set([int(carrier)])
        elif isinstance(carrier, list):
            carrier_list = [int(c) for c in carrier]  # ensure integers and yarn-carriers are in one format.
            carrier = Yarn_Carrier_Set(carrier_list)
        elif isinstance(carrier, Yarn_Carrier):
            carrier = Yarn_Carrier_Set([carrier.carrier_id])
        elif not isinstance(carrier, Yarn_Carrier_Set) and carrier is not None:
            raise TypeError(f"Expected carrier to bes set by int, list of ints,  Yarn Carrier (e.g., c1, c2.., c10) or a Yarn Carrier Set but got {carrier}")
        if self._working_carrier != carrier:
            self._working_carrier = carrier
            if self.Carrier is not None and not self.machine_state.carrier_system.is_active(self.Carrier.carrier_ids):  # not all carriers are active. Needs an inhook operation.
                for carrier in self.Carrier:
                    if self.machine_state.carrier_system.yarn_is_loose(carrier):  # inhook loose yarns
                        inhook_op = Inhook_Instruction.execute_inhook(self.machine_state, carrier, f"Activating carrier {carrier}")
                        self._context.knitout.append(inhook_op)
                    else:  # bring connected yarns out from grippers
                        in_op = In_Instruction.execute_in(self.machine_state, carrier, f"Bring in {carrier} from grippers")
                        self._context.knitout.append(in_op)

    @property
    def Racking(self) -> float:
        """Get current racking of the machine.

        Returns:
            float: Current racking of the machine.
        """
        return self._working_racking

    @Racking.setter
    def Racking(self, value: float) -> None:
        if value != self.Racking:
            self._working_racking = value
            gauge_adjusted_racking = self.Gauge * self.Racking
            rack_instruction = Rack_Instruction.execute_rack(self.machine_state, gauge_adjusted_racking, comment=f"Rack to {self.Racking} at {self.Gauge} gauge")
            self._context.knitout.append(rack_instruction)

    @property
    def gauged_sheet_record(self) -> Gauged_Sheet_Record:
        """
        Returns:
            The gauged sheet record associated with this machine scope.
        """
        return self._gauged_sheet_record

    @property
    def Gauge(self) -> int:
        """Get the current number of sheets on the machine.

        Returns:
            int: The current number of sheets on the machine.
        """
        return self._gauge

    @Gauge.setter
    def Gauge(self, value: int | None) -> None:
        if value is None:
            value = 1
        if not (1 <= value < 10):  # Todo Set max gauge based on header and knitscript context.
            raise Gauge_Value_Exception(value)
        if self.Gauge != int(value):  # New gauge, update the Gauged Sheet Record
            self._gauge = int(value)
            self._gauged_sheet_record = Gauged_Sheet_Record(value, self.machine_state)  # change in gauge forces new gauge-sheet record to be created.
            if self.Gauge <= int(self.Sheet):
                warnings.warn(Sheet_Beyond_Gauge_Warning(self.Sheet, self.Gauge))
                self.Sheet = self.Gauge - 1
            else:
                self.Sheet = Sheet_Identifier(self.Sheet.sheet, self.Gauge)

    @property
    def Sheet(self) -> Sheet_Identifier:
        """Get the current sheet being worked on the machine.

        Returns:
            Sheet_Identifier: The current sheet being worked on the machine.
        """
        return self._sheet

    @Sheet.setter
    def Sheet(self, value: int | Sheet_Identifier | None) -> None:
        if value is None:
            value = Sheet_Identifier(0, self.Gauge)
        elif isinstance(value, int):
            if not (0 <= value < self.Gauge):
                raise Sheet_Value_Exception(value, self.Gauge)
            value = Sheet_Identifier(value, self.Gauge)
        assert isinstance(value, Sheet_Identifier)
        if self.Gauge != value.gauge:
            self.Gauge = value.gauge
        if self.Sheet != value:
            self._sheet = value
            self._context.knitout.append(Knitout_Comment_Line(f"Resetting to sheet {self.Sheet} of {self.Gauge}"))
            self._context.knitout.extend(self.gauged_sheet_record.reset_to_sheet(self.Sheet.sheet))
        if int(self.Sheet) < 0:
            warnings.warn(Sheet_Beyond_Gauge_Warning(self.Sheet, self.Gauge))
            self.Sheet = 0
        elif self.Gauge <= int(self.Sheet):
            warnings.warn(Sheet_Beyond_Gauge_Warning(self.Sheet, self.Gauge))
            self.Sheet = self.Gauge - 1
