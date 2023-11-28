from eecs517project.plotting.base import hist_striking_ion_energies

def initializer(**kwargs):
    outputs = {}
    for key in kwargs.keys():
        if key == "hist_striking_ion_energies":
            func = hist_striking_ion_energies
        outputs[key] = {"func":func, "args":None, "kwargs":{}}
    return outputs