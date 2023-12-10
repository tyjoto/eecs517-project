import numpy as np

def sputter_yield(Y0, f, sigma):
    def sputter(theta):
        """
        theta: [radians]
        """
        inv_costheta = np.divide(1,np.cos(theta))
        term1 = np.multiply(Y0, np.power(inv_costheta, f))
        term2 = np.exp(np.multiply(-sigma,np.subtract(inv_costheta,1)))
        return np.multiply(term1, term2)
    return sputter