"""Statement that cuts a yarn"""

from knit_script.knit_script_interpreter.expressions.expressions import Expression
from knit_script.knit_script_interpreter.knit_script_context import Knit_Script_Context
from knit_script.knit_script_interpreter.statements.Statement import Statement
from knit_script.knitout_interpreter.knitout_structures.knitout_instructions.knitout_instructions import outhook, out, releasehook
from knit_script.knitting_machine.machine_components.yarn_management.Carrier_Set import Carrier_Set


class Cut_Statement(Statement):
    """Cuts a set of carriers. Creates outhook operations"""

    def __init__(self, parser_node, carriers: list[Expression]):
        """
        Instantiate
        :param parser_node:
        :param carriers: List of carriers to outhook
        """
        super().__init__(parser_node)
        self._carriers: list[Expression] = carriers

    def __str__(self):
        return f"Cut({self._carriers})"

    def __repr__(self):
        return str(self)

    def execute(self, context: Knit_Script_Context):
        """
        Cuts with outhook operation carrier
        :param context: The current context of the knit_script_interpreter
        """
        if len(self._carriers) == 0:
            print(f"No carrier to cut specified. Cutting working carrier: {context.carrier}")
            outhook_op = outhook(context.machine_state, context.carrier, "Cutting working carrier")
        else:
            carrier_set = set()

            def _add_carrier(cr):
                if isinstance(cr, list):
                    for sub_cr in cr:
                        _add_carrier(sub_cr)
                elif isinstance(cr, int):
                    carrier_set.add(cr)
                else:
                    assert isinstance(cr, Carrier_Set), f'Expected to cut a carrier, integer representing a carrier, or list of carriers, but got {cr}'
                    carrier_set.update(cr.carrier_ids)

            for c in self._carriers:
                carrier = c.evaluate(context)
                _add_carrier(carrier)
            carrier_set = Carrier_Set([*carrier_set])
            outhook_op = outhook(context.machine_state, carrier_set)
        context.knitout.append(outhook_op)


class Release_Statement(Statement):
    """Removes current carrier on yarn inserting hook or does nothing."""

    def __init__(self, parser_node):
        """
        Instantiate
        :param parser_node:
        :param carriers: List of carriers to outhook
        """
        super().__init__(parser_node)

    def __str__(self):
        return f"ReleaseHook"

    def __repr__(self):
        return str(self)

    def execute(self, context: Knit_Script_Context):
        """
        Cuts with outhook operation carrier
        :param context: The current context of the knit_script_interpreter
        """
        release_op = releasehook(context.machine_state)
        context.knitout.append(release_op)


class Remove_Statement(Statement):
    """
    Statement removing carriers from bed without cuts. Equivalent to out operations
    """

    def __init__(self, parser_node, carriers: list[Expression]):
        """
        Instantiate
        :param parser_node:
        :param carriers: Carriers to out
        """
        super().__init__(parser_node)
        self._carriers: list[Expression] = carriers

    def __str__(self):
        return f"Out({self._carriers})"

    def __repr__(self):
        return str(self)

    def execute(self, context: Knit_Script_Context):
        """
        Cuts with outhook operation carrier
        :param context: The current context of the knit_script_interpreter
        """
        if len(self._carriers) == 0:
            print(f"No carrier to bring out specified. Cutting working carrier: {context.carrier}")
            out_op = outhook(context.machine_state, context.carrier, "Removing working carrier")
        else:
            carrier_set = set()

            def _add_carrier(cr):
                if isinstance(cr, list):
                    for sub_cr in cr:
                        _add_carrier(sub_cr)
                elif isinstance(cr, int):
                    carrier_set.add(cr)
                else:
                    assert isinstance(cr, Carrier_Set), f'Expected to bring out a carrier, integer representing a carrier, or list of carriers, but got {cr}'
                    carrier_set.update(cr.carrier_ids)

            for c in self._carriers:
                carrier = c.evaluate(context)
                _add_carrier(carrier)
            carrier_set = Carrier_Set([*carrier_set])
            out_op = out(context.machine_state, carrier_set)
        context.knitout.append(out_op)
