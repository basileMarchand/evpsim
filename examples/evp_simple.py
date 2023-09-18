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
pot = PotentialEVP(100., criterion, flow, iso, [kin1], name="ep")


elas = isotropic_elasticity(110000., 0.3)
beha = GeneralizedElastoViscoPlastic(elas, [pot])

load = SimuLoad()

t_end = 0.005

load.addComponent('eto11', (0., t_end),
                  (0., 0.01), repeat=1)

simu = MaterialSimulator()
simu.setDTime(t_end/200.)
simu.setMaterial(beha)
simu.setLoad(load)
simu.outputCycles([x for x in range(100)])
_ = simu.updateOutputShapes()

simu.compute(method="lm", options={"xtol": 1.e-2})

plt.plot(simu._strain_history[:, 0, 0], simu._stress_history[:, 0, 0])
plt.show()

data = np.hstack([simu._strain_history[:, 0, 0].reshape(
    (-1, 1)), simu._stress_history[:, 0, 0].reshape((-1, 1))])

np.savetxt("output001.dat", data)
