"""Scoping structure for Knit Script"""
from __future__ import annotations

from typing import Any

from virtual_knitting_machine.Knitting_Machine import Knitting_Machine
from virtual_knitting_machine.machine_components.carriage_system.Carriage_Pass_Direction import Carriage_Pass_Direction
from virtual_knitting_machine.machine_components.needles.Sheet_Needle import Sheet_Identifier
from virtual_knitting_machine.machine_components.yarn_management.Yarn_Carrier_Set import Yarn_Carrier_Set

from knit_script.knit_script_interpreter.scope.global_scope import Knit_Script_Globals
from knit_script.knit_script_interpreter.scope.machine_scope import Machine_Scope, Machine_Variables


class Knit_Script_Scope:
    """Keeps track of values in a confined scope. Also accesses globals and checks python scope."""

    def __init__(self, machine_state: Knitting_Machine, parent: Knit_Script_Scope | None = None,
                 name: str | None = None, is_function: bool = False, is_module: bool = False, module_scope: Knit_Script_Scope | None = None):
        self._machine_state: Knitting_Machine = machine_state
        self._is_module: bool = is_module
        self._is_function = is_function
        self.returned: bool = False
        self.name: str | None = name
        self.parent: Knit_Script_Scope | None = parent
        self.module_scope: Knit_Script_Scope | None = module_scope
        if self.parent is None:
            self.globals: Knit_Script_Globals = Knit_Script_Globals()
            self.machine_scope: Machine_Scope = Machine_Scope(self._machine_state)
            self._sub_scope_globals: set[str] = set()
        else:
            self.globals: Knit_Script_Globals = self.parent.globals
            self.machine_scope: Machine_Scope = self.parent.machine_scope  # Machine_Scope(self.parent.machine_scope)
            self._sub_scope_globals: set[str] = {*self.parent._sub_scope_globals}
        self.child_scope: Knit_Script_Scope | None = None
        self._return_value: Any | None = None

    @property
    def direction(self) -> Carriage_Pass_Direction:
        """Get the current direction the carriage will take.

        Returns:
            Carriage_Pass_Direction: The current direction the carriage will take.
        """
        return self.machine_scope.direction

    @direction.setter
    def direction(self, value: Carriage_Pass_Direction) -> None:
        self.machine_scope.direction = value

    @property
    def carrier(self) -> Yarn_Carrier_Set | None:
        """Get the current carrier being used by the machine.

        Returns:
            Yarn_Carrier_Set | None: The current carrier being used by the machine.
        """
        return self.machine_scope.carrier

    @carrier.setter
    def carrier(self, carrier: Yarn_Carrier_Set | None) -> None:
        self.machine_scope.carrier = carrier

    @property
    def racking(self) -> float:
        """Get current racking of the machine.

        Returns:
            float: Current racking of the machine.
        """
        return float(self.machine_scope.racking)

    @racking.setter
    def racking(self, value: float) -> None:
        self.machine_scope.racking = value

    @property
    def gauge(self) -> int:
        """Get the current number of sheets on the machine.

        Returns:
            int: The current number of sheets on the machine.
        """
        return int(self.machine_scope.gauge)

    @gauge.setter
    def gauge(self, value: int | None) -> None:
        self.machine_scope.gauge = value

    @property
    def sheet(self) -> Sheet_Identifier:
        """Get the current sheet being worked on the machine.

        Returns:
            Sheet_Identifier: The current sheet being worked on the machine.
        """
        return self.machine_scope.sheet

    @sheet.setter
    def sheet(self, value: int | Sheet_Identifier | None) -> None:
        self.machine_scope.sheet = value

    @staticmethod
    def get_value_from_python_scope(key: str) -> tuple[Any | None, bool]:
        """Test if key can be accessed from python scope.

        Args:
            key (str): Value to access.

        Returns:
            tuple: The value from python, True if value was in python scope.
        """
        try:
            value = eval(key)
            return value, True
        except NameError:
            return None, False

    @property
    def is_module(self) -> bool:
        """Check if the variable scope belongs to a knit script module.

        Returns:
            bool: True if the variable scope belongs to a knit script module.
        """
        return self._is_module

    @property
    def is_function(self) -> bool:
        """Check if the variable scope belongs to a function.

        Returns:
            bool: True if the variable scope belongs to a function.
        """
        return self._is_function

    @property
    def return_value(self) -> Any:
        """Get the return value set for this scope.

        Returns:
            Any: The return value set for this scope.
        """
        assert self.is_function, "Cannot return from scope that is not a function"
        return self._return_value

    @return_value.setter
    def return_value(self, value: Any) -> None:
        scope: None | Knit_Script_Scope = self
        while scope is not None and not scope.is_function:
            scope = self.parent
        if scope is None:  # set the exit value since no function can return
            self.globals.exit_value = value
        else:
            scope._return_value = value
            scope.returned = True

    def set_local(self, key: str, value: Any) -> None:
        """Set key to value at this level.

        Args:
            key (str): Variable name.
            value: Value to set key to.
        """
        if self.has_local(key, stop_at_function=True, stop_at_module=True):  # value comes from higher up scope, but not including global
            scope = self
            while not hasattr(scope, key):
                assert scope.parent is not None
                scope = scope.parent
            setattr(scope, key, value)
        else:  # set at lowest scope level
            setattr(self, key, value)

    def set_global(self, key: str, value: Any) -> None:
        """Set a global variable.

        Args:
            key (str): Variable name.
            value: Value to add to globals.
        """
        self._sub_scope_globals.add(key)
        self.globals[key] = value

    def get_local(self, key: str) -> Any:
        """Find the lowest level value in local scope by key.

        Args:
            key (str): The variable name.

        Returns:
            Any: The value in the local hierarchy by that key. Checks against globals last.

        Raises:
            NameError: If key is not in scope.
        """
        if Machine_Variables.in_machine_variables(key):
            return self.machine_scope[key]
        is_global = self.has_global(key)
        if is_global and key in self._sub_scope_globals:  # Set as global in current subscope
            return self.globals[key]
        else:  # check lowest scope then globals
            scope: Knit_Script_Scope | None = self
            while scope is not None:
                if hasattr(scope, key):
                    if is_global:
                        print(f"KnitScript Warning: {key} shadows global variable")
                    return getattr(scope, key)
                elif scope.module_scope is not None:
                    try:
                        return scope.module_scope[key]
                    except NameError:
                        pass
                scope = scope.parent
            if is_global:
                return self.get_global(key)
            else:
                raise NameError(f"Variable {key} is not in scope")

    def add_local_by_path(self, path: list[str], value: Any) -> None:
        """Add module sub scopes to variable space following the given path.

        Sets final value in the lowest module subscope.

        Args:
            path (list[str]): List of module names.
            value: Value to associate with end of path.
        """
        scope = self
        for key in path[:-1]:
            if key not in scope:
                scope[key] = Knit_Script_Scope(self._machine_state, scope, key, is_module=True)
            scope = scope[key]
        scope[path[-1]] = value

    def get_global(self, key: str) -> Any:
        """Access global value.

        Args:
            key (str): The variable name.

        Returns:
            Any: The global value under that var_name.
        """
        assert self.has_global(key), f"Could not find global variable {key}"
        return self.globals[key]

    def has_local(self, key: str, stop_at_function: bool = False, stop_at_module: bool = False) -> bool:
        """Check for key in local scope. Ignores globals.

        Args:
            key (str): The variable name to search for.
            stop_at_function (bool, optional): Will not search for local variable beyond function. Defaults to False.
            stop_at_module (bool, optional): Will not search for local variable beyond module. Defaults to False.

        Returns:
            bool: True if key is in local scope.
        """
        scope: Knit_Script_Scope | None = self
        while scope is not None:
            if hasattr(scope, key):
                return True
            elif stop_at_function and scope.is_function:
                return False
            elif stop_at_module and scope.is_module:
                return False
            scope = scope.parent
        return False

    def has_global(self, key: str) -> bool:
        """Check for global value.

        Args:
            key (str): The variable name.

        Returns:
            bool: True if there is a global variable under this key.
        """
        return key in self.globals

    def delete_local(self, key: str) -> bool:
        """Delete the variable at lowest scope level. If not found, no-op.

        Args:
            key (str): The variable name.

        Returns:
            bool: True if a value was found and deleted.
        """
        scope: Knit_Script_Scope | None = self
        while scope is not None:
            if hasattr(scope, key):
                delattr(scope, key)
                return True
            scope = scope.parent
        return False

    def delete_global(self, key: str) -> bool:
        """Delete global variable. If not found, no-op.

        Args:
            key (str): Variable name.

        Returns:
            bool: True if a global was deleted.
        """
        if self.has_global(key):
            del self.globals[key]
            return True
        return False

    def enter_new_scope(self, name: str | None = None,
                        is_function: bool = False,
                        is_module: bool = False,
                        module_scope: Knit_Script_Scope | None = None) -> Knit_Script_Scope:
        """Enter a new sub scope and put it into the hierarchy.

        Args:
            name (str | None, optional): Name of the sub_scope if a function or module. Defaults to None.
            is_function (bool, optional): If true, may have return values. Defaults to False.
            is_module (bool, optional): If true, module is added by variable name. Defaults to False.
            module_scope: Module scope to use. Defaults to None.

        Returns:
            Knit_Script_Scope: Child scope that was created.
        """
        if is_function:
            assert name is not None, "Functions must be named"
        child_scope = Knit_Script_Scope(self._machine_state, self, name, is_function, is_module, module_scope=module_scope)
        if is_module:
            assert name is not None, f"Modules must be named"
            self[name] = child_scope
        self.child_scope = child_scope
        return self.child_scope

    def exit_current_scope(self) -> None | Knit_Script_Scope:
        """Set child scope to none.

        If the current scope is not a module this may cause values to be deleted and become inaccessible.

        Returns:
            None | Knit_Script_Scope: The parent scope or None if program exits.
        """
        if self.parent is not None:
            self.parent.child_scope = None
        return self.parent

    def __contains__(self, key: str) -> bool:
        value, exists = self.get_value_from_python_scope(key)
        if exists:
            return exists
        return self.has_global(key) or self.has_local(key)

    def __setitem__(self, key: str, value: Any) -> None:
        self.set_local(key, value)

    def __getitem__(self, key: str) -> Any:
        value, exists = self.get_value_from_python_scope(key)
        if exists:
            return value
        return self.get_local(key)

    def __delitem__(self, key: str) -> None:
        self.delete_local(key)
