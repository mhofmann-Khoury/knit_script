"""Expressions associated with slicing and indexing elements"""
from typing import Any

from parglare.parser import LRStackNode

from knit_script.knit_script_interpreter.expressions.expressions import Expression
from knit_script.knit_script_interpreter.knit_script_context import Knit_Script_Context


class Slice_Index(Expression):
    """An expression that slices a given expression using python notation."""

    def __init__(self, start: Expression | None, end: Expression | None, spacer: Expression | None, parser_node: LRStackNode):
        super().__init__(parser_node)
        self.spacer = spacer
        self.end = end
        self.start = start

    def __str__(self) -> str:
        return f"{self.start}:{self.end}:{self.spacer}"

    def __repr__(self) -> str:
        return str(self)

    def evaluate(self, context: Knit_Script_Context) -> slice:
        """Evaluate the expression.

        Args:
            context (Knit_Script_Context): The current context of the knit_script_interpreter.

        Returns:
            slice: The list of values in the given slice or (if no colons given in slice) return the indexed value.
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
    """An expression to index into an expression using python notation."""

    def __init__(self, parser_node: LRStackNode, item: Expression, key: Expression, assign: Expression | None):
        super().__init__(parser_node)
        self.assign = assign
        self.key = key
        self.item = item

    def __str__(self) -> str:
        string = f"{self.item}[{self.key}]"
        if self.assign is not None:
            string += f"= {self.assign}"
        return string

    def __repr__(self) -> str:
        return str(self)

    def evaluate(self, context: Knit_Script_Context) -> list[Any] | Any:
        """Evaluate the expression.

        Args:
            context (Knit_Script_Context): The current context of the knit_script_interpreter.

        Returns:
            list[Any] | Any: The list of values in the given slice or (if no colons given in slice) return the indexed value.
        """
        item = self.item.evaluate(context)
        key = self.key.evaluate(context)
        if self.assign is not None:
            if isinstance(key, slice):
                raise TypeError(f'Cannot set the value of {self.item} of value {item} with type slice {self.key} <{key}> ')
            assign_value = self.assign.evaluate(context)
            item[key] = assign_value
        try:
            return item[key]
        except IndexError as _e:
            raise IndexError(f'Index {self.key}<{key}> is out of range of {self.item} <{item}>')
        except KeyError as _e:
            raise KeyError(f'Key {self.key}<{key}> is not in {self.item} <{item}>')
