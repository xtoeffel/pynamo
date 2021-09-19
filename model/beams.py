"""Structural beam elements with different DOF (degree of freedom).

Classes with 2DOF and 3DOF are available. The 2DOF version does not consider axial DOF - v, phi; the 3DOF version
considers the 3 major DOF: u, v, phi. Beams are Bernoulli beams.
"""

from model.core import DOF
from model.core import AXIS
from model.elements import Node

from dataclasses import dataclass
from dataclasses import field

from typing import List
from typing import Optional
from typing import Tuple
from typing import Any
from typing import Type
from typing import Set
from typing import Protocol
from typing import runtime_checkable

from numpy import array
from numpy import ndarray
from abc import ABC
from abc import abstractmethod
from enum import Enum
from copy import deepcopy


class ABeam(ABC):
    """Abstract beam with 2 nodes at each end.

    Node1 is the start node, node 2 the end node.

    Basic beam class which should not be instanciated."""

    def __init__(
        self,
        n1: Node,
        n2: Node,
        area: float,
        area_moi: float,
        e_modul: float,
        mass: float,
    ) -> None:
        if n1.dofs != n2.dofs:
            raise ValueError(f"Nodes are incompatible by DOF: {n1.dofs}, {n2.dofs}")
        if n1 is n2:
            raise ValueError(f"Start and end node are the same")
        # no value checks here, all done in verify()
        self._node1: Node = n1
        self._node2: Node = n2
        self._area: float = area
        self._area_moi: float = area_moi
        self._e_modul: float = e_modul
        self._mass: float = mass
        self._beam_type: str = "BaseBeam"

    @property
    def length(self) -> float:
        if self.node1 is None:
            raise ValueError("Node1 of beam is None")
        if self.node2 is None:
            raise ValueError("Node2 of beam is None")
        return self.node1.distance(self.node2)

    @property
    def node1(self) -> Node:
        return self._node1

    @property
    def node2(self) -> Node:
        return self._node2

    @property
    def mass(self) -> float:
        return self._mass

    def set_mass(self, mass: float) -> "ABeam":
        self._mass = mass
        return self

    @property
    def area(self) -> float:
        return self._area

    def set_area(self, area: float) -> "ABeam":
        self._area = area
        return self

    @property
    def area_moi(self) -> float:
        return self._area_moi

    def set_area_moi(self, area_moi: float) -> "ABeam":
        self._area_moi = area_moi
        return self

    @property
    def e_modul(self) -> float:
        return self._e_modul

    def set_e_modul(self, e_modul: float) -> "ABeam":
        self._e_modul = e_modul
        return self

    @property
    def beam_type(self) -> str:
        return self._beam_type

    @property
    def order(self) -> int:
        """Returns the order (of the theory) for this beam: 1 or 2 where 2 is potentially (solver must support)
        with p-Delta effects.

        :return: Order of theory for this beam
        :rtype: int
        """
        return 1

    @property
    def dof_num(self) -> int:
        """Returns the number of DOF of each node (end) of the beam.

        :return: Number of DOF
        :rtype: int
        """
        if self.node1.dofs != self.node2.dofs:
            raise ValueError(
                f"Ambiguous number of DOF for node1 and node2: {self.node1.dofs},"
                f" {self.node2.dofs}"
            )
        return self.node1.dof_num

    @property
    def dofs(self) -> Tuple[DOF, ...]:
        """Returns a tuple of DOF of each node (end) of the beam.

        :return: Tuple of DOF
        :rtype: Tuple[DOF]
        """
        # use dof_num to raise ValueError in case nodes are not compatible (unequal DOF count)
        self.dof_num
        return self.node1.dofs

    def verify(self) -> None:
        """Verifies the beam and raises ValueError, if any invalid condition was detected.

        This method must be called by sub-classes verify() method.

        :raises ValueError: If any property is invalid
        """
        if self.e_modul <= 0.0:
            raise ValueError(f"Invalid elastic modulus: {self.e_modul} <= 0.0")
        if self.length <= 0.0:
            raise ValueError(f"Invalid length: {self.length} <= 0.0")
        # TODO: area = 0.0 ok?
        if self.area < 0.0:
            raise ValueError(f"Invalid cross section: {self.area} < 0.0")
        if self.mass <= 0.0:
            raise ValueError(f"Invalid mass: {self.mass} <= 0.0")
        if self.area_moi <= 0.0:
            raise ValueError(f"Invalid area moment of inertia: {self.area_moi} <= 0.0")

    @abstractmethod
    def get_K(self, order: int = 1) -> ndarray:
        """Returns the stiffness matrix of the beam (element matrix).

        The method in the implementing class must call .verify() before returning.

        :param order: Order 1 or 2 (2 is with p-Delta effects)
        :type order: int

        :return: Element stiffness matrix
        :rtype: ndarray

        :raises ValueError: If order is not supported
        """
        raise NotImplementedError("get_K()")

    @abstractmethod
    def get_M(self) -> ndarray:
        """Returns the mass matrix of the beam (element matrix).

        The method in the implementing class must call .verify() before returning.

        :return: Element mass matrix
        :rtype: ndarray
        """
        raise NotImplementedError("get_M()")


class BeamB_2DOF(ABeam):
    """Structural beam element with 2 DOF: w (lateral), phi (rotational), no p-Delta effects."""

    @staticmethod
    def get_dofs() -> Tuple[DOF, DOF]:
        """Returns the DOFs for 2DOF beam type.

        :return: DOFs for 2DOF beam
        :rtype: Tuple[DOF, DOF]
        """
        return DOF.W, DOF.PHI

    def __init__(
        self,
        n1: Node,
        n2: Node,
        area: float,
        area_moi: float,
        e_modul: float,
        mass: float,
    ) -> None:
        # expected DOF
        if n1.dofs != BeamB_2DOF.get_dofs():
            raise ValueError(
                f"Invalid DOF for node1 of {BeamB_2DOF.__name__}, expected"
                f" {BeamB_2DOF.get_dofs()}"
            )
        if n2.dofs != BeamB_2DOF.get_dofs():
            raise ValueError(
                f"Invalid DOF for node2 of {BeamB_2DOF.__name__}, expected"
                f" {BeamB_2DOF.get_dofs()}"
            )

        super().__init__(n1, n2, area, area_moi, e_modul, mass)
        self._beam_type = f"{self.__class__.__name__}: Bernoulli, 2DOF, no p-Delta"

    def get_K(self, order: int = 1) -> ndarray:
        """Returns the [4x4] element stiffness matrix with oder: w1, phi1, w2, phi2

        :return: element stiffness matrix as 2D numpy array, rows are forces, columns are displacements
        :rtype: ndarray

        :raises ValueError: If order != 1
        """
        if order != 1:
            raise ValueError(
                f"Unsupported order {order}, supported is only {self.order}"
            )
        self.verify()

        EI_o_L: float = self.e_modul * self.area_moi / self.length
        EI_o_Lsq: float = EI_o_L / self.length
        EI_o_Lqu: float = EI_o_Lsq / self.length

        return array(
            [
                [12.0 * EI_o_Lqu, 6.0 * EI_o_Lsq, -12.0 * EI_o_Lqu, 6.0 * EI_o_Lsq],
                [6.0 * EI_o_Lsq, 4.0 * EI_o_L, -6.0 * EI_o_Lsq, 2.0 * EI_o_L],
                [-12.0 * EI_o_Lqu, -6.0 * EI_o_Lsq, 12.0 * EI_o_Lqu, -6.0 * EI_o_Lsq],
                [6.0 * EI_o_Lsq, 2.0 * EI_o_L, -6.0 * EI_o_Lsq, 4.0 * EI_o_L],
            ]
        )

    def get_M(self) -> ndarray:
        """Returns the [4x4] element mass matrix with order: w1, phi1, w2, phi2.

        :return: element stiffness matrix as 2D numpy array, rows are forces, columns are displacements
        :rtype: ndarray
        """
        self.verify()

        f: float = self.mass / 420.0
        L: float = self.length

        return array(
            [
                [156.0 * f, 22.0 * L * f, 54.0 * f, -13.0 * L * f],
                [
                    22.0 * L * f,
                    4.0 * pow(L, 2.0) * f,
                    13.0 * L * f,
                    -3.0 * pow(L, 2.0) * f,
                ],
                [54.0 * f, 13.0 * L * f, 156.0 * f, -22.0 * L * f],
                [
                    -13.0 * L * f,
                    -3.0 * pow(L, 2.0) * f,
                    -22.0 * L * f,
                    4.0 * pow(L, 2.0) * f,
                ],
            ]
        )


class BeamB_3DOF(ABeam):
    """Structural beam element with 3 DOF: u (axial), w (lateral), phi (rotational)."""

    @staticmethod
    def get_dofs() -> Tuple[DOF, DOF, DOF]:
        """Returns the DOFs for 3DOF beam type.

        :return: DOFs for 3DOF beam
        :rtype: Tuple[DOF, DOF, DOF]
        """
        return DOF.U, DOF.W, DOF.PHI

    def __init__(
        self,
        n1: Node,
        n2: Node,
        area: float,
        area_moi: float,
        e_modul: float,
        mass: float,
    ) -> None:
        # expected DOF
        if n1.dofs != BeamB_3DOF.get_dofs():
            raise ValueError(
                f"Invalid DOF for node1 of {BeamB_2DOF.__name__}, expected"
                f" {BeamB_3DOF.get_dofs()}"
            )
        if n2.dofs != BeamB_3DOF.get_dofs():
            raise ValueError(
                f"Invalid DOF for node2 of {BeamB_2DOF.__name__}, expected"
                f" {BeamB_3DOF.get_dofs()}"
            )

        super().__init__(n1, n2, area, area_moi, e_modul, mass)
        self._beam_type = f"{self.__class__.__name__}: Bernoulli, 3DOF, no p-Delta"

    def verify(self) -> None:
        """Verifies the beam and raises ValueError, if any invalid condition was detected.

        :raises ValueError: If any property is invalid
        """
        super().verify()
        if self.area <= 0.0:
            raise ValueError(f"Invalid cross section: {self.area} <= 0.0")

    def get_K(self, order: int = 1) -> ndarray:
        """Returns the [6x6] element stiffness matrix with order: u1, v1, phi1, u2, v2, phi2.

        :return: element stiffness matrix as 2D numpy array, rows are forces, columns are displacements
        :rtype: ndarray

        :raises ValueError: If order != 1
        """
        if order != 1:
            raise ValueError(
                f"Unsupported order {order}, supported is only {self.order}"
            )
        self.verify()

        EA_o_L: float = self.e_modul * self.area / self.length
        EI_o_L: float = self.e_modul * self.area_moi / self.length
        EI_o_Lsq: float = EI_o_L / self.length
        EI_o_Lqu: float = EI_o_Lsq / self.length

        return array(
            [
                [EA_o_L, 0.0, 0.0, -EA_o_L, 0.0, 0.0],
                [
                    0.0,
                    12.0 * EI_o_Lqu,
                    6.0 * EI_o_Lsq,
                    0.0,
                    -12.0 * EI_o_Lqu,
                    6.0 * EI_o_Lsq,
                ],
                [0.0, 6.0 * EI_o_Lsq, 4.0 * EI_o_L, 0.0, -6.0 * EI_o_Lsq, 2.0 * EI_o_L],
                [-EA_o_L, 0.0, 0.0, EA_o_L, 0.0, 0.0],
                [
                    0.0,
                    -12.0 * EI_o_Lqu,
                    -6.0 * EI_o_Lsq,
                    0.0,
                    12.0 * EI_o_Lqu,
                    -6.0 * EI_o_Lsq,
                ],
                [0.0, 6.0 * EI_o_Lsq, 2.0 * EI_o_L, 0.0, -6.0 * EI_o_Lsq, 4.0 * EI_o_L],
            ]
        )

    def get_M(self) -> ndarray:
        """Returns the [6x6] element mass matrix with order: u1, v1, phi1, u2, v2, phi2.

        :return: element stiffness matrix as 2D numpy array, rows are forces, columns are displacements
        :rtype: ndarray
        """
        self.verify()

        f: float = self.mass / 420.0
        L: float = self.length

        return array(
            [
                [140.0 * f, 0.0, 0.0, 70.0 * f, 0.0, 0.0],
                [0.0, 156.0 * f, 22.0 * L * f, 0.0, 54.0 * f, -13.0 * L * f],
                [
                    0.0,
                    22.0 * L * f,
                    4.0 * pow(L, 2.0) * f,
                    0.0,
                    13.0 * L * f,
                    -3.0 * pow(L, 2.0) * f,
                ],
                [70.0 * f, 0.0, 0.0, 140.0 * f, 0.0, 0.0],
                [0.0, 54.0 * f, 13.0 * L * f, 0.0, 156.0 * f, -22.0 * L * f],
                [
                    0.0,
                    -13.0 * L * f,
                    -3.0 * pow(L, 2.0) * f,
                    0.0,
                    -22.0 * L * f,
                    4.0 * pow(L, 2.0) * f,
                ],
            ]
        )


@runtime_checkable
class PBeamPDelta(Protocol):
    def get_K1(self) -> ndarray:
        ...

    def get_K2(self) -> ndarray:
        ...

    @property
    @abstractmethod
    def force_x(self) -> float:
        ...


class BeamB_2DOF_II(BeamB_2DOF):
    """Structural beam element with 2 DOF: w (lateral), phi (rotational) including p-Delta effects."""

    @staticmethod
    def get_dofs() -> Tuple[DOF, DOF]:
        """Returns the DOFs for 2DOF beam type with p-Delta effects.

        :return: DOFs for 2DOF beam
        :rtype: Tuple[DOF, DOF]
        """
        return DOF.W, DOF.PHI

    def __init__(
        self,
        n1: Node,
        n2: Node,
        area: float,
        area_moi: float,
        e_modul: float,
        mass: float,
    ) -> None:
        # super will ensure correct DOFs
        super().__init__(n1, n2, area, area_moi, e_modul, mass)
        self._beam_type = f"{self.__class__.__name__}: Bernoulli, 2DOF, with p-Delta"

        self._force_x: float = 0.0

    @property
    def order(self) -> int:
        return 2

    @property
    def force_x(self) -> float:
        return self._force_x

    def set_force_x(self, force_x: float) -> "BeamB_2DOF_II":
        self._force_x = force_x
        return self

    def get_K2(self) -> ndarray:
        return (self._force_x / (30.0 * self.length)) * array(
            [
                [36.0, 3.0 * self.length, -36.0, 3.0 * self.length],
                [
                    3.0 * self.length,
                    4.0 * pow(self.length, 2.0),
                    -3.0 * self.length,
                    -1.0 * pow(self.length, 2.0),
                ],
                [-36.0, -3.0 * self.length, 36.0, -3.0 * self.length],
                [
                    3.0 * self.length,
                    -1.0 * pow(self.length, 2.0),
                    -3.0 * self.length,
                    4.0 * pow(self.length, 2.0),
                ],
            ]
        )

    def get_K1(self) -> ndarray:
        return super().get_K()

    def get_K(self, order: int = 2) -> ndarray:
        if order != 1 and order != 2:
            raise ValueError(f"Invalid order {order}, supported are 1 or 2")
        if order == 1:
            return self.get_K1()
        else:
            return self.get_K1() + self.get_K2()
