"""Expressions for accessing standard needle sets from the machine state"""

from enum import Enum
from typing import List, Optional, Dict, Union

from knit_script.knit_script_interpreter.expressions.expressions import Expression
from knit_script.knit_script_interpreter.knit_script_context import Knit_Script_Context
from knit_script.knitting_machine.machine_components.needles import Needle


class Needle_Sets(Enum):
    """Naming of Needles sets on Machine State"""
    Last_Pass = "Last_Pass"
    Needles = "Needles"
    Front_Needles = "Front_Needles"
    Back_Needles = "Back_Needles"
    Sliders = "Sliders"
    Front_Sliders = "Front_Sliders"
    Back_Sliders = "Back_Sliders"
    Loops = "Loops"
    Front_Loops = "Front_Loops"
    Back_Loops = "Back_Loops"
    Slider_Loops = "Slider_Loops"
    Front_Slider_Loops = "Front_Slider_Loops"
    Back_Slider_Loops = "Back_Slider_Loops"


class Needle_Set_Expression(Expression):
    """Evaluates keywords to sets of needles on the machine"""

    def __init__(self, parser_node, set_str: str):
        """
        Instantiate
        :param parser_node:
        :param set_str: the string to identify the set
        """
        super().__init__(parser_node)
        self._set_str: str = set_str

    @property
    def set_str(self) -> str:
        """
        :return: string for the set of needles to collect
        """
        return self._set_str

    def evaluate(self, context: Knit_Script_Context) -> Union[List[Needle], Dict[Needle, Optional[Needle]]]:
        """
        Evaluate the expression
        :param context: The current context of the knit_script_interpreter
        :return: Specified set of needles
        """
        kp_set = Needle_Sets[self._set_str]
        if kp_set is Needle_Sets.Front_Needles:
            return context.machine_state.front_needles()
        elif kp_set is Needle_Sets.Back_Needles:
            return context.machine_state.back_needles()
        elif kp_set is Needle_Sets.Front_Sliders:
            return context.machine_state.front_sliders()
        elif kp_set is Needle_Sets.Back_Sliders:
            return context.machine_state.back_sliders()
        elif kp_set is Needle_Sets.Front_Loops:
            return context.machine_state.front_loops()
        elif kp_set is Needle_Sets.Back_Loops:
            return context.machine_state.back_loops()
        elif kp_set is Needle_Sets.Needles:
            return context.machine_state.all_needles()
        elif kp_set is Needle_Sets.Front_Slider_Loops:
            return context.machine_state.front_slider_loops()
        elif kp_set is Needle_Sets.Back_Slider_Loops:
            return context.machine_state.back_slider_loops()
        elif kp_set is Needle_Sets.Sliders:
            return context.machine_state.all_sliders()
        elif kp_set is Needle_Sets.Loops:
            return context.machine_state.all_loops()
        elif kp_set is Needle_Sets.Slider_Loops:
            return context.machine_state.all_slider_loops()
        elif kp_set is Needle_Sets.Last_Pass:
            return context.last_carriage_pass_result

    def __str__(self):
        return self._set_str

    def __repr__(self):
        return str(self)
