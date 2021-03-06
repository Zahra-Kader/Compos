# This script uses pyhalofit.py to calculate nonlinear power spectra#

import numpy as np
import matplotlib.pyplot as mp

from compos import const, pyhalofit, growthfactor, matterps


# set parameters(as an example)#

const.initializecosmo()

x = np.linspace(-4, 1, 1000)
k = 10 ** x
d2 = growthfactor.growfunc_z(10)
d1 = growthfactor.growfunc_z(5)
pyhalofit.supparams(growthf=d2)
np2 = pyhalofit.nlpowerspec(k, 10)
pyhalofit.supparams(growthf=d1)
np1 = pyhalofit.nlpowerspec(k, 5)
pyhalofit.supparams()
np0 = pyhalofit.nlpowerspec(k, 0)
t = np.zeros((2, np.size(k)))

p2 = matterps.normalizedmp(k, 10)
p1 = matterps.normalizedmp(k, 5)
p0 = matterps.normalizedmp(k, 0)

mp.loglog(k/const.cosmo['h'], np0, label='nonlinear, z=0')
mp.loglog(k/const.cosmo['h'], p0, label='linear, z=0')
mp.loglog(k/const.cosmo['h'], np1, label='nonlinear,z=5')
mp.loglog(k/const.cosmo['h'], p1, label='linear,z=5')
mp.loglog(k/const.cosmo['h'], np2, label='nonlinear,z=10')
mp.loglog(k/const.cosmo['h'], p2, label='linear,z=10')
mp.text(0.001, 0.1, '$h = 0.7, \Omega_mh^2$=' +
        str(const.cosmo['omega_0']*const.cosmo['h']**2) +
        ',$ \Omega_qh^2 = $' + str(const.cosmo['omega_q'] *
                                   const.cosmo['h']**2)+',', fontsize=15)
mp.text(0.001, 0.01, '$w_0 = -1,w_1 = 0$', fontsize=15)
mp.legend(fontsize=10)
mp.xlabel('k (h Mpc$^{-1}$)')
mp.ylabel('P(k) (h$^{-3}$ Mpc$^{-3}$)')
mp.savefig('../../results/pyhalofit/pyhalofit.pdf')
mp.savefig('../../results/pyhalofit/pyhalofit.jpg')
mp.show()
