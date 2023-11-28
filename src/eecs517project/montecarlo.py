import os

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style

import eecs517project.utls.constants as c

style.use("bmh")
path = os.path.dirname(__file__)

seed = 10 
rng = np.random.default_rng(seed)


def loop_of_particles(particles, background, cross_section):
    ergT = particles.ergT
    p_size = ergT.size



    

    N = rng.random(p_size)


    for n in N:
        print(f"{n} of N")
