"""Structures for Machine headers"""

from knit_script.knit_graphs.Yarn import Yarn
from knit_script.knitout_interpreter.knitout_structures.Knitout_Line import Knitout_Line, Version_Line
from knit_script.knitout_interpreter.knitout_structures.header_operations.Carriers_Declaration import Carriers_Declaration
from knit_script.knitout_interpreter.knitout_structures.header_operations.Gauge_Declaration import Gauge_Declaration
from knit_script.knitout_interpreter.knitout_structures.header_operations.Header_Declaration import Header_Declaration
from knit_script.knitout_interpreter.knitout_structures.header_operations.Machine_Declaration import Machine_Declaration
from knit_script.knitout_interpreter.knitout_structures.header_operations.Position_Declaration import Position_Declaration
from knit_script.knitout_interpreter.knitout_structures.header_operations.Width_Declaration import Width_Declaration
from knit_script.knitout_interpreter.knitout_structures.header_operations.Yarn_Declaration import Yarn_Declaration
from knit_script.knitting_machine.Machine_State import Machine_State
from knit_script.knitting_machine.machine_components.machine_position import Machine_Position
from knit_script.knitting_machine.machine_components.yarn_management.Carrier_Set import Carrier_Set
from knit_script.knitting_machine.machine_specification.Header_ID import Header_ID
from knit_script.knitting_machine.machine_specification.Machine_Type import Machine_Type


class Header:
    """A class structure for generating knitout header files"""

    def __init__(self, width: int = 540,
                 position: Machine_Position = Machine_Position.Right,
                 carrier_count: int = 10, machine_type: Machine_Type = Machine_Type.SWG091N2,
                 max_rack: float = 4.25, hook_size: int = 5, gauge: int = 15):
        self.gauge = gauge
        self.max_rack = max_rack
        self.hook_size = hook_size
        self.machine_type = machine_type
        self.width = width
        self.carrier_count = carrier_count
        self.carriers_to_yarns: dict[int, None | Yarn] = {i: None for i in range(1, self.carrier_count + 1)}
        self.position = position
        self.declarations: dict[Header_ID: None | Header_Declaration] = {hid: None for hid in Header_ID}
        self.extensions: list[str] = []

    def set_value(self, header_id: Header_ID, value):
        """
        Set the header value by id
        :param header_id: Value to set in the header
        :param value: value to set it to
        """
        if header_id is Header_ID.Machine:
            if isinstance(value, str):
                value = Machine_Type[value]
            assert isinstance(value, Machine_Type), f"Expected String for Machine Type but got {value}"
            self.machine_type = value
        elif header_id is Header_ID.Carrier_Count:
            assert isinstance(value, int), f"Expected carrier count but got {value}"
            self.carrier_count = value
        elif header_id is Header_ID.Width:
            assert isinstance(value, int), f"Expected width but got {value}"
            self.width = value
        elif header_id is Header_ID.Gauge:
            assert isinstance(value, int), f"Expected gauge but got {value}"
            self.gauge = value
        elif header_id is Header_ID.Position:
            assert isinstance(value, Machine_Position), \
                f"Expected machine position [left, right, center, keep] but got {value}"
            self.position = value
        elif header_id is Header_ID.Rack:
            assert isinstance(value, float) or isinstance(value, int), f"Expected racking value but got {value}"
            self.max_rack = float(value)
        elif header_id is Header_ID.Hook:
            assert isinstance(value, int), f"Expected hook size but got {value}"
            self.hook_size = value
        elif header_id is Header_ID.Yarn:
            assert isinstance(value, tuple) and len(value) == 2, f"Expected tuple of carrier id and yarn but got {value}"
            cid = value[0]
            assert isinstance(cid, int) and 1 <= cid <= self.carrier_count, f"Expected carrier between 1 and {self.carrier_count} but got {cid}"
            yarn = value[1]
            assert isinstance(yarn, Yarn), f"Expected a yarn but got {yarn}"
            self.carriers_to_yarns[cid] = yarn

    def get_value(self, header_id: Header_ID):
        """
        Set the header value by id
        :param header_id: Value to set in the header
        """
        if header_id is Header_ID.Machine:
            return self.machine_type
        elif header_id is Header_ID.Carrier_Count:
            return self.carrier_count
        elif header_id is Header_ID.Width:
            return self.width
        elif header_id is Header_ID.Gauge:
            return self.gauge
        elif header_id is Header_ID.Position:
            return self.position
        elif header_id is Header_ID.Rack:
            return self.max_rack
        elif header_id is Header_ID.Hook:
            return self.hook_size
        return None

    def update_by_declaration(self, code: Header_Declaration) -> bool:
        """
        Update the header or error on redundant code
        :param code: header code to update by
        :return: True if the header is updated
        """
        caused_update = code.add_to_header(self)
        self.declarations[code.operation] = code
        return caused_update

    def overwriting_declaration(self, code: Header_Declaration) -> bool:
        """
        :param code: header declaration trying to overwrite header
        :return: True if the code overwrites some other declaration
        """
        if self.declarations[code.operation] is None:
            return False
        else:
            return self.declarations[code.operation] == code

    def machine_state(self) -> Machine_State:
        """
        :return: A reset machine state with given specifications
        """
        machine_state = Machine_State(self.width, self.max_rack, self.carrier_count, self.hook_size)
        for cid, yarn in self.carriers_to_yarns.items():  # update yarns on the carriers
            if yarn is not None:
                machine_state.carrier_system[cid].yarn = yarn
        return machine_state

    def header_lines(self) -> list[Knitout_Line]:
        """
        :return: Lines of the knitout header
        """
        lines = [Version_Line(2)]
        lines.extend(self.header_declarations())
        return lines

    def header_declarations(self) -> list[Header_Declaration]:
        """
        :return: header declarations needed to make this header in knitout
        """
        header = [
            Carriers_Declaration(Carrier_Set.carrier_set_by_count(self.carrier_count)),
            Machine_Declaration(self.machine_type.value),
            Gauge_Declaration(self.gauge),
            Width_Declaration(self.width),
            Position_Declaration(str(self.position)),
        ]
        for cid, yarn in self.carriers_to_yarns.items():
            if yarn is not None:
                header.append(Yarn_Declaration(cid, yarn.size, yarn.plies, yarn.color))
        return header
