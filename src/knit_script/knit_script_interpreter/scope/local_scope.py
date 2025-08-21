"""Scoping structure for Knit Script.

This module provides the Knit_Script_Scope class, which manages variable scoping and namespace hierarchy for knit script program execution.
It implements a hierarchical scoping system that supports local variables, global variables, function scopes, module scopes, and machine state management.
The scoping system integrates with Python's namespace and provides comprehensive variable resolution with proper shadowing warnings and scope inheritance.
"""
from __future__ import annotations

import warnings
from typing import TYPE_CHECKING, Any

from virtual_knitting_machine.Knitting_Machine import Knitting_Machine
from virtual_knitting_machine.machine_components.carriage_system.Carriage_Pass_Direction import (
    Carriage_Pass_Direction,
)
from virtual_knitting_machine.machine_components.needles.Sheet_Identifier import (
    Sheet_Identifier,
)
from virtual_knitting_machine.machine_components.yarn_management.Yarn_Carrier_Set import (
    Yarn_Carrier_Set,
)

from knit_script.knit_script_interpreter.scope.global_scope import Knit_Script_Globals
from knit_script.knit_script_interpreter.scope.machine_scope import Machine_Scope
from knit_script.knit_script_warnings.Knit_Script_Warning import (
    Shadows_Global_Variable_Warning,
)

if TYPE_CHECKING:
    from knit_script.knit_script_interpreter.knit_script_context import (
        Knit_Script_Context,
    )


class Knit_Script_Scope:
    """Keeps track of values in a confined scope. Also accesses globals and checks python scope.

    The Knit_Script_Scope class implements a hierarchical variable scoping system for knit script execution.
    It manages local variables, global variables, function scopes, module scopes, and machine state while providing integration with Python's namespace.
    The class supports scope nesting, variable shadowing detection, and proper inheritance of machine settings across scope boundaries.

    This scoping system enables complex knit script programs to maintain proper variable isolation between functions and modules
     while allowing controlled access to global state and machine configuration.
     It provides comprehensive variable resolution that searches through local scope, parent scopes, module scopes, and global scope in the correct order.
    """
    _SCOPE_COUNT: int = 0

    def __init__(self, context: Knit_Script_Context, parent: Knit_Script_Scope | None = None, name: str | None = None,
                 is_function: bool = False, is_module: bool = False, module_scope: Knit_Script_Scope | None = None):
        """Initialize a new scope with the specified configuration.

        Creates a new scope in the hierarchy with the given characteristics.
        Root scopes (those without parents) initialize their own global and machine scope instances, while child scopes inherit from their parents.

        Args:
            context (Knit_Script_Context): The execution context for this scope.
            parent (Knit_Script_Scope | None, optional): The parent scope in the hierarchy. If None, this becomes a root scope. Defaults to None.
            name (str | None, optional): The name of this scope if it represents a named function or module. Defaults to None.
            is_function (bool, optional): If True, this scope can handle return statements and function-specific behavior. Defaults to False.
            is_module (bool, optional): If True, this scope represents a module and will be added to the parent's namespace. Defaults to False.
            module_scope (Knit_Script_Scope | None, optional): Associated module scope for variable resolution. Defaults to None.
        """
        self._scope_id: int = Knit_Script_Scope._SCOPE_COUNT
        Knit_Script_Scope._SCOPE_COUNT += 1
        self._context: Knit_Script_Context = context
        self._is_module: bool = is_module
        self._is_function = is_function
        self._returned: bool = False
        self._name: str | None = name
        self._parent: Knit_Script_Scope | None = parent
        assert module_scope is None or module_scope.is_module, f"Expected Module for module scope but got {module_scope}"
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
        """Get the machine scope for this level of scope.

        Returns:
            Machine_Scope: The machine scope for this level of scope, containing machine state and configuration settings.
        """
        return self._machine_scope

    @property
    def module_scope(self) -> Knit_Script_Scope | None:
        """
        Returns:
            Knit_Script_Scope: The module scope for this variable scope.
        """
        if self._module_scope is not None:
            return self._module_scope
        elif self._parent is None:
            return None
        else:  # Recurse to find the module of the parent scope
            return self._parent._module_scope

    @property
    def variables(self) -> dict[str, Any]:
        """Get the variables as key value pairs in a dictionary of variables set at this level of scope.

        Returns only variables that are defined directly on this scope instance, excluding internal attributes that start with underscore.

        Returns:
            dict[str, Any]: The variables as key value pairs in a dictionary of variables set at this level of scope.
        """
        return {k: v for k, v in vars(self).items() if not k.startswith('_')}

    @property
    def returned(self) -> bool:
        """Check if the scope has found a return value.

        Returns:
            bool: True if the scope has found a return value, indicating that execution should return from this scope.
        """
        return self._returned

    @property
    def machine_state(self) -> Knitting_Machine:
        """Get the current state of the knitting machine at the given execution context.

        Returns:
            Knitting_Machine: The current state of the knitting machine at the given execution context.
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
        """Set the current direction the carriage will take.

        Args:
            value (Carriage_Pass_Direction): The direction to set for carriage movement.
        """
        self.machine_scope.direction = value

    @property
    def Carrier(self) -> Yarn_Carrier_Set | None:
        """Get the current carrier being used by the machine.

        Returns:
            Yarn_Carrier_Set | None: The current carrier being used by the machine, or None if no carrier is active.
        """
        return self.machine_scope.Carrier

    @Carrier.setter
    def Carrier(self, carrier: Yarn_Carrier_Set | None) -> None:
        """Set the current carrier being used by the machine.

        Args:
            carrier (Yarn_Carrier_Set | None): The carrier to set as active, or None to clear the active carrier.
        """
        self.machine_scope.Carrier = carrier

    @property
    def Rack(self) -> float:
        """Get current racking of the machine.

        Returns:
            float: Current racking of the machine as a floating-point value.
        """
        return float(self.machine_scope.Racking)

    @Rack.setter
    def Rack(self, racking: float) -> None:
        """
        Alternate name for setter for the Racking property.
        Args:
            racking (float): Current racking of the machine as a floating-point value.:
        """
        self.Racking = racking

    @property
    def Racking(self) -> float:
        """Get current racking of the machine.

        Returns:
            float: Current racking of the machine as a floating-point value.
        """
        return float(self.machine_scope.Racking)

    @Racking.setter
    def Racking(self, value: float) -> None:
        """Set the current racking of the machine.

        Args:
            value (float): The racking value to set for the machine.
        """
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
        """Set the current number of sheets on the machine.

        Args:
            value (int | None): The gauge value to set, or None to clear the gauge setting.
        """
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
        """Set the current sheet being worked on the machine.

        Args:
            value (int | Sheet_Identifier | None): The sheet to set as active, or None to clear the active sheet.
        """
        self.machine_scope.Sheet = value

    @staticmethod
    def get_value_from_python_scope(key: str) -> tuple[Any | None, bool]:
        """Test if key can be accessed from python scope.

        Attempts to evaluate the given key as a Python expression to determine if it exists in the Python namespace and retrieve its value.

        Args:
            key (str): Value to access from Python's namespace.

        Returns:
            tuple[Any | None, bool]: A tuple containing the value from python and True if value was in python scope, otherwise None and False.
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

        This property can only be accessed on function scopes. It returns the value that was set by a return statement within the function.

        Returns:
            Any: The return value set for this scope.
        """
        return self._return_value

    @return_value.setter
    def return_value(self, value: Any) -> None:
        """Set the return value for the appropriate scope.

        Searches up the scope hierarchy to find the nearest function scope and sets the return value there. If no function scope is found, sets the global exit value instead.

        Args:
            value (Any): The value to return from the function or set as the program exit value.
        """
        scope: None | Knit_Script_Scope = self
        while scope is not None and not scope.is_function:
            scope._return_value = value
            scope._returned = True
            scope = scope._parent
        if scope is None:  # set the exit value since no function can return
            self._globals.exit_value = value
        else:
            scope._return_value = value
            scope._returned = True

    def set_local(self, key: str, value: Any) -> None:
        """Set a local variable by the name <key> to the given value.

        If a local variable exists from a parent scope within this function and module, set that value.
        Otherwise, creates a new local variable within the current scope.

        Args:
            key (str): Variable name to set.
            value (Any): Value to set key to.
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
            key (str): Variable name to set in global scope.
            value (Any): Value to add to globals.
        """
        setattr(self._globals, key, value)

    def get_local(self, key: str) -> Any:
        """Find the lowest level value in local scope by key.

        Looks for value in the following order: 1. The machine scope. 2. Python scope. 3. Local scope 4. Modules owned by the local scope. 5. A parent scope or any of its modules. 6. The Global Scope.

        Args:
            key (str): The variable name to search for.

        Returns:
            Any: The value in the local hierarchy by that key.

        Raises:
            NameError: If key is not in scope.

        Warns:
            Shadows_Global_Variable_Warning: If the key is found in a local scope but also exists in the globals.
        """
        if hasattr(self.machine_scope, key):  # Matches a reserved property of the machine scope.
            return getattr(self.machine_scope, key)
        value, exist_in_python_scope = self.get_value_from_python_scope(key)
        if exist_in_python_scope:
            return value
        is_global = hasattr(self._globals, key)  # Matches a global variable, but look at local scope first.
        scope: Knit_Script_Scope | None = self
        while scope is not None:
            if hasattr(scope, key):
                if is_global:
                    warnings.warn(Shadows_Global_Variable_Warning(key))
                return getattr(scope, key)
            elif scope.module_scope is not None:  # don't check modules if this is already found.
                try:
                    return scope.module_scope[key]
                except NameError:
                    pass  # If you don't find it in the module, that is fine
            scope = scope._parent
        if is_global:
            return getattr(self._globals, key)
        else:
            raise NameError(f"Variable {key} is not in scope")

    def add_local_by_path(self, path: list[str], value: Any) -> None:
        """Add module sub scopes to variable space following the given path.

        Sets final value in the lowest module subscope. Creates intermediate module scopes as needed to establish the full path.

        Args:
            path (list[str]): List of module names representing the path to the final variable.
            value (Any): Value to associate with end of path.
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
            stop_at_function (bool, optional): Will not search for local variable beyond function scope. Defaults to False.
            stop_at_module (bool, optional): Will not search for local variable beyond module scope. Defaults to False.

        Returns:
            bool: True if key is in local scope within the specified boundaries.
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
            key (str): The variable name to delete.

        Returns:
            bool: True if a value was found and deleted, False otherwise.
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
            key (str): Variable name to delete from global scope.

        Returns:
            bool: True if a global was deleted, False if not found.

        Raises:
            NameError: If attempting to delete reserved keywords like 'exit_value'.
        """
        if hasattr(self._globals, key):
            if key == "exit_value":
                raise NameError(f"Cannot delete {key} because this is a reserved keyword")
            delattr(self._globals, key)
            return True
        return False

    def enter_new_scope(self, name: str | None = None, is_function: bool = False, is_module: bool = False, module_scope: Knit_Script_Scope | None = None) -> Knit_Script_Scope:
        """Enter a new sub scope and put it into the hierarchy.

        Args:
            name (str | None, optional): Name of the sub_scope if a function or module. Required for functions and modules. Defaults to None.
            is_function (bool, optional): If true, may have return values and function-specific behavior. Defaults to False.
            is_module (bool, optional): If true, module is added by variable name to parent scope. Defaults to False.
            module_scope (Knit_Script_Scope | None, optional): Module scope to use for variable resolution. Defaults to None.

        Returns:
            Knit_Script_Scope: Child scope that was created and is now active.

        Raises:
            AssertionError: If is_function is True but name is None, or if is_module is True but name is None.
        """
        if is_function:
            assert name is not None, "Functions must be named"
        self._child_scope = Knit_Script_Scope(context=self._context, parent=self, name=name, is_function=is_function, is_module=is_module, module_scope=module_scope)
        if is_module:
            assert name is not None, f"Modules must be named"
            setattr(self, name, self._child_scope)
        return self._child_scope

    def collapse_lower_scope(self) -> None:
        """Brings all values in the child scopes (recursively) up into this scope.

        Recursively collapses child scopes by bringing their variables up to this scope level and inheriting machine scope settings.
        This is used when exiting scopes that should preserve their variables.
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
            collapse_into_parent (bool, optional): If True, brings all lower level values from child scope into the current scope. Defaults to False.

        Returns:
            None | Knit_Script_Scope: The parent scope or None if program exits.
        """
        if self._parent is not None:
            if collapse_into_parent:
                self._parent.collapse_lower_scope()
            else:
                self.machine_scope.update_parent_machine_scope(self._parent.machine_scope)
            self._parent._child_scope = None
        return self._parent

    def __contains__(self, key: str) -> bool:
        """Check if a variable exists in any accessible scope.

        Checks for variable existence in Python scope, global scope, or local scope hierarchy.

        Args:
            key (str): The variable name to check for.

        Returns:
            bool: True if the variable exists in any accessible scope.
        """
        value, exists = self.get_value_from_python_scope(key)
        if exists:
            return exists
        return key in self._globals or self.has_local(key)

    def __getitem__(self, key: str) -> Any:
        """Get a variable value using dictionary-style access.

        Args:
            key (str): The variable name to retrieve.

        Returns:
            Any: The value of the variable.

        Raises:
            NameError: If the variable is not found in any accessible scope.
        """
        return self.get_local(key)

    def __setitem__(self, key: str, value: Any) -> None:
        """Set a variable value using dictionary-style access.

        Args:
            key (str): The variable name to set.
            value (Any): The value to assign to the variable.
        """
        self.set_local(key, value)

    def __hash__(self) -> int:
        return self._scope_id

    def __str__(self) -> str:
        """
        Returns:
            str: The string representation of this scope by its instance count and any name value for modules or functions.
        """
        if self.is_module:
            return f"Module {self._name} (scope {self._scope_id})"
        elif self.is_function:
            return f"Function {self._name} (scope {self._scope_id})"
        elif self._name is not None:
            return f"{self._name} (scope {self._scope_id})"
        else:
            return f"scope {self._scope_id}"

    def __repr__(self) -> str:
        return str(self)
