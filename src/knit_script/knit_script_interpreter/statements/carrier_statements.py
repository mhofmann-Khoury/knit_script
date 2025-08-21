"""Statement that cuts a yarn.

This module provides statement classes for managing yarn carrier operations in knit script programs.
It includes statements for cutting carriers (permanently removing them), releasing the yarn hook, and removing carriers from the working area without cutting the yarn.
"""
from knitout_interpreter.knitout_operations.carrier_instructions import (
    Out_Instruction,
    Outhook_Instruction,
    Releasehook_Instruction,
)
from parglare.parser import LRStackNode
from virtual_knitting_machine.machine_components.yarn_management.Yarn_Carrier import (
    Yarn_Carrier,
)
from virtual_knitting_machine.machine_components.yarn_management.Yarn_Carrier_Set import (
    Yarn_Carrier_Set,
)

from knit_script.knit_script_exceptions.python_style_exceptions import (
    Knit_Script_TypeError,
)
from knit_script.knit_script_interpreter.expressions.expressions import Expression
from knit_script.knit_script_interpreter.knit_script_context import Knit_Script_Context
from knit_script.knit_script_interpreter.statements.Statement import Statement


class Cut_Statement(Statement):
    """Statement for cutting yarn carriers.

    Creates outhook operations that cut and remove yarn carriers from the machine permanently.
    If no carriers are specified, cuts the currently active working carrier. This operation terminates the yarn and removes it from the machine completely.

    The cut operation is typically used at the end of knitting sections or when switching between different yarns that should not be connected.
    Unlike remove operations, cut operations permanently sever the yarn.

    Attributes:
        _carriers (list[Expression]): List of expressions that evaluate to carriers to cut.
    """

    def __init__(self, parser_node: LRStackNode, carriers: list[Expression]) -> None:
        """Initialize a cut statement.

        Args:
            parser_node (LRStackNode): The parser node from the abstract syntax tree.
            carriers (list[Expression]): List of expressions that evaluate to carriers to cut. Can be empty to cut the current working carrier.
        """
        super().__init__(parser_node)
        self._carriers: list[Expression] = carriers

    def __str__(self) -> str:
        """Return string representation of the cut statement.

        Returns:
            str: A string showing the carriers to be cut.
        """
        return f"Cut({self._carriers})"

    def __repr__(self) -> str:
        """Return detailed string representation of the cut statement.

        Returns:
            str: Same as __str__ for this class.
        """
        return str(self)

    def execute(self, context: Knit_Script_Context) -> None:
        """Execute the cut operation on the specified carriers.

        Evaluates all carrier expressions and generates outhook instructions to permanently cut and remove the specified carriers from the machine.
        If no carriers are specified, cuts the current working carrier.

        Args:
            context (Knit_Script_Context): The current execution context of the knit script interpreter.
        """
        if len(self._carriers) == 0:
            print(f"No carrier to cut specified. Cutting working carrier: {context.carrier}")
            for carrier in context.carrier:
                outhook_op = Outhook_Instruction.execute_outhook(context.machine_state, carrier, f"Cutting working carrier {carrier} of {context.carrier}")
                context.knitout.append(outhook_op)
        else:
            carrier_set = set()

            def _add_carrier(cr: list | int | Yarn_Carrier | Yarn_Carrier_Set) -> None:
                """Recursively add carriers to the set to be cut.

                Args:
                    cr (list | int | Yarn_Carrier | Yarn_Carrier_Set): Carrier specification that can be a list, int, Yarn_Carrier, or Yarn_Carrier_Set.

                Raises:
                    TypeError: If cr is not a supported carrier type.
                """
                if isinstance(cr, list):
                    for sub_cr in cr:
                        _add_carrier(sub_cr)
                elif isinstance(cr, int):
                    carrier_set.add(cr)
                elif isinstance(cr, Yarn_Carrier_Set):
                    carrier_set.update(cr.carrier_ids)
                elif isinstance(cr, Yarn_Carrier):
                    carrier_set.add(cr.carrier_id)
                else:
                    raise Knit_Script_TypeError(f'Expected to cut a carrier, integer representing a carrier, or list of carriers, but got {cr}', self)

            for c in self._carriers:
                carrier = c.evaluate(context)
                _add_carrier(carrier)
            carrier_set = Yarn_Carrier_Set([*carrier_set])
            for carrier in carrier_set:
                outhook_op = Outhook_Instruction.execute_outhook(context.machine_state, carrier)
                context.knitout.append(outhook_op)


class Release_Statement(Statement):
    """Statement for releasing the yarn inserting hook.

    Removes the current carrier from the yarn inserting hook or does nothing if no carrier is currently hooked.
    This operation releases the yarn from the hook mechanism without cutting or removing the carrier from the machine, allowing it to be manipulated or repositioned.

    The release operation is typically used when the yarn hook needs to be cleared for racking operations or other machine movements that require the hook to be free.
    """

    def __init__(self, parser_node: LRStackNode) -> None:
        """Initialize a release statement.

        Args:
            parser_node (LRStackNode): The parser node from the abstract syntax tree.
        """
        super().__init__(parser_node)

    def __str__(self) -> str:
        """Return string representation of the release statement.

        Returns:
            str: A string indicating this is a release hook operation.
        """
        return f"ReleaseHook"

    def __repr__(self) -> str:
        """Return detailed string representation of the release statement.

        Returns:
            str: Same as __str__ for this class.
        """
        return str(self)

    def execute(self, context: Knit_Script_Context) -> None:
        """Execute the release hook operation.

        Checks if there is a currently hooked carrier and generates a releasehook instruction to release it from the yarn inserting hook.

        Args:
            context (Knit_Script_Context): The current execution context of the knit script interpreter.
        """
        carrier = context.machine_state.carrier_system.hooked_carrier
        if carrier is not None:
            release_op = Releasehook_Instruction.execute_releasehook(context.machine_state, carrier)
            context.knitout.append(release_op)


class Remove_Statement(Statement):
    """Statement for removing carriers from bed without cutting.

    Equivalent to 'out' operations - removes carriers from the needle bed but does not cut the yarn, allowing the carrier to be brought back later with 'in' operations.
    This is useful for temporarily moving carriers out of the way without permanently terminating them.

    The remove operation maintains the yarn connection but moves the carrier out of the active working area, making it available for later reactivation when needed.

    Attributes:
        _carriers (list[Expression]): List of expressions that evaluate to carriers to remove.
    """

    def __init__(self, parser_node: LRStackNode, carriers: list[Expression]) -> None:
        """Initialize a remove statement.

        Args:
            parser_node (LRStackNode): The parser node from the abstract syntax tree.
            carriers (list[Expression]): List of expressions that evaluate to carriers to remove. Can be empty to remove the current working carrier.
        """
        super().__init__(parser_node)
        self._carriers: list[Expression] = carriers

    def __str__(self) -> str:
        """Return string representation of the remove statement.

        Returns:
            str: A string showing the carriers to be removed.
        """
        return f"Out({self._carriers})"

    def __repr__(self) -> str:
        """Return detailed string representation of the remove statement.

        Returns:
            str: Same as __str__ for this class.
        """
        return str(self)

    def execute(self, context: Knit_Script_Context) -> None:
        """Execute the remove operation on the specified carriers.

        Evaluates all carrier expressions and generates out instructions to remove the specified carriers from the working area without cutting them.
        If no carriers are specified, removes the current working carrier.

        Args:
            context (Knit_Script_Context): The current execution context of the knit script interpreter.
        """
        if len(self._carriers) == 0:
            print(f"No carrier to bring out specified. Cutting working carrier: {context.carrier}")
            for carrier in context.carrier:
                out_op = Out_Instruction.execute_out(context.machine_state, carrier, f"Removing working carrier {carrier} of {context.carrier}")
                context.knitout.append(out_op)
        else:
            carrier_set = set()

            def _add_carrier(cr: list | int | Yarn_Carrier_Set) -> None:
                """Recursively add carriers to the set to be removed.

                Args:
                    cr (list | int | Yarn_Carrier_Set): Carrier specification that can be a list, int, or Yarn_Carrier_Set.

                Raises:
                    TypeError: If cr is not a supported carrier type.
                """
                if isinstance(cr, list):
                    for sub_cr in cr:
                        _add_carrier(sub_cr)
                elif isinstance(cr, int):
                    carrier_set.add(cr)
                else:
                    if not isinstance(cr, Yarn_Carrier_Set):
                        raise Knit_Script_TypeError(f'Expected to bring out a carrier, integer representing a carrier, or list of carriers, but got {cr}', self)
                    carrier_set.update(cr.carrier_ids)

            for c in self._carriers:
                carrier = c.evaluate(context)
                _add_carrier(carrier)
            carrier_set = Yarn_Carrier_Set([*carrier_set])
            for carrier in carrier_set:
                out_op = Out_Instruction.execute_out(context.machine_state, carrier)
                context.knitout.append(out_op)
