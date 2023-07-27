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


criterion = MisesCriterion()
flow = NortonFlow(100., 1.)
iso = LinearIsotropicHardening(0.)
kin1 = LinearKinematicHardening(10.)
pot = PotentialEVP(300., criterion, flow, iso, [])

elas = isotropic_elasticity(110000., 0.3)
beha = GeneralizedElastoViscoPlastic(elas, [pot])


n_step = 100
deto = np.zeros((3, 3))
deto[0, 0] = 1.e-2 / n_step

time = np.linspace(0, 1., n_step)
dtime = time[1:] - time[:-1]

y0 = np.zeros((beha.compute_vint_size(), ))

eto = np.zeros((3, 3))

fid = open("genevp.test", "w")

to_plot = {"eto11": [], "sig11": []}

for t, dt in zip(time, dtime):
    print(f"Increment {t} -> {t+dt}")

    beha.eto.value = eto
    beha.eto.rate = deto / dt
    beha.times = (t, dt)

    out = solve_ivp(beha, (t, t+dt), y0, method="RK45", t_eval=(t, t+dt), )
    y0 = out.y[:, -1].ravel()
    beha(t+dt, y0)
    eto += deto

    line = " ".join([f"{x:.5f}" for x in eto.ravel(
    )] + [f"{x:.5f}" for x in beha.sig.value.ravel()] + [f"{beha.potentials[0].epcum.value[0, 0]:0.5f}"])
    fid.write(line + "\n")

    to_plot["eto11"].append(eto[0, 0])
    to_plot["sig11"].append(beha.sig.value[0, 0])

fid.close()


plt.plot(to_plot["eto11"], to_plot["sig11"])
plt.show()
