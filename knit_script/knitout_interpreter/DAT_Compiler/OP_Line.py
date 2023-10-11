from enum import Enum


class OP_Line(Enum):
    Direction_Line_Left = -1
    Racking_Pitch = -2
    Racking_Offset = -3
    Racking_Left_Right = -4
    Knit_Speed = -5
    Xfer_Speed = -6
    L7 = -7  # todo identify
    L8 = -8  # todo identify
    IDSCS = -9
    Knit_Roller_Speed = -10
    Xfer_Roller_Speed = -11
    L12 = -12  # todo identify
    L13 = -13  # todo identify
    Elastic_Advance = -14
    L15 = -15
    L16 = -16
    L17 = -17
    L18 = -18
    L19 = -19
    L20 = -20
    Direction_Line_Right = 1
    R2 = 2
    Carrier_Combination = 3
    R4 = 4
    Knit_Cancel = 5
    Stitch_Number = 6
    Drop_Failure = 7
    Yarn_IN_Out = 8
    Ignore_Link_Process = 9
    Yarn_Holding_Hook = 10
    Fabric_Presser = 11
    R12 = 12
    Stitch_Range = 13
    R14 = 14
    Yarn_Inserting_Hook = 15
    R16 = 16
    R17 = 17
    R18 = 18
    R19 = 19
    R20 = 20
    Pause = -100  # todo: identify Pause line

    def __hash__(self):
        return self.value

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def __int__(self):
        return self.value

    @staticmethod
    def get_enum(value):
        """
        :param value: integer of the operation line
        :return: the operation Enumerator for that op code
        """
        return getattr(OP_Line, value)
