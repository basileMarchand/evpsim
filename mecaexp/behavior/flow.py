import numpy as np

from mecaexp.behavior.base_classes import Flow
import mecaexp.tools.tenalg as tn


class NortonFlow(Flow):
    def __init__(self, K: float, n: float):
        super().__init__()
        self._coeff_k = K
        self._coeff_n = n

    def rate(self, seff: np.ndarray) -> float:
        return (seff/self._coeff_k)**self._coeff_n
    
    