"""Manages variable scope and machine state of knit pass during execution.

This module provides the Knit_Script_Context class, which serves as the primary execution context for knit script programs.
It manages variable scoping, machine state, and provides convenient access to machine configuration parameters.
The context integrates scope management with machine operations to provide a unified execution environment for knit script programs.
"""
from __future__ import annotations

from typing import Any

from knitout_interpreter.knitout_operations import Knitout_Comment_Line
from knitout_interpreter.knitout_operations.Header_Line import Knitout_Header_Line, Knitout_Header_Line_Type
from virtual_knitting_machine.Knitting_Machine import Knitting_Machine
from virtual_knitting_machine.Knitting_Machine_Specification import Knitting_Machine_Specification
from virtual_knitting_machine.knitting_machine_exceptions.Knitting_Machine_Exception import Knitting_Machine_Exception
from virtual_knitting_machine.machine_components.carriage_system.Carriage_Pass_Direction import Carriage_Pass_Direction
from virtual_knitting_machine.machine_components.needles.Needle import Needle
from virtual_knitting_machine.machine_components.needles.Sheet_Needle import Slider_Sheet_Needle, Sheet_Needle
from virtual_knitting_machine.machine_components.needles.Slider_Needle import Slider_Needle
from virtual_knitting_machine.machine_components.yarn_management.Yarn_Carrier_Set import Yarn_Carrier_Set, Yarn_Carrier
from virtual_knitting_machine.machine_components.needles.Sheet_Identifier import Sheet_Identifier

from knit_script.knit_script_exceptions.Knit_Script_Exception import Knit_Script_Exception, Knit_Script_Located_Exception
from knit_script.knit_script_exceptions.python_style_exceptions import Knit_Script_TypeError, Knit_Script_NameError, Knit_Script_AttributeError, Knit_Script_IndexError, Knit_Script_KeyError, \
    Knit_Script_ImportError, Knit_Script_ValueError
from knit_script.knit_script_interpreter._Context_Base import _Context_Base
from knit_script.knit_script_interpreter._parser_base import _Parser_Base
from knit_script.knit_script_interpreter.scope.gauged_sheet_schema import Gauged_Sheet_Record
from knit_script.knit_script_interpreter.scope.local_scope import Knit_Script_Scope
from knit_script.knit_script_std_library.carriers import cut_active_carriers


class _Carriers_Header_Line(Knitout_Header_Line):
    """Header line for carrier information in knitout format.

    This class generates knitout header lines that specify the available yarn carriers for the knitting machine.
    It handles the formatting and execution of carrier configuration information in the knitout output.

    Attributes:
        _carrier_ids (list[int]): List of carrier IDs available on the machine.
    """

    def __init__(self, carrier_ids: list[int], comment: str | None = None) -> None:
        """Initialize carrier header line.

        Args:
            carrier_ids (list[int]): List of carrier IDs to include in the header.
            comment (str | None, optional): Optional comment string for the header. Defaults to None.
        """
        self._carrier_ids = carrier_ids
        super().__init__(Knitout_Header_Line_Type.Carriers, carrier_ids, comment)

    def __str__(self) -> str:
        """Return string representation of carrier header.

        Returns:
            str: Formatted carrier header string in knitout format.
        """
        carrier_str = ""
        for cid in self._carrier_ids:
            carrier_str += f"{cid} "
        carrier_str = carrier_str[:-1]  # removing the space.
        return f";;{self.header_type}: {carrier_str}{self.comment_str}"

    def execute(self, machine_state: Knitting_Machine) -> bool:
        """Execute the carrier header on the machine state.

        Args:
            machine_state (Knitting_Machine): The knitting machine to configure.

        Returns:
            bool: True if execution was successful.
        """
        _carrier_count = len(self.header_value)
        # machine_state.carrier_system = carrier_count # Todo: allow dynamic setting of machine state
        return True


class Knit_Script_Context(_Context_Base):
    """Manages the state of the Knitting machine during program execution.

    The Knit_Script_Context class serves as the primary execution context for knit script programs.
    It extends the base context with variable scoping capabilities and provides convenient access to machine configuration parameters.
    The context manages the integration between variable scopes and machine state, ensuring that machine settings are properly maintained across different execution scopes.

    This class provides the execution environment for knit script programs, handling variable management, scope transitions, and machine state coordination.
    It offers convenient properties for accessing and modifying machine parameters while maintaining proper scope isolation and inheritance.

    Attributes:
        variable_scope (Knit_Script_Scope): The current variable scope for the execution context.
        last_carriage_pass_result (list[Needle] | dict[Needle, Needle | None]): Results from the most recent carriage pass operation.
    """

    def __init__(self, parent_scope: Knit_Script_Scope | None = None, machine_specification: Knitting_Machine_Specification = Knitting_Machine_Specification(), ks_file: str | None = None,
                 parser: _Parser_Base | None = None):
        """Initialize the knit script context.

        Args:
            parent_scope (Knit_Script_Scope | None, optional): Parent scope for variable management inheritance. Defaults to None.
            machine_specification (Knitting_Machine_Specification, optional): Specification for the knitting machine configuration. Defaults to Knitting_Machine_Specification().
            ks_file (str | None, optional): Path to the knit script file being executed. Defaults to None.
            parser (Knit_Script_Parser | None, optional): Parser instance for processing knit script syntax. Defaults to None.
        """
        super().__init__(machine_specification, ks_file, parser)
        self.variable_scope: Knit_Script_Scope = Knit_Script_Scope(self, parent_scope)
        self.last_carriage_pass_result: list[Needle] | dict[Needle, Needle | None] = {}

    @property
    def gauged_sheet_record(self) -> Gauged_Sheet_Record:
        """Get the current record of loops stored on each sheet in the current gauge.

        Returns:
            Gauged_Sheet_Record: The current record of loops stored on each sheet in the current gauge configuration.
        """
        return self.variable_scope.machine_scope.gauged_sheet_record

    def add_variable(self, key: str, value: Any) -> None:
        """Add a variable to the variable scope by the name of key.

        Args:
            key (str): Name of variable to be used in the knit script.
            value (Any): Value of the variable to store in the scope.
        """
        self.variable_scope.__setattr__(key, value)

    def enter_sub_scope(self, function_name: str | None = None, module_name: str | None = None, module_scope: Knit_Script_Scope | None = None) -> Knit_Script_Scope:
        """Create a child scope and set it as the current variable scope.

        Args:
            function_name (str | None, optional): The name of the function owning this scope. Defaults to None.
            module_name (str | None, optional): The name of the module owning this scope. Defaults to None.
            module_scope (Knit_Script_Scope | None, optional): The scope of the function declaration context. Defaults to None.

        Returns:
            Knit_Script_Scope: The scope that was entered and is now active.
        """
        if function_name is not None:
            self.variable_scope = self.variable_scope.enter_new_scope(function_name, is_function=True, module_scope=module_scope)
        elif module_name is not None:
            self.variable_scope = self.variable_scope.enter_new_scope(module_name, is_module=True, module_scope=module_scope)
        else:
            self.variable_scope = self.variable_scope.enter_new_scope(module_scope=module_scope)
        return self.variable_scope

    def exit_current_scope(self, collapse_into_parent: bool = False) -> None:
        """Exit the lowest level variable scope and reset the current variable scope up a level.

        Args:
            collapse_into_parent (bool, optional): If True, brings values from lower scope into the next scope level. Defaults to False.
        """
        self.variable_scope = self.variable_scope.exit_current_scope(collapse_into_parent)

    @property
    def sheet_needle_count(self, gauge: int | None = None) -> int:
        """Get the needle count of the bed broken up by current gauge.

        Args:
            gauge (int | None): The gauge to calculate needle count for. If None, uses current gauge.

        Returns:
            int: The needle count per sheet in the specified gauge configuration.
        """
        return int(self.machine_state.needle_count / gauge)

    @property
    def direction(self) -> Carriage_Pass_Direction:
        """Get the carriage pass direction at current scope.

        Returns:
            Carriage_Pass_Direction: The current carriage pass direction.
        """
        return self.variable_scope.direction

    @direction.setter
    def direction(self, value: Carriage_Pass_Direction) -> None:
        """Set the carriage pass direction.

        Args:
            value (Carriage_Pass_Direction): The direction to set for carriage movement.
        """
        self.variable_scope.direction = value

    @property
    def carrier(self) -> Yarn_Carrier_Set | None:
        """Get the carrier in use at current scope.

        Returns:
            Yarn_Carrier_Set | None: The current carrier set or None if no carrier is active.
        """
        return self.variable_scope.Carrier

    @carrier.setter
    def carrier(self, carrier: int | float | list[int | Yarn_Carrier] | Yarn_Carrier_Set | Yarn_Carrier | None) -> None:
        """Set the active carrier.

        Args:
            carrier (int | float | list[int | Yarn_Carrier] | Yarn_Carrier_Set | Yarn_Carrier | None): The value to set the carrier set by.
        """
        self.variable_scope.Carrier = carrier  # update working carrier variable

    @property
    def racking(self) -> float:
        """Get the racking at current scope.

        Returns:
            float: The current racking value.
        """
        return float(self.variable_scope.Racking)

    @racking.setter
    def racking(self, value: float) -> None:
        """Set the racking value.

        Args:
            value (float): The racking value to set.
        """
        self.variable_scope.Racking = value

    @property
    def sheet(self) -> Sheet_Identifier:
        """Get the current sheet at current scope.

        Returns:
            Sheet_Identifier: The current sheet identifier.
        """
        return self.variable_scope.Sheet

    @sheet.setter
    def sheet(self, value: Sheet_Identifier | int | None) -> None:
        """Set the current sheet.

        Args:
            value (Sheet_Identifier | int | None): The sheet value to set.
        """
        self.variable_scope.Sheet = value

    @property
    def gauge(self) -> int:
        """Get the gauge (number of layers) that is being worked.

        Note:
            Resetting gauge will cause the machine state to forget all current layer records.

        Returns:
            int: The current gauge value.
        """
        return int(self.variable_scope.Gauge)

    @gauge.setter
    def gauge(self, value: int | None) -> None:
        """Set the gauge value.

        Args:
            value (int | None): The gauge value to set.
        """
        self.variable_scope.Gauge = value

    def execute_statements(self, statements: list) -> None:
        """Execute the list of statements on current context.

        Args:
            statements (list): Statements to execute in the current context.

        Raises:
            AssertionError: If assertions in the script fail during execution.
            Knit_Script_Exception: If knit script specific errors occur during interpretation or execution.
            Knitting_Machine_Exception: If machine operation errors occur during the knitting process.
        """
        for statement in statements:
            try:
                statement.execute(self)
            except Exception as e:
                self.knitout.extend(cut_active_carriers(self.machine_state))
                if len(self.knitout) > 0:
                    with open(f"error.k", "w") as out:
                        out.writelines([str(k) for k in self.knitout])
                        if isinstance(e, (Knitting_Machine_Exception, Knit_Script_Exception)):
                            error_comments = [Knitout_Comment_Line(e.message)]
                            out.writelines([str(ec) for ec in error_comments])
                if not isinstance(e, Knit_Script_Located_Exception):
                    if isinstance(e, TypeError):
                        raise Knit_Script_TypeError(str(e), statement)
                    elif isinstance(e, NameError):
                        raise Knit_Script_NameError(str(e), statement)
                    elif isinstance(e, AttributeError):
                        raise Knit_Script_AttributeError(str(e), statement)
                    elif isinstance(e, IndexError):
                        raise Knit_Script_IndexError(str(e), statement)
                    elif isinstance(e, KeyError):
                        raise Knit_Script_KeyError(str(e), statement)
                    elif isinstance(e, ImportError):
                        raise Knit_Script_ImportError(str(e), statement)
                    elif isinstance(e, ValueError):
                        raise Knit_Script_ValueError(str(e), statement)
                    else:
                        raise Knit_Script_Located_Exception(e, statement)
                else:
                    raise e

    def get_needle(self, is_front: bool, pos: int, is_slider: bool = False, global_needle: bool = False, sheet: int | None = None, gauge: int | None = None) -> Needle:
        """Get a needle based on current gauging configuration.

        Args:
            is_front (bool): Whether this is a front needle.
            pos (int): Position within the current layer.
            is_slider (bool, optional): Whether this is a slider needle. Defaults to False.
            global_needle (bool, optional): If true, ignore the gauging scheme. Defaults to False.
            sheet (int | None, optional): Specify the sheet to get needles from, defaults to the current sheet. Defaults to None.
            gauge (int | None, optional): Specify gauging to get needles from, defaults to current gauge. Defaults to None.

        Returns:
            Needle: Needle based on current gauging configuration.
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

    def get_machine_needle(self, is_front: bool, pos: int, is_slider: bool = False, global_needle: bool = False, sheet: int | None = None, gauge: int | None = None) -> Needle:
        """Get the exact needle instance in use on the machine state.

        Args:
            is_front (bool): Whether this is a front needle.
            pos (int): Position in current layer.
            is_slider (bool, optional): Whether this is a slider needle. Defaults to False.
            global_needle (bool, optional): If true, ignore the gauging scheme. Defaults to False.
            sheet (int | None, optional): Specify the sheet to get needles from, defaults to the current sheet. Defaults to None.
            gauge (int | None, optional): Specify gauging to get needles from, defaults to current gauge. Defaults to None.

        Returns:
            Needle: The exact needle instance in use on the machine state.
        """
        return self.machine_state[self.get_needle(is_front, pos, is_slider, global_needle, sheet, gauge)]
