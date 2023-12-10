import numpy as np

from eecs517project.utls import constants as c
from eecs517project.cross_sections import helpers as h

m_i_amu = 131.3
m_i = m_i_amu*c.m_p

def make_CEX():
    k1 = -0.8821
    k2 = 15.1262
    cxn_func= h.charge_exchange(k1,k2)
    return cxn_func

def make_MEX():
    mex_func = h.momentum_exchange()
    return mex_func

# following use cr [m/s]
cex_func = make_CEX()
mex_func = make_MEX()

def CEX(E):
    cr = np.sqrt(E*c.e*2/m_i) # m/s
    #cr = cr*(100/1) # cm/s
    return cex_func(cr) # m^2
    #return 1e-15 # m^2


def MEX(E):
    cr = np.sqrt(E*c.e*2/m_i) # m/s
    #print(cr)
    #return 1e-15 # m^2
    res =  cex_func(cr)
    return res