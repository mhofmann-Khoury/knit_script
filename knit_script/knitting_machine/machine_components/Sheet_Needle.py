"""Constructs used to keep track of the position of sheets to needles"""
from knit_script.knitting_machine.machine_components.needles import Needle, Slider_Needle


class Sheet_Needle(Needle):
    """
        Used for managing needles at a layered gauging schema
    """

    def __init__(self, is_front: bool, sheet_pos: int, sheet: int, gauge: int):
        self._gauge: int = gauge
        self._sheet_pos: int = sheet_pos
        self._sheet: int = sheet
        super().__init__(is_front, Sheet_Needle.get_actual_pos(self.sheet_pos, self.sheet, self.gauge))

    @property
    def gauge(self) -> int:
        """
        :return: The gauge currently knitting in
        """
        return self._gauge

    @property
    def sheet_pos(self) -> int:
        """
        :return: The position of the needle with a sheet.
        """
        return self._sheet_pos

    @property
    def sheet(self) -> int:
        """
        :return: the position of the sheet in the gauge
        """
        return self._sheet

    @staticmethod
    def get_sheet_pos(actual_pos: int, gauge: int) -> int:
        """
        get the sheet position of a needle position at a given gauge
        :param actual_pos: the needle position on the bed
        :param gauge: the number of layers supported by the gauge
        :return: the position in the layer of a given needle position at a specific layering gauge
        """
        return int(actual_pos / gauge)

    @staticmethod
    def get_sheet(actual_pos: int, sheet_pos: int, gauge: int) -> int:
        """
        The sheet of a needle position, sheet position at a given gauge
        :param actual_pos: The needle position on the bed
        :param sheet_pos: the position in the layer
        :param gauge: the number of layers supported by the gauge
        :return: the layer of the needle given the gauging
        """
        return actual_pos - (sheet_pos * gauge)

    @staticmethod
    def get_actual_pos(sheet_pos: int, sheet: int, gauge: int) -> int:
        """
        Get the actual needle position given the components of a sheet needle
        :param sheet: the layer being used
        :param sheet_pos: the position in the layer
        :param gauge: the number of layers supported by the gauge
        :return: the position of the needle on the bed
        """
        return sheet + sheet_pos * gauge

    def offset_in_sheet(self, offset: int, slider: bool = False):
        """
        a needle offset while staying within the sheet
        :param offset: number of layer positions to move
        :param slider: true, if returning a slider needle
        :return: the needle offset by the given value in the layer (not actual needle positions)
        """
        if slider:
            return Slider_Sheet_Needle(is_front=self.is_front, sheet_pos=self.sheet_pos + offset, sheet=self.sheet, gauge=self.gauge)
        else:
            return Sheet_Needle(is_front=self.is_front, sheet_pos=self.sheet_pos + offset, sheet=self.sheet, gauge=self.gauge)

    def main_needle(self):
        """
        :return: The non-slider needle at this needle positions
        """
        return Sheet_Needle(is_front=self.is_front, sheet_pos=self.sheet_pos, sheet=self.sheet, gauge=self.gauge)

    def gauge_neighbors(self) -> list:
        """
        :return: List of needles that neighbor this loop in other gauges
        """
        neighbors = []
        for i in range(0, self.gauge):
            if i != self.sheet:
                neighbors.append(Sheet_Needle(self.is_front, self.sheet_pos, i, self.gauge))
        return neighbors

    def __add__(self, other):
        position = other
        if isinstance(other, Sheet_Needle):
            position = other.sheet_pos
        elif isinstance(other, Needle):
            position = other.position
        return Sheet_Needle(self.is_front, self.sheet_pos + position, self.sheet, self.gauge)

    def __radd__(self, other):
        position = other
        if isinstance(other, Sheet_Needle):
            position = other.sheet_pos
        elif isinstance(other, Needle):
            position = other.position
        return Sheet_Needle(self.is_front, position + self.sheet_pos, self.sheet, self.gauge)

    def __sub__(self, other):
        position = other
        if isinstance(other, Sheet_Needle):
            position = other.sheet_pos
        elif isinstance(other, Needle):
            position = other.position
        return Sheet_Needle(self.is_front, self.sheet_pos - position, self.sheet, self.gauge)

    def __rsub__(self, other):
        position = other
        if isinstance(other, Sheet_Needle):
            position = other.sheet_pos
        elif isinstance(other, Needle):
            position = other.position
        return Sheet_Needle(self.is_front, position - self.sheet_pos, self.sheet, self.gauge)

    def __mul__(self, other):
        position = other
        if isinstance(other, Sheet_Needle):
            position = other.sheet_pos
        elif isinstance(other, Needle):
            position = other.position
        return Sheet_Needle(self.is_front, self.sheet_pos * position, self.sheet, self.gauge)

    def __rmul__(self, other):
        position = other
        if isinstance(other, Sheet_Needle):
            position = other.sheet_pos
        elif isinstance(other, Needle):
            position = other.position
        return Sheet_Needle(self.is_front, position * self.sheet_pos, self.sheet, self.gauge)

    def __truediv__(self, other):
        position = other
        if isinstance(other, Sheet_Needle):
            position = other.sheet_pos
        elif isinstance(other, Needle):
            position = other.position
        return Sheet_Needle(self.is_front, self.sheet_pos / position, self.sheet, self.gauge)

    def __rtruediv__(self, other):
        position = other
        if isinstance(other, Sheet_Needle):
            position = other.sheet_pos
        elif isinstance(other, Needle):
            position = other.position
        return Sheet_Needle(self.is_front, position / self.sheet_pos, self.sheet, self.gauge)

    def __floordiv__(self, other):
        position = other
        if isinstance(other, Sheet_Needle):
            position = other.sheet_pos
        elif isinstance(other, Needle):
            position = other.position
        return Sheet_Needle(self.is_front, self.sheet_pos // position, self.sheet, self.gauge)

    def __rfloordiv__(self, other):
        position = other
        if isinstance(other, Sheet_Needle):
            position = other.sheet_pos
        elif isinstance(other, Needle):
            position = other.position
        return Sheet_Needle(self.is_front, position // position, self.sheet, self.gauge)

    def __mod__(self, other):
        position = other
        if isinstance(other, Sheet_Needle):
            position = other.sheet_pos
        elif isinstance(other, Needle):
            position = other.position
        return Sheet_Needle(self.is_front, self.sheet_pos % position, self.sheet, self.gauge)

    def __rmod__(self, other):
        position = other
        if isinstance(other, Sheet_Needle):
            position = other.sheet_pos
        elif isinstance(other, Needle):
            position = other.position
        return Sheet_Needle(self.is_front, position % self.sheet_pos, self.sheet, self.gauge)

    def __pow__(self, power, modulo=None):
        position = power
        if isinstance(power, Sheet_Needle):
            position = power.sheet_pos
        elif isinstance(power, Needle):
            position = power.position
        return Sheet_Needle(self.is_front, self.sheet_pos ** position, self.sheet, self.gauge)

    def __rpow__(self, power, modulo=None):
        position = power
        if isinstance(power, Sheet_Needle):
            position = power.sheet_pos
        elif isinstance(power, Needle):
            position = power.position
        return Sheet_Needle(self.is_front, position ** self.sheet_pos, self.sheet, self.gauge)


class Slider_Sheet_Needle(Sheet_Needle, Slider_Needle):
    """
        Used for slider needles in gauging schema
    """

    def __init__(self, is_front: bool, sheet_pos: int, sheet: int, gauge: int):
        super().__init__(is_front, sheet_pos, sheet, gauge)

    def __add__(self, other):
        position = other
        if isinstance(other, Sheet_Needle):
            position = other.sheet_pos
        elif isinstance(other, Needle):
            position = other.position
        return Slider_Sheet_Needle(self.is_front, self.sheet_pos + position, self.sheet, self.gauge)

    def __radd__(self, other):
        position = other
        if isinstance(other, Sheet_Needle):
            position = other.sheet_pos
        elif isinstance(other, Needle):
            position = other.position
        return Slider_Sheet_Needle(self.is_front, position + self.sheet_pos, self.sheet, self.gauge)

    def __sub__(self, other):
        position = other
        if isinstance(other, Sheet_Needle):
            position = other.sheet_pos
        elif isinstance(other, Needle):
            position = other.position
        return Slider_Sheet_Needle(self.is_front, self.sheet_pos - position, self.sheet, self.gauge)

    def __rsub__(self, other):
        position = other
        if isinstance(other, Sheet_Needle):
            position = other.sheet_pos
        elif isinstance(other, Needle):
            position = other.position
        return Slider_Sheet_Needle(self.is_front, position - self.sheet_pos, self.sheet, self.gauge)

    def __mul__(self, other):
        position = other
        if isinstance(other, Sheet_Needle):
            position = other.sheet_pos
        elif isinstance(other, Needle):
            position = other.position
        return Slider_Sheet_Needle(self.is_front, self.sheet_pos * position, self.sheet, self.gauge)

    def __rmul__(self, other):
        position = other
        if isinstance(other, Sheet_Needle):
            position = other.sheet_pos
        elif isinstance(other, Needle):
            position = other.position
        return Slider_Sheet_Needle(self.is_front, position * self.sheet_pos, self.sheet, self.gauge)

    def __truediv__(self, other):
        position = other
        if isinstance(other, Sheet_Needle):
            position = other.sheet_pos
        elif isinstance(other, Needle):
            position = other.position
        return Slider_Sheet_Needle(self.is_front, self.sheet_pos / position, self.sheet, self.gauge)

    def __rtruediv__(self, other):
        position = other
        if isinstance(other, Sheet_Needle):
            position = other.sheet_pos
        elif isinstance(other, Needle):
            position = other.position
        return Slider_Sheet_Needle(self.is_front, position / self.sheet_pos, self.sheet, self.gauge)

    def __floordiv__(self, other):
        position = other
        if isinstance(other, Sheet_Needle):
            position = other.sheet_pos
        elif isinstance(other, Needle):
            position = other.position
        return Slider_Sheet_Needle(self.is_front, self.sheet_pos // position, self.sheet, self.gauge)

    def __rfloordiv__(self, other):
        position = other
        if isinstance(other, Sheet_Needle):
            position = other.sheet_pos
        elif isinstance(other, Needle):
            position = other.position
        return Slider_Sheet_Needle(self.is_front, position // position, self.sheet, self.gauge)

    def __mod__(self, other):
        position = other
        if isinstance(other, Sheet_Needle):
            position = other.sheet_pos
        elif isinstance(other, Needle):
            position = other.position
        return Slider_Sheet_Needle(self.is_front, self.sheet_pos % position, self.sheet, self.gauge)

    def __rmod__(self, other):
        position = other
        if isinstance(other, Sheet_Needle):
            position = other.sheet_pos
        elif isinstance(other, Needle):
            position = other.position
        return Slider_Sheet_Needle(self.is_front, position % self.sheet_pos, self.sheet, self.gauge)

    def __pow__(self, power, modulo=None):
        position = power
        if isinstance(power, Sheet_Needle):
            position = power.sheet_pos
        elif isinstance(power, Needle):
            position = power.position
        return Slider_Sheet_Needle(self.is_front, self.sheet_pos ** position, self.sheet, self.gauge)

    def __rpow__(self, power, modulo=None):
        position = power
        if isinstance(power, Sheet_Needle):
            position = power.sheet_pos
        elif isinstance(power, Needle):
            position = power.position
        return Slider_Sheet_Needle(self.is_front, position ** self.sheet_pos, self.sheet, self.gauge)


def get_sheet_needle(needle: Needle, gauge: int, slider: bool = False) -> Sheet_Needle:
    """
    Get a sheet needle from a given needle
    :param needle: the original needle
    :param gauge: the gauge of the sheet
    :param slider: true if returning a slider
    :return: Sheet Needle given the gauging schema from a standard needle
    """
    sheet_pos = Sheet_Needle.get_sheet_pos(needle.position, gauge)
    sheet = Sheet_Needle.get_sheet(needle.position, sheet_pos, gauge)
    if slider:
        return Slider_Sheet_Needle(needle.is_front, sheet_pos, sheet, gauge)
    else:
        return Sheet_Needle(needle.is_front, sheet_pos, sheet, gauge)


class Sheet_Identifier:
    """
    Used to convert needles given a defined sheet
    ...

    Attributes
    ----------

    """

    def __init__(self, sheet: int, gauge: int):
        assert gauge > 0, f"Knit Pass Error: Cannot make sheets for gauge {gauge}"
        assert 0 <= sheet < gauge, f"Cannot identify sheet {sheet} at gauge {gauge}"
        self._sheet: int = sheet
        self._gauge: int = gauge

    @property
    def sheet(self) -> int:
        """
        :return: The position of the sheet in the gauge
        """
        return self._sheet

    @property
    def gauge(self) -> int:
        """
        :return: The number of active sheets
        """
        return self._gauge

    def get_needle(self, needle: Needle) -> Sheet_Needle:
        """
        :param needle: Needle to access from sheet. Maybe a sheet needle which will be retargeted to this sheet
        :return: the sheet needle at the given needle index and bed
        """
        pos = needle.position
        if isinstance(needle, Sheet_Needle):
            pos = needle.sheet_pos
        if isinstance(needle, Slider_Needle):
            return Slider_Sheet_Needle(needle.is_front, pos, self.sheet, self.gauge)
        else:
            return Sheet_Needle(needle.is_front, pos, self.sheet, self.gauge)

    def needle(self, is_front: bool, position: int) -> Sheet_Needle:
        """
        Gets a needle within the sheet with specified position
        :param is_front: True if needle is on front bed
        :param position: position within the sheet
        :return: the specified sheet needle
        """
        return Sheet_Needle(is_front, position, self.sheet, self.gauge)

    def __str__(self):
        return f"s{self.sheet}:g{self.gauge}"

    def __repr__(self):
        return str(self)

    def __int__(self):
        return self.sheet

    def __le__(self, other):
        return self.sheet <= int(other)

    def __lt__(self, other):
        return self.sheet < int(other)

    def __eq__(self, other):
        if isinstance(other, Sheet_Identifier):
            return self.sheet == other.sheet and self.gauge == other.gauge
        else:
            return self.sheet == int(other)

    def __gt__(self, other):
        return self.sheet > int(other)

    def __ge__(self, other):
        return self.sheet >= int(other)

    def __add__(self, other):
        return self.sheet + int(other)

    def __sub__(self, other):
        return self.sheet - int(other)

    def __neg__(self):
        return self.sheet * -1

    def __divmod__(self, other):
        return self.sheet % int(other)

    def __mul__(self, other):
        return self.sheet * int(other)

    def __pow__(self, power, modulo=None):
        return self.sheet ^ int(power)
