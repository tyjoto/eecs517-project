
import numpy as np

import eecs517project.utls.constants as c

seed = 10
rng = np.random.default_rng(seed)

def ideal_gas_law_density(P_gas, T_gas = 300):
    """
    Returns neutral gas density [Torr]

    Parameters:
    P_gas [Torr]
    T_gas (optional=300) [K]
    """

    P = P_gas
    P = P*101325/760            # unit: Torr = [Pa]*[760 Torr/101325 Pa] NOTE: 1 atm = 101325 Pa = 760 Torr
    N = P/(c.k_B*T_gas )           # unit: m^-3 = [1/m^3]/[J/K]*[K]
    return N                    # unit: m^-3

def isotropic_scattering(vel):
    vmag = np.linalg.norm(vel, axis=1).reshape((vel.shape[0],1))
    vmag = np.array(vmag)
    shape = vmag.shape
    if not shape: # if empty 
        R1 = rng.random()
        R2 = rng.random()
    else:
        R1 = rng.random(shape)
        R2 = rng.random(shape)

    theta = np.arccos(np.multiply(2,R1)-1) 
    phi = np.multiply(2*np.pi, R2)


    vx = np.multiply(vmag,np.cos(theta))
    vy = np.multiply(vmag,np.multiply(np.sin(theta),np.cos(phi)))
    vz = np.multiply(vmag, np.multiply(np.sin(theta),np.sin(phi)))
    
    if not shape:
        return np.array([vx,vy,vz])
    else:
        vx = vx.reshape((shape[0],))
        vy = vy.reshape((shape[0],))
        vz = vz.reshape((shape[0],))
        v = np.array([vx,vy,vz]).transpose()
        return v