import numpy as np
import numpy.typing as npt

import eecs517project.utls.constants as c

class Particle:
    def __init__(
            self, m_i: float, pos: npt.ArrayLike, vel: npt.ArrayLike, 
            isotropic: bool = False, amu:bool = True, W: int | float = 1) -> None:
        self.m_i = m_i*c.m_p if amu is True else m_i
        try:
            pos = np.array(pos)
            vel = np.array(vel)
        except ValueError as msg:
            raise ValueError(msg)
        except Exception as e:
            raise e
        self._xdim, self._xsize = pos.ndim, pos.size
        self._vdim, self._vsize = vel.ndim, vel.size
        self.pos = pos
        self.vel = vel
        self._W = W
    
    @property
    def m_i(self):
        return self._m_i
    @m_i.setter
    def m_i(self, val):
        acceptables = tuple((float,))
        if isinstance(val, acceptables):
            self._m_i = val
        else:
            raise TypeError(f"'{val}' is of type '{type(val)}' not of types: '{acceptables}'")

    @property
    def W(self):
        return self._W

    @property
    def xdim(self):
        return self._xdim
    @property
    def xsize(self):
        return self._xsize
    @property
    def vdim(self):
        return self._vdim
    @property
    def vsize(self):
        return self._vsize

    @property
    def pos(self):
        return self._pos
    @pos.setter
    def pos(self, val):
        acceptables = tuple((npt.ArrayLike,))
        try:
            array = np.array(val)
        except Exception as e:
            raise e(f"'{val}' is of type '{type(val)}' not of types: '{acceptables}'")
        if array.ndim == self._xdim: # match dimension
            if array.size == self._xsize:
                self._pos = array
            else: 
                raise ValueError(f"new pos array size {array.size} not original {self.xsize}")
        else: 
            raise ValueError(f"new pos array ndim is {array.ndim} not original {self.xdim}")

    @property
    def vel(self):
        return self._vel
    @vel.setter
    def vel(self, val):
        acceptables = tuple((npt.ArrayLike,))
        try:
            array = np.array(val)
        except Exception as e:
            raise e(f"'{val}' is of type '{type(val)}' not of types: '{acceptables}'")
        if array.ndim == self._vdim: # match dimension
            if array.size == self._vsize:
                self._vel = array
            else: 
                raise ValueError(f"new vel array size {array.size} not original {self.vsize}")
        else: 
            raise ValueError(f"new vel array ndim is {array.ndim} not original {self.vdim}")

    @property
    def erg(self):
        energy = np.multiply(np.square(self.vel), 0.5*self.m_i/c.e)
        return energy
    @property
    def ergT(self):
        energyT = np.linalg.norm(self.erg, axis=1).reshape((self.erg.shape[0],1))
        return energyT