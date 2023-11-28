import numpy as np

import eecs517project.utls.constants as c
from eecs517project.particles import Particle

def initialize_one(
        m_i, I, D, Vb, T, *args,
        Vg = 0, amu = True, Z = 1,
        **kwargs
):
    # beam parameteres
    A = np.pi*D*D/4 # m^2
    J = I/A     # A/m^2
    # beam energies in z-dir
    ez = Vb + Vg# eV
    # calculated beam ion velocities in z-direction
    vz0_calculated = np.sqrt(ez*c.e*2/m_i)
    n_ib0 = J/c.e/vz0_calculated # m^-3

    # defined velocities
    vx0 = 0      # m/s
    vy0 = 0      # m/s
    vz0 = vz0_calculated   # m/s

    # initial velocities of each particle
    vel0 = [vx0, vy0, vz0]

    # initial position of each particle (1D)
    pos0 = [0]

    # determine number of particles need
    Nparticles = I/Z*T

    # determine time particles were born
    #t0 = Nparticles/T

    # create particles
    particles = Particle(m_i,pos=[pos0]*Nparticles, vel=[vel0]*Nparticles, amu=amu)

    return particles

def initializer(particles):
    created_particles = {}
    for key in particles.keys():
        created_particles[key] = initialize_one(**particles[key])
    return created_particles
