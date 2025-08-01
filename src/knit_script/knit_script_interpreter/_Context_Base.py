from __future__ import annotations

from knitout_interpreter.knitout_operations.Header_Line import get_machine_header
from knitout_interpreter.knitout_operations.Knitout_Line import Knitout_Line
from virtual_knitting_machine.Knitting_Machine import Knitting_Machine
from virtual_knitting_machine.Knitting_Machine_Specification import Knitting_Machine_Specification
from virtual_knitting_machine.machine_components.needles.Needle import Needle

from knit_script.knit_script_interpreter._parser_base import _Parser_Base


class _Context_Base:

    def __init__(self, machine_specification: Knitting_Machine_Specification = Knitting_Machine_Specification(),
                 ks_file: str |  None = None, parser: _Parser_Base | None = None, knitout_version: int = 2):
        self.machine_state: Knitting_Machine = Knitting_Machine(machine_specification=machine_specification)
        self.ks_file: str | None = ks_file
        self.parser: _Parser_Base | None = parser
        self.last_carriage_pass_result: list[Needle] | dict[Needle, Needle | None] = {}
        self._version = knitout_version
        self.knitout: list[Knitout_Line] = get_machine_header(self.machine_state, self.version)

    @property
    def version(self) -> int:
        """The knitout version being written.

        Returns:
            The knitout version number
        """
        return self._version

    @version.setter
    def version(self, version: int) -> None:
        """Sets the knitout version.

        Args:
            version: The version number to set
        """
        self._version = version
