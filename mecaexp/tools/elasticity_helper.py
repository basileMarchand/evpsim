import numpy as np

from mecaexp.tools.tenalg import J4, K4


def isotropic_elasticity(young: float, poisson: float):
    two_mu = young / (1. + poisson)
    three_K = young / (1. - 2. * poisson)
    return two_mu*J4() + three_K*K4()


