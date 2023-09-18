from typing import List
import numpy as np

from evpsim.behavior.base_classes import Potential, Criterion, Flow, IsotropicHardening, KinematicHardening
from evpsim.tools import StateVariable, MathType, VarStatus


class PotentialEVP(Potential):
    # Variables
    epcum = StateVariable(MathType.Scalar, VarStatus.Vint)

    def __init__(self, R0, criterion: Criterion, flow: Flow, isotropic: IsotropicHardening, kinematics: List[KinematicHardening], name="ep"):
        super().__init__(name=name)
        self.R0 = R0
        self.criterion = criterion
        self.criterion.link_to(self)
        self.flow = flow
        self.flow.link_to(self)
        self.isotropic = isotropic
        self.isotropic.link_to(self)
        self.kinematics = kinematics
        for kin in self.kinematics:
            kin.link_to(self)

    def derive(self, sig: np.ndarray) -> np.ndarray:
        X = np.zeros((3, 3))
        for kin in self.kinematics:
            X += kin.compute_X()

        seq = self.criterion.sigma_eq(sig - X)
        R = self.R0 + self.isotropic.R(self.epcum.value)

        dep = np.zeros((3, 3))
        if seq - R <= 0.:
            self.epcum.rate = 0.
            dep[:, :] = 0.
        else:
            rate = self.flow.rate(seq - R)
            self.epcum.rate = rate
            dep = rate * self.criterion.normal(sig - X)

        for kin in self.kinematics:
            kin.dalpha(dep, self.epcum.rate)

        return dep
