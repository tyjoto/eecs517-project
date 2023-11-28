import numpy as np

def constant(I0,A,x):
    J0 = I0/A
    def J(x):
        return J0*x
    return J