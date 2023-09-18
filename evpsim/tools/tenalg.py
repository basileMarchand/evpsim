import numpy as np
import math
from numba import njit, float64

I2 = np.eye(3)


@njit(float64(float64[:, :]))
def trace(s):
    return s[0, 0]+s[1, 1]+s[2, 2]


C_13 = 1./3.


@njit(float64[:, :](float64[:, :]))
def deviator(s):
    t = trace(s)
    return s - C_13 * t*I2


@njit(float64(float64[:, :]))
def mises(s):
    d = deviator(s)
    dd = d*d
    sum_s = dd[0, 0]+2*dd[0, 1]+2*dd[0, 2] + dd[1, 1] + 2*dd[1, 2] + dd[2, 2]
    return math.sqrt(1.5 * sum_s)


def kronecker(i, j):
    return 1. if i == j else 0


def _I4():
    I = np.zeros((3, 3, 3, 3))
    for i in range(3):
        for j in range(3):
            for k in range(3):
                for l in range(3):
                    I[i, j, k, l] = kronecker(i, k) * kronecker(j, l)
    return I


def _K4():
    I = np.zeros((3, 3, 3, 3))
    for i in range(3):
        for j in range(3):
            for k in range(3):
                for l in range(3):
                    I[i, j, k, l] = 1/3. * kronecker(i, j) * kronecker(k, l)
    return I


def _J4():
    return _I4() - _K4()


def outer_ikjl(u: np.ndarray, v: np.ndarray):
    ret = np.zeros((3, 3, 3, 3))
    for i in (0, 1, 2):
        for j in (0, 1, 2):
            for k in (0, 1, 2):
                for l in (0, 1, 2):
                    ret[i, j, k, l] = u[i, k]*v[j, l]
    return ret


I4 = _I4()
K4 = _K4()
J4 = _J4()

if __name__ == "__main__":
    a = np.random.rand(3, 3)
    b = np.random.rand(3, 3)

    c1 = outer_ikjl(a, b)
