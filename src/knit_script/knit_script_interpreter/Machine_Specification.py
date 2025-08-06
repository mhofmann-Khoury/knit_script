"""Module containing enumerations of common machine value terms.

This module provides enumerations and utilities for representing knitting machine specifications and bed positions.
It defines the Machine_Bed_Position enumeration which represents different needle bed positions on knitting machines,
along with utility methods for working with bed positions and determining bed characteristics.
"""

from __future__ import annotations

from enum import Enum


class Machine_Bed_Position(Enum):
    """Enumeration of positions on needle beds.

    The Machine_Bed_Position enumeration defines the different types of needle bed positions available on knitting machines.
    It distinguishes between front and back beds, as well as standard needle beds and slider beds, providing a comprehensive representation of needle positioning options.

    This enumeration includes utility methods for determining bed characteristics such as whether a position is on the front bed or represents a slider bed,
     making it easier to work with needle positioning logic throughout the knit script system.
    """
    Front = "front"
    Front_Slider = "front_slider"
    Back = "back"
    Back_Slider = "back_slider"

    @property
    def is_front(self) -> bool:
        """Check if this is a front bed position.

        Returns:
            bool: True if this represents a front bed position (either standard front bed or front slider bed).
        """
        return self is Machine_Bed_Position.Front or self is Machine_Bed_Position.Front_Slider

    @property
    def is_slider(self) -> bool:
        """Check if this represents a slider bed.

        Returns:
            bool: True if this represents a slider bed position (either front slider or back slider).
        """
        return self is Machine_Bed_Position.Front_Slider or self is Machine_Bed_Position.Back_Slider

    @staticmethod
    def get_bed(is_front: bool, is_slider: bool = False) -> Machine_Bed_Position:
        """Get the corresponding bed position from criteria.

        Args:
            is_front (bool): Whether the bed is on the front of the machine.
            is_slider (bool, optional): Whether the bed is a slider bed. Defaults to False.

        Returns:
            Machine_Bed_Position: The corresponding bed position based on the specified criteria.
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
