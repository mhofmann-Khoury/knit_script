"""Used to access attributes from instances in code"""
from typing import Any

from interpreter.expressions.expressions import Expression
from interpreter.expressions.variables import Variable_Expression
from interpreter.expressions.function_expressions import Function_Call
from interpreter.expressions.needle_set_expression import Needle_Set_Expression, Needle_Sets
from interpreter.parser.knit_script_context import Knit_Script_Context
from interpreter.statements.function_dec_statement import Function_Signature
from knitting_machine.Machine_State import Machine_State
from knitting_machine.machine_components.Sheet_Needle import Sheet_Identifier
from knitting_machine.machine_components.needles import Needle


class Attribute_Accessor_Expression(Expression):
    """
        Accesses attributes of expression either from knitscript or underlying python
    """

    def __init__(self, parent_expression: Expression,
                 attribute: Expression):
        """
        instantiate
        :param parent_expression: the expression to access and attribute from
        :param attribute: the attribute of the parent expression
        """
        super().__init__()
        self._attribute = attribute
        self._parent_expression = parent_expression

    def __str__(self):
        return f"{self._parent_expression}.{self._attribute}"

    def __repr__(self):
        return str(self)

    def evaluate(self, context: Knit_Script_Context) -> Any:
        """
        Evaluate the expression
        :param context: The current context of the interpreter
        :return: accessed attribute of parent expression
        """
        parent = self._parent_expression.evaluate(context)
        if isinstance(self._attribute, Variable_Expression):  # variable name, access directly from parent instance
            attr = getattr(parent, self._attribute.variable_name)
            if isinstance(attr, Expression):
                return attr.evaluate(context)
            else:
                return attr
        elif isinstance(self._attribute, Needle_Set_Expression):  # get needle set from machine or sheet specification
            kp_set = Needle_Sets[self._attribute.set_str]
            if isinstance(parent, Machine_State):
                if kp_set is Needle_Sets.Front_Needles:
                    return context.machine_state.front_needles(on_sheet=False)
                elif kp_set is Needle_Sets.Back_Needles:
                    return context.machine_state.back_needles(on_sheet=False)
                elif kp_set is Needle_Sets.Front_Sliders:
                    return context.machine_state.front_sliders(on_sheet=False)
                elif kp_set is Needle_Sets.Back_Sliders:
                    return context.machine_state.back_sliders(on_sheet=False)
                elif kp_set is Needle_Sets.Front_Loops:
                    return context.machine_state.front_loops(on_sheet=False)
                elif kp_set is Needle_Sets.Back_Loops:
                    return context.machine_state.back_loops(on_sheet=False)
                elif kp_set is Needle_Sets.Needles:
                    return context.machine_state.all_needles(on_sheet=False)
                elif kp_set is Needle_Sets.Front_Slider_Loops:
                    return context.machine_state.front_slider_loops(on_sheet=False)
                elif kp_set is Needle_Sets.Back_Slider_Loops:
                    return context.machine_state.back_slider_loops(on_sheet=False)
                elif kp_set is Needle_Sets.Sliders:
                    return context.machine_state.all_sliders(on_sheet=False)
                elif kp_set is Needle_Sets.Loops:
                    return context.machine_state.all_loops(on_sheet=False)
                elif kp_set is Needle_Sets.Slider_Loops:
                    return context.machine_state.all_slider_loops(on_sheet=False)
            elif isinstance(parent, Sheet_Identifier):
                if kp_set is Needle_Sets.Front_Needles:
                    return context.machine_state.front_needles(sheet=parent.sheet, gauge=parent.gauge)
                elif kp_set is Needle_Sets.Back_Needles:
                    return context.machine_state.back_needles(sheet=parent.sheet, gauge=parent.gauge)
                elif kp_set is Needle_Sets.Front_Sliders:
                    return context.machine_state.front_sliders(sheet=parent.sheet, gauge=parent.gauge)
                elif kp_set is Needle_Sets.Back_Sliders:
                    return context.machine_state.back_sliders(sheet=parent.sheet, gauge=parent.gauge)
                elif kp_set is Needle_Sets.Front_Loops:
                    return context.machine_state.front_loops(sheet=parent.sheet, gauge=parent.gauge)
                elif kp_set is Needle_Sets.Back_Loops:
                    return context.machine_state.back_loops(sheet=parent.sheet, gauge=parent.gauge)
                elif kp_set is Needle_Sets.Needles:
                    return context.machine_state.all_needles(sheet=parent.sheet, gauge=parent.gauge)
                elif kp_set is Needle_Sets.Front_Slider_Loops:
                    return context.machine_state.front_slider_loops(sheet=parent.sheet, gauge=parent.gauge)
                elif kp_set is Needle_Sets.Back_Slider_Loops:
                    return context.machine_state.back_slider_loops(sheet=parent.sheet, gauge=parent.gauge)
                elif kp_set is Needle_Sets.Sliders:
                    return context.machine_state.all_sliders(sheet=parent.sheet, gauge=parent.gauge)
                elif kp_set is Needle_Sets.Loops:
                    return context.machine_state.all_loops(sheet=parent.sheet, gauge=parent.gauge)
                elif kp_set is Needle_Sets.Slider_Loops:
                    return context.machine_state.all_slider_loops(sheet=parent.sheet, gauge=parent.gauge)
            else:
                assert False, f"KP error: Cannot access needle set {kp_set} from {parent}"
        else:
            attribute = self._attribute.evaluate(context)
            if isinstance(parent, Machine_State):
                assert isinstance(attribute, Needle), f"Cannot access {attribute} from machine state"
                return parent[attribute]
            elif isinstance(parent, Sheet_Identifier):
                assert isinstance(attribute, Needle), f"Cannot access {attribute} from sheet {parent}"
                sheet_needle = parent.get_needle(attribute)
                return context.machine_state[sheet_needle]
            else:
                assert False, f"Cannot access {self._attribute} from {parent}"


class Indexing_Expression(Expression):
    """
        Used to index into values
    """

    def __init__(self, expression: Expression, index: Expression):
        """
        :param expression: the expression to index to
        :param index: the value of the index
        """
        super().__init__()
        self._expression = expression
        self._index = index

    def __str__(self):
        return f"{self._expression}[{self._index}]"

    def __repr__(self):
        return str(self)

    def evaluate(self, context: Knit_Script_Context) -> Any:
        """
        Evaluate the expression
        :param context: The current context of the interpreter
        :return: Indexed value of expression, indexing errors come from python directly
        """
        val = self._expression.evaluate(context)
        index = self._index.evaluate(context)
        return val[index]


class Method_Call(Expression):
    """
        Used to call methods of expression, supports functions from knitscript and python
    """

    def __init__(self, parent_expression: Expression,
                 method_call: Function_Call):
        """
        instantiate
        :param parent_expression: the expression to call a method from
        :param method_call: the method to call of the expression
        """
        super().__init__()
        self._parent_expression = parent_expression
        self._method_call = method_call

    def __str__(self):
        return f"{self._parent_expression}.{self._method_call}"

    def __repr__(self):
        return str(self)

    def evaluate(self, context: Knit_Script_Context) -> Any:
        """
        Evaluate the expression
        :param context: The current context of the interpreter
        :return: Result of calling expression method
        """
        parent = self._parent_expression.evaluate(context)
        method_name = self._method_call.func_name.variable_name
        attribute = getattr(parent, method_name)
        if isinstance(attribute, Function_Signature):
            return_value = attribute.execute(context,
                                             self._method_call.args,
                                             self._method_call.kwargs)
            return return_value
        else:  # attempt to treat method as python class method
            args = [arg.evaluate(context) for arg in self._method_call.args]
            kwargs = {kwarg.variable_name: kwarg.value(context) for kwarg in self._method_call.kwargs}
            return attribute(*args, **kwargs)
