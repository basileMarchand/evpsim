from scipy.optimize import root
from scipy.integrate import solve_ivp
import numpy as np

from evpsim.simulator.simulator_load import SimuLoad
from evpsim.simulator.rotation import LocalFrame
from evpsim.behavior import Behavior


class MaterialWrapper(object):
    def __init__(self, behavior: Behavior):
        self._behavior = behavior
        self._local = None
        self.vint = None
        self.stress = None
        self.imposed_stress = None
        self.strain = None
        self.dstrain = None
        self.noel = 1
        self.time = None
        self.dtime = None

        self.rMatrix = None
        self.free_stress_idx = None

    def getNbVars(self) -> int:
        return self._behavior.compute_vint_size()

    def func(self, x, save=False):
        strain = self.strain.copy()
        dstrain = self.dstrain.copy()
        dstrain.ravel()[self.free_stress_idx] = x

        if self._local:
            strain = self._local.rotate_tensor2_to_material(strain)
            dstrain = self._local.rotate_tensor2_to_material(dstrain)

        self._behavior.eto.value = strain
        self._behavior.eto.rate = dstrain / self.dtime
        self._behavior.times = (self.time[0], self.dtime)

        y0 = self.vint.copy()
        out = solve_ivp(self._behavior, self.time, y0,
                        method="RK23", t_eval=self.time, rtol=1.e-6, atol=1.e-9)

        stress = self._behavior.sig.value[:]

        if self._local:
            stress = self._local.rotate_tensor2_from_material(stress)
            strain = self._local.rotate_tensor2_from_material(strain)
            dstrain = self._local.rotate_tensor2_from_material(dstrain)

        if save is True:
            self.stress[:, :] = stress
            self.strain[:, :] = strain[:] + dstrain[:]
            self.vint[:] = out.y[:, -1].ravel()
            self.dstrain[:, :] = dstrain[:, :]
        stress_diff = stress - self.imposed_stress
        return (self.rMatrix @ stress_diff.reshape((-1, 1))).ravel()

    def dfunc(self, x):
        ddsdde = self._behavior.elasticity
        if self._local:
            ddsdde = self._local.rotate_tensor4_from_material(ddsdde)
        return self.rMatrix @ ddsdde.reshape((9, 9)) @ self.rMatrix.T


class MaterialSimulator(object):
    def __init__(self):
        self._timedis = None
        self._dtime = 0.
        self._curtime = 0.
        self._freq = 1
        self._cycs = set([0])
        self._mask = set()
        self._local = None

    def setDTime(self, dtime):
        self._dtime = dtime

    def setOutputFrequency(self, freq: int):
        self._freq = freq

    def outputCycles(self, cycs):
        self._cycs = set(cycs)

    def updateOutputShapes(self):
        if self._dtime == 0.:
            return None
        tmax = self._load.gettmax(False)
        self._timedis = np.arange(0., tmax+self._dtime, self._dtime)
        self._timedis[-1] = tmax
        indices = np.arange(0, self._timedis.size, self._freq)
        cyc_eval = self._load.cycle(self._timedis[indices])
        self._mask = set()
        res = []
        for cur_cyc in self._cycs:
            cur_indices = indices[np.where(cyc_eval == cur_cyc)[0]]
            res.append((cur_cyc, len(cur_indices), self._timedis[cur_indices]))
            self._mask.update(cur_indices)
        return res

    def setLoad(self, load: SimuLoad):
        self._load = load

    def setLocalFrame(self, local: LocalFrame):
        self._local = local

    def setMaterial(self, mat: Behavior):
        self._mat = MaterialWrapper(mat)

    def setup(self):
        nb_steps = len(self._mask)
        if not (0 in self._mask):
            nb_steps += 1
        self._stress_history = np.zeros((nb_steps, 3, 3))
        self._last_stress = np.zeros((3, 3))
        self._strain_history = np.zeros((nb_steps, 3, 3))
        self._last_strain = np.zeros((3, 3))

        nbvars = self._mat.getNbVars()
        self._statev_history = np.zeros((nb_steps, nbvars))
        self._last_statev = np.zeros((nbvars,))

    def compute(self, method="lm", options=None):

        if options is None:
            options = {"xtol": 1.e-2}

        self.setup()

        self._mat.rMatrix = self._load.getRestrictionMatrix()
        self._mat.free_stress_idx = self._load.getDrivenStress()
        self._mat.dtime = self._dtime
        if self._local:
            self._mat._local = self._local

        time = [0.]
        cycs = [self._load.cycle(0.)]
        output = 1

        for i, (t0, t1) in enumerate(zip(self._timedis[:-1], self._timedis[1:]), start=1):
            #print(f"Compute step {t0} -> {t1}")
            self._mat.time = np.array([t0, t1])
            dstrain = self._load.deto(t0, self._dtime)
            self._mat.imposed_stress = self._load.sig(t1)
            # Set variables
            self._mat.stress = self._last_stress.copy()
            self._mat.vint = self._last_statev.copy()
            self._mat.strain = self._last_strain.copy()
            self._mat.dstrain = dstrain

            # Newton algorithm to find dstrain values associated to free stress componenents
            xInit = np.zeros(self._load.nbUnkownStrain())
            out = root(self._mat.func, jac=self._mat.dfunc,
                       x0=xInit, method=method, options=options)
            # Evaluate for the strain increment
            unknown_dstrain = out.x
            self._mat.func(unknown_dstrain, save=True)
            if i in self._mask:
                self._statev_history[output, :] = self._mat.vint.copy()
                self._stress_history[output, :, :] = self._mat.stress.copy()
                self._strain_history[output, :,
                                     :] = self._last_strain + self._mat.dstrain
                time.append(t1)
                cycs.append(self._load.cycle(t1))
                output += 1

            # Update variables
            self._last_statev = self._mat.vint.copy()
            self._last_stress = self._mat.stress.copy()
            self._last_strain += self._mat.dstrain
        return np.array(time), np.array(cycs)
