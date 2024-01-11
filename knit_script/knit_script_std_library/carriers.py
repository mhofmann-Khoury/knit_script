from knit_script.knitting_machine.Machine_State import Machine_State
from knit_script.knitting_machine.machine_components.yarn_management.Carrier import Carrier


def carrier(machine_state: Machine_State, carrier_id: int) -> Carrier:
    return machine_state.carrier_system[carrier_id]
