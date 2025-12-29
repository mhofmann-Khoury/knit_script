"""Scoping structure for Knit Script.

This module provides the Knit_Script_Scope class, which manages variable scoping and namespace hierarchy for knit script program execution.
It implements a hierarchical scoping system that supports local variables, global variables, function scopes, module scopes, and machine state management.
The scoping system integrates with Python's namespace and provides comprehensive variable resolution with proper shadowing warnings and scope inheritance.
"""

from __future__ import annotations

import warnings
from collections.abc import Sequence
from typing import TYPE_CHECKING, Any

from virtual_knitting_machine.Knitting_Machine import Knitting_Machine
from virtual_knitting_machine.machine_components.carriage_system.Carriage_Pass_Direction import Carriage_Pass_Direction
from virtual_knitting_machine.machine_components.needles.Sheet_Identifier import Sheet_Identifier
from virtual_knitting_machine.machine_components.yarn_management.Yarn_Carrier import Yarn_Carrier
from virtual_knitting_machine.machine_components.yarn_management.Yarn_Carrier_Set import Yarn_Carrier_Set

from knit_script.knit_script_interpreter.scope.machine_scope import Machine_Scope
from knit_script.knit_script_interpreter.scope.variable_space import Variable_Space
from knit_script.knit_script_warnings.Knit_Script_Warning import Shadows_Global_Variable_Warning

if TYPE_CHECKING:
    from knit_script.knit_script_interpreter.knit_script_context import Knit_Script_Context


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

    def __init__(
        self,
        context: Knit_Script_Context,
        parent: Knit_Script_Scope | None = None,
        name: str | None = None,
        is_function: bool = False,
        is_module: bool = False,
        module_scope: Knit_Script_Scope | None = None,
    ):
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
        self._variables: Variable_Space = Variable_Space()
        Knit_Script_Scope._SCOPE_COUNT += 1
        self._context: Knit_Script_Context = context
        self._is_module: bool = is_module
        self._is_function = is_function
        self._returned: bool = False
        self._return_value: Any | None = None
        self._name: str | None = name
        self._parent: Knit_Script_Scope | None = parent
        assert module_scope is None or module_scope.is_module, f"Expected Module for module scope but got {module_scope}"
        self._module_scope: Knit_Script_Scope | None = module_scope
        if self._parent is None:
            self._globals: Variable_Space = Variable_Space()
            self._machine_scope: Machine_Scope = Machine_Scope(self._context)
        else:
            self._globals = self._parent._globals
            self._machine_scope = Machine_Scope(self._context, prior_settings=self._parent.machine_scope)  # start with settings from parent scope, but edit them locally
        self._child_scope: Knit_Script_Scope | None = None

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
    def scope_name(self) -> str | None:
        """
        Returns:
            str | None: The name of this scope if it represents a named function or module.
        """
        return self._name

    @property
    def function_name(self) -> str | None:
        """
        Returns:
            str | None: The name of this scope if it represents a function.
        """
        return self.scope_name if self.is_function else None

    @property
    def module_name(self) -> str | None:
        """
        Returns:
            str | None: The name of this scope if it represents a module.
        """
        return self.scope_name if self.is_module else None

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
    def returned(self) -> bool:
        """Check if the scope has found a return value.

        Returns:
            bool: True if the scope has found a return value, indicating that execution should return from this scope.
        """
        return self._returned

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
        if scope is not None:
            scope._return_value = value
            scope._returned = True

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
    def Carrier(self, carrier: int | float | Sequence[int | Yarn_Carrier] | Yarn_Carrier_Set | Yarn_Carrier | None) -> None:
        """Set the current carrier being used by the machine.

        Args:
            carrier (int | float | Sequence[int | Yarn_Carrier] | Yarn_Carrier_Set | Yarn_Carrier | None): The carrier to set as active, or None to clear the active carrier.
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

    def enter_new_scope(self, name: str | None = None, is_function: bool = False, is_module: bool = False, module_scope: Knit_Script_Scope | None = None) -> Knit_Script_Scope:
        """Enter a new sub scope and put it into the hierarchy.

        Args:
            name (str | None, optional): Name of the sub_scope if a function or module. Required for functions and modules. Defaults to None.
            is_function (bool, optional): If True, may have return values and function-specific behavior. Defaults to False.
            is_module (bool, optional): If True, module is added by variable name to parent scope. Defaults to False.
            module_scope (Knit_Script_Scope | None, optional): Module scope to use for variable resolution. Defaults to None.

        Returns:
            Knit_Script_Scope: Child scope that was created and is now active.

        Raises:
            NameError: If is_function is True but name is None, or if is_module is True but name is None.
        """
        if is_function and name is None:
            raise NameError("Functions must be named")
        self._child_scope = Knit_Script_Scope(context=self._context, parent=self, name=name, is_function=is_function, is_module=is_module, module_scope=module_scope)
        if is_module:
            if name is None:
                raise NameError("Modules must be named")
            self._variables[name] = self._child_scope
        return self._child_scope

    def collapse_descendant_scopes(self) -> None:
        """Brings all values in the child scopes (recursively) up into this scope. If there is no child scope, this is a no-op.

        Recursively collapses child scopes by bringing their variables up to this scope level and inheriting machine scope settings.
        This is used when exiting scopes that should preserve their variables.

        The machine state will be updated by any changes in the descendant scopes.
        """
        if self._child_scope is not None:
            self._child_scope.collapse_descendant_scopes()
            for key, value in vars(self._child_scope._variables).items():
                if not key.startswith("__"):  # Exclude object type variables in Variable_Space
                    self[key] = value
            self.machine_scope.inherit_from_scope(self._child_scope.machine_scope, inherit_raw_values=False)  # Inherit machine values and update machine state accordingly
            self._child_scope = None

    def exit_current_scope(self, collapse_into_parent: bool = False) -> None | Knit_Script_Scope:
        """Set child scope to None.

        If the current scope is not a module this may cause values to be deleted and become inaccessible.

        Args:
            collapse_into_parent (bool, optional): If True, brings all lower level values from child scope into the current scope. Defaults to False.

        Returns:
            None | Knit_Script_Scope: The parent scope or None if program exits.
        """
        if self._parent is not None:
            if collapse_into_parent:
                self._parent.collapse_descendant_scopes()
            else:
                self.machine_scope.update_parent_machine_scope(self._parent.machine_scope)
            self._parent._child_scope = None
        return self._parent

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

    def set_global(self, key: str, value: Any) -> None:
        """
        Set a global variable with the given key name.
        Overrides any global variable already defined by that key.

        Args:
            key (str): The name of the global variable to set.
            value (Any): The value of the global variable.
        """
        self._globals[key] = value

    def add_local_by_path(self, path: list[str], value: Any) -> None:
        """Add module sub scopes to variable space following the given path.

        Sets final value in the lowest module subscope. Creates intermediate module scopes as needed to establish the full path.

        Args:
            path (list[str]): List of module names representing the path to the final variable.
            value (Any): Value to associate with end of path.

        Raises:
            NameError: If path is empty. No variable names can be used to set the value.
        """
        if len(path) == 0:
            raise NameError("Cannot set value by path without at least one variable name in path.")
        scope = self
        for key in path[:-1]:
            if key in scope and isinstance(scope[key], Knit_Script_Scope):  # If this knitscript module is found, use it instead of overriding it.
                scope = scope[key]
            else:
                module_scope = Knit_Script_Scope(self._context, scope, name=key, is_module=True)
                scope[key] = module_scope
                scope = module_scope
        scope[path[-1]] = value  # Use the last element of the path as a variable name and set its value.

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
            if key in scope._variables:
                return True
            elif (stop_at_function and scope.is_function) or (stop_at_module and scope.is_module):
                return False
            scope = scope._parent
        return False

    def delete_local(self, key: str) -> None:
        """Delete the variable at lowest scope level.

        Args:
            key (str): The variable name to delete.

        Raises:
            NameError: If key is not in scope and cannot be deleted.
        """
        scope: Knit_Script_Scope | None = self
        while scope is not None:
            if key in scope._variables:
                del scope._variables[key]
                return
            scope = scope._parent
        raise NameError(f"Variable {key} is not in scope. Could not be deleted")

    def __contains__(self, key: str) -> bool:
        """Check if a variable exists in any accessible scope.

        Checks for variable existence in Python scope, global scope, or local scope hierarchy.

        Args:
            key (str): The variable name to check for.

        Returns:
            bool: True if the variable exists in any accessible scope.
        """
        value, exists = self.get_value_from_python_scope(key)
        return exists or key in self._globals or self.has_local(key)

    def __getitem__(self, variable_name: str) -> Any:
        """
        Find the lowest level value of the given variable name in local scope.

        Looks for value in the following order:
            1. The machine scope.
            2. Python scope.
            3. Local scope
            4. Modules owned by the local scope.
            5. A parent scope or any of its modules.
            6. The Global Scope.

        Args:
            variable_name (str): The variable name to search for.

        Returns:
            Any: The value in the local hierarchy by that key.

        Raises:
            NameError: If key is not in scope.

        Warns:
            Shadows_Global_Variable_Warning: If the key is found in a local scope but also exists in the globals.
        """
        if variable_name in self.machine_scope:  # Matches a reserved property of the machine scope.
            return self.machine_scope[variable_name]
        value, exist_in_python_scope = self.get_value_from_python_scope(variable_name)
        if exist_in_python_scope:
            return value
        is_global = variable_name in self._globals  # Matches a global variable, but look at local scope first.
        scope: Knit_Script_Scope | None = self
        while scope is not None:
            if variable_name in scope._variables:
                if is_global:
                    warnings.warn(Shadows_Global_Variable_Warning(variable_name), stacklevel=1)
                return scope._variables[variable_name]
            elif scope.module_scope is not None and variable_name in scope.machine_scope:
                return scope.module_scope[variable_name]
            scope = scope._parent
        if is_global:
            return self._globals[variable_name]
        else:
            raise NameError(f"Variable {variable_name} is not in scope")

    def __setitem__(self, variable_name: str, value: Any) -> None:
        """Set a local variable to the given value.

        If a local variable exists in a parent scope within this function and module, set that value.
        Otherwise, creates a new local variable within the current scope.

        Args:
            variable_name (str): Variable name to set.
            value (Any): Value to set key to.
        """
        if variable_name in self.machine_scope:
            self.machine_scope[variable_name] = value
        if self.has_local(variable_name, stop_at_function=True, stop_at_module=True):  # Local variable is present within the function or module scope.
            scope = self
            while variable_name not in self:
                assert scope._parent is not None
                scope = scope._parent
            scope._variables[variable_name] = value
        else:  # set at lowest scope level
            self._variables[variable_name] = value

    def __delitem__(self, key: str) -> None:
        if self.has_local(key):
            self.delete_local(key)
        elif key in self._globals:
            del self._globals[key]

    def __hash__(self) -> int:
        return self._scope_id

    def __str__(self) -> str:
        """
        Returns:
            str: The string representation of this scope by its instance count and any name value for modules or functions.
        """
        if self.is_module:
            return f"Module {self.module_name} (scope {self._scope_id})"
        elif self.is_function:
            return f"Function {self.function_name} (scope {self._scope_id})"
        else:
            return f"scope {self._scope_id}"

    def __repr__(self) -> str:
        return str(self)
