from knit_script.knitout_optimization.knitout_structures.header_operations.Header_Declaration import Header_Declaration, Header_Operation
from knit_script.knitout_optimization.knitout_structures.knitout_values.Carrier_Set import Carrier_Set


class Carriers_Declaration(Header_Declaration):
    def __init__(self, carrier_set: Carrier_Set):
        super().__init__(Header_Operation.Carriers)
        self.carrier_set = carrier_set

    def __str__(self):
        return f";;{self.operation}: {self.carrier_set};{self.comment_str}\n"
