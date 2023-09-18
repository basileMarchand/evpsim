import numpy as np
import math

from evpsim.behavior.base_classes import Flow
import evpsim.tools.tenalg as tn


class NortonFlow(Flow):
    def __init__(self, K: float, n: float):
        super().__init__()
        self._coeff_k_inv = 1./K
        self._coeff_n = n

    def rate(self, seff: np.ndarray) -> float:
        return math.pow(seff*self._coeff_k_inv, self._coeff_n)


class PlasticFlow(Flow):
    def __init__(self):
        super().__init__()

    def rate(self, seff: np.ndarray) -> float:
        return seff*1.e-1
