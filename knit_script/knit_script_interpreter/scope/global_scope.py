"""Used for tracking global variable space of program execution"""
from typing import Dict, Any

from knit_script.knit_script_interpreter.scope.machine_scope import Machine_Variables


class Knit_Script_Globals:
    """
        Tracks all the global variables
    """
    def __init__(self):
        self.values: Dict[str, Any] = {}
        # self._direction: Pass_Direction = Pass_Direction.Leftward
        # self._carrier: Optional[Yarn_Carrier] = None
        # self._racking: float = 0.0
        # self._gauge: int = 1
        # self._sheet: int = 0
        self._exit_value: Any = None

    @property
    def exit_value(self):
        """
        :return: Return value for whole knit script execution
        """
        return self._exit_value


    @exit_value.setter
    def exit_value(self, value: Any):
        self._exit_value = value

    # @property
    # def direction(self) -> Pass_Direction:
    #     """
    #     :return: The current direction the carriage will take
    #     """
    #     return self._direction
    #
    # @direction.setter
    # def direction(self, value: Pass_Direction):
    #     assert isinstance(value, Pass_Direction), f"Direction has been set to non-direction {value}"
    #     self._direction = value
    #
    # @property
    # def carrier(self) -> Optional[Yarn_Carrier]:
    #     """
    #     :return: the current carrier being used by the machine
    #     """
    #     return self._carrier
    #
    # @carrier.setter
    # def carrier(self, carrier: Optional[Union[int, float, list, Yarn_Carrier]]):
    #     if isinstance(carrier, int):
    #         carrier = Yarn_Carrier(carrier)
    #     elif isinstance(carrier, float):
    #         carrier = Yarn_Carrier(int(carrier))
    #     elif isinstance(carrier, list):
    #         carrier = Yarn_Carrier(carrier)
    #     assert carrier is None or isinstance(carrier, Yarn_Carrier), f"Cannot set Carrier to non-carrier, int, or list of ints/carriers {carrier}"
    #     self._carrier = carrier
    # @property
    # def racking(self) -> float:
    #     """
    #     :return: current racking of the machine
    #     """
    #     return self._racking
    #
    # @racking.setter
    # def racking(self, value: float):
    #     self._racking = value
    #
    # @property
    # def gauge(self) -> int:
    #     """
    #     :return: The current number of sheets on the machine
    #     """
    #     return self._gauge
    #
    # @gauge.setter
    # def gauge(self, value: Optional[int]):
    #     if value is None:
    #         value = 1
    #     assert 0 < value < Machine_State.MAX_GAUGE, \
    #         f"KnitScript Error: Gauge must be between 0 and {Machine_State.MAX_GAUGE} but got {value}"
    #     self._gauge = int(value)
    #     if self.sheet >= self.gauge:
    #         print(f"Knit Script Warning: Gauge of {self.gauge} is greater than current sheet {self.sheet} so sheet is set to {self.gauge-1}")
    #         self.sheet = self.gauge - 1
    #
    # @property
    # def sheet(self) -> int:
    #     """
    #     :return: The current sheet being worked on the machine
    #     """
    #     return self._sheet
    #
    # @sheet.setter
    # def sheet(self, value: Optional[Union[int, Sheet_Identifier]]):
    #
    #     if value is None:
    #         value = Sheet_Identifier(0, self.gauge)
    #     elif isinstance(value, int):
    #         assert 0 <= value < self.gauge, \
    #             f"Sheet must be between 0 and gauge {self.gauge}, {value}"
    #         value = Sheet_Identifier(value, self.gauge)
    #     self.gauge = value.gauge
    #     self._sheet = value.sheet

    def __getitem__(self, key:str) -> Any:
        return getattr(self, key)

    def __setitem__(self, key: str, value:Any):
        setattr(self, key, value)

    def __delitem__(self, key:str):
        delattr(self, key)

    def __contains__(self, key:str):
        return hasattr(self, key)
