import numpy as np

from eecs517project.utls.helpers import ideal_gas_law_density

def initialize_one(
    Pg, Tg, *args,
    **kwargs
    ):
    Ng0 = ideal_gas_law_density(P_gas=Pg,T_gas=Tg)
    def Ng(x):
        return Ng0
    return Ng

def initializer(background_gases_parameters: dict) -> dict:
    background_gases_neutral_density = {}
    for key in background_gases_parameters.keys():
        background_gases_neutral_density[key] = initialize_one(**background_gases_parameters[key])

    return background_gases_neutral_density  
