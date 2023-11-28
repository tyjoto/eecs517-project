import numpy.typing as npt

from eecs517project.particles.base import Particle
from eecs517project.utls.elements import amu


class Carbon(Particle):
    def __init__(
            self, pos: npt.ArrayLike, vel: npt.ArrayLike, 
            m_i: float = amu.carbon, isotropic: bool = False, amu: bool = True) -> None:
        super().__init__(m_i, pos, vel, isotropic, amu)

class Nitrogen(Particle):
    def __init__(
            self, pos: npt.ArrayLike, vel: npt.ArrayLike, 
            m_i: float = amu.nitrogen, isotropic: bool = False, amu: bool = True) -> None:
        super().__init__(m_i, pos, vel, isotropic, amu)

class Nitrogen2(Particle):
    def __init__(
            self, pos: npt.ArrayLike, vel: npt.ArrayLike, 
            m_i: float = amu.nitrogen2, isotropic: bool = False, amu: bool = True) -> None:
        super().__init__(m_i, pos, vel, isotropic, amu)

class Xenon(Particle):
    def __init__(
            self, pos: npt.ArrayLike, vel: npt.ArrayLike, 
            m_i: float = amu.xenon, isotropic: bool = False, amu: bool = True) -> None:
        super().__init__(m_i, pos, vel, isotropic, amu)