"""Module containing enumerations of common machine value terms."""
from enum import Enum


class Xfer_Direction(Enum):
    """Enumerator for needle positioning"""
    Left = "Left"
    Right = "Right"

    def __str__(self) -> str:
        return self.name

    def __repr__(self):
        return str(self)

    def __hash__(self):
        return hash(str(self))


class Machine_Bed_Position(Enum):
    """
        Enumeration of positions on needle beds
    """
    Front = "front"
    Front_Slider = "front_slider"
    Back = "back"
    Back_Slider = "back_slider"

    @property
    def is_front(self) -> bool:
        """
        :return: True if front bed (slider or standard bed)
        """
        return self is Machine_Bed_Position.Front or self is Machine_Bed_Position.Front_Slider

    @property
    def is_slider(self) -> bool:
        """
        :return: True if represents a slider bed
        """
        return self is Machine_Bed_Position.Front_Slider or self is Machine_Bed_Position.Back_Slider

    @staticmethod
    def get_bed(is_front: bool, is_slider: bool = False):
        """
        :param is_front:
        :param is_slider:
        :return: corresponding bed from criteria
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
