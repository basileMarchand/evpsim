import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import solve_ivp

from mecaexp.behavior.criterion import MisesCriterion
from mecaexp.behavior.flow import NortonFlow
from mecaexp.behavior.isotropic_hardening import LinearIsotropicHardening
from mecaexp.behavior.kinematic_hardening import LinearKinematicHardening, NonLinearKinematicHardening
from mecaexp.behavior.potential import PotentialEVP
from mecaexp.behavior.genevp import GeneralizedElastoViscoPlastic
from mecaexp.tools.elasticity_helper import transverse_elasticity

from mecaexp.simulator import SimuLoad, MaterialSimulator, LocalFrame

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

elas = transverse_elasticity(160_000., 200_000., 0.3, 0.3, 80_000.)
beha = GeneralizedElastoViscoPlastic(elas, [pot, pot2])

load = SimuLoad()


load.addComponent('eto11', (0., 0.75),
                  (0., 0.015), )


eto_start = 0.015
eto_incr = 0.005
factor = 10.
jump = 10
for i in range(jump):
    if i % 2 == 0:
        time_end = 0.25/factor
    else:
        time_end = 0.25
    eto_end = eto_start + eto_incr
    load.addComponent('eto11', (0., time_end), (eto_start, eto_end))
    eto_start = eto_end


local = LocalFrame(np.array([1., 1., 0.]), np.array([-1., 1., 0.]))


simu = MaterialSimulator()
simu.setDTime(1./100.)
simu.setMaterial(beha)
simu.setLoad(load)


simu.setLocalFrame( local )
#simu.outputCycles([x for x in range(100)])
_ = simu.updateOutputShapes()

simu.compute(method="lm", options={"xtol": 1.e-2})

plt.plot(simu._strain_history[:, 0, 0], simu._stress_history[:, 0, 0])
plt.show()
