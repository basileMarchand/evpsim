import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import solve_ivp

from mecaexp.behavior.criterion import MisesCriterion
from mecaexp.behavior.flow import NortonFlow
from mecaexp.behavior.isotropic_hardening import LinearIsotropicHardening
from mecaexp.behavior.kinematic_hardening import LinearKinematicHardening, NonLinearKinematicHardening
from mecaexp.behavior.potential import PotentialEVP
from mecaexp.behavior.genevp import GeneralizedElastoViscoPlastic
from mecaexp.tools.elasticity_helper import isotropic_elasticity

from mecaexp.simulator import SimuLoad, MaterialSimulator, MaterialWrapper

criterion = MisesCriterion()
flow = NortonFlow(100., 1.)
iso = LinearIsotropicHardening(0.)
kin1 = NonLinearKinematicHardening(30000., 200., 0)
pot = PotentialEVP(100., criterion, flow, iso, [kin1], name="ep")

elas = isotropic_elasticity(110000., 0.3)
beha = GeneralizedElastoViscoPlastic(elas, [pot])

load = SimuLoad()

load.addComponent('sig11', (0., 0.25, 0.5, 0.75, 1.),
                  (0., 200, 0., -100, 0.), repeat=4)
simu = MaterialSimulator()
simu.setDTime(1./99.)
simu.setMaterial(beha)
simu.setLoad(load)
simu.outputCycles([x for x in range(100)])
_ = simu.updateOutputShapes()

simu.compute(method="lm", options={"xtol": 1.e-2})

plt.plot(simu._strain_history[:, 0, 0], simu._stress_history[:, 0, 0])
plt.show()
