"""Scope of machine variables.

This module provides the Machine_Scope class, which manages machine state and configuration within different execution scopes of a knit script program.
It tracks machine settings like carriage direction, active carriers, racking position, gauge configuration, and active sheets
while automatically generating appropriate knitout instructions when these settings change.
The machine scope integrates with the broader scoping system to provide proper inheritance and isolation of machine state across different program contexts.
"""

from __future__ import annotations

import warnings
from collections.abc import Sequence
from typing import TYPE_CHECKING, cast

from knitout_interpreter.knitout_operations.carrier_instructions import Inhook_Instruction, Releasehook_Instruction
from knitout_interpreter.knitout_operations.Knitout_Line import Knitout_Comment_Line
from knitout_interpreter.knitout_operations.Rack_Instruction import Rack_Instruction
from virtual_knitting_machine.Knitting_Machine import Knitting_Machine
from virtual_knitting_machine.knitting_machine_exceptions.Yarn_Carrier_Error_State import Yarn_Carrier_Exception
from virtual_knitting_machine.machine_components.carriage_system.Carriage_Pass_Direction import Carriage_Pass_Direction
from virtual_knitting_machine.machine_components.needles.Sheet_Identifier import Sheet_Identifier
from virtual_knitting_machine.machine_components.yarn_management.Yarn_Carrier import Yarn_Carrier
from virtual_knitting_machine.machine_components.yarn_management.Yarn_Carrier_Set import Yarn_Carrier_Set

from knit_script.knit_script_interpreter.scope.gauged_sheet_schema.Gauged_Sheet_Record import Gauged_Sheet_Record
from knit_script.knit_script_warnings.Knit_Script_Warning import Gauge_Value_Warning, Negative_Sheet_Warning, Sheet_Beyond_Gauge_Warning

if TYPE_CHECKING:
    from knit_script.knit_script_interpreter.knit_script_context import Knit_Script_Context


class Machine_Scope:
    """Keeps track of the machine state within different scopes.

    The Machine_Scope class manages knitting machine configuration and state within a specific execution scope.
    It tracks essential machine parameters including carriage direction, active yarn carriers, racking position, gauge settings, and active sheet configuration.
    When these parameters are modified, the class automatically generates the appropriate knitout instructions to implement the changes on the physical machine.

    This class provides scope-aware machine state management,
    allowing different parts of a knit script program to have different machine configurations while maintaining proper inheritance and isolation.
    It integrates with the gauged sheet system to handle complex multi-sheet knitting operations and ensures that machine state changes are properly reflected in the generated knitout code.
    """

    def __init__(self, context: Knit_Script_Context, prior_settings: Machine_Scope | None = None) -> None:
        """Initialize the machine scope with default settings or inherited from prior scope.

        Creates a new machine scope with default machine settings, then optionally inherits settings from a parent scope.
        This allows child scopes to start with the same machine configuration as their parent while maintaining the ability to make local changes.

        Args:
            context (Knit_Script_Context): The execution context that this machine scope operates within.
            prior_settings (Machine_Scope | None, optional): A parent machine scope to inherit settings from. If provided, all machine settings will be copied from this scope. Defaults to None.
        """
        self._context: Knit_Script_Context = context
        self._direction: Carriage_Pass_Direction = self.machine_state.carriage.last_direction
        self._working_carrier: Yarn_Carrier_Set | None = None
        all_needle_mod = 0.0
        if self.machine_state.all_needle_rack:
            all_needle_mod = 0.25 if self.machine_state.rack >= 0 else -0.75
        self._working_racking: float = self.machine_state.rack + all_needle_mod
        self._gauge: int = 1
        self._sheet: Sheet_Identifier = Sheet_Identifier(0, self._gauge)
        self._gauged_sheet_record: Gauged_Sheet_Record = Gauged_Sheet_Record(self.Gauge, self.machine_state)
        if prior_settings is not None:  # Update these values but do not update the machine state.
            self.inherit_from_scope(prior_settings, inherit_raw_values=True)

    @property
    def machine_state(self) -> Knitting_Machine:
        """Get the current machine state in the current context.

        Returns:
            Knitting_Machine: The current machine state in the current context.
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
        """Set the current direction the carriage will take.

        Args:
            value (Carriage_Pass_Direction): The direction to set for carriage movement.

        Raises:
            TypeError: If value is not a Carriage_Pass_Direction instance.
        """
        if not isinstance(value, Carriage_Pass_Direction):
            raise TypeError(f"Direction cannot be set to to non-direction {value}")
        self._direction = value

    @property
    def Carrier(self) -> Yarn_Carrier_Set | None:
        """Get the current carrier being used by the machine.

        Returns:
            Yarn_Carrier_Set | None: The current carrier being used by the machine, or None if no carrier is active.
        """
        return self._working_carrier

    @Carrier.setter
    def Carrier(self, carrier: int | float | Sequence[int | Yarn_Carrier] | Yarn_Carrier_Set | Yarn_Carrier | None) -> None:
        """Set the working carrier.

        Adds inhook/in operations as needed to work with inactive carriers.
        When a carrier is set that is not currently active on the machine,
        appropriate activation instructions (inhook for loose yarns, in for gripped yarns) are automatically generated and added to the knitout.

        Args:
            carrier (int | float | Sequence[int | Yarn_Carrier] | Yarn_Carrier_Set | Yarn_Carrier | None): The value to interpret into a new working yarn carrier set.
            Can be a single carrier ID, a list of carrier IDs, or carrier objects.

        Raises:
            TypeError: If carrier is not one of the accepted types.
        """
        if isinstance(carrier, float):
            carrier_set: Yarn_Carrier_Set | None = Yarn_Carrier_Set(int(carrier))
        elif isinstance(carrier, (int, Sequence, Yarn_Carrier)):
            carrier_set = Yarn_Carrier_Set(carrier)
        else:
            carrier_set = carrier
        if not isinstance(carrier_set, Yarn_Carrier_Set) and carrier_set is not None:
            raise TypeError(f"Cannot set Carrier to value {carrier}.\n\tExpected Carrier to be one or more carriers or numbers")
        if self._working_carrier != carrier_set:
            self._working_carrier = carrier_set
            if self.Carrier is not None:  # Check for missing carrier to inhook prior to operations.
                missing_carriers = self.machine_state.carrier_system.missing_carriers(cast(list[int | Yarn_Carrier], self.Carrier.carrier_ids))
                if len(missing_carriers) > 1:
                    raise Yarn_Carrier_Exception(missing_carriers[1], f"Cannot Inhook multiple carriers at once without unstable yarns. \n\tActivate missing carriers <{missing_carriers}>")
                elif len(missing_carriers) == 1:
                    if self.machine_state.carrier_system.hooked_carrier is not None:
                        release_op = Releasehook_Instruction.execute_releasehook(self.machine_state, self.machine_state.carrier_system.hooked_carrier)
                        self._context.knitout.append(release_op)
                    inhook_op = Inhook_Instruction.execute_inhook(self.machine_state, missing_carriers[0])
                    self._context.knitout.append(inhook_op)

    @property
    def last_working_carrier(self) -> Yarn_Carrier_Set | None:
        """
        Returns:
            Yarn_Carrier_Set | None: The explicitly set working carrier or the active carrier with the most recently formed loop or None if there are no active carriers.
        """
        if self._working_carrier is not None:
            return self._working_carrier
        elif len(self.machine_state.carrier_system.active_carriers) > 0:
            latest_used_carrier = max(self.machine_state.carrier_system.active_carriers, key=lambda carrier: max(carrier.yarn.active_loops))
            return Yarn_Carrier_Set(latest_used_carrier)
        else:
            return None

    @property
    def Racking(self) -> float:
        """
        Returns:
            float: Current racking of the machine as a floating-point value.
        """
        return self._working_racking

    @Racking.setter
    def Racking(self, rack: float) -> None:
        """Set the current racking of the machine.

        When the racking value changes, automatically generates a rack instruction with the gauge-adjusted racking value and appends it to the knitout.
        The actual racking sent to the machine is multiplied by the current gauge value.

        Args:
            rack (float): The new racking value to set.
        """
        if rack != self.Racking:
            self._working_racking = rack
            gauge_adjusted_racking = self.Gauge * self.Racking
            rack_instruction = Rack_Instruction.execute_rack(self.machine_state, gauge_adjusted_racking, comment=None if self.Gauge == 1 else f"{rack} Rack adjusted for 1/{self.Gauge} gauge")
            self._context.knitout.append(rack_instruction)

    @property
    def Rack(self) -> float:
        """
        Returns:
            float: Current racking of the machine as a floating-point value.
        """
        return self.Racking

    @Rack.setter
    def Rack(self, racking: float) -> None:
        """
        Alternate name for setter for the Racking property.
        Args:
            racking (float): Current racking of the machine as a floating-point value.
        """
        self.Racking = racking

    @property
    def gauged_sheet_record(self) -> Gauged_Sheet_Record:
        """Get the gauged sheet record associated with this machine scope.

        Returns:
            Gauged_Sheet_Record: The gauged sheet record associated with this machine scope, which tracks loop positions and sheet organization.
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
    def Gauge(self, gauge_value: int | None) -> None:
        """Set the current gauge (number of sheets) on the machine.

        When the gauge changes, creates a new gauged sheet record and adjusts the current sheet if necessary to ensure it remains within the valid range.
        Issues warnings if the current sheet exceeds the new gauge limits.

        Args:
            gauge_value (int | None): The new gauge value. If None, defaults to 1. Must be between 1 and 9 inclusive.

        Raises:
            Gauge_Value_Exception: If the gauge value is not between 1 and 9 inclusive.

        Warns:
            Sheet_Beyond_Gauge_Warning: If the current sheet number exceeds the new gauge limits.
        """
        gauge = gauge_value if gauge_value is not None else 1
        if gauge < 1:
            warnings.warn(Gauge_Value_Warning(gauge), stacklevel=1)
            gauge = 1
        if self.Gauge != gauge:
            self._gauged_sheet_record = Gauged_Sheet_Record(gauge, self.machine_state)  # change in gauge forces new gauge-sheet record to be created.
            self._gauge = gauge
            self.Sheet = Sheet_Identifier(self.Sheet.sheet, gauge)  # Sheet change will handle any discrepancies in sheet-gauge range values.

    @property
    def Sheet(self) -> Sheet_Identifier:
        """Get the current sheet being worked on the machine.

        Returns:
            Sheet_Identifier: The current sheet being worked on the machine.
        """
        return self._sheet

    @Sheet.setter
    def Sheet(self, sheet_value: int | Sheet_Identifier | None) -> None:
        """Set the current active sheet on the machine.

        When the sheet changes, automatically generates sheet reset instructions and appends them to the knitout.
        Also validates that the sheet number is within the current gauge limits and issues warnings for out-of-range values.

        Args:
            sheet_value (int | Sheet_Identifier | None): The sheet to set as active. If None, defaults to sheet 0. If an integer, must be within the current gauge range.

        Warns:
            Sheet_Beyond_Gauge_Warning: If the sheet number is outside the valid range and gets automatically corrected.
            Negative_Sheet_Warning: If the sheet number is less than 0 and automatically reset to 0.
        """
        if sheet_value is None:
            sheet = 0
            gauge = self.Gauge
        elif isinstance(sheet_value, int):
            sheet = sheet_value
            gauge = self.Gauge
        else:
            sheet = sheet_value.sheet
            gauge = sheet_value.gauge
        if sheet < 0:
            warnings.warn(Negative_Sheet_Warning(sheet), stacklevel=1)
            sheet = 0
        elif gauge <= sheet:
            warnings.warn(Sheet_Beyond_Gauge_Warning(sheet, gauge), stacklevel=1)
            sheet = gauge - 1
        if self.Gauge != gauge:
            self.Gauge = gauge
        if self.Sheet != Sheet_Identifier(sheet, self.Gauge):
            self._sheet = Sheet_Identifier(sheet, self.Gauge)
            self._context.knitout.append(Knitout_Comment_Line(f"Resetting to sheet {self.Sheet} of {self.Gauge}"))
            self._context.knitout.extend(self.gauged_sheet_record.reset_to_sheet(self.Sheet.sheet))

    def inherit_from_scope(self, scope: Machine_Scope, inherit_raw_values: bool = False) -> None:
        """Set the machine scope values based on the given scope.

        Copies all machine configuration settings from the specified scope to this scope, including direction, carrier, racking, gauge, sheet, and gauged sheet record.
        This method is used to establish initial settings when creating child scopes.

        Args:
            inherit_raw_values (bool): If true, don't use the property setters which may modify the knitout.
            scope (Machine_Scope): The machine scope to inherit the values from.
        """
        if inherit_raw_values:
            self._direction = scope.direction
            self._working_carrier = scope.Carrier
            self._working_racking = scope.Racking
            self._gauge = scope.Gauge
            self._sheet = scope.Sheet
        else:
            self.direction = scope.direction
            self.Carrier = scope.Carrier
            self.Racking = scope.Racking
            self.Gauge = scope.Gauge
            self.Sheet = scope.Sheet
        self._gauged_sheet_record = scope._gauged_sheet_record

    def update_parent_machine_scope(self, parent_scope: Machine_Scope) -> None:
        """
        Passes machine status values up to the given parent scope with the following effects:
        * Resets the rack of the machine to the racking value of the parent scope.
        * Sets the direction of the parent scope to match the direction of this scope.
        * Update the sheet to the sheet in the parent scope.
        * Update the gauge sheet record of the parent to reflect the current state.

        Args:
            parent_scope (Machine_Scope): The parent machine scope to pass values up to.
        """
        self.Racking = parent_scope.Racking  # will trigger a rack instruction to be added if there is a shift back to a prior racking
        parent_scope.direction = self._direction
        self.Sheet = parent_scope.Sheet  # set back to prior sheet before passing record along.
        parent_scope._gauged_sheet_record = self._gauged_sheet_record

    def __contains__(self, variable_name: str) -> bool:
        """

        Args:
            variable_name (str): The variable to search for in the machine scope.

        Returns:
            bool: True if the variable name is a machine scope property, False otherwise.
        """
        return hasattr(self, variable_name) and isinstance(getattr(type(self), variable_name, None), property)

    def __getitem__(self, variable_name: str) -> Sheet_Identifier | int | float | Yarn_Carrier_Set | Carriage_Pass_Direction | Knitting_Machine | None:
        """
        Args:
            variable_name (str): The variable to get from the machine scope.

        Returns:
            Sheet_Identifier | int | float | Yarn_Carrier_Set | Carriage_Pass_Direction | Knitting_Machine | None:
                The value to return from the machine scope.
                * Sheet will return a Sheet_Identifier.
                * Gauge will return an integer.
                * Racking or Rack will return a float.
                * Carrier will return a Yarn_Carrier_Set or None if there is not working carrier.
                * Direction will return a Carriage_Pass_Direction.
                * machine_state will return the current knitting machine state.

        Raises:
            AttributeError: If the variable name is not a machine scope variable.
        """
        if variable_name not in self:
            raise AttributeError(f"Cannot get attribute {variable_name} from Machine Scope.\n\t Expected Sheet, Gauge, Rack, Racking, Carrier, Direction, or machine_state")
        return cast((Sheet_Identifier | int | float | Yarn_Carrier_Set | Carriage_Pass_Direction | Knitting_Machine | None), getattr(self, variable_name))

    def __setitem__(self, variable_name: str, value: int | float | Sheet_Identifier | Sequence[int | Yarn_Carrier] | Yarn_Carrier_Set | Yarn_Carrier | Carriage_Pass_Direction | None) -> None:
        """
        Sets the given value to the specified machine scope variable.
        Args:
            variable_name (str): The variable to set to the machine scope. Expects: Sheet, Gauge, Rack, Racking, Carrier, or Direction.
            value (int | float | Sheet_Identifier | Sequence[int | Yarn_Carrier] | Yarn_Carrier_Set | Yarn_Carrier | Carriage_Pass_Direction | None): The value to set the specified variable.

        Raises:
            AttributeError: If the variable name is not a machine scope variable.
        """
        if variable_name not in self or variable_name == "machine_state":
            raise AttributeError(f"Cannot set attribute {variable_name} in Machine Scope.")
        setattr(self, variable_name, value)
