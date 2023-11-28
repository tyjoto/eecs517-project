from eecs517project.initiate import initializer

def solver(settings: dict):
    print(">>Starting EECS517-project:solver")

    parameters = initializer(settings)

    beam_particles = parameters["particles"]["beam"]
    
    # pass to montecarlo

    # pass to outputs

    print("done.")
