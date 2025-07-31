"""A pass of drop operations"""
from knitout_interpreter.knitout_operations.knitout_instruction import Knitout_Instruction_Type
from parglare.parser import LRStackNode
from virtual_knitting_machine.machine_components.carriage_system.Carriage_Pass_Direction import Carriage_Pass_Direction
from virtual_knitting_machine.machine_components.needles.Needle import Needle

from knit_script.knit_script_interpreter.expressions.expressions import Expression
from knit_script.knit_script_interpreter.knit_script_context import Knit_Script_Context
from knit_script.knit_script_interpreter.statements.Carriage_Pass_Specification import Carriage_Pass_Specification
from knit_script.knit_script_interpreter.statements.Statement import Statement


class Drop_Pass(Statement):
    """Executes a set of drop operations from left to right.

    Creates a specialized carriage pass that drops stitches from the specified
    needles. Always executes in rightward direction for consistency.
    """

    def __init__(self, parser_node: LRStackNode, needles: list[Expression]) -> None:
        """Initialize a drop pass.

        Args:
            parser_node: The parser node from the abstract syntax tree.
            needles: List of expressions that evaluate to needles to drop from.
                Can include nested lists of needles.
        """
        super().__init__(parser_node)
        self._needles: list[Expression] = needles

    def execute(self, context: Knit_Script_Context) -> None:
        """Execute drop operations on all specified needles.

        Evaluates all needle expressions, flattens any nested lists,
        then creates a carriage pass to drop all stitches.

        Args:
            context: The current execution context of the knit script interpreter.

        Raises:
            TypeError: If any expression doesn't evaluate to a Needle object.
        """
        needles = []
        for needle in self._needles:
            n = needle.evaluate(context)
            if isinstance(n, list):
                needles.extend(n)
            else:
                needles.append(n)
        for n in needles:
            if not isinstance(n, Needle):
                raise TypeError(f"Expected to drop needles but got {n} in {self._needles} <{needles}>")

        needles_to_instruction = {n: Knitout_Instruction_Type.Drop for n in needles}

        machine_pass = Carriage_Pass_Specification(needles_to_instruction, Carriage_Pass_Direction.Rightward, is_drop_pass=True)

        needle_results = machine_pass.write_knitout(context)
        context.last_carriage_pass_result = [n for n in needle_results.keys()]  # stores needles that were dropped
