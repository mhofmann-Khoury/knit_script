def sortD(diction):
    sortedDict = dict(sorted(diction.items(), key=lambda x: x[1]))
    return sortedDict


