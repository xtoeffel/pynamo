# -*- coding: utf-8 -*-
"""Solution of the eigenvalues, frequency and mode shapes."""
from model.system import CompBeamModel
from model.core import DOF, AXIS
from model.elements import Node
from model.entry import Spring
from model.utils import is_equal

from typing import Optional, Tuple, List
from numpy import array
from numpy import ndarray
from numpy import size
from numpy import argsort
from numpy import delete
from numpy import insert
from numpy.linalg import eig, inv
from pandas import DataFrame
from math import sqrt, pi
from copy import deepcopy

from solve.forces import CompBeamSolver


class SolutionError(ValueError):
    """Error that prevents finding the solution."""


class FlexEigenSolver:
    """Solves eigenvalue problem for flexural modes and finds frequency and mode shapes for composite beam models.

    Note: This assumes that the system's flexural modes are the once with the lowest frequency. If that would not
    be the case, e.g. with an extrem soft axial boundary condition, it might be that frequencies other than
    the flexural are returned.
    """

    def __init__(self) -> None:
        self._model: Optional[CompBeamModel] = None
        self._pref_positive_lat_msv: bool = False
        self._mode_count: int = 3
        self._normalize_shapes: bool = True
        self._order: int = 1
        self._gravity: float = 9.81

    @property
    def model(self) -> Optional[CompBeamModel]:
        """Composite beam model for which to find solution of eigenvalue problem.

        :return: Composite beam model
        :rtype: CompBeamModel
        """
        return self._model

    def set_model(self, model: CompBeamModel) -> "FlexEigenSolver":
        """Sets the model for which to find the solution of the eigenvalue problem.

        :param model: Composite beam model
        :type model: CompBeamModel

        :return: self for chaining of calls
        :rtype: FlexEigenSolver

        :raises ValueError: If model is None
        """
        if model is None:
            raise ValueError("Unable to set model as None")
        self._model = model
        return self

    @property
    def gravity(self) -> float:
        """Gravity or earth acceleration.

        :return: gravity
        :rtype: float
        """
        return self._gravity

    def set_gravity(self, gravity: float) -> "FlexEigenSolver":
        """Set the gravity (or earth acceleration).

        :param gravity: gravity or earth acceleration
        :type gravity: float

        :return: self for chaining of calls
        :rtype: FlexEigenSolver

        :raises ValueError: if gravity < 0.0
        """
        if gravity < 0.0:
            raise ValueError(f"Invalid gravity={gravity}, required: gravity >= 0.0")
        self._gravity = gravity
        return self

    @property
    def order(self) -> int:
        """Returns the order of the theory: 1 or 2 (2 is with p-Delta effects).

        :return: Order of theory
        :rtype: int
        """
        return self._order

    def set_order(self, order: int) -> "FlexEigenSolver":
        """Sets the order of the theory.

        :param order: Order of theory 1 or 2 (2 is with p-Delta effects)
        :type order: int

        :raises ValueError: If order any value other than 1 or 2
        """
        if order != 1 and order != 2:
            raise ValueError(
                f"Unsupported order (of theory): {order}, allowed are: 1 or 2"
            )
        self._order = order
        return self

    @property
    def is_pref_positive_lat_msv(self) -> bool:
        """Indicates whether positive lateral (z-axis) mode shape values are preferred.

        If True, then the mode shape values of all modes will be multiplied by -1.0 if the
        last z-value or mode shape value (at greatest x-coordinate) of the natural mode shape
        is negative. This is to ensure that the mode shape values of the natural mode shape are
        rather positive than negative.

        :return: True if positive
        :rtype: bool
        """
        return self._pref_positive_lat_msv

    def set_pref_positive_lat_msv(self, pref_positive: bool) -> "FlexEigenSolver":
        """Sets the indicator for preferred positive lateral (z-axis) mode shape values.

        If True, then the mode shape values of all modes will be multiplied by -1.0 if the
        last z-value or mode shape value (at greatest x-coordinate) of the natural mode shape
        is negative. This is to ensure that the mode shape values of the natural mode shape are
        rather positive than negative.

        :param pref_positive: True to prefer positive lateral mode shape values
        :type pref_positive: bool
        """
        self._pref_positive_lat_msv = pref_positive
        return self

    @property
    def mode_count(self) -> int:
        """Returns the number of the first lowest modes to compute mode shape values and frequencies for.

        :return: Mode count
        :rtype: int
        """
        return self._mode_count

    def set_mode_count(self, mode_count: int) -> "FlexEigenSolver":
        """Sets the number of the first lowest modes to compute mode shape values and frequencies for.

        :param mode_count: First lowest mode count
        :type mode_count: int

        :raises ValueError: If not 1 <= mode_count <= 10
        """
        if not (1 <= mode_count <= 10):
            raise ValueError(
                f"Invalid mode count {mode_count}, valid is: 1 <= mode_count <= 10"
            )
        self._mode_count = mode_count
        return self

    @property
    def is_normalize_shapes(self) -> bool:
        """Returns the indicator for normalization of mode shapes.

        :return: True if mode shape values will be normalized to 1.0, otherwise False
        :rtype: bool
        """
        return self._normalize_shapes

    def set_normalize_shapes(self, normalize: bool) -> "FlexEigenSolver":
        """Sets the indicator for normalization of mode shape values to 1.0.

        :param normalize: True to normalize mode shape values, False otherwise
        :type normalize: bool
        """
        self._normalize_shapes = normalize
        return self

    def solve(self) -> Tuple[ndarray, ndarray]:
        """Solves the eigenvalue problem and returns frequencies and mode shape values.

        :return: Tuple of first is frequencies, second is mode shape values
        :rtype: Tuple[ndarray, ndarray]

        :raises SolutionError: if solution cannot be found
        """
        if self._model is None:
            raise SolutionError(f"Unable to solve with model None")
        if self._model.is_empty:
            raise SolutionError(f"Model is empty")
        if self._order > self._model.order:
            raise SolutionError(
                f"Order of solution is set to {self._order} but model only supports"
                f" {self._model.order} for {self._model.beam_type}"
            )

        # cache properties
        model: CompBeamModel = deepcopy(self._model)
        dof: int = model.dof_num
        dofs: Tuple[DOF, ...] = self._model.dofs
        assert model.start_node is not None, "model start node is None"
        start_node: Node = model.start_node

        if self._order == 2:
            beam_solver: CompBeamSolver = CompBeamSolver(model)
            beam_solver.set_axial_forces(
                beam_solver.get_beams_normal_forces(
                    gravity=self.gravity, accumulate=True
                )
            )

        sys_M: ndarray = model.get_M()
        sys_K: ndarray = model.get_K(self._order)

        # determine boundary conditions
        # base spring
        start_spring: Optional[Spring] = (
            model.get_spring(start_node) if model.has_spring(start_node) else None
        )
        spring_set: bool = start_spring is not None and all(
            start_spring.has_dof(dof) for dof in dofs
        )
        # 0.0 for all DOF?
        dof_tol: float = 1.0e-12
        start_node_dof_0: bool = all(
            start_node.is_set(dof) and is_equal(0.0, start_node.get_dof(dof), dof_tol)
            for dof in dofs
        )
        # evaluate
        if not spring_set and not start_node_dof_0:
            raise SolutionError(
                f"Insufficient boundary conditions, set spring or 0.0 for all DOF of"
                f" start node."
            )

        # reduction of system matrixes if all start node DOF = 0.0;
        # mode shape values will be extended by 0.0 later
        if start_node_dof_0:
            sys_M = delete(
                delete(sys_M, list(range(0, dof)), 0), list(range(0, dof)), 1
            )
            sys_K = delete(
                delete(sys_K, list(range(0, dof)), 0), list(range(0, dof)), 1
            )

        # solve eigenvalue problem, compute frequencies
        omega_sq, ms = eig(inv(sys_M).dot(sys_K))
        sorted_idx: ndarray = argsort(omega_sq)
        freq: ndarray = array([sqrt(o.real) / (2 * pi) for o in omega_sq])

        # filter frequency and mode shapes (first specified)
        freq = freq[sorted_idx[: self._mode_count]]
        mode_shapes: ndarray = ms[:, sorted_idx[: self._mode_count]]
        num_rows: int = size(mode_shapes, 0)

        # interest is lateral deflection
        lat_idx: int = model.dofs.index(DOF.W)
        mode_shapes = mode_shapes[list(range(lat_idx, num_rows, model.dof_num)), :]
        # normalize
        if self._normalize_shapes:
            abs_max: float = 0.0
            for col_idx in range(0, size(mode_shapes, 1)):
                abs_max = max(abs(mode_shapes[:, col_idx]))
                mode_shapes[:, col_idx] = mode_shapes[:, col_idx] / abs_max
        # adding 0.0 for base lateral deflection if all DOF of start node were set to 0.0
        if start_node_dof_0:
            mode_shapes = insert(mode_shapes, 0, [0.0] * len(freq), axis=0)
        # adding column of x-coordinate
        mode_shapes = insert(mode_shapes, 0, model.get_coords(AXIS.X), axis=1)

        # prefer positive msv, only for lateral DOF, use first mode to determine
        if self._pref_positive_lat_msv and mode_shapes[-1, 0] < 0.0:
            for col_idx in range(0, size(mode_shapes, 1)):
                mode_shapes[:, col_idx] = mode_shapes[:, col_idx] * -1.0

        return freq, mode_shapes

    @staticmethod
    def to_dataframe(
        freq: ndarray, mode_shapes: ndarray
    ) -> Tuple[DataFrame, DataFrame]:
        """Converts the results of the solve() method to DataFrames.

        :param freq: Frequency result
        :type freq: ndarray
        :param mode_shapes: Mode shape value results
        :type mode_shapes: ndarray

        :return: DataFrame of frequency (converted from freq), DataFrame of
                    mode shape values (converted from mode_shapes)
        :rtype: Tuple[DataFrame, DataFrame]
        """

        mode_names: List[str] = [f"mode{m}" for m in range(1, len(freq) + 1)]
        freq_df: DataFrame = DataFrame(freq, index=mode_names, columns=["frequency"])
        msv_df: DataFrame = DataFrame(mode_shapes, columns=["x", *mode_names])

        return freq_df, msv_df
