import numpy as np

from evpsim.behavior.base_classes import Criterion
import evpsim.tools.tenalg as tn


class MisesCriterion(Criterion):
    def __init__(self):
        super().__init__()

    def sigma_eq(self, seff: np.ndarray) -> float:
        return tn.mises(seff)

    def normal(self, seff) -> np.ndarray:
        sig_eq = self.sigma_eq(seff)
        if sig_eq < 1.e-10:
            return np.zeros((3, 3))
        return (1.5/sig_eq)*tn.deviator(seff)
