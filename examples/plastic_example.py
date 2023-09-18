import json
import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import solve_ivp

from evpsim.behavior.criterion import MisesCriterion
from evpsim.behavior.flow import PlasticFlow
from evpsim.behavior.isotropic_hardening import LinearIsotropicHardening
from evpsim.behavior.kinematic_hardening import LinearKinematicHardening, NonLinearKinematicHardening
from evpsim.behavior.potential import PotentialEVP
from evpsim.behavior.genevp import GeneralizedElastoViscoPlastic
from evpsim.tools.elasticity_helper import isotropic_elasticity

from evpsim.simulator import SimuLoad, MaterialSimulator, MaterialWrapper

criterion = MisesCriterion()
flow = PlasticFlow()
iso = LinearIsotropicHardening(0.)
kin = LinearKinematicHardening(10000., 1)

pot = PotentialEVP(100., criterion, flow, iso, [], name="ep")


elas = isotropic_elasticity(110000., 0.3)
beha = GeneralizedElastoViscoPlastic(elas, [pot])

load = SimuLoad()

load.addComponent('eto11', (0., 1.),
                  (0., 0.002), repeat=1)

simu = MaterialSimulator()
simu.setDTime(1./99.)
simu.setMaterial(beha)
simu.setLoad(load)
simu.outputCycles([x for x in range(100)])
_ = simu.updateOutputShapes()

simu.compute(method="lm", options={"xtol": 1.e-2})

plt.plot(simu._strain_history[:, 0, 0], simu._stress_history[:, 0, 0])
plt.show()


data = {}
data["strain"] = simu._strain_history[:, 0, 0].tolist()
data["stress"] = simu._stress_history[:, 0, 0].tolist()

with open("plastic_perfect.json", "w") as fout:
    json.dump(data, fout)
