"""Statement that cuts a yarn"""

from typing import List

from knit_script.knit_script_interpreter.expressions.expressions import Expression
from knit_script.knit_script_interpreter.knit_script_context import Knit_Script_Context
from knit_script.knit_script_interpreter.statements.Statement import Statement
from knit_script.knitting_machine.knitout_instructions import outhook, out
from knit_script.knitting_machine.machine_components.yarn_carrier import Yarn_Carrier


class Cut_Statement(Statement):
    """Cuts a set of carriers. Creates outhook operations"""

    def __init__(self, carriers: List[Expression]):
        """
        Instantiate
        :param carriers: list of carriers to outhook
        """
        super().__init__()
        self._carriers: List[Expression] = carriers

    def __str__(self):
        return f"Cut({self._carriers})"

    def __repr__(self):
        return str(self)

    def execute(self, context: Knit_Script_Context):
        """
        Cuts with outhook operation carrier
        :param context: The current context of the knit_script_interpreter
        """
        if len(self._carriers) is None:
            carriers = context.machine_state.yarn_manager.active_carriers
            print(f"No carrier to cut specified. Cutting all active carriers: {carriers}")
            for c in carriers:
                cmd = outhook(context.machine_state, Yarn_Carrier([c]))
                context.knitout.append(cmd)
        else:
            carriers = set()

            def _add_carrier(cr):
                if isinstance(cr, list):
                    for sub_cr in cr:
                        _add_carrier(sub_cr)
                elif isinstance(cr, int):
                    carriers.add(cr)
                else:
                    assert isinstance(cr, Yarn_Carrier), f'Expected to cut a carrier, integer representing a carrier, or list of carriers, but got {cr}'
                    carriers.update(cr.carrier_ids)

            for c in self._carriers:
                carrier = c.evaluate(context)
                _add_carrier(carrier)
        for c in carriers:
            cmd = outhook(context.machine_state, Yarn_Carrier([c]))
            context.knitout.append(cmd)


class Remove_Statement(Statement):
    """
    Statement removing carriers from bed without cuts. Equivalent to out operations
    """

    def __init__(self, carriers: List[Expression]):
        """
        Instantiate
        :param carriers: Carriers to out
        """
        super().__init__()
        self._carriers: List[Expression] = carriers

    def __str__(self):
        return f"Out({self._carriers})"

    def __repr__(self):
        return str(self)

    def execute(self, context: Knit_Script_Context):
        """
        Cuts with outhook operation carrier
        :param context: The current context of the knit_script_interpreter
        """
        for c in self._carriers:
            carrier = c.evaluate(context)
            assert isinstance(carrier, Yarn_Carrier), f'Expected to bring out a yarn, but got {carrier}'
            cmd = out(context.machine_state, carrier)
            context.knitout.append(cmd)
