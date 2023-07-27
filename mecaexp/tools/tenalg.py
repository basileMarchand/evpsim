import numpy as np


def trace(s):
    return np.einsum("ii", s)


def deviator(s):
    return s - (1./3.)*trace(s)*np.eye(3)


def mises(s):
    d = deviator(s)
    return np.sqrt(1.5 * np.einsum("ij,ji", d, d))


def kronecker(i, j):
    return 1. if i == j else 0


def I4():
    I = np.zeros((3, 3, 3, 3))
    for i in range(3):
        for j in range(3):
            for k in range(3):
                for l in range(3):
                    I[i, j, k, l] = kronecker(i, k) * kronecker(j, l)
    return I


def K4():
    I = np.zeros((3, 3, 3, 3))
    for i in range(3):
        for j in range(3):
            for k in range(3):
                for l in range(3):
                    I[i, j, k, l] = 1/3. * kronecker(i, j) * kronecker(k, l)
    return I


def J4():
    return I4() - K4()
