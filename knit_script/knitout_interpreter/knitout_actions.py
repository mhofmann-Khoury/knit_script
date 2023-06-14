"""Actions for reducing in Knitout Parser"""
from typing import Tuple, List, Optional

from parglare import get_collector

from knit_script.knitout_interpreter.knitout_structures.Knitout_Line import Knitout_Line, Version_Line, Comment_Line
from knit_script.knitout_interpreter.knitout_structures.header_operations.Carriers_Declaration import Carriers_Declaration
from knit_script.knitout_interpreter.knitout_structures.header_operations.Gauge_Declaration import Gauge_Declaration
from knit_script.knitout_interpreter.knitout_structures.header_operations.Header_Declaration import Header_Declaration
from knit_script.knitout_interpreter.knitout_structures.header_operations.Header_Extension_Declaration import Header_Extension_Declaration
from knit_script.knitout_interpreter.knitout_structures.header_operations.Machine_Declaration import Machine_Declaration
from knit_script.knitout_interpreter.knitout_structures.header_operations.Position_Declaration import Position_Declaration
from knit_script.knitout_interpreter.knitout_structures.header_operations.Width_Declaration import Width_Declaration
from knit_script.knitout_interpreter.knitout_structures.header_operations.Yarn_Declaration import Yarn_Declaration
from knit_script.knitout_interpreter.knitout_structures.knitout_instructions.Extension_Instruction import Extension_Instruction
from knit_script.knitout_interpreter.knitout_structures.knitout_instructions.Pause_Instruction import Pause_Instruction
from knit_script.knitout_interpreter.knitout_structures.knitout_instructions.Rack_Instruction import Rack_Instruction
from knit_script.knitout_interpreter.knitout_structures.knitout_instructions.Stitch_Instruction import Stitch_Instruction
from knit_script.knitout_interpreter.knitout_structures.knitout_instructions.carrier_instructions import In_Instruction, Inhook_Instruction, Releasehook_Instruction, Out_Instruction, \
    Outhook_Instruction
from knit_script.knitout_interpreter.knitout_structures.knitout_instructions.needle_instructions import Knit_Instruction, Tuck_Instruction, Miss_Instruction, Split_Instruction, Drop_Instruction, \
    Amiss_Instruction, Xfer_Instruction
from knit_script.knitting_machine.machine_components.needles import Needle, Slider_Needle
from knit_script.knitting_machine.machine_components.yarn_management.Carrier_Set import Carrier_Set

action = get_collector()


@action
def comment(_, __, content: Optional[str]) -> Optional[str]:
    return content


@action
def code_line(_, __, c: Optional[Knitout_Line], com: Optional[str]) -> Optional[Knitout_Line]:
    if c is None:
        if com is None:
            return None
        c = Comment_Line(comment=com)
    if com is not None:
        c.comment = com
    return c


@action
def magic_string(_, __, v: int) -> Version_Line:
    """
    :param _:  The parser element that created this value
    :param __:
    :param v: version number
    :return: v
    """
    return Version_Line(v)


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
def machine_op(_, __, m: str) -> Machine_Declaration:
    """
    :param _: The parser element that created this value
    :param __:
    :param m: the machine name as a string
    :return: the machine declaration operation
    """
    return Machine_Declaration(m)


@action
def gauge_op(_, __, g: int) -> Gauge_Declaration:
    """
    :param _: The parser element that created this value
    :param __:
    :param g: gauge value
    :return: Gauge_Declaration
    """
    return Gauge_Declaration(g)


@action
def yarn_op(_, __, C: int, size: int, plies: int, color: str) -> Yarn_Declaration:
    """
    :param plies:
    :param size:
    :param _: The parser element that created this value
    :param __:
    :param C: The carrier to assign the yarn too.
    :param color: The yarn color
    :return: Yarn declaration
    """
    return Yarn_Declaration(C, size, plies, color)


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
def carriers_op(_, __, CS: Carrier_Set) -> Carriers_Declaration:
    """
    :param _: The parser element that created this value
    :param __:
    :param __:
    :param CS: the carriers that are available
    :return: carrier declaration
    """
    return Carriers_Declaration(CS)


@action
def position_op(_, __, p: str) -> Position_Declaration:
    """
    :param _: The parser element that created this value
    :param __:
    :param p: the position of operations
    :return: the position declaration
    """
    return Position_Declaration(p)


@action
def h_extension_op(_, __, code: str) -> Header_Extension_Declaration:
    """
    :param _: The parser element that created this value
    :param __:
    :param code: the extension code
    :return: extension declaration
    """
    return Header_Extension_Declaration(code)


@action
def width_op(_, __, w: int) -> Width_Declaration:
    """
    :param _: The parser element that created this value
    :param __:
    :param w: width of needle bed
    :return: width declaration
    """
    return Width_Declaration(w)


@action
def in_op(_, __, cs: Carrier_Set) -> In_Instruction:
    """
    :param _: The parser element that created this value
    :param __:
    :param cs: carrier set
    :return: in operation on a carrier set
    """
    return In_Instruction(cs)


@action
def inhook_op(_, __, cs: Carrier_Set) -> Inhook_Instruction:
    """
    :param _: The parser element that created this value
    :param __:
    :param cs: Carrier set.
    :return: Inhook operation on carrier set
    """
    return Inhook_Instruction(cs)


@action
def releasehook_op(_, __, cs: Carrier_Set) -> Releasehook_Instruction:
    """
    :param _: The parser element that created this value
    :param __:
    :param cs: carrier set
    :return: releasehook operation on carrier set
    """
    return Releasehook_Instruction(cs)


@action
def out_op(_, __, cs: Carrier_Set) -> Out_Instruction:
    """
    :param _: The parser element that created this value
    :param __:
    :param cs: carrier set
    :return: out operation on the carrier set
    """
    return Out_Instruction(cs)


@action
def outhook_op(_, __, cs: Carrier_Set) -> Outhook_Instruction:
    """
    :param _: The parser element that created this value
    :param __:
    :param cs: carrier set
    :return: outhook operation on the carrier set
    """
    return Outhook_Instruction(cs)


@action
def stitch_op(_, __, L: float, T: float) -> Stitch_Instruction:
    """
    :param _: The parser element that created this value
    :param __:
    :param L: prior to loop units
    :param T: post-loop units
    :return: Stitch lengthening operation
    """
    return Stitch_Instruction(L, T)


@action
def rack_op(_, __, R: float) -> Rack_Instruction:
    """
    :param _: The parser element that created this value
    :param __:
    :param R: rack value
    :return: rack operation
    """
    return Rack_Instruction(R)


@action
def knit_op(_, __, D: str, N: Needle, CS: Carrier_Set) -> Knit_Instruction:
    """
    :param _: The parser element that created this value
    :param __:
    :param D: direction operates in
    :param N: needle to operate on
    :param CS: a carrier set
    :return: knit operation
    """
    return Knit_Instruction(N, D, CS)


@action
def tuck_op(_, __, D: str, N: Needle, CS: Carrier_Set) -> Tuck_Instruction:
    """
    :param _: The parser element that created this value
    :param __:
    :param D: direction operates in
    :param N: needle to operate on
    :param CS: a carrier set
    :return: tuck operation
    """
    return Tuck_Instruction(N, D, CS)


@action
def miss_op(_, __, D: str, N: Needle, CS: Carrier_Set) -> Miss_Instruction:
    """
    :param _: The parser element that created this value
    :param __:
    :param D: direction to operate in
    :param N: needle to operate on
    :param CS: a carrier set
    :return: miss operation
    """
    return Miss_Instruction(N, D, CS)


@action
def split_op(_, __, D: str, N: Needle, N2: Needle, CS: Carrier_Set) -> Split_Instruction:
    """
    :param N2: second needle to move to.
    :param _: The parser element that created this value
    :param __:
    :param D: Direction operates in
    :param N: needle to operate on
    :param CS: a carrier set
    :return: knit operation
    """
    return Split_Instruction(N, D, N2, CS)


@action
def drop_op(_, __, N: Needle) -> Drop_Instruction:
    """
    :param _: The parser element that created this value
    :param __:
    :param N: needle to drop from
    :return: drop operation
    """
    return Drop_Instruction(N)


@action
def amiss_op(_, __, N: Needle) -> Amiss_Instruction:
    """
    :param _: The parser element that created this value
    :param __:
    :param N: needle to activate
    :return: a miss operation
    """
    return Amiss_Instruction(N)


@action
def xfer_op(_, __, N: Needle, N2: Needle) -> Xfer_Instruction:
    """
    :param _: The parser element that created this value
    :param __:
    :param N: Needle to transfer from
    :param N2: needle to transfer to.
    :return: Xfer operation
    """
    return Xfer_Instruction(N, N2)


@action
def pause_op(_, __) -> Pause_Instruction:
    """
    :param _:
    :param __:
    :return: pause operation
    """
    return Pause_Instruction()


@action
def extension_op(_, __, code: str) -> Extension_Instruction:
    """
    :param _:
    :param __:
    :param code: extension code
    :return: extension operation
    """
    return Extension_Instruction(code)


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
def needle_id(_, node: str) -> Needle:
    is_front = "f" in node
    slider = "s" in node
    num_str = node[1:]  # cut bed off
    if slider:
        num_str = node[1:]  # cut slider off
    pos = int(num_str)
    if slider:
        return Slider_Needle(is_front, pos)
    else:
        return Needle(is_front, pos)


@action
def carrier_set(_, __, carriers: List[int]):
    """
    :param _: The parser element that created this value
    :param __:
    :param carriers: Carriers in set.
    :return: Carrier set
    """
    return Carrier_Set(carriers)
