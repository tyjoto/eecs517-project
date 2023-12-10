import os

import numpy as np
import matplotlib.pyplot as plt

from eecs517project.plotting.basic import (
    beam_dump_striking_ion_energies_hist,
)

def make_plots(x,y,particles, saveto, outputs: dict, domain: dict, settings:dict):
    p = particles["Xe+"]
    pos = p.pos
    ergs = p.ergT
    Z = str(domain["Z"])
    Vb = str(settings["particles"]["Xe+"]["Vb"]+settings["particles"]["Xe+"]["Vg"])
    Pgas = str(settings["background"]["Xe"]["Pg"])

    Z = Z.replace(".","_")
    Vb = Vb.replace(".","_")
    Pgas = Pgas.replace(".","_")

    Z = "L"+Z
    Vb = "Vb"+Vb
    Pgas = "Pgas"+Pgas
    ergs = np.where(pos>=domain["Z"], ergs, ergs)

    extension = "_"+Pgas+"_"+Vb+"_"+Z

    for key in outputs.keys():
        output = outputs[key]
        saveas = os.path.join(saveto, key+extension+".png")
        func = output["func"]
        args = output["args"]
        args = tuple()  if args is None else args
        kwargs = output["kwargs"]

        fig, ax = func(*args, **kwargs, saveas=saveas, ergs=ergs)
    
    plt.close()

    



def choose_plot(string, outputs: dict):

    if string  == "hist_striking_ion_energies":
        func = beam_dump_striking_ion_energies_hist
    else:
        raise ValueError(f"'{string}' does not match knowns")
    
    return func