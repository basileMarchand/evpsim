import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import solve_ivp

from evpsim.behavior.criterion import MisesCriterion
from evpsim.behavior.flow import NortonFlow
from evpsim.behavior.isotropic_hardening import LinearIsotropicHardening
from evpsim.behavior.kinematic_hardening import LinearKinematicHardening, NonLinearKinematicHardening
from evpsim.behavior.potential import PotentialEVP
from evpsim.behavior.genevp import GeneralizedElastoViscoPlastic
from evpsim.tools.elasticity_helper import isotropic_elasticity

from evpsim.simulator import SimuLoad, MaterialSimulator, MaterialWrapper

criterion = MisesCriterion()
flow = NortonFlow(100., 1.)
iso = LinearIsotropicHardening(300.)
kin1 = NonLinearKinematicHardening(60000., 400., 0)
kin2 = NonLinearKinematicHardening(120000., 400., 1)

pot = PotentialEVP(100., criterion, flow, iso, [kin1, kin2], name="ep")

criterion2 = MisesCriterion()
flow2 = NortonFlow(1000., 10.)
iso2 = LinearIsotropicHardening(0.)
pot2 = PotentialEVP(0., criterion2, flow2, iso2, [], name="ev")

elas = isotropic_elasticity(110000., 0.3)
beha = GeneralizedElastoViscoPlastic(elas, [pot, pot2])

load = SimuLoad()

load.addComponent('eto11', (0., 0.25, 0.5, 0.75, 1.),
                  (0., 0.01, 0., -0.01, 0.), repeat=1)
load.addComponent('eto11', (0., 0.5, 1., 1.5, 2.),
                  (0., 0.015, 0., -0.015, 0.), repeat=1)
simu = MaterialSimulator()
simu.setDTime(1./99.)
simu.setMaterial(beha)
simu.setLoad(load)
simu.outputCycles([x for x in range(100)])
_ = simu.updateOutputShapes()

simu.compute(method="lm", options={"xtol": 1.e-2})

plt.plot(simu._strain_history[:, 0, 0], simu._stress_history[:, 0, 0])
plt.show()
