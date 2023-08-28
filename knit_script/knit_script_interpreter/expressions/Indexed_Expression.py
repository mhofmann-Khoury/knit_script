from parglare.parser import LRStackNode

from knit_script.Knit_Errors import Knit_Script_Error
from knit_script.knit_script_interpreter.expressions.expressions import Expression
from knit_script.knit_script_interpreter.knit_script_context import Knit_Script_Context


class Slice_Index(Expression):

    def __init__(self, start: Expression | None, end: Expression | None, spacer: Expression | None, parser_node: LRStackNode):
        super().__init__(parser_node)
        self.spacer = spacer
        self.end = end
        self.start = start

    def __str__(self):
        return f"{self.start}:{self.end}:{self.spacer}"

    def __repr__(self):
        return str(self)

    def evaluate(self, context: Knit_Script_Context) -> slice:
        """
        Evaluate the expression
        :param context: The current context of the knit_script_interpreter
        :return: The list of values in the given slice or (if no colons given in slice) return the indexed value
        """
        if self.start is not None:
            start = self.start.evaluate(context)
        else:
            start = None
        if self.end is not None:
            end = self.end.evaluate(context)
        else:
            end = None
        if self.spacer is not None:
            spacer = self.spacer.evaluate(context)
        else:
            spacer = None
        return slice(start, end, spacer)


class Indexed_Expression(Expression):

    def __init__(self, parser_node: LRStackNode, item: Expression, key: Expression, assign: Expression | None):
        super().__init__(parser_node)
        self.assign = assign
        self.key = key
        self.item = item

    def __str__(self):
        string = f"{self.item}[{self.key}]"
        if self.assign is not None:
            string += f"= {self.assign}"
        return string

    def __repr__(self):
        return str(self)

    def evaluate(self, context: Knit_Script_Context):
        """
        Evaluate the expression
        :param context: The current context of the knit_script_interpreter
        :return: The list of values in the given slice or (if no colons given in slice) return the indexed value
        """
        item = self.item.evaluate(context)
        key = self.key.evaluate(context)
        if self.assign is not None:
            if isinstance(key, slice):
                raise Knit_Script_Error(f"Cannot __setitem__ with slice as index: {self}")
            assign_value = self.assign.evaluate(context)
            item[key] = assign_value
        return item[key]