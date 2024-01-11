"""Scope of machine variables"""

from enum import Enum
from typing import Optional, Union, Any

from knit_script.Knit_Errors.gauge_errors import Gauge_Value_Error, Sheet_Value_Error
from knit_script.knitting_machine.Machine_State import Machine_State
from knit_script.knitting_machine.machine_components.Sheet_Needle import Sheet_Identifier
from knit_script.knitting_machine.machine_components.machine_pass_direction import Pass_Direction
from knit_script.knitting_machine.machine_components.yarn_management.Carrier_Set import Carrier_Set


class Machine_Variables(Enum):
    """
    Tracks Knit-script names for global machine variables
    """
    Gauge = "gauge"
    Carrier = "carrier"
    Rack = "racking"
    Sheet = "sheet"

    @staticmethod
    def in_machine_variables(key: str) -> bool:
        """
        :param key: variable string
        :return: True if key is a variable
        """
        return key in [i.name for i in Machine_Variables]

    def get_value(self, scope):
        """
        :param scope: variable scope to access value from
        :return: the accessed value
        """
        return getattr(scope, self.value)

    def set_value(self, context, value):
        """
        Sets the machine variable at the global level
        :param value: the value to set the machine variable to
        :param context: Scope or global scope to set the value to
        """
        setattr(context, self.value, value)


class Machine_Scope:
    """
        Keeps track of the machine state within different scopes
    """

    def __init__(self, context, parent_scope=None):
        self.context = context
        if parent_scope is None:
            self._direction: Pass_Direction = Pass_Direction.Leftward
            self._carrier: Optional[Carrier_Set] = None
            self._racking: float = 0.0
            self._gauge: int = 1
            self._sheet: Sheet_Identifier = Sheet_Identifier(0, self._gauge)
        else:
            assert isinstance(parent_scope, Machine_Scope)
            self._direction: Pass_Direction = parent_scope.direction
            self._carrier: Optional[Carrier_Set] = parent_scope.carrier
            self._racking: float = parent_scope.racking
            self._gauge: int = parent_scope.gauge
            self._sheet: Sheet_Identifier = parent_scope.sheet

    def copy(self):
        """
        :return: machine scope that is a copy of this machine scope
        """
        scope = Machine_Scope(self.context)
        scope.direction = self.direction
        scope.carrier = self.carrier
        scope.racking = self.racking
        scope.gauge = self.gauge
        scope.sheet = self.sheet
        return scope

    @property
    def direction(self) -> Pass_Direction:
        """
        :return: The current direction the carriage will take
        """
        return self._direction

    @direction.setter
    def direction(self, value: Pass_Direction):
        if not isinstance(value, Pass_Direction):
            raise TypeError(f"Direction has been set to non-direction {value}")
        self._direction = value

    @property
    def carrier(self) -> Optional[Carrier_Set]:
        """
        :return: the current carrier being used by the machine
        """
        return self._carrier

    @carrier.setter
    def carrier(self, carrier: Optional[Union[int, float, list, Carrier_Set]]):
        if isinstance(carrier, int):
            carrier = Carrier_Set(carrier)
        elif isinstance(carrier, float):
            carrier = Carrier_Set(int(carrier))
        elif isinstance(carrier, list):
            carrier = Carrier_Set(carrier)
        assert carrier is None or isinstance(carrier, Carrier_Set), f"Cannot set Carrier to non-carrier, int, or list of ints/carriers {carrier}"
        self._carrier = carrier

    @property
    def racking(self) -> float:
        """
        :return: current racking of the machine
        """
        return self._racking

    @racking.setter
    def racking(self, value: float):
        self._racking = value

    @property
    def gauge(self) -> int:
        """
        :return: The current number of sheets on the machine
        """
        return self._gauge

    @gauge.setter
    def gauge(self, value: Optional[int]):
        if value is None:
            value = 1
        if not (0 < value < Machine_State.MAX_GAUGE):
            raise Gauge_Value_Error(value)
        if self.gauge != int(value):
            self._gauge = int(value)
            self.context.machine_state.gauge = self.gauge
            if 0 > int(self.sheet) or int(self.sheet) >= self.gauge:
                print(f"Knit Script Warning: Gauge of {self.gauge} is greater than current sheet {self.sheet} so sheet is set to {self.gauge - 1}")
                self.sheet = self.gauge - 1
            else:
                self.sheet = Sheet_Identifier(self.sheet.sheet, self.gauge)

    @property
    def sheet(self) -> Sheet_Identifier:
        """
        :return: The current sheet being worked on the machine
        """
        return self._sheet

    @sheet.setter
    def sheet(self, value: Optional[Union[int, Sheet_Identifier]]):
        if value is None:
            value = Sheet_Identifier(0, self.gauge)
        elif isinstance(value, int):
            if not (0 <= value < self.gauge):
                raise Sheet_Value_Error(value, self.gauge)
            value = Sheet_Identifier(value, self.gauge)
        if self.gauge != value.gauge:
            self.gauge = value.gauge
        if self.sheet != value:
            self._sheet = value
            self.context.machine_state.sheet = self.sheet.sheet
        if 0 > int(self.sheet) or int(self.sheet) >= self.gauge:
            print(f"Knit Script Warning: Gauge of {self.gauge} is greater than current sheet {self.sheet} so sheet is set to {self.gauge - 1}")
            self.sheet = self.gauge - 1

    def __getitem__(self, key: str) -> Any:
        if Machine_Variables.in_machine_variables(key):
            return Machine_Variables[key].get_value(self)
        return getattr(self, key)

    def __setitem__(self, key: str, value: Any):
        setattr(self, key, value)

    def __delitem__(self, key: str):
        delattr(self, key)

    def __contains__(self, key: str):
        return Machine_Variables.in_machine_variables(key)
