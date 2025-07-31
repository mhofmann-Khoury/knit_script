"""Scope of machine variables"""
from __future__ import annotations

import warnings
from enum import Enum
from typing import Any

from virtual_knitting_machine.Knitting_Machine import Knitting_Machine
from virtual_knitting_machine.machine_components.carriage_system.Carriage_Pass_Direction import Carriage_Pass_Direction
from virtual_knitting_machine.machine_components.needles.Sheet_Needle import Sheet_Identifier
from virtual_knitting_machine.machine_components.yarn_management.Yarn_Carrier import Yarn_Carrier
from virtual_knitting_machine.machine_components.yarn_management.Yarn_Carrier_Set import Yarn_Carrier_Set

from knit_script.knit_script_exceptions.ks_exceptions import Gauge_Value_Exception, Sheet_Value_Exception
from knit_script.knit_script_interpreter.gauged_sheet_schema.Gauged_Sheet_Record import Gauged_Sheet_Record
from knit_script.knit_script_warnings.Knit_Script_Warning import Sheet_Beyond_Gauge_Warning


class Machine_Variables(Enum):
    """Tracks Knit-script names for global machine variables."""
    Gauge = "gauge"
    Carrier = "carrier"
    Rack = "racking"
    Sheet = "sheet"

    @staticmethod
    def in_machine_variables(key: str) -> bool:
        """Check if key is a machine variable.

        Args:
            key (str): Variable string.

        Returns:
            bool: True if key is a variable.
        """
        return key in [i.name for i in Machine_Variables]

    def get_value(self, scope: Machine_Scope) -> Any:
        """Get the accessed value from the variable scope.

        Args:
            scope (Machine_Scope): Variable scope to access value from.

        Returns:
            Any: The accessed value.
        """
        return getattr(scope, self.value)

    def set_value(self, context: Any, value: Any) -> None:
        """Set the machine variable at the global level.

        Args:
            context (Knit_Script_Context): Scope or global scope to set the value to.
            value (Any): The value to set the machine variable to.
        """
        setattr(context, self.value, value)


class Machine_Scope:
    """Keeps track of the machine state within different scopes."""

    def __init__(self, machine_state: Knitting_Machine, parent_scope: Machine_Scope | None = None) -> None:
        self._machine_state: Knitting_Machine = machine_state
        if parent_scope is None:
            self._direction: Carriage_Pass_Direction = Carriage_Pass_Direction.Leftward
            self._carrier: Yarn_Carrier_Set | None = None
            self._racking: float = 0.0
            self._gauge: int = 1
            self._sheet: Sheet_Identifier = Sheet_Identifier(0, self._gauge)
            self._gauged_sheet_record: Gauged_Sheet_Record = Gauged_Sheet_Record(self.gauge, self._machine_state)
        else:
            self._direction: Carriage_Pass_Direction = parent_scope.direction
            self._carrier: Yarn_Carrier_Set | None = parent_scope.carrier
            self._racking: float = parent_scope.racking
            self._gauge: int = parent_scope.gauge
            self._sheet: Sheet_Identifier = parent_scope.sheet
            self._gauged_sheet_record: Gauged_Sheet_Record = parent_scope._gauged_sheet_record

    def copy(self) -> Machine_Scope:
        """Create a machine scope that is a copy of this machine scope.

        Returns:
            Machine_Scope: Machine scope that is a copy of this machine scope.
        """
        scope = Machine_Scope(self._machine_state)
        scope.direction = self.direction
        scope.carrier = self.carrier
        scope.racking = self.racking
        scope.gauge = self.gauge
        scope.sheet = self.sheet
        return scope

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
            raise TypeError(f"Direction has been set to non-direction {value}")
        self._direction = value

    @property
    def carrier(self) -> Yarn_Carrier_Set | None:
        """Get the current carrier being used by the machine.

        Returns:
            Yarn_Carrier_Set | None: The current carrier being used by the machine.
        """
        return self._carrier

    @carrier.setter
    def carrier(self, carrier: int | float | list[int] | Yarn_Carrier_Set | None) -> None:
        if isinstance(carrier, int):
            carrier = Yarn_Carrier_Set([carrier])
        elif isinstance(carrier, float):
            carrier = Yarn_Carrier_Set([int(carrier)])
        elif isinstance(carrier, list):
            carrier = Yarn_Carrier_Set(carrier)
        elif isinstance(carrier, Yarn_Carrier):
            carrier = Yarn_Carrier_Set([carrier.carrier_id])
        elif not isinstance(carrier, Yarn_Carrier_Set) and carrier is not None:
            raise TypeError(f"Expected carrier to bes set by int, list of ints,  Yarn Carrier (e.g., c1, c2.., c10) or a Yarn Carrier Set but got {carrier}")
        self._carrier = carrier

    @property
    def racking(self) -> float:
        """Get current racking of the machine.

        Returns:
            float: Current racking of the machine.
        """
        return self._racking

    @racking.setter
    def racking(self, value: float) -> None:
        self._racking = value

    @property
    def gauge(self) -> int:
        """Get the current number of sheets on the machine.

        Returns:
            int: The current number of sheets on the machine.
        """
        return self._gauge

    @gauge.setter
    def gauge(self, value: int | None) -> None:
        if value is None:
            value = 1
        if not (0 < value < 10):  # Todo Set max gauge based on header and knitscript context.
            raise Gauge_Value_Exception(value)
        if self.gauge != int(value):
            self._gauge = int(value)
            self._gauged_sheet_record = Gauged_Sheet_Record(value, self._machine_state)
            if 0 > int(self.sheet) or int(self.sheet) >= self.gauge:
                warnings.warn(Sheet_Beyond_Gauge_Warning(self.sheet, self.gauge))
                self.sheet = self.gauge - 1
            else:
                self.sheet = Sheet_Identifier(self.sheet.sheet, self.gauge)

    @property
    def sheet(self) -> Sheet_Identifier:
        """Get the current sheet being worked on the machine.

        Returns:
            Sheet_Identifier: The current sheet being worked on the machine.
        """
        return self._sheet

    @sheet.setter
    def sheet(self, value: int | Sheet_Identifier | None) -> None:
        if value is None:
            value = Sheet_Identifier(0, self.gauge)
        elif isinstance(value, int):
            if not (0 <= value < self.gauge):
                raise Sheet_Value_Exception(value, self.gauge)
            value = Sheet_Identifier(value, self.gauge)
        assert isinstance(value, Sheet_Identifier)
        if self.gauge != value.gauge:
            self.gauge = value.gauge
        if self.sheet != value:
            self._sheet = value
            self._machine_state.sheet = self.sheet.sheet
        if 0 > int(self.sheet) or int(self.sheet) >= self.gauge:
            warnings.warn(Sheet_Beyond_Gauge_Warning(self.sheet, self.gauge))
            self.sheet = self.gauge - 1

    def __getitem__(self, key: str) -> Any:
        if Machine_Variables.in_machine_variables(key):
            return Machine_Variables[key].get_value(self)
        return getattr(self, key)

    def __setitem__(self, key: str, value: Any) -> None:
        setattr(self, key, value)

    def __delitem__(self, key: str) -> None:
        delattr(self, key)

    def __contains__(self, key: str) -> bool:
        return Machine_Variables.in_machine_variables(key)
