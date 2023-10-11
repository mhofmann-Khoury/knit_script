#sort into new list that is treated like stack
def sortCompDictPriority(posList, offList, lList):
    dictC = {p: [o, l] for (p, o, l) in zip(posList, offList, lList)}
    #print(dictC)
    sortedPDict = dict(sorted(dictC.items(), key=lambda x: x[1][1]))

    return sortedPDict
