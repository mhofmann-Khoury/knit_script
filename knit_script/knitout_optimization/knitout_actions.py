"""Actions for reducing in Knitout Parser"""
from typing import Tuple, List

from parglare import get_collector
from parglare.parser import LRStackNode

from knit_script.knitout_optimization.knitout_structures.Knitout_Line import Knitout_Line, Version_Line
from knit_script.knitout_optimization.knitout_structures.header_operations.Carriers_Declaration import Carriers_Declaration
from knit_script.knitout_optimization.knitout_structures.header_operations.Gauge_Declaration import Gauge_Declaration
from knit_script.knitout_optimization.knitout_structures.header_operations.Header_Declaration import Header_Declaration
from knit_script.knitout_optimization.knitout_structures.header_operations.Header_Extension_Declaration import Header_Extension_Declaration
from knit_script.knitout_optimization.knitout_structures.header_operations.Machine_Declaration import Machine_Declaration
from knit_script.knitout_optimization.knitout_structures.header_operations.Position_Declaration import Position_Declaration
from knit_script.knitout_optimization.knitout_structures.header_operations.Width_Declaration import Width_Declaration
from knit_script.knitout_optimization.knitout_structures.header_operations.Yarn_Declaration import Yarn_Declaration
from knit_script.knitout_optimization.knitout_structures.knitout_instructions.Extension_Instruction import Extension_Instruction
from knit_script.knitout_optimization.knitout_structures.knitout_instructions.Pause_Instruction import Pause_Instruction
from knit_script.knitout_optimization.knitout_structures.knitout_instructions.Rack_Instruction import Rack_Instruction
from knit_script.knitout_optimization.knitout_structures.knitout_instructions.Stitch_Instruction import Stitch_Instruction
from knit_script.knitout_optimization.knitout_structures.knitout_instructions.carrier_instructions import In_Instruction, Inhook_Instruction, Releasehook_Instruction, Out_Instruction, \
    Outhook_Instruction
from knit_script.knitout_optimization.knitout_structures.knitout_instructions.needle_instructions import Knit_Instruction, Tuck_Instruction, Miss_Instruction, Split_Instruction, Drop_Instruction, \
    Amiss_Instruction, Xfer_Instruction
from knit_script.knitting_machine.machine_components.needles import Needle
from knit_script.knitting_machine.machine_components.yarn_management.Carrier_Set import Carrier_Set

action = get_collector()


@action
def program(_, __, code: List[Knitout_Line]):
    """
    :param code: Lines of code in knitout
    :param _: The parser element that created this value
    :param __:
    :return: version, head, instructions
    """
    version = -1
    head = []
    instructions = []
    for c in code:
        if isinstance(c, Version_Line):
            assert version == c.version or version < 0, f"Cannot have multiple versions of knitout {version} and {c}"
            version = c
        elif isinstance(c, Header_Declaration):
            head.append(c)
        else:
            instructions.append(c)
    return version, head, instructions


@action
def code_line(stack_node: LRStackNode, nodes: List[Knitout_Line]) -> Knitout_Line:
    """
    Processes code_line and records its location in the lines of code
    :param stack_node: stack node responsible for the line of code
    :param nodes: nodes that make up the code.
    :return: The code to be added to the program output
    """
    parser = stack_node.parser.knitout_parser
    code = nodes[0]
    if len(parser.held_comments) > 0 and not code.has_comment:
        code.comment = parser.held_comments.pop(0).comment
    parser.add_code_line(code)
    while len(parser.held_comments) > 0:
        comment = parser.held_comments.pop(0)
        parser.add_code_line(comment)
    return code


@action
def magic_string(stack_node: LRStackNode, __, v: int) -> Version_Line:
    """
    :param stack_node:  The parser element that created this value
    :param __:
    :param v: version number
    :return: v
    """
    parser = stack_node.parser.knitout_parser
    comment = parser.associate_with_comment(stack_node)
    return Version_Line(v, comment)


@action
def header_line(_, __, h_op: Header_Declaration) -> Header_Declaration:
    """
    :param _: The parser element that created this value
    :param __:
    :param h_op: operation on the line
    :return: the header operation
    """
    return h_op


@action
def machine_op(stack_node, __, m: str) -> Machine_Declaration:
    """
    :param stack_node: The parser element that created this value
    :param __:
    :param m: the machine name as a string
    :return: the machine declaration operation
    """
    parser = stack_node.parser.knitout_parser
    comment = parser.associate_with_comment(stack_node)
    return Machine_Declaration(m, comment=comment)


@action
def gauge_op(stack_node, __, g: int) -> Gauge_Declaration:
    """
    :param stack_node: The parser element that created this value
    :param __:
    :param g: gauge value
    :return: Gauge_Declaration
    """
    parser = stack_node.parser.knitout_parser
    comment = parser.associate_with_comment(stack_node)
    return Gauge_Declaration(g, comment=comment)


@action
def yarn_op(stack_node, __, C: int, yt: Tuple[int, int], color: str) -> Yarn_Declaration:
    """
    :param stack_node: The parser element that created this value
    :param __:
    :param C: The carrier to assign the yarn too.
    :param yt: The yarn gauge
    :param color: the yarn color
    :return: Yarn declaration
    """
    parser = stack_node.parser.knitout_parser
    comment = parser.associate_with_comment(stack_node)
    return Yarn_Declaration(C, size, plies, color, comment=comment)


@action
def yarn_type(_, __, l: int, r: int) -> Tuple[int, int]:
    """
    :param _: The parser element that created this value
    :param __:
    :param l:
    :param r:
    :return: yarn gauge
    """
    return l, r


@action
def carriers_op(stack_node, __, CS: Carrier_Set) -> Carriers_Declaration:
    """
    :param stack_node: The parser element that created this value
    :param __:
    :param __:
    :param CS: the carriers that are available
    :return: carrier declaration
    """
    parser = stack_node.parser.knitout_parser
    comment = parser.associate_with_comment(stack_node)
    return Carriers_Declaration(CS, comment=comment)


@action
def position_op(stack_node, __, p: str) -> Position_Declaration:
    """
    :param stack_node: The parser element that created this value
    :param __:
    :param p: the position of operations
    :return: the position declaration
    """
    parser = stack_node.parser.knitout_parser
    comment = parser.associate_with_comment(stack_node)
    return Position_Declaration(p, comment=comment)


@action
def h_extension_op(stack_node, __, code: str) -> Header_Extension_Declaration:
    """
    :param stack_node: The parser element that created this value
    :param __:
    :param code: the extension code
    :return: extension declaration
    """
    parser = stack_node.parser.knitout_parser
    comment = parser.associate_with_comment(stack_node)
    return Header_Extension_Declaration(code, comment=comment)


@action
def width_op(stack_node, __, w: int) -> Width_Declaration:
    """
    :param stack_node: The parser element that created this value
    :param __:
    :param w: width of needle bed
    :return: width declaration
    """
    parser = stack_node.parser.knitout_parser
    comment = parser.associate_with_comment(stack_node)
    return Width_Declaration(w, comment=comment)


@action
def in_op(stack_node, __, cs: Carrier_Set) -> In_Instruction:
    """
    :param stack_node: The parser element that created this value
    :param __:
    :param cs: carrier set
    :return: in operation on a carrier set
    """
    parser = stack_node.parser.knitout_parser
    comment = parser.associate_with_comment(stack_node)
    return In_Instruction(cs, comment=comment)


@action
def inhook_op(stack_node, __, cs: Carrier_Set) -> Inhook_Instruction:
    """
    :param stack_node: The parser element that created this value
    :param __:
    :param cs: Carrier set.
    :return: Inhook operation on carrier set
    """
    parser = stack_node.parser.knitout_parser
    comment = parser.associate_with_comment(stack_node)
    return Inhook_Instruction(cs, comment)


@action
def releasehook_op(stack_node, __, cs: Carrier_Set) -> Releasehook_Instruction:
    """
    :param stack_node: The parser element that created this value
    :param __:
    :param cs: carrier set
    :return: releasehook operation on carrier set
    """
    parser = stack_node.parser.knitout_parser
    comment = parser.associate_with_comment(stack_node)
    return Releasehook_Instruction(cs, comment)


@action
def out_op(stack_node, __, cs: Carrier_Set) -> Out_Instruction:
    """
    :param stack_node: The parser element that created this value
    :param __:
    :param cs: carrier set
    :return: out operation on the carrier set
    """
    parser = stack_node.parser.knitout_parser
    comment = parser.associate_with_comment(stack_node)
    return Out_Instruction(cs, comment)


@action
def outhook_op(stack_node, __, cs: Carrier_Set) -> Outhook_Instruction:
    """
    :param stack_node: The parser element that created this value
    :param __:
    :param cs: carrier set
    :return: outhook operation on the carrier set
    """
    parser = stack_node.parser.knitout_parser
    comment = parser.associate_with_comment(stack_node)
    return Outhook_Instruction(cs, comment)


@action
def stitch_op(stack_node, __, L: float, T: float) -> Stitch_Instruction:
    """
    :param stack_node: The parser element that created this value
    :param __:
    :param L: prior to loop units
    :param T: post-loop units
    :return: Stitch lengthening operation
    """
    parser = stack_node.parser.knitout_parser
    comment = parser.associate_with_comment(stack_node)
    return Stitch_Instruction(L, T, comment)


@action
def rack_op(stack_node, __, R: float) -> Rack_Instruction:
    """
    :param stack_node: The parser element that created this value
    :param __:
    :param R: rack value
    :return: rack operation
    """
    parser = stack_node.parser.knitout_parser
    comment = parser.associate_with_comment(stack_node)
    return Rack_Instruction(R, comment)


@action
def knit_op(stack_node, __, D: str, N: Needle, CS: Carrier_Set) -> Knit_Instruction:
    """
    :param stack_node: The parser element that created this value
    :param __:
    :param D: direction operates in
    :param N: needle to operate on
    :param CS: a carrier set
    :return: knit operation
    """
    parser = stack_node.parser.knitout_parser
    comment = parser.associate_with_comment(stack_node)
    return Knit_Instruction(N, D, CS, comment)


@action
def tuck_op(stack_node, __, D: str, N: Needle, CS: Carrier_Set) -> Tuck_Instruction:
    """
    :param stack_node: The parser element that created this value
    :param __:
    :param D: direction operates in
    :param N: needle to operate on
    :param CS: a carrier set
    :return: tuck operation
    """
    parser = stack_node.parser.knitout_parser
    comment = parser.associate_with_comment(stack_node)
    return Tuck_Instruction(N, D, CS, comment)


@action
def miss_op(stack_node, __, D: str, N: Needle, CS: Carrier_Set) -> Miss_Instruction:
    """
    :param stack_node: The parser element that created this value
    :param __:
    :param D: direction to operate in
    :param N: needle to operate on
    :param CS: a carrier set
    :return: miss operation
    """
    parser = stack_node.parser.knitout_parser
    comment = parser.associate_with_comment(stack_node)
    return Miss_Instruction(N, D, CS, comment)


@action
def split_op(stack_node, __, D: str, N: Needle, N2: Needle, CS: Carrier_Set) -> Split_Instruction:
    """
    :param N2: second needle to move to.
    :param stack_node: The parser element that created this value
    :param __:
    :param D: Direction operates in
    :param N: needle to operate on
    :param CS: a carrier set
    :return: knit operation
    """
    parser = stack_node.parser.knitout_parser
    comment = parser.associate_with_comment(stack_node)
    return Split_Instruction(N, D, N2, CS, comment)


@action
def drop_op(stack_node, __, N: Needle) -> Drop_Instruction:
    """
    :param stack_node: The parser element that created this value
    :param __:
    :param N: needle to drop from
    :return: drop operation
    """
    parser = stack_node.parser.knitout_parser
    comment = parser.associate_with_comment(stack_node)
    return Drop_Instruction(N, comment)


@action
def amiss_op(stack_node, __, N: Needle) -> Amiss_Instruction:
    """
    :param stack_node: The parser element that created this value
    :param __:
    :param N: needle to activate
    :return: a miss operation
    """
    parser = stack_node.parser.knitout_parser
    comment = parser.associate_with_comment(stack_node)
    return Amiss_Instruction(N, comment)


@action
def xfer_op(stack_node, __, N: Needle, N2: Needle) -> Xfer_Instruction:
    """
    :param stack_node: The parser element that created this value
    :param __:
    :param N: Needle to transfer from
    :param N2: needle to transfer to.
    :return: Xfer operation
    """
    parser = stack_node.parser.knitout_parser
    comment = parser.associate_with_comment(stack_node)
    return Xfer_Instruction(N, N2, comment)


@action
def pause_op(stack_node, __) -> Pause_Instruction:
    """
    :param stack_node:
    :param __:
    :return: pause operation
    """
    parser = stack_node.parser.knitout_parser
    comment = parser.associate_with_comment(stack_node)
    return Pause_Instruction(comment)


@action
def extension_op(stack_node, __, code: str) -> Extension_Instruction:
    """
    :param stack_node:
    :param __:
    :param code: extension code
    :return: extension operation
    """
    parser = stack_node.parser.knitout_parser
    comment = parser.associate_with_comment(stack_node)
    return Extension_Instruction(code, comment)


@action
def identifier(_, node: str) -> str:
    """
    :param _:
    :param node: identifier string
    :return: node
    """
    return node


@action
def float_exp(_, node: str) -> float:
    """
    :param _:
    :param node: float string
    :return: float conversion
    """
    digits = ""
    for c in node:
        if c.isdigit() or c == "." or c == "-":
            digits += c
    return float(digits)


@action
def int_exp(_, node: str) -> int:
    """
    :param _:
    :param node: int string
    :return: int conversion
    """
    return int(float_exp(None, node))


@action
def carrier_set(_, __, carriers: List[int]):
    """
    :param _: The parser element that created this value
    :param __:
    :param carriers: Carriers in set.
    :return: Carrier set
    """
    return Carrier_Set(carriers)
