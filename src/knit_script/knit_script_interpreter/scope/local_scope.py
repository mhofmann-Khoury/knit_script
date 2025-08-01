"""Scoping structure for Knit Script"""
from __future__ import annotations

import warnings
from typing import Any

from virtual_knitting_machine.Knitting_Machine import Knitting_Machine
from virtual_knitting_machine.machine_components.carriage_system.Carriage_Pass_Direction import Carriage_Pass_Direction
from virtual_knitting_machine.machine_components.needles.Sheet_Needle import Sheet_Identifier
from virtual_knitting_machine.machine_components.yarn_management.Yarn_Carrier_Set import Yarn_Carrier_Set

from knit_script.knit_script_interpreter import _Context_Base
from knit_script.knit_script_interpreter.scope.global_scope import Knit_Script_Globals
from knit_script.knit_script_interpreter.scope.machine_scope import Machine_Scope
from knit_script.knit_script_warnings.Knit_Script_Warning import Shadows_Global_Variable_Warning, Shadow_Variable_Warning


class Knit_Script_Scope:
    """Keeps track of values in a confined scope. Also accesses globals and checks python scope."""

    def __init__(self, context: _Context_Base, parent: Knit_Script_Scope | None = None,
                 name: str | None = None,
                 is_function: bool = False, is_module: bool = False,
                 module_scope: Knit_Script_Scope | None = None):
        self._context: _Context_Base = context
        self._is_module: bool = is_module
        self._is_function = is_function
        self._returned: bool = False
        self._name: str | None = name
        self._parent: Knit_Script_Scope | None = parent
        self._module_scope: Knit_Script_Scope | None = module_scope
        if self._parent is None:
            self._globals: Knit_Script_Globals = Knit_Script_Globals()
            self._machine_scope: Machine_Scope = Machine_Scope(self._context)
        else:
            self._globals: Knit_Script_Globals = self._parent._globals
            self._machine_scope: Machine_Scope = Machine_Scope(self._context, prior_settings=self._parent.machine_scope)  # start with settings from parent scope, but edit them locally
        self._child_scope: Knit_Script_Scope | None = None
        self._return_value: Any | None = None

    @property
    def machine_scope(self) -> Machine_Scope:
        """

        Returns:
            The machine scope for this level of scope.
        """
        return self._machine_scope

    @property
    def variables(self) -> dict[str, Any]:
        """
        Returns:
            The variables as key value pairs in a dictionary of variables set at this level of scope.
        """
        return {k: v for k, v in vars(self).items() if not k.startswith('_')}

    @property
    def returned(self) -> bool:
        """
        Returns:
            True if the scope has found a return value.
        """
        return self._returned

    @property
    def machine_state(self) -> Knitting_Machine:
        """
        Returns:
            The current state of the knitting machine at the given execution context.
        """
        return self._context.machine_state

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
    def Carrier(self) -> Yarn_Carrier_Set | None:
        """Get the current carrier being used by the machine.

        Returns:
            Yarn_Carrier_Set | None: The current carrier being used by the machine.
        """
        return self.machine_scope.Carrier

    @Carrier.setter
    def Carrier(self, carrier: Yarn_Carrier_Set | None) -> None:
        self.machine_scope.Carrier = carrier

    @property
    def Racking(self) -> float:
        """Get current racking of the machine.

        Returns:
            float: Current racking of the machine.
        """
        return float(self.machine_scope.Racking)

    @Racking.setter
    def Racking(self, value: float) -> None:
        self.machine_scope.Racking = value

    @property
    def Gauge(self) -> int:
        """Get the current number of sheets on the machine.

        Returns:
            int: The current number of sheets on the machine.
        """
        return int(self.machine_scope.Gauge)

    @Gauge.setter
    def Gauge(self, value: int | None) -> None:
        self.machine_scope.Gauge = value

    @property
    def Sheet(self) -> Sheet_Identifier:
        """Get the current sheet being worked on the machine.

        Returns:
            Sheet_Identifier: The current sheet being worked on the machine.
        """
        return self.machine_scope.Sheet

    @Sheet.setter
    def Sheet(self, value: int | Sheet_Identifier | None) -> None:
        self.machine_scope.Sheet = value

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
            scope = self._parent
        if scope is None:  # set the exit value since no function can return
            self._globals.exit_value = value
        else:
            scope._return_value = value
            scope._returned = True

    def set_local(self, key: str, value: Any) -> None:
        """
        Set a local variable by the name <key> to the given value.
        If a local variable exists from a parent scope within this function and module, set that value.
        Otherwise, creates a new local variable within the current scope.
        Args:
            key (str): Variable name.
            value: Value to set key to.
        """
        if self.has_local(key, stop_at_function=True, stop_at_module=True):  # value comes from higher up scope, but not including global
            scope = self
            while not hasattr(scope, key):
                assert scope._parent is not None
                scope = scope._parent
            setattr(scope, key, value)
        else:  # set at lowest scope level
            setattr(self, key, value)

    def set_global(self, key: str, value: Any) -> None:
        """Set a global variable.

        Args:
            key (str): Variable name.
            value: Value to add to globals.
        """
        setattr(self._globals, key, value)

    def get_local(self, key: str) -> Any:
        """
        Find the lowest level value in local scope by key.

        Looks for value in the following order:
            1. The machine scope.
            2. Python scope.
            3. Local scope
            4. Modules owned by the local scope.
            5. A parent scope or any of its modules.
            6. The Global Scope.

        Args:
            key (str): The variable name.

        Returns:
            Any: The value in the local hierarchy by that key.

        Raises:
            NameError: If key is not in scope.
            Shadows_Global_Variable_Warning: If the key is found in a local scope but also exists in the globals.
            Shadows_Variable_Warning: If the key is found and exists at a higher scope (excludes modules).
        """
        if hasattr(self.machine_scope, key):  # Matches a reserved property of the machine scope.
            return getattr(self.machine_scope, key)
        value, exist_in_python_scope = self.get_value_from_python_scope(key)
        if exist_in_python_scope:
            return value
        is_global = hasattr(self._globals, key)  # Matches a global variable, but look at local scope first.
        scope: Knit_Script_Scope | None = self
        found_value: bool = False
        value: Any = None
        while scope is not None:
            if hasattr(scope, key):
                if is_global:
                    warnings.warn(Shadows_Global_Variable_Warning(key))
                if not found_value:
                    value = getattr(scope, key)
                    found_value = True
                else:
                    warnings.warn(Shadow_Variable_Warning(key))
                    return value  # No need to look further for possible shadows.
            elif not found_value and scope._module_scope is not None:  # don't check modules if this is already found.
                try:
                    value = scope._module_scope[key]
                    found_value = True
                except NameError:
                    pass  # If you don't find it in the module, that is fine
            scope = scope._parent
        if found_value:
            return value
        elif is_global:
            return getattr(self._globals, key)
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
            setattr(scope, key, Knit_Script_Scope(self._context, scope, name=key, is_module=True))
            scope = getattr(scope, key)
        setattr(scope, path[-1], value)  # Use the last element of the path as a variable name

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
            scope = scope._parent
        return False

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
            scope = scope._parent
        return False

    def delete_global(self, key: str) -> bool:
        """Delete global variable. If not found, no-op.

        Args:
            key (str): Variable name.

        Returns:
            bool: True if a global was deleted.
        """
        if hasattr(self._globals, key):
            if key == "exit_value":
                raise NameError(f"Cannot delete {key} because this is a reserved keyword")
            delattr(self._globals, key)
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
        self._child_scope = Knit_Script_Scope(context=self._context, parent=self, name=name, is_function=is_function, is_module=is_module, module_scope=module_scope)
        if is_module:
            assert name is not None, f"Modules must be named"
            setattr(self, name, self._child_scope)
        return self._child_scope

    def collapse_lower_scope(self) -> None:
        """
            Brings all of the values in the child scopes (recursively) up into this scope.
        """
        if self._child_scope is not None:
            self._child_scope.collapse_lower_scope()
            for key, value in self._child_scope.variables.items():
                self.set_local(key, value)
            self.machine_scope.inherit_from_scope(self._child_scope.machine_scope)
            self._child_scope = None

    def exit_current_scope(self, collapse_into_parent: bool = False) -> None | Knit_Script_Scope:
        """Set child scope to none.

        If the current scope is not a module this may cause values to be deleted and become inaccessible.
        Args:
            collapse_into_parent: If True, brings all of the lower level values from child scope into the current scope.
        Returns:
            None | Knit_Script_Scope: The parent scope or None if program exits.
        """
        if self._parent is not None:
            if collapse_into_parent:
                self._parent.collapse_lower_scope()
            else:
                parent_machine_scope = self._parent.machine_scope
                self._parent._machine_scope = self.machine_scope
                self._parent.machine_scope.inherit_from_scope(parent_machine_scope)  # reset from current variables back to state prior to this scope.
            self._parent._child_scope = None
        return self._parent

    def __contains__(self, key: str) -> bool:
        value, exists = self.get_value_from_python_scope(key)
        if exists:
            return exists
        return key in self._globals or self.has_local(key)

    def __getitem__(self, key: str) -> Any:
        return self.get_local(key)

    def __setitem__(self, key: str, value: Any) -> None:
        self.set_local(key, value)
