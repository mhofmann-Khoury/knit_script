"""Keeps track of what modules are accessible from a given scope"""
from __future__ import annotations

from typing import Any


class Knit_Script_Module:
    """Tracks all modules imported at current scope. Used for python and knitscript modules."""

    def __init__(self, name: str, parent_module: None | Knit_Script_Module) -> None:
        self._parent_module = parent_module
        self.__name__ = name
        self._modules: dict[str, Any] = {}

    def __contains__(self, key: str) -> bool:
        return key in self._modules

    def __getitem__(self, key: str) -> Any:
        return self._modules[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self._modules[key] = value

    def get_module(self, key: str) -> Knit_Script_Module:
        """Collect the module value at the given path.

        Args:
            key (str): Key module name with . Separators for parent modules.

        Returns:
            Knit_Script_Module: The module in the hierarchy.

        Raises:
            KeyError: If the key path is not imported into scope.
        """
        module_names = key.split('.')
        sub_module = self
        accessed_path = ""
        for module in module_names:
            if module in sub_module:
                sub_module = sub_module[module]
                accessed_path += f"{module}."
            else:
                raise KeyError(f"Could not find module {key} in {accessed_path}")
        return sub_module

    def add_module(self, key: str, module: Knit_Script_Module) -> None:
        """Add the module to the modules list under parent modules.

        Args:
            key (str): The key (with . separators) to access the module under.
            module: The module to add under the key. Module could be python module or knit script scope.
        """
        module_path = key.split('.')
        sub_module = self
        for module_name in module_path[:-1]:
            if module_name not in sub_module:  # make new sub module
                sub_module[module_name] = Knit_Script_Module(module_name, sub_module)
            sub_module = sub_module[module_name]
        sub_module[module_path[-1]] = module


