"""Module containing enumerations of common machine value terms."""

from __future__ import annotations

from enum import Enum


class Machine_Bed_Position(Enum):
    """Enumeration of positions on needle beds."""
    Front = "front"
    Front_Slider = "front_slider"
    Back = "back"
    Back_Slider = "back_slider"

    @property
    def is_front(self) -> bool:
        """Check if this is a front bed position.

        Returns:
            bool: True if front bed (slider or standard bed).
        """
        return self is Machine_Bed_Position.Front or self is Machine_Bed_Position.Front_Slider

    @property
    def is_slider(self) -> bool:
        """Check if this represents a slider bed.

        Returns:
            bool: True if represents a slider bed.
        """
        return self is Machine_Bed_Position.Front_Slider or self is Machine_Bed_Position.Back_Slider

    @staticmethod
    def get_bed(is_front: bool, is_slider: bool = False) -> Machine_Bed_Position:
        """Get the corresponding bed from criteria.

        Args:
            is_front (bool): Whether the bed is on the front.
            is_slider (bool, optional): Whether the bed is a slider bed. Defaults to False.

        Returns:
            Machine_Bed_Position: Corresponding bed from criteria.
        """
        if is_front:
            if is_slider:
                return Machine_Bed_Position.Front_Slider
            else:
                return Machine_Bed_Position.Front
        else:
            if is_slider:
                return Machine_Bed_Position.Back_Slider
            else:
                return Machine_Bed_Position.Back
