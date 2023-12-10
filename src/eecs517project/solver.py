import time
from pprint import pprint

import numpy as np

from eecs517project.initiate import initializer
from eecs517project.montecarlo import loop_of_particles
from eecs517project.plotter import make_plots
from eecs517project.sputtering.carbon.carbon import loop_of_carbon_sputtering

def solver(settings: dict, returns = False):
    print(">>Starting EECS517-project:solver")
    start_time = time.time()

    print("Input settings")
    pprint(settings)

    print("initializing...")
    parameters = initializer(settings)
    print("done.")

    print("Input parameters")
    pprint(parameters)
    print()
    print(f"Calculated background gas density at thruster exit: {parameters['background']['Xe'](0)} m^-3")
    print(f"Calculated background gas density at beam dump: {parameters['background']['Xe'](parameters['domain']['Z'])} m^-3")

    # get beam particles for montecarlo
    beam_particles = parameters["particles"]["Xe+"]
    #print("Particles:")
    #pprint(beam_particles.pos)
    #pprint(beam_particles.vel)
    #pprint(beam_particles.ergT)
    
    # pass to montecarlo
    parameters["particles"] = loop_of_particles(**parameters)
    #print(parameters["particles"]["Xe+"].vel)

    # determine number of sputtered carbon neutrals
    Pgas = settings["background"]["Xe"]["Pg"]
    Z = settings["domain"]["Z"]
    Vb = settings["particles"]["Xe+"]["Vb"]+settings["particles"]["Xe+"]["Vg"]

    nbeam = beam_particles.pos.size
    hit_target = len(np.where(parameters["particles"]["Xe+"].pos>=parameters["domain"]["Z"])[0])
    miss_target = nbeam-hit_target
    miss_target_percent = miss_target/nbeam*100
    nsputtered = loop_of_carbon_sputtering(parameters["particles"]["Xe+"], parameters["domain"])
    nsputtered_percent = nsputtered/nbeam*100
    sputter_yield = nsputtered/hit_target if hit_target != 0  else np.nan
    print(f"Number of beam particles: {nbeam}")
    print(f"Number of particles that hit target: {hit_target}")
    print(f"\tHit: {hit_target/nbeam*100} %\n\tMiss: {(nbeam-hit_target)/nbeam*100} %")
    print(f"Number of particles sputtered: {nsputtered}")
    print(f"\tPercent of Beam that Sputter: {nsputtered/nbeam*100} %\n\tSputter Yield: {sputter_yield}")
    y = np.array([miss_target_percent, nsputtered_percent, sputter_yield])
    x = np.array([Pgas, Vb, Z])
    

    # pass to outputs
    make_plots(x, y,parameters["particles"], saveto=parameters["saveto"], outputs=parameters["outputs"], domain=parameters["domain"], settings=settings)


    time_total = time.time()-start_time
    print(f"Elaspsed time: {time_total}s\n\ndone.")

    if returns is True:
        return x,y
