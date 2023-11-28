
import eecs517project.utls.constants as c

def ideal_gas_law_density(P_gas, T_gas = 300):
    """
    Returns neutral gas density [Torr]

    Parameters:
    P_gas [Torr]
    T_gas (optional=300) [K]
    """

    P = P_gas
    P = P*101325/760            # unit: Torr = [Pa]*[760 Torr/101325 Pa] NOTE: 1 atm = 101325 Pa = 760 Torr
    N = P/(c.k_B*T_gas )           # unit: m^-3 = [1/m^3]/[J/K]*[K]
    return N                    # unit: m^-3