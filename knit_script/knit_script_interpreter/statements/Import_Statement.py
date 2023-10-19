"""Used to import python and other knitscript code into program"""

import importlib
import os.path
from typing import Optional

import knit_script.knit_script_std_library as ks_library
from knit_script.knit_script_interpreter.expressions.accessors import Attribute_Accessor_Expression
from knit_script.knit_script_interpreter.expressions.expressions import Expression
from knit_script.knit_script_interpreter.expressions.variables import Variable_Expression
from knit_script.knit_script_interpreter.statements.Statement import Statement


class Import_Statement(Statement):
    """
        A statement that imports a python or knit script module
    """

    def __init__(self, parser_node, src: Expression, alias: Optional[Expression] = None):
        super().__init__(parser_node)
        self.src: Expression = src
        self.alias: Optional[str] = alias

    def execute(self, context):
        """
        Add the module with a given alias to the variable scope
        :param context: the current context to execute at
        """
        assert isinstance(self.src, Attribute_Accessor_Expression) or isinstance(self.src, Variable_Expression), \
            f"Cannot Import {self.src}, expected a module name or path"
        src_string = str(self.src)
        if self.alias is not None:
            assert isinstance(self.alias, Variable_Expression), f"Cannot import {src_string} as {self.alias}"
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
                    assert isinstance(parent, Variable_Expression), f"import path must be module names not {parent}"
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
                raise e
        assert module is not None
        if alias is not None:
            context.variable_scope[alias] = module
        else:  # attribute accessor path
            assert isinstance(self.src, Attribute_Accessor_Expression)
            path = [str(p) for p in self.src.parent]
            path.append(str(self.src.attribute))
            context.variable_scope.add_local_by_path(path, module)

    def __str__(self):

        return f"import {self.src} as {self.alias}"

    def __repr__(self):
        return str(self)
