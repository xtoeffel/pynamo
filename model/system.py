# TODO: test quality of system by evaluation of beam length or element size -> improve if possible
# TODO: use alternative software to determine mode shapes and freq for unit testing

"""Structural model with multiple beams like composite beam systems."""

from copy import deepcopy
from model.beams import ABeam
from model.core import DOF
from model.core import AXIS
from model.utils import expand_matrix
from model.elements import Node
from model.elements import by_offset
from model.entry import Mass
from model.entry import Spring
from model.utils import is_equal
from typing import List
from typing import Sequence
from typing import Optional
from typing import Type
from typing import Tuple
from typing import Union
from typing import Dict
from numpy import ndarray
from numpy import array
from numpy import zeros


# TODO: test adding of springs to model
# TODO: test adding of masses to model, especially by height
class CompBeamModel:
    """2D composite beam model of multiple beams of equal type, coordinate system: x=length, z=lateral.

    The system validation for solution is performed by the solver and depends on the solution approach.

    Masses: can be added to Nodes of the model, where the relationship is n to 1. Mass objects
    will be considered in the system mass matrix.

    Springs: can be attached to Nodes of the model where the relationship is 1 to 1. Springs will be
    considered in the system stiffness matrix.
    """

    def __init__(self) -> None:
        self._beams: List[ABeam] = []
        self._masses: Dict[Node, List[Mass]] = {}
        self._springs: Dict[Node, Spring] = {}

    @property
    def is_empty(self) -> bool:
        """Indicates whether the model is empty.

        :return: True if model is empty, otherwise False
        :rtype: bool
        """
        return len(self._beams) == 0

    @property
    def dof_num(self) -> int:
        """Returns the number of degree of freedom of the beams of this model (which apply to each beam).

        :return: DOF of the beams in this model, or 0 if the model is empty
        :rtype: int
        """
        if self.is_empty:
            return 0
        return self._beams[0].dof_num

    @property
    def dofs(self) -> Union[Tuple[()], Tuple[DOF, ...]]:
        """Degree of freedom of each beam of this model, e.g. (DOF.U, DOF.PHI).

        It is guaranteed that each beam is of the same type and therefore supports the same DOF.

        :return: Tuple of DOF of each beam of this model or empty Tuple if model is empty
        :rtype: Tuple[DOF, ...]
        """
        if self.is_empty:
            return ()
        return self._beams[0].dofs

    @property
    def order(self) -> int:
        """Returns the order of the model applicable to every element.

        :return: 1 or 2 (2 is with p-Delta effects) depending on element type, 0 if model is empty
        :rtype: int
        """
        if self.is_empty:
            return 0
        return self._beams[0].order

    @property
    def beam_type(self) -> str:
        """Returns the beam type designator for this model.

        :return: Beam type
        :rtype: str
        """
        if self.is_empty:
            return "undef"
        return self._beams[0].beam_type

    def get_coords(self, axis: AXIS) -> List[float]:
        """Returns a list of coordinates of all nodes in the model.

        Note: The model is a composite beam model. Therefore the y and z coordinates of all nodes should be 0.0;
        however, this is not enforced.

        :param axis: Axis for which to get the coordinates

        :return: List of coordinates of all nodes, or an empty list if model is empty
        :rtype: List[float]
        """
        coords: List[float] = []
        if self.is_empty:
            return coords

        x: float = self._beams[0].node1.get_coord(axis)
        coords.append(x)
        for b in self._beams:
            coords.append(b.node2.get_coord(axis))
        return coords

    @property
    def nodes(self) -> List[Node]:
        """Returns a list of all nodes.

        :return: List of all nodes
        :rtype: List[Node]
        """
        nodes: List[Node] = [b.node1 for b in self._beams]
        if not self.is_empty:
            assert self.end_node is not None, "Model end node is None"
            nodes.append(self.end_node)
        return nodes

    # TODO: change name of method, node does not have a height, but coords -- get_node_by_coord?
    def get_node_by_height(self, height: float, htol: float = 1.0e-4) -> Node:
        """Gets a node at a specific height.

        :param height: height to get node at
        :type height: float
        :param htol: symmetric height tolerance
        :type htol: float

        :return: node at height
        :rtype: Node

        :raises ValueError: if no node exists at height
        """
        nodes: List[Node] = [
            n for n in self.nodes if is_equal(height, n.get_coord(AXIS.X), atol=htol)
        ]
        if len(nodes) == 1:
            return nodes[0]
        else:
            raise ValueError(f"No node exists at height = {height}")

    def offset(self, vector: Dict[AXIS, float]) -> "CompBeamModel":
        """Offsets the entire model, meaning all nodes of the model by the specified vector (parallel shift).

        :param vector: Offset vector
        :type vector: Dict[AXIS, float]

        :return: self for chaining of calls
        :rtype: CompBeamModel

        :raises ValueError: If vector is empty
        """
        if len(vector) == 0:
            raise ValueError("Empty offset vector")
        for n in self.nodes:
            n.offset(vector)
        return self

    @property
    def beams(self) -> List[ABeam]:
        """List of all beams.

        :return: deepcopied list of all beams
        :rtype: List[ABeam]
        """
        return deepcopy(self._beams)

    def add(self, beam: ABeam) -> "CompBeamModel":
        """Adds a beam to the model.

        All beams must be of the exact same type, subtypes are not accepted.
        The type is defined by the first beam added to the model. Beams must
        be of subtype of ABeam, however, not ABeam itself. Node1 of any beam
        to be added must be Node2 of the prior beam (last beam added before
        or current end beam of the model).

        :param beam: Beam to be added
        :type beam: BaseBeam

        :raises ValueError: If beam is None
        :raises TypeError: If beam is not of correct type, that is type of
                            the first added beam, or on attempt to add
                            a beam of ABeam or not a subtype of ABeam, or if
                            node1 of beam to be added is not node2 of prior beam
                            (current last beam of the model)

        :return: Self for chaining of calls
        :rtype: CompBeamModel
        """
        if beam is None:
            raise ValueError("None is invalid for beam")
        if type(beam) == ABeam:
            raise TypeError(f'Cannot add beam of type "{ABeam.__class__.__name__}"')
        if not issubclass(beam.__class__, ABeam):
            raise TypeError(
                f'Invalid beam type "{beam.__class__.__name__}", '
                f'not a subtype of "{ABeam.__name__}"'
            )
        if not self.is_empty and type(self._beams[-1]) != type(beam):
            raise TypeError(
                f'Invalid beam type "{beam.__class__.__name__}": '
                f'expected "{self._beams[-1].__class__.__name__}", '
                "beam types cannot be mixed in model"
            )
        # TODO: check for node types and DOF instead of beam type? allow insertion of 'spring' elements, etc.
        if any(beam is b for b in self._beams):
            raise ValueError(f"The beam {beam} exists in the model")
        if not self.is_empty and not self._beams[-1].node2 is beam.node1:
            raise ValueError(
                f"Node1 of {beam} is not Node2 of current end beam of model"
            )

        self._beams.append(beam)
        return self

    def add_all(self, beams: Sequence[ABeam]) -> "CompBeamModel":
        """Adds a sequence of beams to the model.

        All beams in the list must be of the exact same type, subtypes are
        not accepted. If this model has beams already, then all beams must
        be exact of that type.

        :param beams: Beams to be added
        :type beams: Sequence[BaseBeam]

        :return: Self for chaining of calls
        :rtype: CompBeamModel

        :raises ValueError: see .add() method
        :raises TypeError: see .add() method
        """

        for beam in beams:
            self.add(beam)
        return self

    def append(self, length: float, **beam_data: float) -> "CompBeamModel":
        """Append a beam by using the end node of the last beam in the model as start node of the new beam to be added.

        :param length: Length of beam to be appended
        :type length: float
        :param beam_data: Values defining the beam properties; these are all arguments after the two nodes for the
                            ABeam.__init__() method -- area, area_moi, e_modul, mass
        :type beam_data: float

        :raises ValueError: If this model is empty (append impossible), or length <= 0.0
        """
        if self.is_empty:
            raise ValueError("Empty model cannot append beam")
        if length <= 0.0:
            raise ValueError(f"Invalid beam length = {length}, allowed is length > 0.0")

        n1: Optional[Node] = self.end_node
        assert n1 is not None, "End node is None"
        end_beam: Optional[ABeam] = self.end_beam
        assert end_beam is not None, "End beam is None"
        new_beam: ABeam = end_beam.__class__(
            n1, by_offset(n1, {AXIS.X: length}), **beam_data
        )
        return self.add(new_beam)

    @property
    def count(self) -> int:
        """Returns the number of beams in this model.

        :return: Number of beams
        :rtype: int
        """
        return len(self._beams)

    def get(self, index: int) -> ABeam:
        """Returns a beam at a specific index.

        :return: Beam at index
        :rtype:

        :raises IndexError: If index is out of bounds
        """
        return self._beams[index]

    @property
    def end_node(self) -> Node:
        """Returns the current end node of the model, that is the end node of the last beam.

        :return: End node of model or None if model is empty
        :rtype: Node

        :raise ValueError: if end node is not defined (available)
        """
        if self.is_empty:
            raise ValueError("Undefined end node, model is empty")
        return self._beams[-1].node2

    @property
    def end_beam(self) -> ABeam:
        """Returns the last beam of the model, that is the last beam that was added.

        :return: Last (end) beam of the model
        :rtype: ABeam

        :raise ValueError: if end beam is undefined (not available)
        """
        if self.is_empty:
            raise ValueError("Undefined end beam, model is empty")
        return self._beams[-1]

    @property
    def start_node(self) -> Node:
        """Returns the start or first node of the model.

        :return: Start (first) node of model
        :rtype: Node

        :raise ValueError: if start node is not defined (available)
        """
        if self.is_empty:
            raise ValueError("Undefined start node, model is empty")
        return self._beams[0].node1

    @property
    def start_beam(self) -> ABeam:
        """Returns the start beam of the model.

        :return: Start beam
        :rtype: ABeam

        :raise ValueError: if start beam is undefined (not available)
        """
        if self.is_empty:
            raise ValueError("Undefined start beam, model is empty")
        return self._beams[0]

    # TODO: rename every attribute for node masses to include 'node', like 'add_mass' to 'add_node_mass'?
    @property
    def node_masses(self) -> Dict[Node, List[Mass]]:
        """All node masses.

        :return: deepcopied dict of all node masses
        :rtype: Dict[Node, List[Mass]]
        """
        return deepcopy(self._masses)

    def add_mass(self, node: Node, mass: Mass) -> "CompBeamModel":
        """Adds a mass to a specific node.

        More than one mass can be added to a node as a list of masses is saved per node.

        :param node: Node to add mass to
        :type node: Node
        :param mass: Mass to add to node
        :type mass: Mass

        :return: Self for chaining of calls
        :rtype: CompBeamModel

        :raises ValueError: If node does not exist (for this model)
        """
        if node not in self.nodes:
            raise ValueError(f"Node {node} does not exist")
        if node in self._masses:
            self._masses[node].append(mass)
        else:
            self._masses[node] = [mass]
        return self

    def assign_mass(
        self, mass: Mass, x: float, htol: float = 1.0e-4
    ) -> "CompBeamModel":
        """Assign a mass at a specific x-coordinate by selecting the nearest node to add the mass to.

        The nearest node to x will be determined and the mass will be added to that node. The lower nodes is preferred
        in case that x is located exactly in the center between two adjacent nodes.

        :param mass: mass to attach
        :type mass: Mass
        :param x: x-coordinate
        :type x: float
        :param htol: symmetric height tolerance
        :type htol: float

        :return: self for chaining of calls
        :rtype: CompBeamModel

        :raises ValueError: if count node of model < 2, if x out of range from start to end nodes x-coordinate
        """
        assert self.end_node is not None
        assert self.start_node is not None
        x_low: float = self.start_node.get_coord(AXIS.X)
        x_high: float = self.end_node.get_coord(AXIS.X)

        if self.count < 2:
            raise ValueError(
                f"Insufficient nodes to assign mass: found {self.count}, required are 2"
            )
        if not is_equal(x, x_low, htol) and x < x_low:
            raise ValueError(f"Invalid x-coordinate = {x} < {x_low} (start beam)")
        if not is_equal(x, x_high, htol) and x > x_high:
            raise ValueError(f"Invalid x-coordinate = {x} > {x_high} (end beam)")

        nodes: List[Node] = self.nodes
        nodes_at_x: List[Node] = [
            n for n in nodes if is_equal(n.get_coord(AXIS.X), x, htol)
        ]

        if len(nodes_at_x) >= 1:
            self.add_mass(nodes_at_x[0], mass)
        else:
            n_below: Node = max(
                [n for n in nodes if n.get_coord(AXIS.X) < x],
                key=lambda n: n.get_coord(AXIS.X),
            )
            n_above: Node = min(
                [n for n in nodes if n.get_coord(AXIS.X) > x],
                key=lambda n: n.get_coord(AXIS.X),
            )
            if abs(x - n_below.get_coord(AXIS.X)) <= abs(n_above.get_coord(AXIS.X) - x):
                self.add_mass(n_below, mass)
            else:
                self.add_mass(n_above, mass)

        return self

    def has_mass_at_node(self, node: Node) -> bool:
        """Indicates whether a mass is registered for the specific node.

        :param node: node to check for mass
        :type node: Node

        :return: True if node has at least one mass registered, otherwise False
        """
        return node in self._masses

    def get_masses_of_node(self, node: Node) -> List[Mass]:
        """Gets the list of defined masses for a specified node.

        The list is a copy of the internal list.

        :return: List of mass of node
        :rtype: List[Mass]
        """
        if node not in self._masses:
            raise IndexError(f"No mass defined for node {node}")
        return list(self._masses[node])

    def mass_count(self, node: Optional[Node] = None) -> int:
        """Returns the number of masses defined for a specific node or the total number of for all nodes.

        :param node: Node to get mass count for, or None for total mass count of model
        :type node: Node

        :return: Number of masses per node or total number of masses for the model (if node is None)
        :rtype: int
        """
        if node is not None and node not in self._masses:
            raise IndexError(f"Node {node} does not exist")
        return (
            len([m for n in self._masses.values() for m in n])
            if node is None
            else len(self._masses[node])
        )

    # TODO: how to handle DOFs for mass? -- masses act in either direction not DOF! -> global CSYS missing?
    @property
    def total_node_masses(self) -> float:
        """Returns the total mass of all masses added to nodes of the model.

        :return: total mass of all point masses
        :rtype: float
        """
        return sum(m.get_value(DOF.W) for n, ms in self._masses.items() for m in ms)

    @property
    def mass(self) -> float:
        """Returns the total mass of the model, that is beam mass and added masses.

        :return: total mass of model
        :rtype: float
        """
        return self.total_mass_beams + self.total_node_masses

    @property
    def total_mass_beams(self) -> float:
        """Returns the mass of all beams of the model, excluding additional masses like point masses.

        :return: Total beam mass of the model
        :rtype: float
        """
        return sum(b.mass for b in self._beams)

    # TODO: test attaching of springs, check for fails by unsupported DOF (if DOF that does not exist in model)
    def attach_spring(self, node: Node, spring: Spring) -> "CompBeamModel":
        """Attach a spring to a specific node of the model.

        :param node: Node to attach spring to
        :type node: Node
        :param spring: Spring to attach
        :type spring: Spring

        :return: self for chaining of calls
        :rtype: CompBeamModel

        :raises ValueError: if node does not exist (is not a node of this model)
        """
        if node not in self.nodes:
            raise ValueError(f"Node {node} does not exist")
        for dof in spring.dofs:
            if dof not in node.dofs:
                raise ValueError(f"Spring has DOF {dof} which is not supported by node")
        self._springs[node] = spring
        return self

    def has_spring(self, node: Node) -> bool:
        """Indicates whether a spring exists for a specific node.

        :param node: node to check for spring
        :type node: Node

        :return: True if spring exist for node, otherwise False
        """
        return node in self._springs

    def get_spring(self, node: Node) -> Spring:
        """Returns the spring for a specific node.

        :param node: Node to get spring for
        :type node: Node

        :raises KeyError: if spring does not exist for node
        """
        return self._springs[node]

    @property
    def spring_count(self) -> int:
        """Returns the number of attached springs.

        Note: the relationship between model node and spring is 1 to 1

        :return: Number of attached springs
        """
        return len(self._springs)

    @property
    def springs(self) -> Dict[Node, Spring]:
        """Returns a dictionary of all attached springs.

        :return: Dictionary of attached springs -- changes to that dictionary will not effect self
        :rtype: Dict[Node, Spring]
        """
        return deepcopy(self._springs)

    @property
    def length(self) -> float:
        """Returns the total length of the model.

        :return: Total model length
        :rtype: float
        """
        return sum(b.length for b in self._beams)

    def _point_masses_to_sys_M(self, sys_mass_matrix: ndarray) -> ndarray:
        """Insert point mass matrixes of all defined masses into system mass matrix and return combined matrix.

        :param sys_mass_matrix: System mass matrix
        :type sys_mass_matrix: ndarray

        :return: System mass matrix with mass points inserted
        """
        if self.mass_count == 0:
            return sys_mass_matrix
        else:
            assert self.start_node is not None

            dofs: Tuple[DOF, ...] = self.dofs
            dof_num: int = self.dof_num
            nodes: List[Node] = self.nodes

            # loop over masses and insert in system mass matrix
            for node, masses in self._masses.items():
                node_idx: int = nodes.index(node)
                # index of the first DOF of the node in system matrix
                sys_idx: int = node_idx * dof_num
                # insert point mass matrix in system mass matrix
                for mass in masses:
                    sys_mass_matrix[
                        sys_idx : sys_idx + dof_num, sys_idx : sys_idx + dof_num
                    ] += mass.get_M(dofs)

            return sys_mass_matrix

    def get_M(self) -> ndarray:
        """Returns the system mass matrix.

        :return: System mass matrix
        :rtype: ndarray

        :raises ValueError: If model is empty
        """
        if self.is_empty:
            raise ValueError(f"Empty model, unable to generate mass matrix")
        sys_M = self._beams[0].get_M()
        for beam in self._beams[1:]:
            sys_M = expand_matrix(sys_M, beam.get_M())
        return self._point_masses_to_sys_M(sys_M)

    def _springs_to_sys_K(self, sys_K: ndarray) -> ndarray:
        """Inserts the element stiffness matrix of all springs into the system stiffness matrix.

        :param sys_K: system stiffness matrix
        :type sys_K: ndarray

        :return: system stiffness matrix with all spring element matrixes included or sys_K if none defined
        """
        if len(self._springs) == 0:
            return sys_K

        assert self.start_node is not None

        # cache some variables
        nodes: List[Node] = self.nodes
        node_dofs: Tuple[DOF, ...] = self.start_node.dofs
        dof_num: int = self.dof_num

        for node, spring in self._springs.items():
            # insert spring K in system K
            idx_node: int = nodes.index(node)
            sys_idx: int = idx_node * dof_num
            sys_K[
                sys_idx : sys_idx + dof_num, sys_idx : sys_idx + dof_num
            ] += spring.get_K(node_dofs)
        return sys_K

    def get_K(self, order: int = 1) -> ndarray:
        """Returns the system stiffness matrix.

        :param order: 1 or 2 (2 includes p-Delta effects)
        :type order: int

        :return: System stiffness matrix
        :rtype: ndarray

        :raises ValueError: If model is empty or if specified order is not supported
        """
        if self.is_empty:
            raise ValueError(f"Empty model, unable to generate stiffness matrix")
        sys_K = self._beams[0].get_K(order)
        for beam in self._beams[1:]:
            sys_K = expand_matrix(sys_K, beam.get_K(order))
        return self._springs_to_sys_K(sys_K)
