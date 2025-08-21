"""Used to import python and other knitscript code into program.

This module provides the Import_Statement class, which handles importing functionality from Python modules, knit script standard library modules, and local knit script files.
It supports both direct imports and aliased imports with comprehensive fallback logic for module resolution.
"""

import importlib
import os.path
from typing import Iterable

from parglare.parser import LRStackNode

import knit_script.knit_script_std_library as ks_library
from knit_script.knit_script_exceptions.Knit_Script_Exception import (
    Knit_Script_Located_Exception,
)
from knit_script.knit_script_exceptions.python_style_exceptions import (
    Knit_Script_ImportError,
)
from knit_script.knit_script_interpreter.expressions.accessors import (
    Attribute_Accessor_Expression,
)
from knit_script.knit_script_interpreter.expressions.expressions import Expression
from knit_script.knit_script_interpreter.expressions.variables import (
    Variable_Expression,
)
from knit_script.knit_script_interpreter.knit_script_context import Knit_Script_Context
from knit_script.knit_script_interpreter.statements.Statement import Statement


class Import_Statement(Statement):
    """Statement that imports a Python or knit script module.

    Supports importing Python modules, knit script standard library modules, and local knit script files.
    Handles both direct imports and aliased imports with comprehensive module resolution that searches multiple locations for the requested module.

    The import system follows a priority order: Python modules first, then knit script standard library, then local files, and finally standard library knit script files.
     This allows knit script programs to seamlessly integrate with Python libraries while providing access to knit script-specific functionality.

    Attributes:
        src (Expression): Expression representing the module name or path to import.
        alias (Expression | None): Optional alias name for the imported module.
    """

    def __init__(self, parser_node: LRStackNode, src: Expression, alias: Expression | None = None) -> None:
        """Initialize an import statement.

        Args:
            parser_node (LRStackNode): The parser node from the abstract syntax tree.
            src (Expression): Expression representing the module name or path to import. Must evaluate to a Variable_Expression or Attribute_Accessor_Expression.
            alias (Expression | None, optional): Optional alias name for the imported module. If None and src is a Variable_Expression, uses the module name as the alias. Defaults to None.
        """
        super().__init__(parser_node)
        self.src: Expression = src
        self.alias: Expression | None = alias

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
        if not (isinstance(self.src, Attribute_Accessor_Expression) or isinstance(self.src, Variable_Expression)):
            raise Knit_Script_ImportError(f"Cannot Import {self.src}, expected a module name or path", self)
        src_string = str(self.src)
        if self.alias is not None:
            if not isinstance(self.alias, Variable_Expression):
                raise Knit_Script_ImportError(f"Cannot import {src_string} as {self.alias}", self)
            alias = self.alias.variable_name
        elif isinstance(self.src, Variable_Expression):
            alias = self.src.variable_name
        else:
            alias = None
        try:
            try:
                module = importlib.import_module(src_string)
            except ModuleNotFoundError:
                module = importlib.import_module(f'knit_script.knit_script_std_library.{src_string}')
        except (ImportError, ModuleNotFoundError) as e:
            local_path = os.path.dirname(context.ks_file)
            library_path = os.path.dirname(ks_library.__file__)
            if isinstance(self.src, Variable_Expression):
                local_path_to_src = os.path.join(local_path, f'{self.src.variable_name}.ks')
                local_is_file = os.path.isfile(local_path_to_src)
                library_path_to_src = os.path.join(library_path, f'{self.src.variable_name}.ks')
                library_is_file = os.path.isfile(library_path_to_src)
                module = context.enter_sub_scope(module_name=alias)  # enter sub scope for module
            else:
                assert isinstance(self.src, Attribute_Accessor_Expression)
                local_path_to_src = local_path
                library_path_to_src = library_path
                for parent in self.src.parent:
                    if not isinstance(parent, Variable_Expression):
                        raise Knit_Script_ImportError(f"import path must be module names not {parent}", self)
                    local_path_to_src = os.path.join(local_path_to_src, parent.variable_name)
                    library_path_to_src = os.path.join(library_path_to_src, parent.variable_name)
                local_path_to_src = os.path.join(local_path_to_src, f'{self.src.attribute}.ks')
                local_is_file = os.path.isfile(local_path_to_src)
                library_path_to_src = os.path.join(library_path_to_src, f'{self.src.attribute}.ks')
                library_is_file = os.path.isfile(library_path_to_src)
                assert isinstance(self.src.attribute, Variable_Expression)
                module = context.enter_sub_scope(module_name="__temp_module__")
            if local_is_file:  # try local files before checking library
                statements = context.parser.parse(local_path_to_src, pattern_is_file=True)
                context.execute_statements(statements)
                context.exit_current_scope()
            elif library_is_file:
                statements = context.parser.parse(library_path_to_src, pattern_is_file=True)
                context.execute_statements(statements)
                context.exit_current_scope()
            else:
                if not isinstance(e, Knit_Script_Located_Exception):
                    raise Knit_Script_Located_Exception(e, self)
                else:
                    raise e
        assert module is not None
        if alias is not None:
            context.variable_scope[alias] = module
        else:  # attribute accessor path
            assert isinstance(self.src, Attribute_Accessor_Expression)
            assert isinstance(self.src.parent, Iterable)
            path = [str(p) for p in self.src.parent]
            path.append(str(self.src.attribute))
            context.variable_scope.add_local_by_path(path, module)

    def __str__(self) -> str:
        """Return string representation of the import statement.

        Returns:
            str: A string showing the source and optional alias.
        """
        return f"import {self.src} as {self.alias}"

    def __repr__(self) -> str:
        """Return detailed string representation of the import statement.

        Returns:
            str: Same as __str__ for this class.
        """
        return str(self)
