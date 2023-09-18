import numpy as np
import math 

from mecaexp.behavior.base_classes import Flow
import mecaexp.tools.tenalg as tn


class NortonFlow(Flow):
    def __init__(self, K: float, n: float):
        super().__init__()
        self._coeff_k_inv = 1./K
        self._coeff_n = n

    def rate(self, seff: np.ndarray) -> float:
        return math.pow(seff*self._coeff_k_inv, self._coeff_n)
    
    