from knitout_interpreter.knitout_operations.carrier_instructions import Outhook_Instruction
from virtual_knitting_machine.Knitting_Machine import Knitting_Machine
from virtual_knitting_machine.machine_components.yarn_management.Yarn_Carrier import Yarn_Carrier


def carrier(machine_state: Knitting_Machine, carrier_id: int) -> Yarn_Carrier:
    """
    :param machine_state:
    :param carrier_id:
    :return: The carrier in the virtual knitting machine indexed by the carrier_id.
    """
    return machine_state.carrier_system[carrier_id]


def cut_active_carriers(machine_state: Knitting_Machine) -> list[Outhook_Instruction]:
    """
    :param machine_state:
    :return: A list of outhook instructions that cut all active carriers in the machine state.
    """
    outhooks = [Outhook_Instruction(c, f"Outhooking all active carriers") for c in machine_state.carrier_system.active_carriers]
    for outhook in outhooks:
        outhook.execute(machine_state)
    return outhooks
