"""Used for container structures (tuples, lists, dicts, comprehensions)"""
from typing import Iterable, Any

from parglare.parser import LRStackNode
from virtual_knitting_machine.Knitting_Machine import Knitting_Machine
from virtual_knitting_machine.machine_components.needles.Needle import Needle

from knit_script.knit_script_interpreter.expressions.expressions import Expression
from knit_script.knit_script_interpreter.expressions.variables import Variable_Expression
from knit_script.knit_script_interpreter.knit_script_context import Knit_Script_Context


class Unpack(Expression):
    """Used to unpack values into a tuple with * function."""

    def __init__(self, parser_node: LRStackNode, exp: Expression) -> None:
        """Initialize the Unpack.

        Args:
            parser_node (LRStackNode): The parser node from the parse tree.
            exp (Expression): Expression to unpack.
        """
        super().__init__(parser_node)
        self._exp = exp

    def evaluate(self, context: Knit_Script_Context) -> tuple:
        """Evaluate the expression.

        Args:
            context (Knit_Script_Context): The current context of the knit_script_interpreter.

        Returns:
            tuple: Tuple with unpacked values from expression.
        """
        return tuple([*self._exp.evaluate(context)])

    def __str__(self) -> str:
        return f"(*{self._exp})"

    def __repr__(self) -> str:
        return str(self)


class Knit_Script_List(Expression):
    """Evaluates to list of expression values. Lists are not typed following python style conventions."""

    def __init__(self, parser_node: LRStackNode, expressions: list[Expression]) -> None:
        """Initialize the Knit_Script_List.

        Args:
            parser_node (LRStackNode): The parser node from the parse tree.
            expressions (list[Expression]): Expressions to fill list with.
        """
        super().__init__(parser_node)
        self.expressions: list[Expression] = expressions

    def evaluate(self, context: Knit_Script_Context) -> list[Any]:
        """Evaluate the expression.

        Args:
            context (Knit_Script_Context): The current context of the knit_script_interpreter.

        Returns:
            list[Any]: List of expression evaluations at current context.
        """
        values: list[Any] = []
        for exp in self.expressions:
            if isinstance(exp, Unpack):
                values.extend(exp.evaluate(context))
            else:
                values.append(exp.evaluate(context))
        return values

    def __str__(self) -> str:
        values = ""
        for exp in self.expressions:
            values += f"{exp}, "
        values = values[:-2]
        return f"[{values}]"

    def __repr__(self) -> str:
        return str(self)


class Sliced_List(Expression):
    """Slices a list using standard python syntax."""

    def __init__(self, parser_node: LRStackNode, iter_exp: Expression, start: Expression | None = None, start_to_end: bool = False, end: Expression | None = None, end_to_spacer: bool = False,
                 spacer: Expression | None = None, is_index: bool = False) -> None:
        """Initialize the Sliced_List.

        Args:
            parser_node (LRStackNode): The parser node from the parse tree.
            iter_exp (Expression): Iterable to slice.
            start (Expression | None, optional): Start of slice, inclusive, defaults to 0.
            start_to_end (bool, optional): Whether to include start to end range. Defaults to False.
            end (Expression | None, optional): End of slice, exclusive, defaults to last element.
            end_to_spacer (bool, optional): Whether to include end to spacer range. Defaults to False.
            spacer (Expression | None, optional): Spacer of slice, defaults to 1.
            is_index (bool, optional): Whether this is an index operation. Defaults to False.
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
        """Evaluate the expression.

        Args:
            context (Knit_Script_Context): The current context of the knit_script_interpreter.

        Returns:
            Iterable[Any] | Any: The list of values in the given slice or (if no colons given in slice) return the indexed value.
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
        iterable = [i for i in iterable]
        if self._is_index:
            assert isinstance(self._start, Expression)
            index = self._start.evaluate(context)
            return iterable[index]
        else:
            if self._start is None:
                start = 0
            else:
                start = int(self._start.evaluate(context))
            if self._end is None:
                end = len(iterable)
            else:
                end = int(self._end.evaluate(context))
            if self._spacer is None:
                spacer = 1
            else:
                spacer = int(self._spacer.evaluate(context))
            return iterable[start:end:spacer]

    def _is_slice(self) -> bool:
        return self._start_to_end or self._end_to_spacer

    def __str__(self) -> str:
        if self._is_slice():
            return f"{self._iter_exp}[{self._start}:{self._end}:{self._spacer}]"
        else:
            return f"{self._iter_exp}[{self._start}]"

    def __repr__(self) -> str:
        return str(self)


class List_Comp(Expression):
    """Runs a list comprehension over an iterator."""

    def __init__(self, parser_node: LRStackNode, fill_exp: Expression, variables: list[Variable_Expression], iter_exp: Expression, comp_cond: Expression | None) -> None:
        """Initialize the List_Comp.

        Args:
            parser_node (LRStackNode): The parser node from the parse tree.
            fill_exp (Expression): Expression that fills the list.
            variables (list[Variable_Expression]): Variables to fill from iterable.
            iter_exp (Expression): The iterable to pass over.
            comp_cond (Expression | None): Condition to evaluate for adding a value.
        """
        super().__init__(parser_node)
        self._comp_cond: Expression | None = comp_cond
        self._spacer: str | None | Expression = None
        self._fill_exp: Expression = fill_exp
        self._vars: list[Variable_Expression] = variables
        if len(self._vars) == 1:
            self._var_name: str | None = self._vars[0].variable_name
        else:
            self._var_name: str | None = None
        self._iter_exp: Expression = iter_exp

    def evaluate(self, context: Knit_Script_Context) -> list[Any]:
        """Evaluate the expression.

        Args:
            context (Knit_Script_Context): The current context of the knit_script_interpreter.

        Returns:
            list[Any]: Result of list comprehension inside list.
        """
        iterable = self._iter_exp.evaluate(context)
        assert isinstance(iterable, Iterable), f'Cannot iterate over non-iterable value {iterable}'
        if self._spacer is not None:
            assert isinstance(iterable, list)
            if isinstance(self._spacer, str):
                if self._spacer == "even":
                    iterable = [val for i, val in enumerate(iterable) if i % 2 == 0]
                elif self._spacer == "odd":
                    iterable = [val for i, val in enumerate(iterable) if i % 2 == 1]
                else:  # "other"
                    iterable = iterable[::2]
            else:
                spacer = int(self._spacer.evaluate(context))
                iterable = iterable[::spacer]
        context.enter_sub_scope()  # create new scope that holds iterator variable
        values = []
        for var in iterable:
            if self._var_name is not None:
                context.variable_scope[self._var_name] = var  # update iterator variable in scope
            else:  # multiple vars to unpack
                iterated_var = [*var]
                assert len(iterated_var) == len(self._vars), "Unpacked values do not match variables provided"
                for var_name, var_val in zip(self._vars, iterated_var):
                    context.variable_scope[var_name.variable_name] = var_val
            if self._comp_cond is None:
                condition_result = True
            else:
                condition_result = bool(self._comp_cond.evaluate(context))
            if condition_result:
                values.append(self._fill_exp.evaluate(context))
        context.exit_current_scope()  # exit scope, removing access to iterator variable
        return values

    def __str__(self) -> str:
        spacer = ""
        if self._spacer is not None:
            spacer = f" every {self._spacer}"
        comp = ""
        if self._comp_cond is not None:
            comp = f" if {self._comp_cond}"
        return f"[{self._fill_exp} for{spacer} {self._vars} in {self._iter_exp}{comp}]"

    def __repr__(self) -> str:
        return str(self)


class Knit_Script_Dictionary(Expression):
    """Used to process dictionary structures."""

    def __init__(self, parser_node: LRStackNode, kwargs: list[tuple[Expression, Expression]]) -> None:
        """Initialize the Knit_Script_Dictionary.

        Args:
            parser_node (LRStackNode): The parser node from the parse tree.
            kwargs (list[tuple[Expression, Expression]]): The key value pairs of a dictionary.
        """
        super().__init__(parser_node)
        self._kwargs: list[tuple[Expression, Expression]] = kwargs

    def evaluate(self, context: Knit_Script_Context) -> dict[Any, Any]:
        """Evaluate the expression.

        Args:
            context (Knit_Script_Context): The current context of the knit_script_interpreter.

        Returns:
            dict[Any, Any]: Dictionary with keys assigned to arguments.
        """
        return {kwarg[0].evaluate(context): kwarg[1].evaluate(context) for kwarg in self._kwargs}

    def __str__(self) -> str:
        values = ""
        for assign in self._kwargs:
            values += f"{assign[0]}:{assign[1]}, "
        values = values[:-2]
        return "{" + values + "}"

    def __repr__(self) -> str:
        return str(self)


class Dictionary_Comprehension(Expression):
    """Used for supporting dictionary comprehension."""

    def __init__(self, parser_node: LRStackNode, key: Expression, value: Expression, variables: list[Variable_Expression], iter_exp: Expression,
                 comp_cond: Expression | None = None) -> None:
        """Initialize the Dictionary_Comprehension.

        Args:
            parser_node (LRStackNode): The parser node from the parse tree.
            key (Expression): Key expression.
            value (Expression): Value expression.
            variables (list[Variable_Expression]): Variables to parse from iterable.
            iter_exp (Expression): The iterable to parse over.
            comp_cond (Expression | None, optional): Conditions to evaluate for comprehension.
        """
        super().__init__(parser_node)
        self._spacer: None | str | Expression = None
        self._comp_cond: Expression | None = comp_cond
        self._key: Expression = key
        self._value: Expression = value
        self._iter_exp: Expression = iter_exp
        self._vars: list[Variable_Expression] = variables
        if len(self._vars) == 1:
            self._var_name: str | None = self._vars[0].variable_name
        else:
            self._var_name: str | None = None

    def evaluate(self, context: Knit_Script_Context) -> dict[Any, Any]:
        """Evaluate the expression.

        Args:
            context (Knit_Script_Context): The current context of the knit_script_interpreter.

        Returns:
            dict[Any, Any]: Result of dictionary comprehension.
        """
        iterable = self._iter_exp.evaluate(context)
        assert isinstance(iterable, Iterable), f'Cannot iterate over non-iterable value {iterable}'
        if self._spacer is not None:
            assert isinstance(iterable, list)
            if isinstance(self._spacer, str):
                if self._spacer == "even":
                    iterable = [val for i, val in enumerate(iterable) if i % 2 == 0]
                elif self._spacer == "odd":
                    iterable = [val for i, val in enumerate(iterable) if i % 2 == 1]
                else:  # "other"
                    iterable = iterable[::2]
            else:
                spacer = int(self._spacer.evaluate(context))
                iterable = iterable[::spacer]
        context.enter_sub_scope()  # create new scope that holds iterator variable
        values = {}
        for var in iterable:
            if self._var_name is not None:
                context.variable_scope[self._var_name] = var  # update iterator variable in scope
            else:  # multiple vars to unpack
                iterated_var = [*var]
                assert len(iterated_var) == len(self._vars), "Unpacked values do not match variables provided"
                for var_name, var_val in zip(self._vars, iterated_var):
                    context.variable_scope[var_name.variable_name] = var_val
            if self._comp_cond is None:
                condition_result = True
            else:
                condition_result = bool(self._comp_cond.evaluate(context))
            if condition_result:
                values[self._key.evaluate(context)] = self._value.evaluate(context)
        context.exit_current_scope()  # exit scope, removing access to iterator variable
        return values

    def __str__(self) -> str:
        spacer = ""
        if self._spacer is not None:
            spacer = f" every {self._spacer}"
        comp = ""
        if self._comp_cond is not None:
            comp = f" if {self._comp_cond}"
        return "{" + f"{self._key}:{self._value} for{spacer} {self._vars} in {self._iter_exp}{comp}" + "}"

    def __repr__(self) -> str:
        return str(self)
