"""Code manages a variable scope symbol table with undefined variables by default"""
from __future__ import annotations
from typing import Any

from virtual_knitting_machine.machine_components.carriage_system.Carriage_Pass_Direction import Carriage_Pass_Direction
from virtual_knitting_machine.machine_components.needles.Sheet_Needle import Sheet_Identifier
from virtual_knitting_machine.machine_components.yarn_management.Yarn_Carrier_Set import Yarn_Carrier_Set

from knit_script.knit_script_exceptions.ks_exceptions import Gauge_Value_Exception


class Variable_Scope:
    """A table that manages function scope for knit-pass variables."""

    def __init__(self, parent_scope: Variable_Scope | None = None, function_name: str | None = None) -> None:
        """Instantiate the variable scope.

        Args:
            parent_scope: Scope for entering sub-scope, defaults to none at top
            function_name: The name of the function that this scope belongs to, may be none
        """
        self._parent_name: str | None = function_name
        self._parent_scope: Variable_Scope | None = parent_scope
        self._child_scope: Variable_Scope | None = None
        self._variable_values: dict[str, Any] = {}
        self.return_value: Any = None
        self.has_return: bool = False
        self._direction_id: str = "Direction"
        self._carrier_id: str = "Carrier"
        self._rack_id: str = "Racking"
        self._sheet_id: str = "Sheet"
        self._gauge_id: str = "Gauge"
        self._reserved_words: set[str] = {"def", "while", "try", "catch", "for", "in", "assert", "print", "pause",
                                          "if", "elif", "else", "not", "with", "as", "return",
                                          "None", "direction", "across", "Carrier", "Bed", "direction", "reverse", "machine",
                                          "knit", "tuck", "split", "miss", "drop", "xfer", "cut", "remove",
                                          "to", "slider", "sliders", "needles", "on", "every", "even", "odd", "other",
                                          "of", "from", "layer", "at", "rack", "all", "current", "carrier", "push", "sheets",
                                          "True", "False", self._direction_id, self._carrier_id, self._rack_id, self._gauge_id
                                          }
        if self._parent_scope is None:
            self.current_direction = Carriage_Pass_Direction.Leftward
            self.current_carrier = None
            self.current_racking = 0
            self.current_gauge = 1
            self.current_sheet = 0

    @property
    def _is_function_scope(self) -> bool:
        """Checks if this is a function scope.

        Returns:
            True if this scope belongs to a function
        """
        return self._parent_name is not None

    def return_scope(self, set_value: bool = False, value: Any = None) -> Variable_Scope | None:
        """Collect the scope that holds a return value.

        Args:
            set_value: If True, sets the given value as the return value
            value: Value to be returned

        Returns:
            The function_scope that has the set return value
        """
        if set_value:  # set by return statements, otherwise pass up what is there
            self.return_value = value
        scope: Variable_Scope | None = self
        while scope is not None and not scope._is_function_scope:  # Not a function, continue
            if scope._parent_scope is not None:
                scope._parent_scope.return_value = self.return_value
            scope = scope.exit_current_scope()  # returns parent scope with stored return value
        return scope

    def is_main(self) -> bool:
        """Checks if this is the outermost (main) scope.

        Returns:
            True if this is the outermost (main) scope
        """
        return self._parent_scope is None

    @property
    def current_sheet(self) -> Sheet_Identifier:
        """The active sheet_id for N-Bed Knitting.

        Returns:
            The active sheet identifier
        """
        return self[self._sheet_id]

    @current_sheet.setter
    def current_sheet(self, value: int | Sheet_Identifier | None) -> None:
        """Sets the current sheet.

        Args:
            value: The sheet value to set

        Raises:
            AssertionError: If sheet value is out of valid range
        """
        if value is None:
            value = Sheet_Identifier(0, self.current_gauge)
        elif isinstance(value, int):
            assert 0 <= value < self.current_gauge, \
                f"Sheet must be between 0 and gauge {self.current_gauge}, {value}"
            value = Sheet_Identifier(value, self.current_gauge)
        assert isinstance(value, Sheet_Identifier)
        self.current_gauge = value.gauge
        self[self._sheet_id] = value

    @property
    def current_gauge(self) -> int:
        """The current Gauge being worked, the number of layers that can be accessed.

        Returns:
            The current gauge value

        Raises:
            Gauge_Value_Exception: If gauge is in invalid range
        """
        gauge = int(self[self._gauge_id])
        if 0 < gauge < 10:  # Todo better handling of MAX Gauge
            raise Gauge_Value_Exception(gauge)
        return gauge

    @current_gauge.setter
    def current_gauge(self, value: int | None) -> None:
        """Sets the current gauge.

        Args:
            value: The gauge value to set

        Raises:
            Gauge_Value_Exception: If gauge is in invalid range
        """
        if value is None:
            value = 1
        if 0 < value < 10:  # Todo better handling of MAX Gauge
            raise Gauge_Value_Exception(value)
        self[self._gauge_id] = int(value)

    @property
    def current_direction(self) -> Carriage_Pass_Direction:
        """Machine direction at current scope.

        Returns:
            The current carriage pass direction
        """
        direction = self[self._direction_id]
        return direction

    @current_direction.setter
    def current_direction(self, value: Carriage_Pass_Direction) -> None:
        """Sets the current direction.

        Args:
            value: The direction to set

        Raises:
            AssertionError: If value is not a valid direction
        """
        assert isinstance(value, Carriage_Pass_Direction), f"Direction has been set to non-direction {value}"
        self[self._direction_id] = value

    @property
    def current_carrier(self) -> Yarn_Carrier_Set | None:
        """Active carrier at current scope.

        Returns:
            The current carrier or None
        """
        carrier = self[self._carrier_id]
        return carrier

    @current_carrier.setter
    def current_carrier(self, carrier: Yarn_Carrier_Set | None) -> None:
        """Sets the current carrier.

        Args:
            carrier: The carrier to set

        Raises:
            TypeError: If carrier is not a valid type
        """
        if isinstance(carrier, int):
            carrier = Yarn_Carrier_Set([carrier])
        elif isinstance(carrier, float):
            carrier = Yarn_Carrier_Set([int(carrier)])
        elif isinstance(carrier, list):
            carrier = Yarn_Carrier_Set(carrier)
        elif not isinstance(carrier, Yarn_Carrier_Set) and carrier is not None:
            raise TypeError(f"Cannot set Carrier to non-carrier, int, or list of ints/carriers {carrier}")
        self[self._carrier_id] = carrier

    @property
    def current_racking(self) -> int:
        """Racking value at scope.

        Returns:
            The current racking value
        """
        return int(self[self._rack_id])

    @current_racking.setter
    def current_racking(self, value: int) -> None:
        """Sets the current racking.

        Args:
            value: The racking value to set
        """
        self[self._rack_id] = value

    def is_reserved_word(self, word: str) -> bool:
        """Checks if a word is reserved in the language.

        Args:
            word: The word being checked

        Returns:
            True if the word is reserved in the language
        """
        return word in self._reserved_words

    def exit_current_scope(self) -> Variable_Scope | None:
        """Exits the current scope.

        Returns:
            The parent scope with no reference to current function scope
        """
        if self._parent_scope is not None:
            self._parent_scope._child_scope = None
        return self._parent_scope

    def enter_new_scope(self, function_name: str | None = None) -> Variable_Scope:
        """Creates and enters a new child scope.

        Args:
            function_name: Name of the function for this scope

        Returns:
            Child scope that is created and connected to current scope
        """
        self._child_scope = Variable_Scope(self, function_name=function_name)
        return self._child_scope

    def get_var(self, var_name: str) -> Any:
        """Gets the value of a variable.

        Args:
            var_name: The name of the variable to get a value of

        Returns:
            The value of the variable at the given scope

        Raises:
            KeyError: If variable is not in scope
        """
        current_scope: Variable_Scope | None = self
        while current_scope is not None:
            if var_name in current_scope._variable_values:
                return current_scope._variable_values[var_name]
            current_scope = current_scope._parent_scope
        if current_scope is None:
            raise KeyError(f"Variable {var_name} is not in scope")

    def __getitem__(self, var_name: str) -> Any:
        """Gets a variable value using bracket notation.

        Args:
            var_name: The variable name to get

        Returns:
            The variable value
        """
        return self.get_var(var_name)

    def set_var(self, var_name: str, value: Any) -> None:
        """Sets a variable value.

        Args:
            var_name: The variable to set
            value: The value to set the variable to
        """
        # assert var_name not in self._reserved_words, f"Cannot assign to {var_name} is a reserved keyword"
        if var_name in self:  # Move up scope to set the value
            current_scope: Variable_Scope | None = self
            while current_scope is not None:
                if var_name in current_scope._variable_values:
                    current_scope._variable_values[var_name] = value
                    return
                current_scope = current_scope._parent_scope
        else:  # set the new value at this scope
            self._variable_values[var_name] = value

    def __setitem__(self, var_name: str, value: Any) -> None:
        """Sets a variable value using bracket notation.

        Args:
            var_name: The variable name to set
            value: The value to set
        """
        return self.set_var(var_name, value)

    def var_in_scope(self, var_name: str) -> bool:
        """Checks if a variable exists in scope.

        Args:
            var_name: The name of the variable to check for

        Returns:
            True if the variable is in the scope of the given function
        """
        current_scope: Variable_Scope | None = self
        while current_scope is not None:
            if var_name in current_scope._variable_values:
                return True
            current_scope = current_scope._parent_scope
        return False

    def __contains__(self, var_name: str) -> bool:
        """Checks if a variable is in scope using 'in' operator.

        Args:
            var_name: The variable name to check

        Returns:
            True if variable is in scope
        """
        return self.var_in_scope(var_name)

    def delete_item_in_scope(self, var_name: str) -> None:
        """Removes a variable from scope.

        Args:
            var_name: The name of the variable to remove at scope
        """
        current_scope: Variable_Scope | None = self
        while current_scope is not None:
            if var_name in current_scope._variable_values:
                del current_scope._variable_values[var_name]
            current_scope = current_scope._parent_scope

    def __delitem__(self, var_name: str) -> None:
        """Deletes a variable using del operator.

        Args:
            var_name: The variable name to delete
        """
        self.delete_item_in_scope(var_name)

    def var_depth(self) -> int:
        """Gets the depth of this scope.

        Returns:
            The depth of this scope
        """
        d = -1
        current_scope: Variable_Scope | None = self
        while current_scope is not None:
            d += 1
            current_scope = current_scope._parent_scope
        return d

    def __str__(self) -> str:
        """Returns string representation of the scope.

        Returns:
            String representation showing scope hierarchy
        """
        scope_str = f"{self.var_depth()}"
        if self._is_function_scope:
            scope_str = f"{self._parent_name}({scope_str})"
        if self.has_return:
            scope_str = f"{scope_str}=={self.return_value}"
        if self._parent_scope is None:
            return scope_str
        else:
            return f"{self._parent_scope}->{scope_str}"
