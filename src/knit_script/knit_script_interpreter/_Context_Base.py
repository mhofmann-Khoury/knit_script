"""Module containing the base context class for knit script execution.

This module provides the _Context_Base class, which serves as the foundation for managing execution context in knit script programs.
It maintains the knitting machine state, file references, parser instances, and knitout generation capabilities that are essential for knit script execution across different contexts and scopes.
"""
from __future__ import annotations

from knitout_interpreter.knitout_operations.Header_Line import get_machine_header
from knitout_interpreter.knitout_operations.Knitout_Line import Knitout_Line
from virtual_knitting_machine.Knitting_Machine import Knitting_Machine
from virtual_knitting_machine.Knitting_Machine_Specification import Knitting_Machine_Specification
from virtual_knitting_machine.machine_components.needles.Needle import Needle

from knit_script.knit_script_interpreter._parser_base import _Parser_Base


class _Context_Base:
    """Base class for managing execution context in knit script programs.

    The _Context_Base class provides the fundamental infrastructure for knit script execution contexts.
    It manages the knitting machine state, maintains references to the source file and parser,
    tracks carriage pass results, and handles knitout generation with proper versioning and header information.

    This class serves as the foundation for more specialized context classes that add additional functionality like variable scoping and advanced state management.
    It ensures that all execution contexts have consistent access to machine state and knitout generation capabilities.

    Attributes:
        machine_state (Knitting_Machine): The current state of the knitting machine.
        ks_file (str | None): Path to the knit script file being executed.
        parser (_Parser_Base | None): Parser instance used for processing knit script code.
        last_carriage_pass_result (list[Needle] | dict[Needle, Needle | None]): Results from the most recent carriage pass operation.
        _version (int): The knitout format version being used for output generation.
        knitout (list[Knitout_Line]): List of knitout instructions generated during execution.
    """

    def __init__(self, machine_specification: Knitting_Machine_Specification = Knitting_Machine_Specification(), ks_file: str | None = None, parser: _Parser_Base | None = None,
                 knitout_version: int = 2):
        """Initialize the base execution context.

        Creates a new execution context with the specified machine configuration and execution parameters.
        Initializes the knitting machine state, sets up knitout generation with appropriate headers, and establishes references to the source file and parser.

        Args:
            machine_specification (Knitting_Machine_Specification, optional): Specification defining the capabilities and configuration of the knitting machine.
            Defaults to Knitting_Machine_Specification().
            ks_file (str | None, optional): Path to the knit script file being executed. Used for error reporting and debugging. Defaults to None.
            parser (_Parser_Base | None, optional): Parser instance for processing knit script syntax. Defaults to None.
            knitout_version (int, optional): Version number of the knitout format to generate. Defaults to 2.
        """
        self.machine_state: Knitting_Machine = Knitting_Machine(machine_specification=machine_specification)
        self.ks_file: str | None = ks_file
        self.parser: _Parser_Base | None = parser
        self.last_carriage_pass_result: list[Needle] | dict[Needle, Needle | None] = {}
        self._version = knitout_version
        self.knitout: list[Knitout_Line] = get_machine_header(self.machine_state, self.version)

    @property
    def version(self) -> int:
        """Get the knitout version being written.

        Returns:
            int: The knitout version number currently in use for output generation.
        """
        return self._version

    @version.setter
    def version(self, version: int) -> None:
        """Set the knitout version for output generation.

        Args:
            version (int): The version number to set for knitout format output.
        """
        self._version = version
