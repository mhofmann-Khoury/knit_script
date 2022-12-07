"""Used for container structures (tuples, lists, dicts, comprehensions)"""

from typing import List, Optional, Union, Tuple, Iterable

from interpreter.expressions.expressions import Expression
from interpreter.expressions.variables import Variable_Expression
from interpreter.parser.knit_pass_context import Knit_Script_Context


class Unpack(Expression):
    """
        Used to unpack values into a tuple with * function
    """

    def __init__(self, exp: Expression):
        """
        Instantiate
        :param exp: expression to unpack
        """
        super().__init__()
        self._exp = exp

    def evaluate(self, context: Knit_Script_Context) -> tuple:
        """
        Evaluate the expression
        :param context: The current context of the interpreter
        :return: tuple with unpacked values from expression
        """
        return tuple([*self._exp.evaluate(context)])

    def __str__(self):
        return f"(*{self._exp})"

    def __repr__(self):
        return str(self)


class Knit_Script_List(Expression):
    """
        Evaluates to list of expression values. Lists are not typed following python style conventions
    """

    def __init__(self, expressions: List[Expression]):
        """
        Instantiate
        :param expressions: expressions to fill list with
        """
        super().__init__()
        self._expressions: List[Expression] = expressions

    def evaluate(self, context: Knit_Script_Context) -> list:
        """
        Evaluate the expression
        :param context: The current context of the interpreter
        :return: List of expression evaluations at current context
        """
        values = []
        for exp in self._expressions:
            if isinstance(exp, Unpack):
                values.extend(exp.evaluate(context))
            else:
                values.append(exp.evaluate(context))
        return values

    def __str__(self):
        values = ""
        for exp in self._expressions:
            values += f"{exp}, "
        values = values[:-2]
        return f"[{values}]"

    def __repr__(self):
        return str(self)


class Sliced_List(Expression):
    """
        Slices a list using standard python syntax
    """
    def __init__(self, iter_exp: Expression, start: Optional[Expression],
                 end: Optional[Expression], spacer: Optional[Expression]):
        """
        Instantiate
        :param iter_exp: iterable to slice
        :param start: start of slice, inclusive, defaults to 0
        :param end: end of slice, exclusive, defaults to last element
        :param spacer: spacer of slice, defaults to 1
        """
        super().__init__()
        self._spacer = spacer
        self._end = end
        self._start = start
        self._iter_exp = iter_exp

    def evaluate(self, context: Knit_Script_Context) -> list:
        """
        Evaluate the expression
        :param context: The current context of the interpreter
        :return: The list of values in the given slice
        """
        iterable = self._iter_exp.evaluate(context)
        assert isinstance(iterable, Iterable)
        iterable = [i for i in iterable]
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

    def __str__(self):
        return f"{self._iter_exp}[{self._start}:{self._end}:{self._spacer}]"

    def __repr__(self):
        return str(self)


class List_Comp(Expression):
    """
        Runs a list comprehension over an iterator
    """

    def __init__(self, fill_exp: Expression, spacer: Optional[Union[str, Expression]],
                 variables: List[Variable_Expression], iter_exp: Expression, comp_cond: Optional[Expression]):
        """
        Instantiate
        :param fill_exp: Expression that fills the list
        :param spacer: the spacer value across the variables
        :param variables: variables to fill from iterable
        :param iter_exp: the iterable to pass over
        :param comp_cond: condition to evaluate for adding a value
        """
        super().__init__()
        self._comp_cond: Optional[Expression] = comp_cond
        self._spacer: Optional[Union[str, Expression]] = spacer
        self._fill_exp: Expression = fill_exp
        self._vars: List[Variable_Expression] = variables
        if len(self._vars) == 1:
            self._var_name: Optional[str] = self._vars[0].variable_name
        else:
            self._var_name: Optional[str] = None
        self._iter_exp = iter_exp

    def evaluate(self, context: Knit_Script_Context) -> list:
        """
        Evaluate the expression
        :param context: The current context of the interpreter
        :return: result of list comprehension inside list
        """
        iterable = self._iter_exp.evaluate(context)
        assert isinstance(iterable, Iterable), f'Cannot iterate over non-iterable value {iterable}'
        if self._spacer is not None:
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
                assert len(iterated_var) == self._vars, "Unpacked values do not match variables provided"
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

    def __str__(self):
        return f"[{self._fill_exp} for {self._vars} in {self._iter_exp}]"

    def __repr__(self):
        return str(self)


class Knit_Script_Dictionary(Expression):
    """
        Used to process dictionary structures
    """

    def __init__(self, kwargs: List[Tuple[Expression, Expression]]):
        """
        Instantiate
        :param kwargs: the key value pairs of a dictionary
        """
        super().__init__()
        self._kwargs: List[Tuple[Expression, Expression]]= kwargs

    def evaluate(self, context: Knit_Script_Context) -> dict:
        """
        :param context:
        :return: dictionary with keys assigned to arguments
        """
        return {kwarg[0].evaluate(context): kwarg[1].evaluate(context) for kwarg in self._kwargs}

    def __str__(self):
        values = ""
        for assign in self._kwargs:
            values += f"{assign[0]}:{assign[1]}, "
        values = values[:-2]
        return "{" + values + "}"

    def __repr__(self):
        return str(self)


class Dictionary_Comprehension(Expression):
    """
        Used for supporting dictionary comprehension
    """

    def __init__(self, key: Expression, value: Expression, variables: List[Variable_Expression], iter_exp: Expression):
        """
        Instantiate
        :param key: key expression
        :param value: value expression
        :param variables: variables to parse from iterable
        :param iter_exp: the iterable to parse over
        todo add conditions to comprehension
        """
        super().__init__()
        self._key: Expression = key
        self._value: Expression = value
        self._iter_exp: Expression = iter_exp
        self._vars: List[Variable_Expression] = variables
        if len(self._vars) == 1:
            self._var_name: Optional[str] = self._vars[0].variable_name
        else:
            self._var_name: Optional[str] = None

    def evaluate(self, context: Knit_Script_Context) -> dict:
        """
        :param context:
        :return: result of list comprehension inside list
        """
        iterable = self._iter_exp.evaluate(context)
        assert isinstance(iterable, Iterable), f'Cannot iterate over non-iterable value {iterable}'
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
            values[self._key.evaluate(context)] = self._value.evaluate(context)
        context.exit_current_scope()  # exit scope, removing access to iterator variable
        return values

    def __str__(self):
        return "{" + f"{self._key}:{self._value} for {self._vars} in {self._iter_exp}" + "}"

    def __repr__(self):
        return str(self)

