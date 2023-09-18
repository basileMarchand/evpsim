import numpy as np

from evpsim.tools.tenalg import J4, K4


def isotropic_elasticity(young: float, poisson: float):
    two_mu = young / (1. + poisson)
    three_K = young / (1. - 2. * poisson)
    return two_mu*J4 + three_K*K4


def transverse_elasticity(young_p: float, young_z: float, poisson_p: float, poisson_pz: float, shear_zp: float) -> np.ndarray:
    ret = np.zeros((3, 3, 3, 3))
    poisson_zp = poisson_pz*(young_z/young_p)
    denominator = (1 + poisson_p)*(1 - poisson_p - 2. *
                                   poisson_pz*poisson_zp)/(young_z * young_p**2)
    ret[0, 0, 0, 0] = (1 - poisson_pz * poisson_zp) / \
        (young_p * young_z * denominator)
    ret[1, 1, 1, 1] = (1 - poisson_pz * poisson_zp) / \
        (young_p * young_z * denominator)
    ret[2, 2, 2, 2] = (1 - pow(poisson_p, 2.)) / \
        (pow(young_p, 2.) * denominator)

    ret[0, 0, 1, 1] = ret[1, 1, 0, 0] = (
        poisson_p + poisson_zp * poisson_pz) / (young_p * young_z * denominator)
    ret[0, 0, 2, 2] = ret[2, 2, 0, 0] = (
        poisson_zp + poisson_p * poisson_zp) / (young_p * young_z * denominator)
    ret[1, 1, 2, 2] = ret[2, 2, 1, 1] = (
        poisson_zp + poisson_zp * poisson_p) / (young_p * young_z * denominator)

    ret[1, 2, 1, 2] = ret[1, 2, 2, 1] = ret[2,
                                            1, 1, 2] = ret[2, 1, 2, 1] = shear_zp
    ret[0, 2, 0, 2] = ret[0, 2, 2, 0] = ret[2,
                                            0, 0, 2] = ret[2, 0, 2, 0] = shear_zp
    ret[0, 1, 0, 1] = ret[0, 1, 1, 0] = ret[1, 0, 0,
                                            1] = ret[1, 0, 1, 0] = 0.5 * young_p / (1 + poisson_p)
    return ret
