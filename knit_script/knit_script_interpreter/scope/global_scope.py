"""Used for tracking global variable space of program execution"""
from typing import Dict, Any

from knit_script.knit_script_interpreter.scope.machine_scope import Machine_Variables


class Knit_Script_Globals:
    """
        Tracks all the global variables
    """

    def __init__(self):
        self.values: Dict[str, Any] = {}
        self._exit_value: Any = None

    def copy(self):
        """
        :return: shallow copy of the current values
        """
        copy_values = Knit_Script_Globals()
        copy_values.values = {k: v for k,v in self.values.items()}
        copy_values._exit_value = self._exit_value
        return copy_values
    @property
    def exit_value(self):
        """
        :return: Return value for whole knit script execution
        """
        return self._exit_value

    @exit_value.setter
    def exit_value(self, value: Any):
        self._exit_value = value

    def __getitem__(self, key: str) -> Any:
        return getattr(self, key)

    def __setitem__(self, key: str, value: Any):
        setattr(self, key, value)

    def __delitem__(self, key: str):
        delattr(self, key)

    def __contains__(self, key: str):
        return hasattr(self, key)
