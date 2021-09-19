"""Entries are items applied to the model such as loads, masses and others."""
from typing import Dict
from typing import List
from typing import Sequence
from typing import Tuple
from model.core import AXIS
from model.core import DOF
from model.core import DOF_TYPE
from numpy import ndarray
from numpy import array
from numpy import zeros
from copy import deepcopy


# TODO: mass is still strange with DOF.W and DOF.X - perhaps set mass and return for both CSYS the value?
class Mass:
    """Mass defined by mass values for specific DOF.

    Mass values for displacement DOF are in unit [MASS] and for rotational DOF in [Mass * Length^2]
    (mass moment of inertia or MMOI).
    """

    def __init__(self) -> None:
        self._mass_values: Dict[DOF, float] = {}

    def values(self, default_value: float = 0.0) -> Dict[DOF, float]:
        """Mass (mass, mmoi) values for all existing DOF where unset values will be filled with default_value.

        :return: mass values for all existing DOF
        :rtype: Dict[DOF, float]
        """
        value_dict: Dict[DOF, float] = {}
        for dof in DOF:
            value_dict[dof] = self._mass_values.get(dof, default_value)
        return value_dict

    def set_mmoi(self, dof: DOF, value: float) -> "Mass":
        """Set mass moment of inertia for specific rotational DOF.

        :param dof: dof to set mmoi for
        :type dof: DOF

        :return: self for chaining of calls
        :rtype: Mass

        :raises ValueError: if dof.dof_type != DOF_TYPE.ROT, if value < 0.0
        """
        if dof.dof_type != DOF_TYPE.ROT:
            raise ValueError(f"Invalid DOF type {dof.dof_type.name} for MMOI")
        if value < 0.0:
            raise ValueError(
                f"Invalid value {value} for MMOI {dof.name}, allowed is >= 0.0"
            )
        self._mass_values[dof] = value
        return self

    def set_mass(self, value: float) -> "Mass":
        """Sets the mass value, that is the actual mass which will be set to all displacement DOF.

        :param value: mass value
        :type value: float

        :raises ValueError: if value < 0.0
        """
        if value < 0.0:
            raise ValueError(f"Invalid mass value {value}, allowed is >= 0.0")
        for dof in DOF.get_by_type(DOF_TYPE.DISP):
            self._mass_values[dof] = value
        return self

    def get_value(self, dof: DOF) -> float:
        """Returns the value for a specific DOF.

        :param dof: DOF to get mass value for
        :type dof: DOF

        :return: Mass value (the actual mass) on any DOF of type DOF_TYPE.DISP,
                 the MMOI for DOF of type DOF_TYPE.ROT
        :rtype: float

        :raises KeyError: if no mass value is registered for dof
        """
        return self._mass_values[dof]

    @property
    def dofs(self) -> Tuple[DOF, ...]:
        """Returns a tuple of the DOF for which are mass values registered.

        :return: tuple of DOF with mass values
        :rtype: Tuple[DOF, ...]
        """
        return tuple(self._mass_values.keys())

    def has_dof(self, dof: DOF) -> bool:
        """Indicates whether a mass value is registered for a specific dof.

        :param dof: DOF to check for mass value
        :type dof: DOF

        :return: True if mass value is registered for dof, otherwise False
        """
        return dof in self._mass_values

    def get_M(self, dofs: Sequence[DOF]) -> ndarray:
        """Returns a mass matrix of the size len(dofs) x len(dofs) with columns and rows in the order of DOF in dofs.

        Values in the matrix will be 0.0, except for these elements [dof, dof] where mass values are defined. DOF
        that are defined for the Mass but are not in dofs will be ignored.

        :param dofs: DOF to be considered for the mass matrix
        :type dofs: Sequence[DOF]

        :return: Mass matrix
        :rtype: ndarray

        :raises ValueError: if dofs contains duplicates
        """
        if len(dofs) != len(set(dofs)):
            raise ValueError(f"Duplicate DOF in {[str(d) for d in dofs]}")

        dof_num: int = len(dofs)
        m: ndarray = zeros([dof_num, dof_num])

        for dof, val in self._mass_values.items():
            if dof in dofs:
                idx: int = dofs.index(dof)
                m[idx, idx] = val

        return m


class Spring:
    """Linear translational or rotational springs for specific DOFs.

    Spring values for displacement DOF are in unit [Force/Length] and for rotational DOF in [Moment/RAD].
    """

    def __init__(self) -> None:
        self._spring_values: Dict[DOF, float] = {}

    def set_value(self, dof: DOF, value: float) -> "Spring":
        """Sets a spring value for specific DOF.

        :param dof: DOF to set spring value for
        :type dof: DOF
        :param value: Spring value
        :type value: float

        :raises ValueError: If value <= 0
        """
        if value <= 0.0:
            raise ValueError(f"Invalid spring value {value} for {dof}")

        self._spring_values[dof] = value
        return self

    def get_value(self, dof: DOF) -> float:
        """Returns the spring value for a specific DOF.

        :param dof: DOF to get spring value for
        :type dof: DOF

        :raises KeyError: if no spring value is registered for dof
        """
        return self._spring_values[dof]

    @property
    def dofs(self) -> Tuple[DOF, ...]:
        """Returns the list of DOF.

        :return: Tuple of DOF
        :rtype: Tuple[DOF]
        """
        return tuple(self._spring_values.keys())

    def has_dof(self, dof: DOF) -> bool:
        """Indicates whether a spring value is specified for a specific DOF.

        :param dof: DOF to evaluate for spring value
        :type dof: DOF

        :return: True if spring value exists for dof, otherwise False
        """
        return dof in self._spring_values

    def get_K(self, dofs: Sequence[DOF]) -> ndarray:
        """Returns an element stiffness matrix of the spring in order of the provided DOF.

        Values in the matrix will be 0.0, except for these elements [dof, dof] where spring values are defined. DOF
        that are defined for the Spring but are not in dofs will be ignored.

        :param dofs: DOFs to consider in stiffness matrix
        :type dofs: Sequence[DOF]

        :return: element stiffness matrix
        :rtype: ndarray

        :raises ValueError: if dofs contains duplicate DOF
        """
        if len(dofs) != len(set(dofs)):
            raise ValueError(f"Duplicate DOF in {[str(d) for d in dofs]}")

        dof_num: int = len(dofs)
        k: ndarray = zeros([dof_num, dof_num])

        for dof, value in self._spring_values.items():
            if dof in dofs:
                idx: int = dofs.index(dof)
                k[idx, idx] = value

        return k
