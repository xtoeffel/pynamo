"""Nodes for beam ends and other related elements, like point masses."""
from model.core import DOF, AXIS
from model.entry import Mass
from typing import Tuple
from typing import Set
from typing import List
from typing import Dict
from typing import TypeVar
from typing import Generic
from typing import Type
from typing import Union
from typing import Final
from typing import Optional
from math import pow
from math import sqrt
from copy import deepcopy

# TODO: DOF must also be computed, if they are not set (to define BC)
class Node:
    """3D Node with set of DOF.

    Location: A node has 3 coordinate values (defined by the enum AXIS) which define its location in 3D-CSYS.

    DOF: Each node has a DOF definition which defines what DOF the nodes supports.
    For instance, although it has a 3D coordinate system, it might only support a single DOF, like DOF.W.

    Values: It is allowed to set values for each DOF - e.g. to define boundary conditions a node's DOF.W can
    be set to 0.0. Solvers use that information to manage boundary conditions. DOF with no values set will be
    free and their displacement will be computed.
    """

    def __init__(self, dofs: Tuple[DOF, ...], coords: Dict[AXIS, float] = {}) -> None:
        """Creates a new node.

        :param dofs: Defines the degree of freedom the node will have
        :type dofs: Tuple[DOF, ...]
        :param coords: Coordinates in 3D-CSYS defined by AXIS
        :type coords: Dict[AXIS, float]

        :raises ValueError: if dofs is None or empty, if dofs contains any duplicates
        """
        if dofs is None:
            raise ValueError("Undefined set of DOF")
        if len(dofs) == 0:
            raise ValueError("Empty set of DOF")
        if len(dofs) != len(set(dofs)):
            raise ValueError(f"Duplicate DOF in {dofs}")

        self._dofs: Final[Tuple[DOF, ...]] = dofs
        self._dof_num = len(self._dofs)
        self._dof_values: Dict[DOF, float] = dict()

        self._coords: Dict[AXIS, float] = dict()
        for c in AXIS:
            self._coords[c] = 0.0

        # sets only these coords that are specified
        for k, v in coords.items():
            self._coords[k] = v

    @property
    def dof_num(self) -> int:
        """Returns the number of DOF.

        :return: number of DOF
        :rtype: int
        """
        return self._dof_num

    @property
    def dofs(self) -> Tuple[DOF, ...]:
        """Returns the tuple of all DOF supported by this node.

        :return: Tuple of supported DOF
        :rtype: Tuple[DOF, ...]
        """
        return self._dofs

    def set_coord(self, axis: AXIS, value: float) -> "Node":
        """Sets the value for a specific coordinate specified by AXIS.

        :param axis: Axis to set coordinate for
        :type axis: AXIS
        :param value: coordinate value
        :type value: float
        """
        self._coords[axis] = value
        return self

    def set_coords(self, coords: Dict[AXIS, float]) -> "Node":
        """Sets the coordinates for specific AXIS.

        :param coords: Cooridnate value by axis
        :type coords: Dict[AXIS, float]

        :return: Self for chaining of calls

        :raises ValueError: if coord is None
        """
        if coords is None:
            raise ValueError("Dictionary of coordinates is None")
        for coord, value in coords.items():
            self.set_coord(coord, value)
        return self

    def get_coord(self, axis: AXIS) -> float:
        """Gets the coordinate value for a specific axis.

        :param axis: Axis to get coordinate value for
        :type axis: AXIS

        :return: coordinate value of specified axis
        """
        return self._coords[axis]

    @property
    def coords(self) -> Dict[AXIS, float]:
        """Returns a dictionary with all coordinate values by AXIS.

        Note: chaning this dictionary will not have any effect on the coordinates of this object.

        :return: Dictionary with all coordinates
        :rtype: Dict[AXIS, float]
        """
        return deepcopy(self._coords)

    def offset(self, vector: Dict[AXIS, float]) -> "Node":
        """Offsets the node by a specific vector:

        :param vector: Offset vector
        :type vector: Dict[AXIS, float]

        :return: Self for chaining of calls

        :raises ValueError: if vector is empty
        """
        if len(vector) == 0:
            raise ValueError("Empty offset vector")
        for axis, value in vector.items():
            self._coords[axis] = value + self._coords[axis]
        return self

    def set_dof(self, dof: DOF, value: float) -> "Node":
        """Sets the value of a specific DOF.

        :param dof: DOF to set value for
        :type dof: DOF

        :return: Self for chaining of calls

        :raises ValueError: if dof is not supported
        """
        if dof not in self._dofs:
            raise ValueError(f"Unsupported DOF {dof.name}")
        self._dof_values[dof] = value
        return self

    def get_dof(self, dof: DOF) -> float:
        """Returns the value of a specific DOF.

        :param dof: DOF to get value for
        :type dof: DOF

        :return: Value of dof
        :rtype: float

        :raises KeyError: if no value is set for dof
        """
        return self._dof_values[dof]

    def is_set(self, dof: DOF) -> bool:
        """Indicates whether a value is set for a specific DOF.

        :param dof: DOF to check for value
        :type dof: DOF

        :return: True if value is set for dof, otherwise False -- dof must be supported for this node

        :raises KeyError: if dof is not supported for this node
        """
        if dof not in self._dofs:
            raise KeyError(f"Unsupported DOF {dof} for node {self}")
        return dof in self._dof_values

    @property
    def set_dofs(self) -> List[DOF]:
        """Returns the list of DOFs for which are values set for.

        :return: List of DOFs with values set
        :rtype: List[DOF]
        """
        return list(self._dof_values.keys())

    @property
    def has_set_dofs(self) -> bool:
        """Indicates whether values for DOFs are set.

        :return: True if values for any DOFs are set, otherwise False
        :rtype: bool
        """
        return len(self._dof_values) > 0

    def distance(self, to_other: "Node") -> float:
        """Computes the straight distance to any another node ignoring the fact that the DOFs might differ.

        :param to_other: other node to compute distance to
        :type to_other: Node

        :return: Straight distance from this to other node
        """
        dx: float = to_other.get_coord(AXIS.X) - self.get_coord(AXIS.X)
        dy: float = to_other.get_coord(AXIS.Y) - self.get_coord(AXIS.Y)
        dz: float = to_other.get_coord(AXIS.Z) - self.get_coord(AXIS.Z)

        return sqrt(pow(dx, 2.0) + pow(dy, 2.0) + pow(dz, 2.0))

    def __str__(self) -> str:
        """Returns the string representation of node."""
        return (
            self.__class__.__name__
            + "["
            + ", ".join(f"{a.name}={v}" for a, v in self._coords.items())
            + "]"
        )


def by_axial_length(dofs: Tuple[DOF, ...], length: float) -> Tuple[Node, Node]:
    """Creates a pair of nodes that are appart by length on the x-axis, all other coordinates are 0.0.

    The first node (also first element in returned tuple) is at CSYS origin (all coords 0.0) where the
    second (second element) is x=length away (y and z = 0.0).

    :param dofs: Set of DOF for nodes
    :type dofs: Set[DOF]

    :return: Tuple of node1, node2 where node1 has coords 0.0 for all axis and node2 as well, except x=length
    :rtype: Tuple[Node, Node]

    :raises ValueError: If length <= 0.0
    """
    if length <= 0.0:
        raise ValueError(f"Invalid length = {length}, allowed is length > 0.0")
    node1: Node = Node(dofs)
    node2: Node = Node(dofs, {AXIS.X: length})

    return node1, node2


def by_offset(node: Node, vector: Dict[AXIS, float]) -> Node:
    """Creates a new node by offsetting from another by vector.

    :param node: Node to offset from
    :type node: Node

    :raises ValueError: If vector is empty
    """
    new_node: Node = Node(node.dofs, node.coords)
    new_node.offset(vector)
    return new_node
