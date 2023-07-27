import numpy as np

from mecaexp.behavior.base_classes import KinematicHardening
from mecaexp.tools import StateVariable, MathType, VarStatus
import mecaexp.tools.tenalg as tn

C_23 = 2./3.


class LinearKinematicHardening(KinematicHardening):
    def __init__(self, C: float):
        self._coeff_c = C
        super().__init__()

    def compute_X(self) -> np.ndarray:
        return C_23 * self._coeff_c * self.alpha.value

    def dalpha(self, dep: np.ndarray, epcum_rate: float) -> None:
        self.alpha.rate = dep


class NonLinearKinematicHardening(KinematicHardening):
    def __init__(self, C: float, D: float):
        self._coeff_c = C
        self._coeff_d = D
        super().__init__()

    def compute_X(self) -> np.ndarray:
        return C_23 * self._coeff_c * self.alpha.value

    def dalpha(self, dep: np.ndarray, epcum_rate: float) -> None:
        self.alpha.rate = dep - self._coeff_d*epcum_rate*self.alpha.value
