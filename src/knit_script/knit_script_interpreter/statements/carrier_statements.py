"""Statement that cuts a yarn"""
from knitout_interpreter.knitout_operations.carrier_instructions import Releasehook_Instruction, Outhook_Instruction, Out_Instruction
from virtual_knitting_machine.machine_components.yarn_management.Yarn_Carrier import Yarn_Carrier
from virtual_knitting_machine.machine_components.yarn_management.Yarn_Carrier_Set import Yarn_Carrier_Set

from knit_script.knit_script_interpreter.expressions.expressions import Expression
from knit_script.knit_script_interpreter.knit_script_context import Knit_Script_Context
from knit_script.knit_script_interpreter.statements.Statement import Statement


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
            for carrier in context.carrier:
                outhook_op = Outhook_Instruction.execute_outhook(context.machine_state, carrier, f"Cutting working carrier {carrier} of {context.carrier}")
                context.knitout.append(outhook_op)
        else:
            carrier_set = set()

            def _add_carrier(cr):
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
        carrier = context.machine_state.carrier_system.hooked_carrier
        if carrier is not None:
            release_op = Releasehook_Instruction.execute_releasehook(context.machine_state, carrier)
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
            for carrier in context.carrier:
                out_op = Out_Instruction.execute_out(context.machine_state, carrier, f"Removing working carrier {carrier} of {context.carrier}")
                context.knitout.append(out_op)
        else:
            carrier_set = set()

            def _add_carrier(cr):
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
