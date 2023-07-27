import numpy as np
from mecaexp.tools import BaseMagic
from mecaexp.tools import StateVariable, MathType, VarStatus


class Criterion(BaseMagic):
    def sigma_eq(self, seff: np.ndarray) -> float:
        raise NotImplementedError()

    def normal(self, seff: np.ndarray) -> np.ndarray:
        raise NotImplementedError()


class Flow(BaseMagic):
    def rate(self, seff: np.ndarray) -> float:
        raise NotImplementedError()


class IsotropicHardening(BaseMagic):
    def R(self, epcum: float):
        raise NotImplementedError()


class KinematicHardening(BaseMagic):
    alpha = StateVariable(MathType.Tensor2, VarStatus.Vint)

    def __init__(self):
        super().__init__()

    def compute_X(self) -> np.ndarray:
        raise NotImplementedError()

    def dalpha(self, dep: np.ndarray, epcum_rate: float) -> None:
        raise NotImplementedError()


class Potential(BaseMagic):
    def derive(self, sig: np.ndarray) -> np.ndarray:
        raise NotImplementedError()
