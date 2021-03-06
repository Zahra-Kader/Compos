# This code write a 'param.ini' file for initializing a CAMB routine.
import os
import const

global cambpath, path
path = const.cosmo['path']
cambpath = const.cosmo['cambpath']  # path where CAMB is

# write parameters: ombh2, omch2, omnuh2, omk, hubble, temp_cmb.#


def writeparam(cosmo, k_max=10):
    global cambpath, path
    h = cosmo['h']
    hubble = h * 100
    ns = cosmo['n_s']
    ombh2 = cosmo['omega_b'] * h ** 2
    omch2 = cosmo['omega_c'] * h ** 2
    omnuh2 = cosmo['omega_nu'] * h ** 2
    omk = cosmo['omega_k']
    temp_cmb = cosmo['T_CMB'] * 2.7
    os.chdir(cambpath)
    param = open('paramsformps.ini', 'r')
    text = param.read()
    thb = text.find('hubble')
    thbend = text.find('use_physical')
    tb = text.find('ombh2')
    tc = text.find('omch2')
    tnu = text.find('omnuh2')
    tk = text.find('omk')
    ttcmb = text.find('temp_cmb')
    tend = text.find('helium_fraction')
    kmax = text.find('transfer_kmax')
    kmaxend = text.find('transfer_k_per_logint')
    tn = text.find('scalar_spectral_index(1)')
    tnend = text.find('scalar_nrun(1)')
    hb = text[thb:thbend]
    omb = text[tb:tc]
    omc = text[tc:tnu]
    omnu = text[tnu:tk]
    tomk = text[tk:ttcmb]
    tcmb = text[ttcmb:tend]
    km = text[kmax:kmaxend]
    nscalar = text[tn:tnend]
    text = text.replace(hb, 'hubble = '+str(hubble)+'\n')
    text = text.replace(omb, 'ombh2 = '+str(ombh2)+'\n')
    text = text.replace(omc, 'omch2 = '+str(omch2)+'\n')
    text = text.replace(omnu, 'omnuh2 = '+str(omnuh2)+'\n')
    text = text.replace(tomk, 'omk = '+str(omk)+'\n')
    text = text.replace(tcmb, 'temp_cmb = '+str(temp_cmb)+'\n')
    text = text.replace(km, 'transfer_kmax='+str(k_max)+'\n')
    text = text.replace(nscalar, 'scalar_spectral_index(1) = '+str(ns)+'\n')
    param.close()
    param = open('paramsformps.ini', 'w')
    param.write(text)
    param.close()
    return

# write notes to output files.#


def writeoutput(cosmo):
    global cambpath, path
    h = cosmo['h']
    hubble = h * 100
    ombh2 = cosmo['omega_b'] * h ** 2
    omch2 = cosmo['omega_c'] * h ** 2
    omnuh2 = cosmo['omega_nu'] * h ** 2
    omk = cosmo['omega_k']
    temp_cmb = cosmo['T_CMB'] * 2.7
    os.chdir(cambpath)
    param = open('paramsformps.ini', 'r')
    text = param.read()
    t1 = text.find('output_root')
    t2 = text.find('get_scalar_cls')
    root = text[t1:t2]
    text = text.replace(root, 'output_root = ' + path +
                        '/scripts/results/callcamb/spectra/test(' +
                        str(ombh2) + ',' + str(omch2) + ',' +
                        str(omnuh2) + ',' + str(omk) +
                        ',' + str(hubble) + ',' + str(temp_cmb) + ')\n')
    param.close()
    param = open('paramsformps.ini', 'w')
    param.write(text)
    param.close()
    return
