import numpy as np

import eecs517project.initiate.particles as particles
import eecs517project.initiate.background as background
import eecs517project.initiate.cross_sections as cross_sections
import eecs517project.initiate.outputs as outputs

def initializer(settings:dict) -> dict:
    parameters = {
        "particles": particles.initializer(**settings["particles"]),
        "Ng": background.initializer(**settings["background"]),
        "cross_sections": cross_sections.initializer(**settings["cross_sections"]),
        "outputs": outputs.initializer(**settings["outputs"]),
    }
    return parameters