"""Statement that cuts a yarn"""
from knitout_interpreter.knitout_operations.carrier_instructions import Releasehook_Instruction, Outhook_Instruction, Out_Instruction
from parglare.parser import LRStackNode
from virtual_knitting_machine.machine_components.yarn_management.Yarn_Carrier import Yarn_Carrier
from virtual_knitting_machine.machine_components.yarn_management.Yarn_Carrier_Set import Yarn_Carrier_Set

from knit_script.knit_script_interpreter.expressions.expressions import Expression
from knit_script.knit_script_interpreter.knit_script_context import Knit_Script_Context
from knit_script.knit_script_interpreter.statements.Statement import Statement


class Cut_Statement(Statement):
    """Statement for cutting yarn carriers.

    Creates outhook operations that cut and remove yarn carriers from the machine.
    If no carriers are specified, cuts the currently active working carrier.
    """

    def __init__(self, parser_node: LRStackNode, carriers: list[Expression]) -> None:
        """Initialize a cut statement.

        Args:
            parser_node: The parser node from the abstract syntax tree.
            carriers: List of expression that evaluate to carriers to cut.
                Can be empty to cut the current working carrier.
        """
        super().__init__(parser_node)
        self._carriers: list[Expression] = carriers

    def __str__(self) -> str:
        """Return string representation of the cut statement.

        Returns:
            A string showing the carriers to be cut.
        """
        return f"Cut({self._carriers})"

    def __repr__(self) -> str:
        """Return detailed string representation of the cut statement.

        Returns:
            Same as __str__ for this class.
        """
        return str(self)

    def execute(self, context: Knit_Script_Context) -> None:
        """Execute the cut operation on the specified carriers.

        Args:
            context: The current execution context of the knit script interpreter.
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
                    cr: Carrier specification that can be a list, int, Yarn_Carrier, or Yarn_Carrier_Set.

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
                    raise TypeError(f'Expected to cut a carrier, integer representing a carrier, or list of carriers, but got {cr}')

            for c in self._carriers:
                carrier = c.evaluate(context)
                _add_carrier(carrier)
            carrier_set = Yarn_Carrier_Set([*carrier_set])
            for carrier in carrier_set:
                outhook_op = Outhook_Instruction.execute_outhook(context.machine_state, carrier)
                context.knitout.append(outhook_op)


class Release_Statement(Statement):
    """Statement for releasing the yarn inserting hook.

    Removes the current carrier from the yarn inserting hook or does nothing
    if no carrier is currently hooked.
    """

    def __init__(self, parser_node: LRStackNode) -> None:
        """Initialize a release statement.

        Args:
            parser_node: The parser node from the abstract syntax tree.
        """
        super().__init__(parser_node)

    def __str__(self) -> str:
        """Return string representation of the release statement.

        Returns:
            A string indicating this is a release hook operation.
        """
        return f"ReleaseHook"

    def __repr__(self) -> str:
        """Return detailed string representation of the release statement.

        Returns:
            Same as __str__ for this class.
        """
        return str(self)

    def execute(self, context: Knit_Script_Context) -> None:
        """Execute the release hook operation.

        Args:
            context: The current execution context of the knit script interpreter.
        """
        carrier = context.machine_state.carrier_system.hooked_carrier
        if carrier is not None:
            release_op = Releasehook_Instruction.execute_releasehook(context.machine_state, carrier)
            context.knitout.append(release_op)


class Remove_Statement(Statement):
    """Statement for removing carriers from bed without cutting.

    Equivalent to 'out' operations - removes carriers from the needle bed
    but does not cut the yarn, allowing the carrier to be brought back later.
    """

    def __init__(self, parser_node: LRStackNode, carriers: list[Expression]) -> None:
        """Initialize a remove statement.

        Args:
            parser_node: The parser node from the abstract syntax tree.
            carriers: List of expressions that evaluate to carriers to remove.
                Can be empty to remove the current working carrier.
        """
        super().__init__(parser_node)
        self._carriers: list[Expression] = carriers

    def __str__(self) -> str:
        """Return string representation of the remove statement.

        Returns:
            A string showing the carriers to be removed.
        """
        return f"Out({self._carriers})"

    def __repr__(self) -> str:
        """Return detailed string representation of the remove statement.

        Returns:
            Same as __str__ for this class.
        """
        return str(self)

    def execute(self, context: Knit_Script_Context) -> None:
        """Execute the remove operation on the specified carriers.

        Args:
            context: The current execution context of the knit script interpreter.
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
                    cr: Carrier specification that can be a list, int, or Yarn_Carrier_Set.

                Raises:
                    AssertionError: If cr is not a supported carrier type.
                """
                if isinstance(cr, list):
                    for sub_cr in cr:
                        _add_carrier(sub_cr)
                elif isinstance(cr, int):
                    carrier_set.add(cr)
                else:
                    assert isinstance(cr, Yarn_Carrier_Set), f'Expected to bring out a carrier, integer representing a carrier, or list of carriers, but got {cr}'
                    carrier_set.update(cr.carrier_ids)

            for c in self._carriers:
                carrier = c.evaluate(context)
                _add_carrier(carrier)
            carrier_set = Yarn_Carrier_Set([*carrier_set])
            for carrier in carrier_set:
                out_op = Out_Instruction.execute_out(context.machine_state, carrier)
                context.knitout.append(out_op)
