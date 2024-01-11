"""Scoping structure for Knit Script"""

from typing import Optional, Tuple, Any, List, Union

from knit_script.knit_script_interpreter.scope.global_scope import Knit_Script_Globals
from knit_script.knit_script_interpreter.scope.machine_scope import Machine_Scope, Machine_Variables
from knit_script.knitting_machine.machine_components.Sheet_Needle import Sheet_Identifier
from knit_script.knitting_machine.machine_components.machine_pass_direction import Pass_Direction
from knit_script.knitting_machine.machine_components.yarn_management.Carrier_Set import Carrier_Set


class Knit_Script_Scope:
    """
        Keeps track of values in a confined scope. Also accesses globals and checks python scope
    """

    def __init__(self, context, parent=None, name: Optional[str] = None, is_function: bool = False, is_module: bool = False, module_scope=None):
        self.context = context
        self._is_module = is_module
        self._is_function = is_function
        self.returned: bool = False
        self.name = name
        self.parent: Optional[Knit_Script_Scope] = parent
        self.module_scope: Optional[Knit_Script_Scope] = module_scope
        if self.parent is None:
            self.globals: Knit_Script_Globals = Knit_Script_Globals()
            self.machine_scope: Machine_Scope = Machine_Scope(self.context)
            self._sub_scope_globals = set()
        else:
            self.globals: Knit_Script_Globals = self.parent.globals
            self.machine_scope: Machine_Scope = self.parent.machine_scope  # Machine_Scope(self.parent.machine_scope)
            self._sub_scope_globals = {*self.parent._sub_scope_globals}
        self.child_scope = None
        self._return_value = None

    @property
    def direction(self) -> Pass_Direction:
        """
        :return: The current direction the carriage will take
        """
        return self.machine_scope.direction

    @direction.setter
    def direction(self, value: Pass_Direction):
        self.machine_scope.direction = value

    @property
    def carrier(self) -> Optional[Carrier_Set]:
        """
        :return: the current carrier being used by the machine
        """
        return self.machine_scope.carrier

    @carrier.setter
    def carrier(self, carrier: Optional[Carrier_Set]):
        self.machine_scope.carrier = carrier

    @property
    def racking(self) -> float:
        """
        :return: current racking of the machine
        """
        return self.machine_scope.racking

    @racking.setter
    def racking(self, value: float):
        self.machine_scope.racking = value

    @property
    def gauge(self) -> int:
        """
        :return: The current number of sheets on the machine
        """
        return self.machine_scope.gauge

    @gauge.setter
    def gauge(self, value: Optional[int]):
        self.machine_scope.gauge = value

    @property
    def sheet(self) -> Sheet_Identifier:
        """
        :return: The current sheet being worked on the machine
        """
        return self.machine_scope.sheet

    @sheet.setter
    def sheet(self, value: Optional[Union[int, Sheet_Identifier]]):
        self.machine_scope.sheet = value

    @staticmethod
    def get_value_from_python_scope(key: str) -> Tuple[Any, bool]:
        """
        Tests if key can be accessed from python scope
        :param key: value to access
        :return: the value from python, True if value was in python scope
        """
        try:
            value = eval(key)
            return value, True
        except NameError:
            return None, False

    @property
    def is_module(self) -> bool:
        """
        :return: True if the variable scope belongs to a knit script module
        """
        return self._is_module

    @property
    def is_function(self) -> bool:
        """
        :return: True if the variable scope belongs to a function
        """
        return self._is_function

    @property
    def return_value(self) -> Any:
        """
        :return: The return value set for this scope
        """
        assert self.is_function, "Cannot return from scope that is not a function"
        return self._return_value

    @return_value.setter
    def return_value(self, value: Any):
        scope = self
        while scope is not None and not scope.is_function:
            scope = self.parent
        if scope is None:  # set the exit value since no function can return
            self.globals.exit_value = value
        else:
            scope._return_value = value
            scope.returned = True

    def set_local(self, key: str, value: Any):
        """
        sets key to value at this level
        :param key: variable name
        :param value: value to set key to
        """
        if self.has_local(key, stop_at_function=True, stop_at_module=True):  # value comes from higher up scope, but not including global
            scope = self
            while not hasattr(scope, key):
                scope = scope.parent
            setattr(scope, key, value)
        else:  # set at lowest scope level
            setattr(self, key, value)

    def set_global(self, key: str, value: Any):
        """
        :param key: variable name
        :param value: value to add to globals
        """
        self._sub_scope_globals.add(key)
        self.globals[key] = value

    def get_local(self, key: str) -> Any:
        """
        Finds the lowest level value in local scope by key
        :raise KeyError: if key is not in scope
        :param key: the variable name
        :return: The value in the local hierarchy by that key. Checks against globals last
        """
        if Machine_Variables.in_machine_variables(key):
            return self.machine_scope[key]
        is_global = self.has_global(key)
        if is_global and key in self._sub_scope_globals:  # Set as global in current subscope
            return self.globals[key]
        else:  # check lowest scope then globals
            scope = self
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

    def add_local_by_path(self, path: List[str], value: Any):
        """
        Adds module sub scopes to variable space following the given path.
        Sets final value in the lowest module subscope
        :param value: value to associate with end of path
        :param path: list of module names
        """
        scope = self
        for key in path[:-1]:
            if key not in scope:
                scope[key] = Knit_Script_Scope(self.context, scope, key, is_module=True)
            scope = scope[key]
        scope[path[-1]] = value

    def get_global(self, key: str) -> Any:
        """
        access global value
        :param key: the variable name
        :return: the global value under that var_name
        """
        assert self.has_global(key), f"Could not find global variable {key}"
        return self.globals[key]

    def has_local(self, key: str, stop_at_function=False, stop_at_module=False) -> bool:
        """
        Checks for key in local scope. Ignores globals
        :param stop_at_module: will not search for local variable beyond module
        :param stop_at_function: will not search for local variable beyond function
        :param key: the variable name to search for
        :return: True if key is in local scope
        """
        scope = self
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
        """
        check for global value
        :param key: the variable name
        :return: True if there is a global variable under this key
        """
        return key in self.globals

    def delete_local(self, key: str) -> bool:
        """
        Delete the variable at lowest scope level. If not found, no-op
        :param key: the variable name
        :return: True if a value was found and deleted
        """
        scope = self
        while scope is not None:
            if hasattr(scope, key):
                delattr(scope, key)
                return True
            scope = scope.parent
        return False

    def delete_global(self, key: str) -> bool:
        """
        Delete global variable. If not found, no-op
        :param key: variable name
        :return: True if a global was deleted
        """
        if self.has_global(key):
            del self.globals[key]
            return True
        return False

    def enter_new_scope(self, name: Optional[str] = None,
                        is_function: bool = False,
                        is_module: bool = False,
                        module_scope=None):
        """
        Enters a new sub scope and puts it into the hierarchy
        :param module_scope:
        :param name: name of the sub_scope if a function or module
        :param is_function: If true, may have return values
        :param is_module: If true, module is added by variable name
        :return: Child scope that was created.
        """
        if is_module or is_function:
            assert name is not None, "Functions and Modules must be named"
        child_scope = Knit_Script_Scope(self.context, self, name, is_function, is_module, module_scope=module_scope)
        if is_module:
            self[name] = child_scope
        self.child_scope = child_scope
        return self.child_scope

    def exit_current_scope(self):
        """
        Sets child scope to none.
        If the current scope is not a module this may cause values to be deleted and become inaccessible
        :return: The parent scope or None if program exits
        """
        if self.parent is not None:
            self.parent.child_scope = None
        return self.parent

    def __contains__(self, key: str) -> bool:
        value, exists = self.get_value_from_python_scope(key)
        if exists:
            return exists
        return self.has_global(key) or self.has_local(key)

    def __setitem__(self, key: str, value: Any):
        self.set_local(key, value)

    def __getitem__(self, key: str) -> Any:
        value, exists = self.get_value_from_python_scope(key)
        if exists:
            return value
        return self.get_local(key)

    def __delitem__(self, key: str):
        self.delete_local(key)
