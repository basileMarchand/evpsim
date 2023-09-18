import numpy as np
from evpsim.tools import BaseMagic
from evpsim.tools import StateVariable, MathType, VarStatus


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

    def __init__(self, suffix=""):
        rename = {}
        if suffix != "":
            rename["alpha"] = f"alpha{suffix}"
        super().__init__(rename=rename)

    def compute_X(self) -> np.ndarray:
        raise NotImplementedError()

    def dalpha(self, dep: np.ndarray, epcum_rate: float) -> None:
        raise NotImplementedError()


class Potential(BaseMagic):
    def __init__(self, name="ep"):
        rename = {}
        if name != "ep":
            rename["epcum"] = f"{name}cum"
        super().__init__(rename=rename)

    def derive(self, sig: np.ndarray) -> np.ndarray:
        raise NotImplementedError()
