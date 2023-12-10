import numpy as np

from eecs517project.cross_sections import helpers as h

def CEX(E):
    return 1e-15 # m^2

def MEX(E):
    return 1e-15 # m^2


def make_electron_impact_ionization():
    # TeV = eV
    alpha = 360
    Ei = 11.26  # eV
    A = 12.2
    B = -3.91
    C = 1.85
    D = -10.3
    cxn_func = h.electron_impact_ionization(alpha, Ei, A, B, C, D)
    return cxn_func


electron_impact_ionization = make_electron_impact_ionization()
# only inmput parameter is TeV in [eV]