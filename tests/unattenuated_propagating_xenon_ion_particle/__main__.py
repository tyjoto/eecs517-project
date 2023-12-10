import os

import numpy as np

import eecs517project.utls.constants as c
from eecs517project.solver import solver

path = os.path.dirname(__file__)


def get_settings():
    # particles
    Nparticles = 1


    # beam ions parameters
    m_i = 131.30# amu
    amu = True  # not needed to be defined

    # Length to beam dump parameter
    L = 2.08    # m

    # beam parameteres
    I = 0.53    # A = c/s
    D = 0.30    # m 
    Z = 1       # [-]
    Vb = 850    # V
    Vg = 0      # V
    # beam calculations for next two parameters
    A = np.pi*D*D/4 # m^2
    J = I/A     # A/m^2
    ez = Vb + Vg# eV
    vz0_calculated = np.sqrt(ez*c.e*2/m_i/c.m_p)
    n_ib = J/c.e/vz0_calculated # m^-3
    # Parameters that are predefined for this special case
    T = L/vz0_calculated
    Wparticles = I*T/Nparticles

    # background neutral parameters
    Pg = 0.0  # Torr
    Tg = 300  # K

    # cross section bool paremetrs 
    Xe_CEX = False
    Xe_MEX = False
    C_CEX = False
    C_MEX = False

    # output bool paremeters
    hist_striking_ion_energies = True

    beam = {
        "Xe+": {
            "I": I,
            "D": D,
            "Vb": Vb,
            "Vg": Vg,
            "T": T,
            "Z": Z,
            "W": Wparticles,
            "m_i": m_i,
            "src": "beam"
        }
    }
    background = {
        "Xe": {
            "Pg": Pg,
            "Tg": Tg,
        }
    }
    cross_sections = {
        "Xe+": {
            "CEX": Xe_CEX,
            "MEX": Xe_MEX,
        },
        "C+": {
            "CEX": C_CEX,
            "MEX": C_MEX,
        }
    }
    outputs = {
        "hist_striking_ion_energies": hist_striking_ion_energies,
    }
    domain = {
        "Z": L,
        "T": T,
    }


    settings = {
        "particles": beam,
        "background": background,
        "cross_sections": cross_sections,
        "outputs": outputs,
        "domain": domain,
        "saveto": path,
    }

    return settings

def main():
    print(">>Starting Unattenuated propagating xenon ion particle")

    settings = get_settings()

    solver(settings)

    print("done.")

if __name__ == "__main__":
    main()