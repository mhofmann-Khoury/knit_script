"""Used to import python and other knitscript code into program.

This module provides the Import_Statement class, which handles importing functionality from Python modules, knit script standard library modules, and local knit script files.
It supports both direct imports and aliased imports with comprehensive fallback logic for module resolution.
"""

import importlib
import os.path
from types import ModuleType

from parglare.parser import LRStackNode

from knit_script.knit_script_interpreter.expressions.accessors import Attribute_Accessor_Expression
from knit_script.knit_script_interpreter.expressions.variables import Variable_Expression
from knit_script.knit_script_interpreter.knit_script_context import Knit_Script_Context
from knit_script.knit_script_interpreter.scope.local_scope import Knit_Script_Scope
from knit_script.knit_script_interpreter.statements.scoped_statement import Scoped_Statement
from knit_script.knit_script_std_library import get_ks_library_path


class Import_Statement(Scoped_Statement):
    """Statement that imports a Python or knit script module.

    Supports importing Python modules, knit script standard library modules, and local knit script files.
    Handles both direct imports and aliased imports with comprehensive module resolution that searches multiple locations for the requested module.

    The import system follows a priority order: Python modules first, then knit script standard library, then local files, and finally standard library knit script files.
     This allows knit script programs to seamlessly integrate with Python libraries while providing access to knit script-specific functionality.

    Attributes:
        src (Expression): Expression representing the module name or path to import.
        alias (Expression | None): Optional alias name for the imported module.
    """

    def __init__(self, parser_node: LRStackNode, src: Attribute_Accessor_Expression | Variable_Expression, alias: Variable_Expression | None = None) -> None:
        """Initialize an import statement.

        Args:
            parser_node (LRStackNode): The parser node from the abstract syntax tree.
            src (Attribute_Accessor_Expression | Variable_Expression): A Variable or Attribute_Accessor expression representing the module name or path to import.
            alias (Variable_Expression, optional): Optional variable expression that declares the alias name for the imported module. Defaults to no alias.
        """
        super().__init__(parser_node, [])
        self.src: Attribute_Accessor_Expression | Variable_Expression = src
        self.alias: Variable_Expression | None = alias

    @property
    def source_string(self) -> str:
        """
        Returns:
            str: The string representing the path of values in the source expression.

        Raises:
            AttributeError | ImportError: If the source attribute cannot be parsed into a path of variables names.
        """
        if isinstance(self.src, Variable_Expression):
            return self.src.variable_name
        elif isinstance(self.src.attribute, Variable_Expression):
            return f"{self.src.parent_path()}.{self.src.attribute.variable_name}"
        else:
            raise ImportError(f"Expected to import path-like-string but got attribute {self.src.attribute}")

    @property
    def source_ks_file(self) -> str:
        """
        Returns:
            str: The string representing the file path to a ks file for the source expression.

        Raises:
            AttributeError | ImportError: If the source attribute cannot be parsed into a path of variables names.
        """
        return f"{self.source_string}.ks"

    @property
    def alias_name(self) -> str:
        """
        Returns:
            str: The alias of this import statement derived from the alias expression or the variable name of the source expression.
        """
        if self.alias is not None:
            return self.alias.variable_name
        if isinstance(self.src, Variable_Expression):
            return self.src.variable_name
        elif isinstance(self.src.attribute, Variable_Expression):
            return self.src.attribute.variable_name
        else:
            return "__temp_unnamed_module__"

    def _import_from_ks_standard_library(self) -> ModuleType:
        """
        Returns:
            ModuleType: The python module imported from the knitscript standard library.

        Raises:
            ModuleNotFoundError | ImportError | AttributeError: If the module cannot be imported from the knitscript standard library.
        """
        return importlib.import_module(f"knit_script.knit_script_std_library.{self.source_string}")

    def _import_local_module(self) -> ModuleType:
        """
        Returns:
            ModuleType: The python module imported locally.

        Raises:
            ModuleNotFoundError | AttributeError | ImportError: If the module cannot be imported locally.
        """
        return importlib.import_module(self.source_string)

    def _execute_local_ks_file(self, context: Knit_Script_Context) -> Knit_Script_Scope | None:
        """
        Args:
            context (Knit_Script_Context): The current context the import is being executed in.

        Returns:
            Knit_Script_Scope | None: The knitscript module imported from a local ks file. None, if no local ks file was found to import.
        """
        if self.local_path is None:
            return None
        local_path_to_src = os.path.join(self.local_path, self.source_ks_file)
        if not os.path.isfile(local_path_to_src):
            return None  # File not found in local directory
        return self._execute_ks_module_from_path(context, local_path_to_src)

    def _execute_ks_file_in_std_lbry(self, context: Knit_Script_Context) -> Knit_Script_Scope | None:
        """
        Args:
            context (Knit_Script_Context): The current context the import is being executed in.

        Returns:
            Knit_Script_Scope | None: The knitscript module imported from the standard library. None, if no local ks file was found to import.
        """
        library_path_to_src = os.path.join(get_ks_library_path(), self.source_ks_file)
        if not os.path.isfile(library_path_to_src):
            return None  # File not found in standard library
        return self._execute_ks_module_from_path(context, library_path_to_src)

    def _execute_ks_module_from_path(self, context: Knit_Script_Context, path: str) -> Knit_Script_Scope:
        """
        Args:
            context (Knit_Script_Context): The current context the import is being executed in.
            path (str): The path to the knitscript module to import.

        Returns:
            Knit_Script_Scope: The knitscript module imported from the given path.

        Raises:
            Parsing_Exception: If the imported module has a knitscript syntax error.
        """
        statements = context.parser.parse(path, pattern_is_file=True)
        module = context.enter_sub_scope(module_name=self.alias_name)  # enter sub scope for module
        context.execute_statements(statements)
        context.exit_current_scope()
        return module

    def _get_python_module(self) -> ModuleType | None:
        """
        Returns:
            ModuleType | None: The python module imported or None if a module could not be found.
        """
        try:
            try:
                return self._import_local_module()
            except (ImportError, ModuleNotFoundError) as _failed_local_python_import:
                return self._import_from_ks_standard_library()
        except (ImportError, ModuleNotFoundError) as _failed_ks_python_import:
            return None

    def execute(self, context: Knit_Script_Context) -> None:
        """Execute the import by loading the module and adding it to scope.

        Attempts to import in the following order: 1. Python module with the exact name 2. Knit script standard library module 3. Local knit script file 4. Standard library knit script file.
        Once found, adds the module to the current variable scope with the appropriate name or alias.

        Args:
            context (Knit_Script_Context): The current execution context to import into.

        Raises:
            ImportError: If src is not a module name or path expression, or if alias is not a valid variable expression.
                If the module cannot be found in any location after trying all resolution methods.
        """

        module: ModuleType | Knit_Script_Scope | None = self._get_python_module()
        if module is None:
            module = self._execute_local_ks_file(context)
        if module is None:
            module = self._execute_ks_file_in_std_lbry(context)
        if module is None:
            raise ImportError(f"Could not find a python or knitscript module <{self.source_ks_file}> in local module or ks standard library")
        if self.alias is not None or isinstance(self.src, Variable_Expression):
            context.variable_scope[self.alias_name] = module
        else:  # attribute accessor path
            context.variable_scope.add_local_by_path(self.src.parent_path_list(), module)
