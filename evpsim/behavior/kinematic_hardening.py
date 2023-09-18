import numpy as np

from evpsim.behavior.base_classes import KinematicHardening
from evpsim.tools import StateVariable, MathType, VarStatus
import evpsim.tools.tenalg as tn

C_23 = 2./3.


class LinearKinematicHardening(KinematicHardening):
    def __init__(self, C: float, suffix=""):
        self._coeff_c = C
        super().__init__(suffix=suffix)

    def compute_X(self) -> np.ndarray:
        return C_23 * self._coeff_c * self.alpha.value

    def dalpha(self, dep: np.ndarray, epcum_rate: float) -> None:
        self.alpha.rate = dep


class NonLinearKinematicHardening(KinematicHardening):
    def __init__(self, C: float, D: float, suffix=""):
        self._coeff_c = C
        self._coeff_d = D
        super().__init__(suffix=suffix)

    def compute_X(self) -> np.ndarray:
        return C_23 * self._coeff_c * self.alpha.value

    def dalpha(self, dep: np.ndarray, epcum_rate: float) -> None:
        self.alpha.rate = dep - self._coeff_d*epcum_rate*self.alpha.value
