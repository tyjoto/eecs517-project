import numpy as np

from eecs517project.sputtering  import sputtering as s

seed = 10 
rng = np.random.default_rng(seed)

"""
def make_sputter_yield(gas="Xe"):
    if gas == "Xe":
        A = 1.31e-4 # Xe
        n = 1.16    # Xe
    else:
        raise NotImplementedError(f"'{gas}' is not a known gas type")
    Y0 = np.multiply(A,np.power(E,n))
    f = 7/2 # Kolasinski, R. D., Polk, J. E., Goebel, D., & Johnson, L. K. (2008). Carbon sputtering yield measurements at grazing incidence. Applied Surface Science, 254(8), 2506-2515. 
    sigma =
    y_func = s.sputter_yield(Y0, f, sigma)
    return y_func

sputter_yield = make_sputter_yield()
# only parameter E for incidenct energy and theta in radiansor deg=True to make in degres
"""
def sputter_yield(E, gas="Xe"):
    if gas == "Xe":
        A = 1.31e-4 # Xe
        n = 1.16    # Xe
    else:
        raise NotImplementedError(f"'{gas}' is not a known gas type")
    Y0 = np.multiply(A,np.power(E,n))
    return Y0

def loop_of_carbon_sputtering(particles, domain,**kwargs):
    indices = np.where(particles.pos>=domain["Z"])
    ncolls = len(indices[0])
    ergT0 = particles.ergT
    ergT = ergT0[indices].reshape((ncolls,1))
    W = particles.W
    R = rng.random((ncolls,1))
    Y = sputter_yield(ergT)
    #print("ncolls:\n",ncolls,"\nY:\n",Y,"\nR:\n",R)

    intY = Y.astype(int)
    nsputtered = np.where(Y>=R, intY+np.where(Y-intY>=R, 1, 0), 0)
    nsputtered = np.sum(nsputtered)

    return nsputtered
    
