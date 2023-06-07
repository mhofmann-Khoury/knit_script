"""Code manages a variable scope symbol table with undefined variables by default"""
from typing import Dict, Any, Optional, Set, Union

from knit_script.knitting_machine.Machine_State import Machine_State
from knit_script.knitting_machine.machine_components.Sheet_Needle import Sheet_Identifier
from knit_script.knitting_machine.machine_components.machine_pass_direction import Pass_Direction
from knit_script.knitting_machine.machine_components.yarn_management.Carrier_Set import Carrier_Set


class Variable_Scope:
    """
        A table that manages function scope for knit-pass variables
    """

    def __init__(self, parent_scope=None, function_name: Optional[str] = None):
        """
        Instantiate
        :param parent_scope: scope for entering sub-scope, defaults to none at top
        :param function_name: the name of the function that this scope belongs to, may be none
        """
        self._parent_name: Optional[str] = function_name
        self._parent_scope: Optional[Variable_Scope] = parent_scope
        self._child_scope: Optional[Variable_Scope] = None
        self._variable_values: Dict[str, Any] = {}
        self.return_value: Any = None
        self.has_return: bool = False
        self._direction_id = "Direction"
        self._carrier_id = "Carrier"
        self._rack_id = "Racking"
        self._sheet_id = "Sheet"
        self._gauge_id = "Gauge"
        self._reserved_words: Set[str] = {"def", "while", "try", "catch", "for",  "in","assert", "print", "pause",
                                          "if", "elif", "else", "not", "with", "as", "return",
                                          "None", "direction",  "across","Carrier", "Bed", "direction", "reverse", "machine",
                                          "knit", "tuck", "split", "miss", "drop", "xfer", "cut", "remove",
                                          "to", "slider", "sliders", "needles", "on", "every", "even", "odd", "other",
                                          "of", "from", "layer", "at", "rack", "all", "current", "carrier", "push",  "sheets",
                                          "True", "False", self._direction_id, self._carrier_id, self._rack_id, self._gauge_id
                                          }
        if self._parent_scope is None:
            self.current_direction = Pass_Direction.Leftward
            self.current_carrier = None
            self.current_racking = 0
            self.current_gauge = 1
            self.current_sheet = 0

    @property
    def _is_function_scope(self):
        return self._parent_name is not None

    def return_scope(self, set_value: bool = False, value: Any = None):
        """
        Collect the scope that holds a return value
        :param set_value: if True, sets the given value as the return value
        :param value: value to be returned
        :return: the function_scope that has the set return value.
        """
        if set_value:  # set by return statements, otherwise pass up what is there
            self.return_value = value
        scope = self
        while scope is not None and not scope._is_function_scope:  # Not a function, continue
            if scope._parent_scope is not None:
                scope._parent_scope.return_value = self.return_value
            scope = scope.exit_current_scope()  # returns parent scope with stored return value
        return scope

    def is_main(self) -> bool:
        """
        :return: True if this is the outermost (main) scope
        """
        return self._parent_scope is None

    @property
    def current_sheet(self) -> Sheet_Identifier:
        """
        :return: The active sheet_id for N-Bed Knitting
        """
        return self[self._sheet_id]

    @current_sheet.setter
    def current_sheet(self, value: Optional[Union[int, Sheet_Identifier]]):
        if value is None:
            value = Sheet_Identifier(0, self.current_gauge)
        elif isinstance(value, int):
            assert 0 <= value < self.current_gauge, \
                f"Sheet must be between 0 and gauge {self.current_gauge}, {value}"
            value = Sheet_Identifier(value, self.current_gauge)
        self.current_gauge = value.gauge
        self[self._sheet_id] = value

    @property
    def current_gauge(self) -> int:
        """
        :return: The current Gauge being worked, the number of layers that can be accessed
        """
        gauge = self[self._gauge_id]
        assert 0 < gauge < Machine_State.MAX_GAUGE, \
            f"KnitScript Error: Gauge must be between 0 and {Machine_State.MAX_GAUGE} but got {gauge}"
        return gauge

    @current_gauge.setter
    def current_gauge(self, value: Optional[int]):
        if value is None:
            value = 1
        assert 0 < value < Machine_State.MAX_GAUGE, \
            f"KnitScript Error: Gauge must be between 0 and {Machine_State.MAX_GAUGE} but got {value}"
        self[self._gauge_id] = int(value)


    @property
    def current_direction(self) -> Pass_Direction:
        """
        :return: Machine direction at current scope
        """
        direction = self[self._direction_id]
        return direction

    @current_direction.setter
    def current_direction(self, value: Pass_Direction):
        assert isinstance(value, Pass_Direction), f"Direction has been set to non-direction {value}"
        self[self._direction_id] = value

    @property
    def current_carrier(self) -> Optional[Carrier_Set]:
        """
        :return: Active carrier at current scope
        """
        carrier = self[self._carrier_id]
        return carrier

    @current_carrier.setter
    def current_carrier(self, carrier: Optional[Carrier_Set]):
        if isinstance(carrier, int):
            carrier = Carrier_Set(carrier)
        elif isinstance(carrier, float):
            carrier = Carrier_Set(int(carrier))
        elif isinstance(carrier, list):
            carrier = Carrier_Set(carrier)
        assert carrier is None or isinstance(carrier, Carrier_Set), f"Cannot set Carrier to non-carrier, int, or list of ints/carriers {carrier}"
        self[self._carrier_id] = carrier

    @property
    def current_racking(self) -> int:
        """
        :return: Racking value at scope
        """
        rack = self[self._rack_id]
        return rack

    @current_racking.setter
    def current_racking(self, value: int):
        self[self._rack_id] = value

    def is_reserved_word(self, word: str) -> bool:
        """
        Parameters
        ----------
        word: the word being checked

        Returns
        -------
        returns true if a word is reserved in the language
        """
        return word in self._reserved_words

    def exit_current_scope(self):
        """

        Returns
        -------
        The parent scope with no reference to current function scope
        """
        self._parent_scope._child_scope = None
        return self._parent_scope

    def enter_new_scope(self, function_name: Optional[str] = None):
        """
        :return: Child scope that is created and connected to current scope
        """
        self._child_scope = Variable_Scope(self, function_name=function_name)
        return self._child_scope

    def get_var(self, var_name: str) -> Any:
        """

        Parameters
        ----------
        var_name: the name of the variable to get a value of

        Returns
        -------
        The value of the variable at the given scope

        """
        current_scope = self
        while current_scope is not None:
            if var_name in current_scope._variable_values:
                return current_scope._variable_values[var_name]
            current_scope = current_scope._parent_scope
        if current_scope is None:
            raise KeyError(f"Variable {var_name} is not in scope")
        return None

    def __getitem__(self, var_name: str) -> Any:
        return self.get_var(var_name)

    def set_var(self, var_name: str, value: Any):
        """
        Parameters
        ----------
        var_name: the variable to set
        value: the value to set the variable to

        """
        # assert var_name not in self._reserved_words, f"Cannot assign to {var_name} is a reserved keyword"
        if var_name in self:  # Move up scope to set the value
            current_scope = self
            while current_scope is not None:
                if var_name in current_scope._variable_values:
                    current_scope._variable_values[var_name] = value
                    return
                current_scope = current_scope._parent_scope
        else:  # set the new value at this scope
            self._variable_values[var_name] = value

    def __setitem__(self, var_name: str, value: Any):
        return self.set_var(var_name, value)

    def var_in_scope(self, var_name: str) -> bool:
        """

        Parameters
        ----------
        var_name: The name of the variable to check for

        Returns
        -------
        True if the variable is the scope of the given function
        """
        current_scope = self
        while current_scope is not None:
            if var_name in current_scope._variable_values:
                return True
            current_scope = current_scope._parent_scope
        return False

    def __contains__(self, var_name: str) -> bool:
        return self.var_in_scope(var_name)

    def delete_item_in_scope(self, var_name: str):
        """

        Parameters
        ----------
        var_name: The name of the variable to remove at scope
        """
        current_scope = self
        while current_scope is not None:
            if var_name in current_scope._variable_values:
                del current_scope._variable_values[var_name]
            current_scope = current_scope._parent_scope

    def __delitem__(self, var_name: str):
        self.delete_item_in_scope(var_name)

    def var_depth(self)-> int:
        """
        :return: The depth of this scope
        """
        d = -1
        current_scope = self
        while current_scope is not None:
            d += 1
            current_scope = current_scope._parent_scope
        return d

    def __str__(self):
        scope_str = f"{self.var_depth()}"
        if self._is_function_scope:
            scope_str = f"{self._parent_name}({scope_str})"
        if self.has_return:
            scope_str = f"{scope_str}=={self.return_value}"
        if self._parent_scope is None:
            return scope_str
        else:
            return f"{self._parent_scope}->{scope_str}"