import importlib
from typing import Optional

from knit_script.knit_script_interpreter.expressions.accessors import Attribute_Accessor_Expression
from knit_script.knit_script_interpreter.expressions.expressions import Expression
from knit_script.knit_script_interpreter.expressions.variables import Variable_Expression
from knit_script.knit_script_interpreter.knit_script_context import Knit_Script_Context
from knit_script.knit_script_interpreter.statements.Statement import Statement


class Import_Statement(Statement):
    """
        A statement that imports a python or knitscript module
    """
    def __init__(self, src: Expression, alias: Optional[Expression] = None):
        super().__init__()
        self.src:Expression = src
        self.alias:Optional[str] = alias

    def execute(self, context: Knit_Script_Context):
        """
        Add the module with a given alias to the variable scope
        :param context: the current context to execute at
        """
        assert  isinstance(self.src, Attribute_Accessor_Expression) or isinstance(self.src, Variable_Expression), f"Cannot Import {self.src}, expected a module name"
        src_string = str(self.src)
        if self.alias is None:
            alias = src_string
        else:
            assert isinstance(self.alias, Variable_Expression), f"Cannot import {src_string} as {str(self.alias)}"
            alias = self.alias.variable_name
        try:
            module = importlib.import_module(src_string)
            context.variable_scope[alias] = module
        except ImportError as e:
            assert False, f"KnitScript imports are not yet supported.\n{e}"

    def __str__(self):

        return f"import {self.src} as {self.alias}"

    def __repr__(self):
        return str(self)