"""Core implementations like DOF which are used by most other classes."""
from enum import Enum
from typing import Sequence
from typing import Tuple
from typing import Set
from typing import List


class AXIS(Enum):
    """Definition of a axis in the global CSYS."""

    X = "axial"
    Y = "vertical"
    Z = "horizontal"

    def __init__(self, description: str) -> None:
        self._description: str = description

    @property
    def description(self) -> str:
        """Short description for axis or direction, as preferrably applied to beams."""
        return self._description

    @property
    def lower(self) -> str:
        """Lower case axis designator like x, y, z."""
        return str(self.name).lower()


class DOF_TYPE(Enum):
    """Type of degree of freedom, that is displacement or rotation."""

    DISP = "displacement"
    ROT = "rotation"

    def __init__(self, description: str) -> None:
        self._description: str = description

    @property
    def description(self) -> str:
        """Description of DOF type.

        :return: 'rotational' or 'displacement'
        """
        return self._description

    @property
    def short(self) -> str:
        """Short designator.

        :return: single letter designator: 'r' for rotational, 'd' for displacement
        """
        return str(self.name).lower()[0]


class DOF(Enum):
    """Definition of degrees of freedom."""

    U = (DOF_TYPE.DISP, AXIS.X, "axial displacement")
    W = (DOF_TYPE.DISP, AXIS.Z, "lateral displacement")
    PHI = (DOF_TYPE.ROT, AXIS.Y, "rotation around y")

    def __init__(self, dof_type: DOF_TYPE, axis: AXIS, description: str):
        self._type: DOF_TYPE = dof_type
        self._axis: AXIS = axis
        self._description: str = description

    @property
    def dof_type(self) -> DOF_TYPE:
        """Returns the type of DOF.

        :return: type of DOF
        :rtype: str
        """
        return self._type

    @property
    def axis(self) -> AXIS:
        """Returns the axis of the DOF in global CSYS.

        :return: Coordinate of DOF
        :rtype: str
        """
        return self._axis

    @property
    def description(self) -> str:
        """Returns the description of the DOF.

        :return: Description of DOF
        :rtype: str
        """
        return self._description

    @property
    def short(self) -> str:
        """Returns a short designator of the DOF compiled of the first character of
        the type and the axis, like 'dx', 'dz', 'ry'.

        :return: Short designator
        :rtype: str
        """
        return self._type.short + str(self._axis.lower)

    @staticmethod
    def axes(dofs: Sequence["DOF"]) -> Tuple[AXIS, ...]:
        """Returns a tuple of the axes of each DOF in a sequence.

        :return: Tuple of axes of each DOF
        :rtype: Tuple[AXIS, ...]
        """
        if dofs is None:
            raise ValueError("Sequence of DOF is None")
        return tuple(dof.axis for dof in dofs)

    @staticmethod
    def get_by_type(dof_type: DOF_TYPE) -> List["DOF"]:
        """Returns a list of all supported DOF of a specific type.
        
        :param dof_type: DOF type
        :type dof_type: DOF_TYPE

        :return: list of DOF for specific type
        """
        return [dof for dof in DOF if dof.dof_type == dof_type]

    def __str__(self) -> str:
        return self.short
