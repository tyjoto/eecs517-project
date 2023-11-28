import eecs517project.cross_sections.xenon as xenon

Xe = ["xe", "Xe"]

def initialize_one(
    gas_type, **kwargs
    ):
    cross_section_funcs = {}
    if gas_type in Xe:
        cxn_gas = xenon
    for key in kwargs.keys():
        if key.upper() == "CEX":
            cxn = cxn_gas.CEX
        elif key.upper() == "MEX":
            cxn = cxn_gas.MEX
        else:
            raise NotImplementedError(f"'{gas_type}' does not have cross section data for '{key}'")
        
        cross_section_funcs[key] = cxn
    return cross_section_funcs

def initializer(cross_sections):
    created_cross_sections = {}
    for gas in cross_sections.keys():
        created_cross_sections[gas] = initialize_one(gas,**cross_sections[gas])
    return created_cross_sections