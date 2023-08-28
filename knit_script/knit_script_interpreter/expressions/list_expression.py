"""Used for container structures (tuples, lists, dicts, comprehensions)"""

from typing import List, Optional, Tuple, Iterable, Any

from knit_script.Knit_Errors import Knit_Script_Error
from knit_script.knit_script_interpreter.expressions.expressions import Expression
from knit_script.knit_script_interpreter.expressions.variables import Variable_Expression
from knit_script.knit_script_interpreter.knit_script_context import Knit_Script_Context
from knit_script.knitting_machine.Machine_State import Machine_State
from knit_script.knitting_machine.machine_components.needles import Needle


class Unpack(Expression):
    """
        Used to unpack values into a tuple with * function
    """

    def __init__(self, parser_node, exp: Expression):
        """
        Instantiate
        :param parser_node:
        :param exp: expression to unpack
        """
        super().__init__(parser_node)
        self._exp = exp

    def evaluate(self, context: Knit_Script_Context) -> tuple:
        """
        Evaluate the expression
        :param context: The current context of the knit_script_interpreter
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

    def __init__(self, parser_node, expressions: List[Expression]):
        """
        Instantiate
        :param parser_node:
        :param expressions: expressions to fill list with
        """
        super().__init__(parser_node)
        self.expressions: List[Expression] = expressions

    def evaluate(self, context: Knit_Script_Context) -> list:
        """
        Evaluate the expression
        :param context: The current context of the knit_script_interpreter
        :return: List of expression evaluations at current context
        """
        values = []
        for exp in self.expressions:
            if isinstance(exp, Unpack):
                values.extend(exp.evaluate(context))
            else:
                values.append(exp.evaluate(context))
        return values

    def __str__(self):
        values = ""
        for exp in self.expressions:
            values += f"{exp}, "
        values = values[:-2]
        return f"[{values}]"

    def __repr__(self):
        return str(self)


class Sliced_List(Expression):
    """
        Slices a list using standard python syntax
    """

    def __init__(self, parser_node, iter_exp: Expression, start: Optional[Expression] = None, start_to_end: bool = False, end: Optional[Expression] = None, end_to_spacer: bool = False,
                 spacer: Optional[Expression] = None, is_index: bool = False):
        """
        Instantiate
        :param parser_node:
        :param iter_exp: iterable to slice
        :param start: start of slice, inclusive, defaults to 0
        :param end: end of slice, exclusive, defaults to last element
        :param spacer: spacer of slice, defaults to 1

        Parameters
        ----------
        end_to_spacer
        start_to_end
        """
        super().__init__(parser_node)
        if is_index:
            assert end is None and spacer is None
        self._is_index = is_index
        self._end_to_spacer = end_to_spacer
        self._start_to_end = start_to_end
        self._spacer = spacer
        self._end = end
        self._start = start
        self._iter_exp = iter_exp

    def evaluate(self, context: Knit_Script_Context) -> Any:
        """
        Evaluate the expression
        :param context: The current context of the knit_script_interpreter
        :return: The list of values in the given slice or (if no colons given in slice) return the indexed value
        """
        iterable = self._iter_exp.evaluate(context)
        if isinstance(iterable, Machine_State):
            if self._is_index:
                start = self._start.evaluate(context)
                assert isinstance(start, Needle), f"Machine_State can only be index by needles not {start}"
                return context.machine_state[start]
            else:
                raise Knit_Script_Error(f"Machine_State is not iterable and cannot be iterated over [{self._start}:{self._end}:{self._spacer}]")
        assert isinstance(iterable, Iterable)
        iterable = [i for i in iterable]
        if self._is_index:
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

    def _is_slice(self):
        return self._start_to_end or self._end_to_spacer

    def __str__(self):
        if self._is_slice():
            return f"{self._iter_exp}[{self._start}:{self._end}:{self._spacer}]"
        else:
            return f"{self._iter_exp}[{self._start}]"

    def __repr__(self):
        return str(self)


class List_Comp(Expression):
    """
        Runs a list comprehension over an iterator
    """

    def __init__(self, parser_node, fill_exp: Expression, variables: List[Variable_Expression], iter_exp: Expression, comp_cond: Optional[Expression]):
        """
        Instantiate
        :param parser_node:
        :param fill_exp: Expression that fills the list
        :param variables: variables to fill from iterable
        :param iter_exp: the iterable to pass over
        :param comp_cond: condition to evaluate for adding a value
        """
        super().__init__(parser_node)
        self._comp_cond: Optional[Expression] = comp_cond
        self._spacer= None
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
        :param context: The current context of the knit_script_interpreter
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

    def __str__(self):
        spacer = ""
        if self._spacer is not None:
            spacer = f" every {self._spacer}"
        comp = ""
        if self._comp_cond is not None:
            comp = f" if {self._comp_cond}"
        return f"[{self._fill_exp} for{spacer} {self._vars} in {self._iter_exp}{comp}]"

    def __repr__(self):
        return str(self)


class Knit_Script_Dictionary(Expression):
    """
        Used to process dictionary structures
    """

    def __init__(self, parser_node, kwargs: List[Tuple[Expression, Expression]]):
        """
        Instantiate
        :param parser_node:
        :param kwargs: the key value pairs of a dictionary
        """
        super().__init__(parser_node)
        self._kwargs: List[Tuple[Expression, Expression]] = kwargs

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

    def __init__(self, parser_node, key: Expression, value: Expression, variables: List[Variable_Expression], iter_exp: Expression,
                 comp_cond: Optional[Expression] = None):
        """
        Instantiate
        :param parser_node:
        :param key: key expression
        :param value: value expression
        :param variables: variables to parse from iterable
        :param iter_exp: the iterable to parse over
        todo add conditions to comprehension
        """
        super().__init__(parser_node)
        self._spacer = None
        self._comp_cond = comp_cond
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

    def __str__(self):
        spacer = ""
        if self._spacer is not None:
            spacer = f" every {self._spacer}"
        comp = ""
        if self._comp_cond is not None:
            comp = f" if {self._comp_cond}"
        return "{" + f"{self._key}:{self._value} for{spacer} {self._vars} in {self._iter_exp}{comp}" + "}"

    def __repr__(self):
        return str(self)
