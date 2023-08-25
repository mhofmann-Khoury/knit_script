"""Used to access attributes from instances in code"""
from typing import Any, Union

from knit_script.knit_script_interpreter.expressions.expressions import Expression
from knit_script.knit_script_interpreter.expressions.function_expressions import Function_Call
from knit_script.knit_script_interpreter.expressions.needle_set_expression import Needle_Set_Expression, Needle_Sets
from knit_script.knit_script_interpreter.expressions.variables import Variable_Expression
from knit_script.knit_script_interpreter.knit_script_context import Knit_Script_Context
from knit_script.knit_script_interpreter.statements.function_dec_statement import Function_Signature
from knit_script.knitting_machine.Machine_State import Machine_State
from knit_script.knitting_machine.machine_components.Sheet_Needle import Sheet_Identifier, Sheet_Needle
from knit_script.knitting_machine.machine_components.needles import Needle


class Attribute_Accessor_Expression(Expression):
    """
        Accesses attributes of expression either from knit-script or underlying python
    """

    def __init__(self, parser_node, parent_path: Union[list[Expression], Expression], attribute: Expression):
        """
        Instantiate
        :param parser_node:
        :param parent_path: The expression to access and attribute from
        :param attribute: the attribute of the parent expression. May produce more accessors
        """
        super().__init__(parser_node)
        self.is_method_call = False
        if isinstance(parent_path, list):
            self.parent: list[Expression] = parent_path
        else:
            self.parent: list[Expression] = [parent_path]
        if isinstance(attribute, Attribute_Accessor_Expression):
            self.attribute: Expression = attribute.attribute
            self.parent.extend(attribute.parent)
        else:
            self.attribute: Expression = attribute
        if isinstance(self.attribute, Function_Call):
            self.is_method_call = True

    def _parent_expression(self) -> Expression:
        if len(self.parent) == 1:
            return self.parent[0]
        else:
            return Attribute_Accessor_Expression(self.parser_node, self.parent[:-1], self.parent[1])

    def parent_path(self):
        """
        :return: path to parent value
        """
        parent_source_str = ""
        for p in self.parent:
            parent_source_str += f"{p}."
        parent_source_str = parent_source_str[0:-1]  # drop extra "."
        return parent_source_str

    def _evaluate_parent(self, context: Knit_Script_Context) -> Any:
        if len(self.parent) == 1:  # one parent expression
            parent_source: Expression = self.parent[0]
            parent = parent_source.evaluate(context)
        else:  # recursively process parent path
            parent_accessor = Attribute_Accessor_Expression(self.parser_node, self.parent[:-1], self.parent[-1])
            parent = parent_accessor.evaluate(context)
        return parent

    def __str__(self):
        return f"{self.parent_path()}.{self.attribute}"

    def __repr__(self):
        return str(self)

    def evaluate(self, context: Knit_Script_Context) -> Any:
        """
        Evaluate the expression
        :param context: The current context of the knit_script_interpreter
        :return: accessed attribute of parent expression
        """
        parent = self._evaluate_parent(context)
        if isinstance(self.attribute, Variable_Expression):  # variable name, access directly from parent instance
            attr = getattr(parent, self.attribute.variable_name)
            if isinstance(attr, Expression):
                return attr.evaluate(context)
            else:
                return attr
        elif isinstance(self.attribute, Needle_Set_Expression):  # get needle set from machine or sheet specification
            kp_set = Needle_Sets[self.attribute.set_str]
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
        elif isinstance(self.attribute, Function_Call):
            method_name = self.attribute.func_name.variable_name
            attribute = getattr(parent, method_name)
            if isinstance(attribute, Function_Signature):
                return_value = attribute.execute(context,
                                                 self.attribute.args,
                                                 self.attribute.kwargs)
                return return_value
            else:  # attempt to treat method as python class method
                args = [arg.evaluate(context) for arg in self.attribute.args]
                kwargs = {kwarg.variable_name: kwarg.value(context) for kwarg in self.attribute.kwargs}
                return attribute(*args, **kwargs)
        else:
            attribute = self.attribute.evaluate(context)
            if isinstance(attribute, Needle):
                if isinstance(parent, Machine_State):
                    if isinstance(attribute, Sheet_Needle):  # assume actual position instead of sheet conversion
                        return parent[Needle(attribute.is_front, attribute.sheet_pos)]
                    else:
                        return parent[attribute]
                elif isinstance(parent, Sheet_Identifier):
                    sheet_needle = parent.get_needle(attribute)
                    return context.machine_state[sheet_needle]
            else:
                return getattr(parent, attribute)
