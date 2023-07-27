
from typing import List
import numpy as np

from mecaexp.behavior import Behavior
from mecaexp.behavior.base_classes import Potential


from mecaexp.tools import StateVariable, MathType, VarStatus, BaseMagic


class GeneralizedElastoViscoPlastic(Behavior):
    sig = StateVariable(MathType.Tensor2, VarStatus.Vout)
    eto = StateVariable(MathType.Tensor2, VarStatus.Vin)
    eel = StateVariable(MathType.Tensor2, VarStatus.Vint)

    def __init__(self, elasticity, potentials: List[Potential]):

        self.elasticity = elasticity
        self.potentials = potentials
        for pot in self.potentials:
            pot.link_to(self)

        super().__init__()

    def derive(self) -> None:
        self.sig.value = np.einsum(
            "ijkl,kl->ij", self.elasticity, self.eel.value)
        dep = np.zeros((3, 3))
        for pot in self.potentials:
            dep += pot.derive(self.sig.value)

        self.eel.rate = self.eto.rate - dep
