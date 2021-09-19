"""Solving for system forces and related computations."""
from model.core import DOF
from model.elements import Node
from model.system import CompBeamModel
from model.beams import ABeam
from typing import List
from typing import Dict
from typing import Any
from typing import Final
from typing import Protocol
from typing import runtime_checkable
from typing import cast

from numpy import array
from numpy import ndarray

from abc import abstractmethod


# TODO: beams should not save the axial force, instead it should be saved in a LoadCase data structure
# TODO: add logic and code structure to show that this is only for CompBeamModels, ensure that w,z == 0 for all nodes
@runtime_checkable
class _PSolvableBeam(Protocol):
    def set_force_x(self, force: float) -> Any:
        ...

    @property
    @abstractmethod
    def mass(self) -> float:
        ...


class CompBeamSolver:
    """Solver forces of for composite beam models.

    Composite beam models are, for instance, cantilever beams or inverted pendulum and
    persit of one or more coupled beam elements (beams).
    """

    def __init__(self, model: CompBeamModel):
        """Creates new composite beam solver object.

        The model will be deepcopied, therefore it's state is frozen into the solver object.

        :param model: model to solve for (will be deepcopied)
        :type model: CompBeamModel

        :raises AttributeError: if any beam of the model is missing required attributes
        :raises ValueError: if model is empty
        """
        if model.is_empty:
            raise ValueError(f"Model is empty")
        protocol_attributes: List[str] = [
            attr for attr in dir(_PSolvableBeam) if not attr.startswith("_")
        ]
        if any(not isinstance(beam, _PSolvableBeam) for beam in model.beams):
            raise AttributeError(
                "At least one beam is missing required attributes"
                f" {protocol_attributes}"
            )

        self._model: CompBeamModel = model
        # CompBeamModel.beams returns deepcopied list; however, the real beam-objects
        # are required for the solver to set attributes to the actual beams of the model
        self._beams: Final[List[_PSolvableBeam]] = [
            cast(_PSolvableBeam, self._model.get(idx))
            for idx in range(0, self._model.count)
        ]

    @property
    def model(self) -> CompBeamModel:
        """Model of the solver.

        :return: model of solver
        :rtype: CompBeamModel
        """
        return self._model

    def get_beams_dead_weight(
        self, gravity: float = 9.81, accumulate: bool = False
    ) -> ndarray:
        """Returns an array of dead weight (self weight force in COG) for each element in their order.

        Compression forces are negative.

        :param gravity: Gravity or earth acceleration to convert mass to force
        :type gravity: float
        :param accumulate: True to accumulate the mass of 'upper' elements to lower (e.g. for vertical structure),
                            False to not accumulate and get single element dead weights
        :type accumulate: bool

        :return: array with all beam dead weights (synchronized to the model's beams by index)
        :rtype: ndarray

        :raise ValueError: If gravity < 0.0
        """
        if gravity < 0.0:
            raise ValueError(f"Invalid gravity={gravity}, required: gravity >= 0.0")

        if not accumulate:
            return array([-1.0 * b.mass * gravity for b in self._beams])

        dead_weights: List[float] = []
        prev_dead_weight: float = 0.0
        beam_dead_weight: float = 0.0

        for idx in range(len(self._beams) - 1, -1, -1):
            beam_dead_weight = -1.0 * self._beams[idx].mass * gravity + prev_dead_weight
            dead_weights.append(beam_dead_weight)
            prev_dead_weight = beam_dead_weight

        dead_weights.reverse()
        return array(dead_weights)

    def get_beams_normal_forces(
        self, gravity: float = 9.81, accumulate: bool = False
    ) -> ndarray:
        """Returns for all beams an array of normal forces from self weight and masses applied to model nodes.

        Compression forces are negative.

        :param gravity: Gravity or earth acceleration to convert mass to force
        :type gravity: float
        :param accumulate: True to accumulate all forces according to their structural configuration
                        (attr.g. upper beams load lower beams)
        :type accumulate: bool

        :return: array with all beam forces (synchronized to the model's beams by index)
                 or empty array if model is empty
        :rtype: ndarray

        :raise ValueError: If gravity < 0.0
        """
        if gravity < 0.0:
            raise ValueError(f"Invalid gravity={gravity}, required: gravity >= 0.0")

        if self._model.is_empty:
            return array([])

        # accumulation of beams dead weight will be done
        # in this method, use accumulate=False here
        beams_dead_weight: ndarray = self.get_beams_dead_weight(
            gravity=gravity, accumulate=False
        )
        total_mass_to_nodes_defined: Dict[Node, float] = {
            node: sum(m.get_value(DOF.U) for m in masses)
            for node, masses in self._model._masses.items()
        }
        total_mass_of_model_nodes: List[float] = [
            total_mass_to_nodes_defined.get(node, 0.0) for node in self._model.nodes
        ]
        force_of_model_nodes: List[float] = [
            -1.0 * mass * gravity for mass in total_mass_of_model_nodes
        ]

        # in the model nodes must have one item more than beams as they are 2 for each
        # beam: beam1.node1, beam1.node2 where node2 is beam2.node1 and so on
        assert (
            len(beams_dead_weight) == len(force_of_model_nodes) - 1
        ), "number of beams != number of nodes - 1"

        force_of_model_beams: List[float] = [
            node1_force + beam_dead_weight
            for node1_force, beam_dead_weight in zip(
                force_of_model_nodes[1:], beams_dead_weight
            )
        ]
        if accumulate:
            for idx in range(len(force_of_model_beams) - 2, -1, -1):
                force_of_model_beams[idx] = (
                    force_of_model_beams[idx + 1] + force_of_model_beams[idx]
                )

        return array(force_of_model_beams)

    def set_axial_forces(self, axial_forces: ndarray) -> "CompBeamSolver":
        """Sets the axial forces to the beams of the model.

        Compression forces are negative, tension is positive.

        :param axial_forces: axial forces of beams
        :type axial_forces: ndarray

        :return: self for chaining of calls
        :rtype: CompBeamSolver

        :raises AttributeError: if any beam of the model does not suppport axial (normal) force to be set
        """
        if self._model.is_empty:
            raise ValueError("Model is empty, unable to set axial forces")

        if len(axial_forces) == 0:
            raise ValueError("Empty vector of axial forces")

        if len(axial_forces) == 1:
            for b in self._beams:
                b.set_force_x(axial_forces[0])  # type: ignore
        else:
            for b, f in zip(self._beams, axial_forces):
                b.set_force_x(f)  # type: ignore
        return self
