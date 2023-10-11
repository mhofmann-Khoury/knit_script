from knit_script.knitting_machine.machine_components.needles import Needle
def rackVal(needle1, needle2):
    if (needle1.is_front == True and needle2.is_front == True) or (needle1.is_front == False and needle2.is_front == False): #on same bed
        return 0
    elif(needle1.is_front == True):
        r = needle1.position - needle2.position  # r = f - b
        return r
    elif (needle2.is_front == True):
        r = needle2.position - needle1.position  # r = f - b
        return r