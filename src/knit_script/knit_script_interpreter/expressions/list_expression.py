"""Used for container structures (tuples, lists, dicts, comprehensions).

This module provides expression classes for handling various container data structures in knit script programs.
It includes support for lists, dictionaries, tuples, list comprehensions, dictionary comprehensions, and unpacking operations, following Python conventions for syntax and behavior.
"""

from collections.abc import Iterable, Sequence
from typing import Any

from parglare.parser import LRStackNode
from virtual_knitting_machine.Knitting_Machine import Knitting_Machine
from virtual_knitting_machine.machine_components.needles.Needle import Needle

from knit_script.knit_script_interpreter.expressions.expressions import Expression
from knit_script.knit_script_interpreter.expressions.variables import Variable_Expression
from knit_script.knit_script_interpreter.knit_script_context import Knit_Script_Context


class Unpack(Expression):
    """Used to unpack values into a tuple with * function.

    The Unpack class implements the unpacking operator (*) functionality for knit script expressions.
    It takes an iterable expression and unpacks its elements into a tuple, similar to Python's unpacking behavior.

    Attributes:
        _expression (Expression): The expression to unpack into individual elements.
    """

    def __init__(self, parser_node: LRStackNode, exp: Expression) -> None:
        """Initialize the Unpack expression.

        Args:
            parser_node (LRStackNode): The parser node from the parse tree.
            exp (Expression): Expression to unpack into individual elements.
        """
        super().__init__(parser_node)
        self._expression = exp

    def evaluate(self, context: Knit_Script_Context) -> tuple[Any, ...]:
        """Evaluate the expression to unpack the contained expression.

        Args:
            context (Knit_Script_Context): The current context of the knit_script_interpreter.

        Returns:
            tuple[Any, ...]: Tuple with unpacked values from the expression.
        """
        return (*self._expression.evaluate(context),)


class Knit_Script_List(Expression):
    """Evaluates to list of expression values. Lists are not typed following python style conventions.

    The Knit_Script_List class implements list literal expressions in knit script programs.
    It supports mixed-type elements and handles unpacking operations within list construction, following Python's list syntax and behavior.

    Attributes:
        expressions (list[Expression]): The expressions to evaluate and include in the list.
    """

    def __init__(self, parser_node: LRStackNode, expressions: list[Expression]) -> None:
        """Initialize the Knit_Script_List.

        Args:
            parser_node (LRStackNode): The parser node from the parse tree.
            expressions (list[Expression]): Expressions to fill the list with.
        """
        super().__init__(parser_node)
        self.expressions: list[Expression] = expressions

    def evaluate(self, context: Knit_Script_Context) -> list[Any]:
        """Evaluate the expression to create a list.

        Evaluates each expression in the list and handles unpacking operations. If an expression is an Unpack, its elements are extended into the list rather than added as a nested structure.

        Args:
            context (Knit_Script_Context): The current context of the knit_script_interpreter.

        Returns:
            list[Any]: List of expression evaluations at current context, with unpacked elements properly expanded.
        """
        values: list[Any] = []
        for exp in self.expressions:
            if isinstance(exp, Unpack):
                values.extend(exp.evaluate(context))
            else:
                values.append(exp.evaluate(context))
        return values


class Sliced_List(Expression):
    """Slices a list using standard python syntax.

    The Sliced_List class implements Python-style slicing and indexing operations for iterable expressions.
    It supports start, end, and step parameters for slicing, as well as simple indexing operations. Special handling is provided for knitting machine objects.

    Attributes:
        _is_index (bool): True if this is an index operation rather than a slice.
        _end_to_spacer (bool): Whether to include end to spacer range.
        _start_to_end (bool): Whether to include start to end range.
        _spacer (Expression | None): The step/spacer expression for slicing.
        _end (Expression | None): The end index expression for slicing.
        _start (Expression | None): The start index expression for slicing.
        _iter_exp (Expression): The iterable expression to slice.
    """

    def __init__(
        self,
        parser_node: LRStackNode,
        iter_exp: Expression,
        start: Expression | None = None,
        start_to_end: bool = False,
        end: Expression | None = None,
        end_to_spacer: bool = False,
        spacer: Expression | None = None,
        is_index: bool = False,
    ) -> None:
        """Initialize the Sliced_List.

        Args:
            parser_node (LRStackNode): The parser node from the parse tree.
            iter_exp (Expression): Iterable expression to slice.
            start (Expression | None, optional): Start of slice, inclusive, defaults to 0. Defaults to None.
            start_to_end (bool, optional): Whether to include start to end range. Defaults to False.
            end (Expression | None, optional): End of slice, exclusive, defaults to last element. Defaults to None.
            end_to_spacer (bool, optional): Whether to include end to spacer range. Defaults to False.
            spacer (Expression | None, optional): Step/spacer of slice, defaults to 1. Defaults to None.
            is_index (bool, optional): Whether this is an index operation rather than a slice. Defaults to False.
        """
        super().__init__(parser_node)
        if is_index:
            assert end is None and spacer is None
        self._is_index: bool = is_index
        self._end_to_spacer: bool = end_to_spacer
        self._start_to_end: bool = start_to_end
        self._spacer: Expression | None = spacer
        self._end: Expression | None = end
        self._start: Expression | None = start
        self._iter_exp: Expression = iter_exp

    def evaluate(self, context: Knit_Script_Context) -> Iterable[Any] | Any:
        """Evaluate the expression to perform slicing or indexing.

        Args:
            context (Knit_Script_Context): The current context of the knit_script_interpreter.

        Returns:
            Iterable[Any] | Any: The list of values in the given slice or the indexed value for single index operations.

        Raises:
            TypeError: If attempting to slice a knitting machine or if the target is not iterable.
        """
        iterable = self._iter_exp.evaluate(context)
        if isinstance(iterable, Knitting_Machine):
            if self._is_index:
                assert isinstance(self._start, Expression)
                start = self._start.evaluate(context)
                if not isinstance(start, Needle):
                    raise TypeError(f"Knitting machine requires needles to index but got {self._start}<{start}>")
                return context.machine_state[start]
            else:
                raise TypeError(f"Knitting Machine is not iterable and cannot be iterated over [{self._start}:{self._end}:{self._spacer}]")
        if not isinstance(iterable, Iterable):
            raise TypeError(f"Cannot Slice non-iterable {self._iter_exp}<{iterable}>.")
        iterable = list(iterable)
        if self._is_index:
            assert isinstance(self._start, Expression)
            index = self._start.evaluate(context)
            return iterable[index]
        else:
            start = 0 if self._start is None else int(self._start.evaluate(context))
            end = len(iterable) if self._end is None else int(self._end.evaluate(context))
            spacer = 1 if self._spacer is None else int(self._spacer.evaluate(context))
            return iterable[start:end:spacer]

    def _is_slice(self) -> bool:
        """Check if this is a slice operation.

        Returns:
            bool: True if this represents a slice operation rather than simple indexing.
        """
        return self._start_to_end or self._end_to_spacer


class Knit_Script_Dictionary(Expression):
    """Used to process dictionary structures.

    The Knit_Script_Dictionary class implements dictionary literal expressions in knit script programs.
     It evaluates key-value pairs and constructs dictionaries following Python's dictionary syntax and behavior.

    Attributes:
        _kwargs (list[tuple[Expression, Expression]]): List of key-value expression pairs for the dictionary.
    """

    def __init__(self, parser_node: LRStackNode, kwargs: list[tuple[Expression, Expression]]) -> None:
        """Initialize the Knit_Script_Dictionary.

        Args:
            parser_node (LRStackNode): The parser node from the parse tree.
            kwargs (list[tuple[Expression, Expression]]): The key-value pairs of expressions for the dictionary.
        """
        super().__init__(parser_node)
        self._kwargs: list[tuple[Expression, Expression]] = kwargs

    def evaluate(self, context: Knit_Script_Context) -> dict[Any, Any]:
        """Evaluate the expression to create a dictionary.

        Evaluates each key-value pair and constructs a dictionary with the results.

        Args:
            context (Knit_Script_Context): The current context of the knit_script_interpreter.

        Returns:
            dict[Any, Any]: Dictionary with evaluated keys mapped to evaluated values.
        """
        return {kwarg[0].evaluate(context): kwarg[1].evaluate(context) for kwarg in self._kwargs}


class Comprehension(Expression):

    def __init__(
        self, parser_node: LRStackNode, value_expressions: Expression | Sequence[Expression], variables: list[Variable_Expression], iter_exp: Expression, comp_cond: Expression | None
    ) -> None:
        super().__init__(parser_node)
        self._comp_cond: Expression | None = comp_cond
        self._values: Expression | Sequence[Expression] = value_expressions
        self._iter_exp: Expression = iter_exp
        self._variables: list[Variable_Expression] = variables
        self._var_name: str | None = self._variables[0].variable_name if len(self._variables) == 1 else None

    def _get_iterable(self, context: Knit_Script_Context) -> Iterable[Any]:
        iter_val = self._iter_exp.evaluate(context)
        return iter_val if isinstance(iter_val, Iterable) else [iter_val]

    def evaluate_iterable(self, context: Knit_Script_Context) -> list[Any]:
        """Evaluate the expression to generate an iterable sequence of values.

        Creates a new scope for iteration variables,
            iterates over the iterable,
                and builds a sequence by evaluating the value expressions for each iteration that passes the optional condition.

        Args:
            context (Knit_Script_Context): The current context of the knit_script_interpreter.

        Returns:
            list[Any]: Result of the comprehension with filtered and transformed values.

        Raises:
            ValueError: If the iterable is not actually iterable or if variable unpacking doesn't match the provided variables.
        """
        iterable = self._get_iterable(context)
        new_var_names = set()
        for var_expression in self._variables:
            if var_expression.variable_name not in context.variable_scope:
                new_var_names.add(var_expression.variable_name)
        values = []
        for var in iterable:
            if self._var_name is not None:
                context.variable_scope[self._var_name] = var  # update iterator variable in scope
            else:  # multiple vars to unpack
                iterated_var = [*var]
                if len(iterated_var) != len(self._variables):
                    raise ValueError(f"Number of keys <{iterated_var}> do not match number of variables <{self._variables}>")
                for var_name, var_val in zip(self._variables, iterated_var, strict=False):
                    context.variable_scope[var_name.variable_name] = var_val
            if bool(self._comp_cond.evaluate(context)) if isinstance(self._comp_cond, Expression) else True:
                if isinstance(self._values, Expression):
                    values.append(self._values.evaluate(context))
                else:
                    values.append(tuple(v.evaluate(context) for v in self._values))
        for new_var in new_var_names:
            del context.variable_scope[new_var]
        return values


class List_Comp(Comprehension):
    """Runs a list comprehension over an iterator.

    The List_Comp class implements Python-style list comprehensions for knit script programs.
    It supports iteration variables, optional filtering conditions, and custom spacing patterns for iteration control.
    """

    def __init__(self, parser_node: LRStackNode, value_expression: Expression, variables: list[Variable_Expression], iter_exp: Expression, comp_cond: Expression | None) -> None:
        """Initialize the List_Comp.

        Args:
            parser_node (LRStackNode): The parser node from the parse tree.
            value_expression (Expression): Expression that fills the list for each iteration.
            variables (list[Variable_Expression]): Variables to bind from the iterable.
            iter_exp (Expression): The iterable expression to iterate over.
            comp_cond (Expression | None): Optional condition expression for filtering values.
        """
        super().__init__(parser_node, value_expression, variables, iter_exp, comp_cond)

    def evaluate(self, context: Knit_Script_Context) -> list[Any]:
        """Evaluate the expression to create a dictionary.

        Creates a new scope for iteration variables, iterates over the iterable, and builds a list by evaluating the fill expression for each iteration that passes the optional condition.

        Args:
            context (Knit_Script_Context): The current context of the knit_script_interpreter.

        Returns:
            list[Any]: Result of list comprehension with filtered and transformed values.

        Raises:
            KeyError: If variable unpacking doesn't match the provided variables.
        """
        return self.evaluate_iterable(context)


class Dictionary_Comprehension(Comprehension):
    """Used for supporting dictionary comprehension.

    The Dictionary_Comprehension class implements Python-style dictionary comprehensions for knit script programs.
    It supports iteration variables, optional filtering conditions, and custom spacing patterns, generating dictionaries through iteration.
    """

    def __init__(self, parser_node: LRStackNode, key: Expression, value: Expression, variables: list[Variable_Expression], iter_exp: Expression, comp_cond: Expression | None = None) -> None:
        """Initialize the Dictionary_Comprehension.

        Args:
            parser_node (LRStackNode): The parser node from the parse tree.
            key (Expression): Expression that generates keys for each dictionary entry.
            value (Expression): Expression that generates values for each dictionary entry.
            variables (list[Variable_Expression]): Variables to bind from the iterable.
            iter_exp (Expression): The iterable expression to iterate over.
            comp_cond (Expression | None, optional): Optional condition expression for filtering entries. Defaults to None.
        """
        super().__init__(parser_node, [key, value], variables, iter_exp, comp_cond)

    def evaluate(self, context: Knit_Script_Context) -> dict[Any, Any]:
        """Evaluate the expression to generate a dictionary through comprehension.

        Creates a new scope for iteration variables, iterates over the iterable,
         and builds a dictionary by evaluating the key and value expressions for each iteration that passes the optional condition.

        Args:
            context (Knit_Script_Context): The current context of the knit_script_interpreter.

        Returns:
            dict[Any, Any]: Result of dictionary comprehension with filtered and transformed key-value pairs.

        Raises:
            KeyError: If variable unpacking doesn't match the provided variables.
        """
        key_value_pairs = self.evaluate_iterable(context)
        return dict(key_value_pairs)
