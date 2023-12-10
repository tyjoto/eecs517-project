import eecs517project.cross_sections.xenon as xenon
import eecs517project.cross_sections.carbon as carbon

Xe_p = ["Xe+", "xe+"]
C_p = ["C+", "c+"]

def empty(x):
    return 0.0

def initialize_one(
    gas_type, **kwargs
    ):
    cross_section_funcs = {}
    if gas_type in Xe_p:
        cxn_gas = xenon
    elif gas_type in C_p:
        cxn_gas = carbon
    else:
        raise ValueError(f"Gas type {gas_type} is not a known gas type")
    for key in kwargs.keys():
        if key.upper() == "CEX":
            cxn = cxn_gas.CEX
        elif key.upper() == "MEX":
            cxn = cxn_gas.MEX
        else:
            raise NotImplementedError(f"'{gas_type}' does not have cross section data for '{key}'")
        
        if kwargs[key] is True:
            cross_section_funcs[key] = cxn
        else:
            cross_section_funcs[key] = empty
    return cross_section_funcs

def initializer(cross_sections):
    created_cross_sections = {}
    for gas in cross_sections.keys():
        created_cross_sections[gas] = initialize_one(gas,**cross_sections[gas])
    return created_cross_sections