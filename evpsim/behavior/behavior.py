import numpy as np
from evpsim.tools import BaseMagic, VarStatus


class Behavior(BaseMagic):

    def __init__(self):
        super().__init__()

        self._rate_saved = {}

        self._times = ()

    @property
    def times(self):
        return self._times

    @times.setter
    def times(self, tdt):
        self._times = tdt

    def derive(self) -> None:
        raise NotImplementedError()

    def integrate(self) -> None:
        raise NotImplementedError()

    def compute_var_positions(self):
        counter = 0
        for _, var in self._all_variables.items():
            if var.status == VarStatus.Vint:
                var.start_pos = counter
                counter += var.size()

    def compute_vint_size(self):
        counter = 0
        for _, var in self._all_variables.items():
            if var.status == VarStatus.Vint:
                counter += var.size()
        return counter

    def compute_time_coeff(self, t):
        t_ini = self._times[0]
        dt = self._times[1]
        coeff = (t - t_ini)/dt
        return coeff

    def __call__(self, t: float, y: np.ndarray) -> np.ndarray:
        """Function wrapper used for scipy.integrate RKXY 

        Args:
            t (float): time 
            y (np.ndarray): Integrated variables vector 

        Returns:
            np.ndarray: dy_dt 
        """

        for _, var in self._all_variables.items():
            if var.status == VarStatus.Vint:
                var.fill_value_from_vector(y)

        self.derive()

        dy_dt = np.zeros(y.shape)
        for _, var in self._all_variables.items():
            if var.status == VarStatus.Vint:
                var.fill_vector_from_rate(dy_dt)
        return dy_dt
