import numpy as np
from scipy.interpolate import interp1d

SYM_MASK = (0, 1, 2, 4, 5, 8)
SYM_MASK_INV = (3, 6, 7)
SYM_RULES = (1, 2, 5)


def extract_indices(var_name: str) -> tuple:
    return (int(var_name[-2]), int(var_name[-1]))


class SimuLoad(object):
    """Utility class to define a loading path for UMAT and Z-mat computation

    """
    _eto_comp = ("eto11", "eto22", "eto33", "eto12",
                 "eto23", "eto31", "eto21", "eto32", "eto13")
    _sig_comp = ("sig11", "sig22", "sig33", "sig12",
                 "sig23", "sig31", "sig21", "sig32", "sig13")
    _tensor_indices = ((0, 0), (1, 1), (2, 2), (0, 1),
                       (1, 2), (2, 0), (1, 0), (2, 1), (0, 2))

    def __init__(self):
        self._interp_x_data = {key: [0.]
                               for key in SimuLoad._eto_comp + SimuLoad._sig_comp}
        self._interp_y_data = {key: [0.]
                               for key in SimuLoad._eto_comp + SimuLoad._sig_comp}
        self._interp_x_data["cyc"] = []
        self._interp_y_data["cyc"] = []

        self._functions = {}
        self._cycs = lambda t: 0

        self._tmax = 0.

    def gettmaxForVar(self, var):
        return self._interp_x_data[var][-1]

    def getNbCycles(self):
        try:
            return max(self._interp_y_data["cyc"])
        except ValueError:
            return 0

    def gettmax(self, raise_error=True):
        tmax = [self._interp_x_data[var][-1] for var in self._functions.keys()]
        if raise_error:
            if not all(t == tmax[0] for t in tmax):
                raise ValueError("Loading is not consistent.")
            self._tmax = tmax[0]
        elif len(tmax) == 0.:
            return self._tmax
        else:
            self._tmax = max(tmax)
        return self._tmax

    def getComponents(self):
        keys = list(self._interp_x_data.keys())
        keys.remove("cyc")
        return keys

    def addComponent(self, var: str, times: np.array, values: np.array, repeat: int = 1, last=False) -> None:
        if not var in SimuLoad._sig_comp + SimuLoad._eto_comp:
            raise ValueError(
                "Please provide a stress or a strain component to load.")
        if not times[0] == 0.:
            raise ValueError("All load components must begin at time=0.s")
        if not values[0] == self._interp_y_data[var][-1]:
            raise ValueError("Loading is not continuous")

        t0 = self.gettmaxForVar(var)

        if repeat > 1:
            if values[0] != values[-1]:
                raise ValueError(
                    f"Cannot repeat a non cyclic loading for var {var}.")
            T = times[-1]
            nb = self.getNbCycles()
            self._interp_x_data["cyc"].append(t0)
            self._interp_y_data["cyc"].append(0 if t0 > 0. else 1)
            for i in range(repeat):
                self._interp_x_data[var] += [t0+i*T+dt for dt in times[1:]]
                self._interp_y_data[var] += [v for v in values[1:]]
                self._interp_x_data["cyc"].append(t0+(i+1)*T)
                self._interp_y_data["cyc"].append(nb+i+1)
            self._cycs = interp1d(self._interp_x_data["cyc"],
                                  self._interp_y_data["cyc"],
                                  kind='next',
                                  bounds_error=False,
                                  fill_value=(self._interp_y_data["cyc"][0],
                                              self._interp_y_data["cyc"][-1]))

        else:
            self._interp_x_data[var] += [t0+t for t in times[1:]]
            self._interp_y_data[var] += [v for v in values[1:]]
            if self._tmax == 0.:
                self._interp_x_data["cyc"].append(0.)
                self._interp_y_data["cyc"].append(0)
            if self._tmax == 0. or t0 + times[-1] > self.gettmax(False):
                self._interp_x_data["cyc"].append(t0 + times[-1])
                self._interp_y_data["cyc"].append(0)
                self._cycs = interp1d(self._interp_x_data["cyc"],
                                      self._interp_y_data["cyc"],
                                      kind='next',
                                      bounds_error=False,
                                      fill_value=(self._interp_y_data["cyc"][0],
                                                  self._interp_y_data["cyc"][-1]))

        self._functions[var] = interp1d(self._interp_x_data[var],
                                        self._interp_y_data[var],
                                        bounds_error=False,
                                        fill_value=(0., self._interp_y_data[var][-1]))

        idx = extract_indices(var)
        if idx[0] != idx[1] and not last:
            vname = var[:-2]+f"{idx[1]}{idx[0]}"
            self.addComponent(vname, times, values, repeat, True)

    def cycle(self, time):
        return self._cycs(time)

    def deto(self, time: float, dtime: float) -> np.ndarray:
        eto1 = self.eto(time)
        eto2 = self.eto(time+dtime)
        return eto2 - eto1

    def eto(self, time: float) -> np.ndarray:
        _eto = np.zeros((3, 3))
        for idx, comp in zip(self._tensor_indices, self._eto_comp):
            if comp in self._functions.keys():
                try:
                    _eto[idx[0], idx[1]] = self._functions[comp](time)
                except ValueError:
                    _eto[idx[0], idx[1]] = self._functions[comp](
                        float("{:.8f}".format(time)))
        return _eto

    def sig(self, time: float) -> np.ndarray:
        _sig = np.zeros((3, 3))
        for idx, comp in zip(self._tensor_indices, self._sig_comp):
            if comp in self._functions.keys():
                try:
                    _sig[idx[0], idx[1]] = self._functions[comp](time)
                except ValueError:
                    _sig[idx[0], idx[1]] = self._functions[comp](
                        float("{:.8f}".format(time)))
        return _sig

    def getRestrictionMatrix(self) -> np.array:
        ntens = 9
        neto = len([x for x in self._functions.keys() if x.startswith("eto")])
        proj_matrix = np.zeros((ntens-neto, ntens))
        incr = 0
        for idx, comp in zip(self._tensor_indices, self._eto_comp):
            if comp not in self._functions.keys():
                col = idx[0]*3+idx[1]
                proj_matrix[incr, col] = 1.
                incr += 1
        return proj_matrix

    def nbUnkownStrain(self) -> int:
        return len(self.getDrivenStress())

    def getDrivenStress(self) -> list:
        stress_idx = []
        for idx, comp in zip(self._tensor_indices, self._eto_comp):
            if comp in self._functions:
                continue
            col = idx[0]*3+idx[1]
            stress_idx.append(col)
        return stress_idx
