from enum import Enum


class Knitting_Operation(Enum):
    """Enumeration of knitting operation to DAT option number"""
    Knit_Front = 51
    Knit_Back = 52
    Knit_Front_Back = 3
    Drop_Front = 51  # todo check
    Drop_Back = 52
    Drop_Front_Back = 3
    Miss = 16
    Miss_Front = 216
    Tuck_Front = 11
    Tuck_Back = 12
    Tuck_Front_Back = -1  # todo
    Xfer_Front = -1  # todo
    Xfer_Back = -1  # todo
    Split_Front = -1  # todo
    Split_Back = -1  # todo
    Boundary = 13

    def __hash__(self):
        return self.value

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def __int__(self):
        return self.value

    @property
    def opposite(self):
        """
        :return: Opposite knitting operation or None if cannot be combined in all needle knitting
        """
        if self is Knitting_Operation.Knit_Front:
            return Knitting_Operation.Knit_Back
        elif self is Knitting_Operation.Knit_Back:
            return Knitting_Operation.Knit_Front
        elif self is Knitting_Operation.Tuck_Front:
            return Knitting_Operation.Tuck_Back
        elif self is Knitting_Operation.Tuck_Back:
            return Knitting_Operation.Tuck_Front
        elif self is Knitting_Operation.Drop_Front:
            return Knitting_Operation.Drop_Back
        elif self is Knitting_Operation.Drop_Back:
            return Knitting_Operation.Drop_Front
        return None

    @staticmethod
    def get_enum(value):
        """
        :param value: integer of the operation line
        :return: the operation Enumerator for that op code
        """
        return getattr(Knitting_Operation, value)

    def all_needle__conversion(self, other_operation):
        """
        :param other_operation: other operation to do in all-needle knitting.
        :return: all needle operation or None if all-needle not compatible
        """
        opposite_op = self.opposite
        if opposite_op is not other_operation:
            return None
        if self in [Knitting_Operation.Knit_Front, Knitting_Operation.Knit_Back]:
            return Knitting_Operation.Knit_Front_Back
        elif self in [Knitting_Operation.Tuck_Back, Knitting_Operation.Tuck_Front]:
            return Knitting_Operation.Tuck_Front_Back
        elif self in [Knitting_Operation.Drop_Front, Knitting_Operation.Drop_Back]:
            return Knitting_Operation.Drop_Front_Back
