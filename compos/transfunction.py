# This file calculates transfer function and gives the shape fit
# of transferfunction without baryonic wiggle for calculation of dewiggled MPS.
# All of the definition and formulas are from arxiv:9709112v1

from __future__ import division
import numpy as np

# redshift and wavelength at matter=radiation#
 

def zeq(cosmo):
    z_eq = 2.5 * 10 ** 4 * cosmo['omega_0'] * cosmo['h'] ** \
           2 * cosmo['T_CMB'] ** (-4)
    return z_eq

# calculate the scale of particle horizon at the equality epoch z_eq (Mpc^-1)#


def keq(cosmo):
    k_eq = 7.46 * 10 ** (- 2) * cosmo['omega_0'] * cosmo['h'] \
           ** 2 * cosmo['T_CMB'] ** (-2)
    return k_eq

# calculate the redshift at drag epoch#


def zdrag(cosmo):
    b1 = 0.313 * (cosmo['omega_0'] * cosmo['h'] ** 2) ** (- 0.419) \
         * (1 + 0.607 * (cosmo['omega_0'] * cosmo['h'] ** 2) ** 0.674)
    b2 = 0.238 * (cosmo['omega_0'] * cosmo['h'] ** 2) ** 0.223
    z_d = 1291 * ((cosmo['omega_0'] * cosmo['h'] ** 2) ** 0.251 /
                  (1 + 0.659 * (cosmo['omega_0'] * cosmo['h'] ** 2) ** 0.828))\
        * (1 + b1 * (cosmo['omega_b'] * cosmo['h'] ** 2) ** b2)
    return z_d
    
# caculate the ratio between baryon to photon#


def ratiob2p(cosmo, z):
    R = 31.5 * cosmo['omega_b'] * cosmo['h'] ** 2 \
        * cosmo['T_CMB'] ** (-4) * (z/1000) ** (-1)
    return R

# calculate soundhorizon#


def soundhorizon(cosmo):
    z_eq = zeq(cosmo)
    z_d = zdrag(cosmo)
    R_eq = ratiob2p(cosmo, z_eq)
    R_d = ratiob2p(cosmo, (z_d))
    k_eq = keq(cosmo)
    s = (2 / (3 * k_eq)) * np.sqrt(6 / R_eq) * \
        np.log((np.sqrt(1 + R_d) + np.sqrt(R_d + R_eq)) / (1 + np.sqrt(R_eq)))
    return s

# calculate k_silk(Mpc^-1)#


def ksilk(cosmo):
    k_silk = 1.6 * (cosmo['omega_b'] * cosmo['h'] ** 2) ** \
             0.52 * (cosmo['omega_0'] * cosmo['h'] ** 2) ** \
             0.73 * (1 + (10.4 * cosmo['omega_0'] *
                          cosmo['h'] ** 2) ** (-0.95))
    return k_silk

# zero order spherical Bessel function#


def j_0(x):
    j = np.sin(x) / x
    return j

# calculate T_tilde


def Ttilde(k, alpha, beta, cosmo):
    k_eq = keq(cosmo)
    q = k / (13.41 * k_eq)
    C = 14.2 / alpha + 386 / (1 + 69.9 * q ** 1.08)
    T_tilde = np.log(np.e + 1.8 * beta * q) / (np.log
                                               (np.e + 1.8 * beta * q) +
                                               C * q ** 2)
    return T_tilde

# calculate the transfer function for cdm.#


def Tcdm(k, cosmo):
    # k_eq = keq(cosmo)
    s = soundhorizon(cosmo)
    a_1 = (46.9 * cosmo['omega_0'] * cosmo['h'] ** 2)\
        ** 0.670 * (1 + (32.1 * cosmo['omega_0'] * cosmo['h'] ** 2) **
                    (-0.532))
    a_2 = (12.0 * cosmo['omega_0'] * cosmo['h'] ** 2) ** 0.424 * \
          (1 + (45.0 * cosmo['omega_0'] * cosmo['h']**2) ** (-0.582))
    b_1 = 0.944 * (1 + (458 * cosmo['omega_0'] * cosmo['h'] ** 2) **
                   (-0.708)) ** (-1)
    b_2 = (0.395 * cosmo['omega_0'] * cosmo['h'] ** 2) ** (-0.0266)
    alpha_c = a_1 ** (-cosmo['omega_b'] / cosmo['omega_0']) * a_2 ** \
        (- (cosmo['omega_b'] / cosmo['omega_0']) ** 3)
    beta_c = 1 / (1 + b_1 * ((cosmo['omega_c'] / cosmo['omega_0']) ** b_2 - 1))
    f = 1 / (1 + (k * s / 5.4) ** 4)
    T_c = f * Ttilde(k, 1, beta_c, cosmo) + (1 - f) \
        * Ttilde(k, alpha_c, beta_c, cosmo)
    return T_c

# calculate the transfer function of baryon#


def Tbaryon(k, cosmo):
    z_eq = zeq(cosmo)
    z_d = zdrag(cosmo)
    # R_eq = ratiob2p(cosmo, z_eq)
    R_d = ratiob2p(cosmo, z_d)
    k_eq = keq(cosmo)
    k_silk = ksilk(cosmo)
    s = soundhorizon(cosmo)

    def Gfunc(y):
        G = y * (-6 * np.sqrt(1 + y) + (2 + 3 * y) * np.log(
            (np.sqrt(1 + y) + 1)/(np.sqrt(1 + y) - 1)))
        return G
    alpha_b = 2.07 * k_eq * s * (1 + R_d) ** (-0.75) * \
        Gfunc((1 + z_eq) / (1 + z_d))
    beta_b = 0.5 + cosmo['omega_b'] / cosmo['omega_0'] + \
        (3 - 2 * cosmo['omega_b'] / cosmo['omega_0']) * \
        np.sqrt((17.2 * cosmo['omega_0'] * cosmo['h'] ** 2) ** 2 + 1)
    beta_node = 8.41 * (cosmo['omega_0'] * cosmo['h'] ** 2) ** 0.435
    s_tilde = s / ((1 + (beta_node / (k * s)) ** 3) ** (1/3))
    T_b = (Ttilde(k, 1, 1, cosmo) / (1 + (k * s / 5.2) ** 2) +
           (alpha_b / (1 + (beta_b / (k * s)) ** 3)) * np.e **
           (-(k / k_silk) ** 1.4)) * j_0(k * s_tilde)
    return T_b

# calculate the transfer function#


def transfunction(k, cosmo):
    T = (cosmo['omega_b'] / cosmo['omega_0']) * Tbaryon(k, cosmo) + \
        (cosmo['omega_c'] / cosmo['omega_0']) * Tcdm(k, cosmo)
    return T

# calculate k of the first peak#


def kpeak(cosmo):
    s = 44.5 * np.log(9.83 / (cosmo['omega_0'] * cosmo['h'] ** 2)) /\
        np.sqrt(1 + 10 * (cosmo['omega_b'] * cosmo['h'] ** 2))
    k_peak = 5 * np.pi / (2 * s) * (1 + 0.217 * cosmo['omega_0'] *
                                    cosmo['h'] ** 2)
    return k_peak

# calculate the effective shape of transferfunction with zero-baryon case#


def efshape(k, cosmo):
    Gamma = cosmo['omega_0'] * cosmo['h']
    q = k / (cosmo['h']) * cosmo['T_CMB'] ** 2 / Gamma
    L_0 = np.log(2 * np.e + 1.8 * q)
    C_0 = 14.2 + 731 / (1 + 62.5 * q)
    T_0 = L_0 / (L_0 + C_0 * q ** 2)
    return T_0

# calculate the non-oscillatory part of the transfer function#


def noosc(k, cosmo):
    alpha_g = 1 - 0.328 * np.log(431 * cosmo['omega_0'] * cosmo['h'] ** 2) * \
              cosmo['omega_b']/cosmo['omega_0'] + 0.38 * \
              np.log(22.3 * cosmo['omega_0'] * cosmo['h'] ** 2) *\
              (cosmo['omega_b'] / cosmo['omega_0']) ** 2
    s = soundhorizon(cosmo)
    Gamma_eff = cosmo['omega_0'] * cosmo['h'] * (alpha_g + (1 - alpha_g) /
                                                 (1 + (0.43 * k * s) ** 4))
    return Gamma_eff

# calculate shape fit with no wiggle#


def t_nowiggle(k, cosmo):
    alpha_g = 1 - 0.328 * np.log(431 * cosmo['omega_0'] * cosmo['h'] ** 2) * \
              cosmo['omega_b']/cosmo['omega_0'] + 0.38 * \
              np.log(22.3 * cosmo['omega_0'] * cosmo['h'] ** 2) \
              * (cosmo['omega_b'] / cosmo['omega_0']) ** 2
    s = soundhorizon(cosmo)
    Gamma_eff = cosmo['omega_0'] * cosmo['h'] * \
        (alpha_g + (1 - alpha_g) / (1 + (0.43 * k * s) ** 4))
    q_eff = k / (cosmo['h']) * cosmo['T_CMB'] ** 2 / Gamma_eff
    L_0 = np.log(2 * np.e + 1.8 * q_eff)
    C_0 = 14.2 + 731 / (1 + 62.5 * q_eff)
    tnowiggle = L_0 / (L_0 + C_0 * q_eff ** 2)
    return tnowiggle
