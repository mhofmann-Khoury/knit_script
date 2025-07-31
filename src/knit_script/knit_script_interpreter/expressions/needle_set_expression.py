"""Expressions for accessing standard needle sets from the machine state"""

from __future__ import annotations
from enum import Enum
from typing import cast

from parglare.parser import LRStackNode
from virtual_knitting_machine.machine_components.needles.Needle import Needle
from virtual_knitting_machine.machine_components.needles.Slider_Needle import Slider_Needle

from knit_script.knit_script_interpreter.expressions.expressions import Expression
from knit_script.knit_script_interpreter.knit_script_context import Knit_Script_Context


class Needle_Sets(Enum):
    """Naming of Needles sets on Machine State."""
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
    """Evaluates keywords to sets of needles on the machine."""

    def __init__(self, parser_node: LRStackNode, set_str: str) -> None:
        """Initialize the Needle_Set_Expression.

        Args:
            parser_node (LRStackNode): The parser node from the parse tree.
            set_str (str): The string to identify the set.
        """
        super().__init__(parser_node)
        self._set_str: str = set_str

    @property
    def set_str(self) -> str:
        """Get the string for the set of needles to collect.

        Returns:
            str: String for the set of needles to collect.
        """
        return self._set_str

    def evaluate(self, context: Knit_Script_Context) -> list[Needle] | dict[Needle, Needle | None] | list[Slider_Needle]:
        """Evaluate the expression.

        Args:
            context (Knit_Script_Context): The current context of the knit_script_interpreter.

        Returns:
            list[Needle] | dict[Needle, Needle | None] | list[Slider_Needle]: Specified set of needles.
        """
        kp_set = Needle_Sets[self._set_str]
        if kp_set is Needle_Sets.Front_Needles:
            return cast(list[Needle], context.gauged_sheet_record.front_needles(context.sheet.sheet))
        elif kp_set is Needle_Sets.Back_Needles:
            return cast(list[Needle], context.gauged_sheet_record.back_needles(context.sheet.sheet))
        elif kp_set is Needle_Sets.Front_Sliders:
            return cast(list[Slider_Needle], context.gauged_sheet_record.front_sliders(context.sheet.sheet))
        elif kp_set is Needle_Sets.Back_Sliders:
            return cast(list[Slider_Needle], context.gauged_sheet_record.back_sliders(context.sheet.sheet))
        elif kp_set is Needle_Sets.Front_Loops:
            return cast(list[Needle], context.gauged_sheet_record.front_loops(context.sheet.sheet))
        elif kp_set is Needle_Sets.Back_Loops:
            return cast(list[Needle], context.gauged_sheet_record.back_loops(context.sheet.sheet))
        elif kp_set is Needle_Sets.Needles:
            return cast(list[Needle], context.gauged_sheet_record.all_needles(context.sheet.sheet))
        elif kp_set is Needle_Sets.Front_Slider_Loops:
            return cast(list[Slider_Needle], context.gauged_sheet_record.front_slider_loops(context.sheet.sheet))
        elif kp_set is Needle_Sets.Back_Slider_Loops:
            return cast(list[Slider_Needle], context.gauged_sheet_record.back_slider_loops(context.sheet.sheet))
        elif kp_set is Needle_Sets.Sliders:
            return cast(list[Needle], context.gauged_sheet_record.all_sliders(context.sheet.sheet))
        elif kp_set is Needle_Sets.Loops:
            return cast(list[Needle], context.gauged_sheet_record.all_loops(context.sheet.sheet))
        elif kp_set is Needle_Sets.Slider_Loops:
            return cast(list[Slider_Needle], context.gauged_sheet_record.all_slider_loops(context.sheet.sheet))
        elif kp_set is Needle_Sets.Last_Pass:
            return cast(list[Needle] | dict[Needle, Needle | None] | list[Slider_Needle], context.last_carriage_pass_result)

    def __str__(self) -> str:
        return self._set_str

    def __repr__(self) -> str:
        return str(self)
