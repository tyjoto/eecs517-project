import numpy as np

def electron_impact_ionization(alpha,Ei,A,B,C,D):

    def cross_section(Te):
        """
        Te: [eV]
        u = Te/Ei [-]
        """
        u = Te/Ei 
        inv_u = np.divide(1,u)
        lnu = np.log(u)
        slope = np.divide(alpha,np.add(u,Ei/np.pi)*Ei*Ei)
        term1 = np.multiply(A, np.subtract(1,inv_u))
        term2 = np.multiply(B, np.square(np.subtract(1,inv_u)))
        term3 = np.multiply(C, lnu)
        term4 = np.multiply(np.multiply(D,inv_u), lnu)

        return np.multiply(slope, np.sum([term1,term2, term3, term4]))
    return cross_section

def charge_exchange(k1,k2):
    def cross_section(cr):
        """
        cr: [m/s]
        """
        return np.multiply(np.square(np.add(np.multiply(k1,np.log(cr)),k2)),1e-20)
    return cross_section

def momentum_exchange():
    def cross_section(cr):
        """
        cr: [m/s]
        """
        return np.divide(6.416e-16, cr) # m^2
    return cross_section

