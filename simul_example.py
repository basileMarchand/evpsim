import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import solve_ivp

from mecaexp.behavior.criterion import MisesCriterion
from mecaexp.behavior.flow import NortonFlow
from mecaexp.behavior.isotropic_hardening import LinearIsotropicHardening
from mecaexp.behavior.kinematic_hardening import LinearKinematicHardening
from mecaexp.behavior.potential import PotentialEVP
from mecaexp.behavior.genevp import GeneralizedElastoViscoPlastic
from mecaexp.tools.elasticity_helper import isotropic_elasticity

from mecaexp.simulator import SimuLoad, MaterialSimulator, MaterialWrapper

criterion = MisesCriterion()
flow = NortonFlow(100., 10.)
iso = LinearIsotropicHardening(300.)
kin1 = LinearKinematicHardening(1500.)
pot = PotentialEVP(300., criterion, flow, iso, [kin1])
elas = isotropic_elasticity(110000., 0.3)
beha = GeneralizedElastoViscoPlastic(elas, [pot])

load = SimuLoad()
load.addComponent('eto11', (0., 0.5, 1.), (0., 0.05, 0.), repeat=4)

simu = MaterialSimulator()
simu.setDTime(1./40.)
simu.setMaterial(beha)
simu.setLoad(load)
simu.outputCycles((0, 1, 2, 3))
_ = simu.updateOutputShapes()

simu.compute()

plt.plot(simu._strain_history[:, 0, 0], simu._stress_history[:, 0, 0])
plt.show()
