import numpy as np



def decompose(array):
    return array.reshape(-1,1)


def add_disjonction(array, var):
    return [ i+[var] for i in array]


def Tseitin(dnf, maxi):
    next = maxi + 1

    ans=decompose(dnf[0]).tolist()

    for i in dnf[1:]:
        ans = add_disjonction(ans, -1*next) + add_disjonction(decompose(i).tolist(), next)
        next += 1
    return ans


