"""Expressions associated with slicing and indexing elements.

This module provides classes for handling Python-style indexing and slicing operations in knit script expressions.
 It includes support for both simple indexing and slice operations with optional step values, as well as indexed assignment operations.
"""
from typing import Any

from parglare.parser import LRStackNode

from knit_script.knit_script_exceptions.python_style_exceptions import (
    Knit_Script_IndexError,
    Knit_Script_KeyError,
    Knit_Script_TypeError,
    Knit_Script_ValueError,
)
from knit_script.knit_script_interpreter.expressions.expressions import Expression
from knit_script.knit_script_interpreter.knit_script_context import Knit_Script_Context


class Slice_Index(Expression):
    """An expression that slices a given expression using python notation.

    The Slice_Index class implements Python-style slice notation for knit script expressions.
    It supports start, end, and step parameters, allowing for flexible slicing operations on lists, strings, and other sequence types.
    The class creates Python slice objects that can be used with standard indexing operations.

    Attributes:
        start (Expression | None): The start index expression for the slice.
        end (Expression | None): The end index expression for the slice.
        spacer (Expression | None): The step/spacer expression for the slice.
    """

    def __init__(self, start: Expression | None, end: Expression | None, spacer: Expression | None, parser_node: LRStackNode):
        """Initialize the Slice_Index expression.

        Args:
            start (Expression | None): The start index expression for the slice, or None for default start.
            end (Expression | None): The end index expression for the slice, or None for default end.
            spacer (Expression | None): The step/spacer expression for the slice, or None for default step of 1.
            parser_node (LRStackNode): The parser node from the parse tree.
        """
        super().__init__(parser_node)
        self.spacer = spacer
        self.end = end
        self.start = start

    def __str__(self) -> str:
        return f"{self.start}:{self.end}:{self.spacer}"

    def __repr__(self) -> str:
        return str(self)

    def evaluate(self, context: Knit_Script_Context) -> slice:
        """Evaluate the expression to create a Python slice object.

        Evaluates the start, end, and step expressions and creates a Python slice object with the resulting values. None values are preserved to allow Python's default slicing behavior.

        Args:
            context (Knit_Script_Context): The current context of the knit_script_interpreter.

        Returns:
            slice: A Python slice object with the evaluated start, end, and step values.
        """
        if self.start is not None:
            try:
                start = int(self.start.evaluate(context))
            except ValueError as e:
                raise Knit_Script_ValueError(str(e), self)
        else:
            start = None
        if self.end is not None:
            try:
                end = int(self.end.evaluate(context))
            except ValueError as e:
                raise Knit_Script_ValueError(str(e), self)
        else:
            end = None
        if self.spacer is not None:
            try:
                spacer = int(self.spacer.evaluate(context))
            except ValueError as e:
                raise Knit_Script_ValueError(str(e), self)
        else:
            spacer = None
        return slice(start, end, spacer)


class Indexed_Expression(Expression):
    """An expression to index into an expression using python notation.

    The Indexed_Expression class implements Python-style indexing operations for knit script expressions.
    It supports both reading from and writing to indexed positions, handling both simple indexing and slice operations. The class provides comprehensive error handling for common indexing issues.

    Attributes:
        item (Expression): The expression to index into.
        key (Expression): The index or slice expression to use for indexing.
        assign (Expression | None): Optional assignment expression for indexed assignment operations.
    """

    def __init__(self, parser_node: LRStackNode, item: Expression, key: Expression, assign: Expression | None):
        """Initialize the Indexed_Expression.

        Args:
            parser_node (LRStackNode): The parser node from the parse tree.
            item (Expression): The expression to index into (list, dict, string, etc.).
            key (Expression): The index or slice expression to use for accessing the item.
            assign (Expression | None): Optional assignment expression for setting values at the indexed position.
        """
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
        """Evaluate the expression to perform indexing or indexed assignment.

        Evaluates the item and key expressions, performs the indexing operation, and optionally handles assignment if an assignment expression is provided.
        Includes comprehensive error handling for common indexing issues.

        Args:
            context (Knit_Script_Context): The current context of the knit_script_interpreter.

        Returns:
            list[Any] | Any: The value at the indexed position, or a list of values for slice operations. For assignment operations, returns the accessed value after assignment.

        Raises:
            TypeError: If attempting to assign to a slice index.
            IndexError: If the index is out of range for the item.
            KeyError: If the key does not exist in a dictionary-like item.
        """
        item = self.item.evaluate(context)
        key = self.key.evaluate(context)
        if self.assign is not None:
            if isinstance(key, slice):
                raise Knit_Script_TypeError(f'Cannot set the value of {self.item} of value {item} with type slice {self.key} <{key}> ', self)
            assign_value = self.assign.evaluate(context)
            item[key] = assign_value
        try:
            return item[key]
        except IndexError as _e:
            raise Knit_Script_IndexError(f'Index {self.key}<{key}> is out of range of {self.item} <{item}>', self)
        except KeyError as _e:
            raise Knit_Script_KeyError(f'Key {self.key}<{key}> is not in {self.item} <{item}>', self)
        except TypeError as _e:
            try:
                return item[int(key)] # attempt to convert to integer
            except ValueError as _e:
                raise Knit_Script_ValueError(f"Key {self.key}<{key}> cannot be set to integer to index in to {self.item} <{item}>", self)
