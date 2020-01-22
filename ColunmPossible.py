import numpy as np


def generatePossibleColunm(array, size):
    first_length = array[0]
    if first_length < 1:
        return [dict()]
    array = np.array(array)[1:]
    array = array[array>0]
    ret = []
    for p in range(int(size-(np.sum(array)+array.shape[0])-first_length+1)):
        d = dict()
        d[0] = p
        d[1] = p+first_length-1
        ret.append(d)
    return buildPossibility(ret, 2, size, array)


def buildPossibility(current, pos, size, left):
    if (left.shape[0] == 0):
        return current
    length = left[0]
    ret = []
    next = left[1:]
    for dict in current:
        for p in range(int(dict[pos - 1]+2), int(size-(np.sum(next)+next.shape[0])-length+1)):
            d = dict.copy()
            d[pos] = p
            d[pos+1] = p+length-1
            ret.append(d)
    return buildPossibility(ret, pos+2, size, next)

