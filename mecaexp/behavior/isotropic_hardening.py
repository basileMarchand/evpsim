import numpy as np

from mecaexp.behavior.base_classes import IsotropicHardening

class NoneIsotropicHardening(IsotropicHardening):
    def __init__(self, H: float):
        super().__init__()
        self._coeff_h = H

    def R(self, epcum: float) -> float:
        return 0.

class LinearIsotropicHardening(IsotropicHardening):
    def __init__(self, H: float):
        super().__init__()
        self._coeff_h = H

    def R(self, epcum: float) -> float:
        return self._coeff_h * epcum

    