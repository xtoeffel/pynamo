from unittest import TestCase
from unittest import main

from model.system import CompBeamModel
from model.beams import PBeamPDelta
from data_io.json import JsonReader
from solve.forces import CompBeamSolver
from solve.eigen import FlexEigenSolver

from pathlib import Path
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from copy import copy

from numpy import ndarray
from numpy import array


wind_tower_model: Optional[CompBeamModel] = None
dlubal_beam_model_I: Optional[CompBeamModel] = None
dlubal_beam_model_II: Optional[CompBeamModel] = None
tower_munich_model: Optional[CompBeamModel] = None


def get_wind_tower_model() -> CompBeamModel:

    global wind_tower_model

    if wind_tower_model is None:
        model_file: Path = Path(__file__).absolute().parent / "ut" / "wind_tower3.json"
        print(f"loading model from {str(model_file)}")
        file_content: Dict[str, Any] = (
            JsonReader().set_file_name(str(model_file)).read()
        )
        wind_tower_model = file_content["model"]

    return wind_tower_model


def get_dlubal_beam_model() -> CompBeamModel:

    global dlubal_beam_model_I

    if dlubal_beam_model_I is None:
        model_file: Path = Path(__file__).absolute().parent / "ut" / "dlubal_beam.json"
        print(f"loading model from {str(model_file)}")
        file_content: Dict[str, Any] = (
            JsonReader().set_file_name(str(model_file)).read()
        )
        dlubal_beam_model_I = file_content["model"]

    return dlubal_beam_model_I


def get_tower_munich_model() -> CompBeamModel:

    global tower_munich_model

    if tower_munich_model is None:
        model_file: Path = Path(__file__).absolute().parent / "ut" / "tower_munich.json"
        print(f"loading model from {str(model_file)}")
        file_content: Dict[str, Any] = (
            JsonReader().set_file_name(str(model_file)).read()
        )
        tower_munich_model = file_content["model"]

    return tower_munich_model


class TestBeamSolver(TestCase):
    def setUp(self) -> None:
        print("Setup test objects: getting model, create beam solver, init expected")
        self.model: CompBeamModel = get_wind_tower_model()
        self.gravity: float = 10.0

        self._compute_expected_beam_dead_weight()
        self._compute_expected_normal_forces()

        self.beam_solver: CompBeamSolver = CompBeamSolver(self.model)

    def _compute_expected_beam_dead_weight(self) -> None:
        self.beams_dead_weight_expected: List[float] = [
            -1.0 * beam.mass * self.gravity for beam in self.model.beams
        ]
        beams_dead_weight_exp_reversed: List[float] = copy(
            self.beams_dead_weight_expected
        )
        beams_dead_weight_exp_reversed.reverse()
        self.beams_dead_weight_acc_expected: List[float] = []
        for idx, dw in enumerate(beams_dead_weight_exp_reversed):
            if idx == 0:
                self.beams_dead_weight_acc_expected.append(dw)
            else:
                self.beams_dead_weight_acc_expected.append(
                    self.beams_dead_weight_acc_expected[idx - 1] + dw
                )
        self.beams_dead_weight_acc_expected.reverse()

    def _compute_expected_normal_forces(self) -> None:
        self.beams_normal_force_expected: List[float] = [
            -168130,
            -229116,
            -200908,
            -175984,
            -259322,
            -209966,
            -231813,
            -154057,
            -150268,
            -161558,
            -184332,
            -53843,
            -77920,
            -103053,
            -117213,
            -130169,
            -129653,
            -326567,
            -123505,
            -120470,
            -117226,
            -114008,
            -111053,
            -127456,
            -131496,
            -101883,
            -72311,
            -44171,
            -68111,
            -89771,
            -94544,
            -99942,
            -96398,
            -106735,
            -105481,
            -452768,
            -97759,
            -213597,
            -196718,
            -93693,
            -105154,
            -97608,
            -52651,
            -1672523,
        ]
        self.beams_normal_force_acc_expected: List[float] = [
            -7770904,
            -7602774,
            -7373658,
            -7172750,
            -6996766,
            -6737444,
            -6527478,
            -6295665,
            -6141608,
            -5991340,
            -5829782,
            -5645450,
            -5591607,
            -5513687,
            -5410634,
            -5293421,
            -5163252,
            -5033599,
            -4707032,
            -4583527,
            -4463057,
            -4345831,
            -4231823,
            -4120770,
            -3993314,
            -3861818,
            -3759935,
            -3687624,
            -3643453,
            -3575342,
            -3485571,
            -3391027,
            -3291085,
            -3194687,
            -3087952,
            -2982471,
            -2529703,
            -2431944,
            -2218347,
            -2021629,
            -1927936,
            -1822782,
            -1725174,
            -1672523,
        ]

    def test_get_beams_dead_weight(self) -> None:
        """
        < Test getting of dead weight of all beams of model.
        """
        print(TestBeamSolver.test_get_beams_dead_weight.__doc__.strip())  # type: ignore

        beams_dead_weight: ndarray = self.beam_solver.get_beams_dead_weight(
            gravity=self.gravity, accumulate=False
        )
        beams_dead_weight_acc: ndarray = self.beam_solver.get_beams_dead_weight(
            gravity=self.gravity, accumulate=True
        )

        tol = 1.0e-12
        self.assertEqual(
            self.model.count,
            len(beams_dead_weight),
            "number of values, accumulate = False",
        )
        self.assertEqual(
            self.model.count,
            len(beams_dead_weight_acc),
            "number of values, accumulate = True",
        )
        print("   single beam dead weight")
        for actual, expected in zip(beams_dead_weight, self.beams_dead_weight_expected):
            self.assertAlmostEqual(actual, expected, delta=tol)
        print("   accumulated beam dead weight")
        for actual, expected in zip(
            beams_dead_weight_acc, self.beams_dead_weight_acc_expected
        ):
            self.assertAlmostEqual(actual, expected, delta=tol)

        print("> OK")

    def test_get_beams_normal_forces(self) -> None:
        """
        < Test getting total normal forces (from beam and node mass) for all beams of model.
        """
        print(TestBeamSolver.test_get_beams_normal_forces.__doc__.strip())  # type: ignore

        beams_normal_forces: ndarray = self.beam_solver.get_beams_normal_forces(
            gravity=10.0, accumulate=False
        )
        beams_normal_forces_acc: ndarray = self.beam_solver.get_beams_normal_forces(
            gravity=10.0, accumulate=True
        )

        tol: float = 1.0e-12
        print("   number of elements")
        self.assertEqual(
            self.model.count,
            len(beams_normal_forces),
            "number of forces, accumulate = False",
        )
        self.assertEqual(
            self.model.count,
            len(beams_normal_forces_acc),
            "number of forces, accumulate = True",
        )
        self.assertEqual(
            self.model.count,
            len(self.beams_normal_force_expected),
            "number of forces, expected",
        )
        self.assertEqual(
            self.model.count,
            len(self.beams_normal_force_acc_expected),
            "number of forces, expected, accumulate = True",
        )
        print("   individual normal forces")
        for exp, act in zip(self.beams_normal_force_expected, beams_normal_forces):
            self.assertAlmostEqual(exp, act, delta=tol)
        print("   accumulated normal forces")
        for exp, act in zip(
            self.beams_normal_force_acc_expected, beams_normal_forces_acc
        ):
            self.assertAlmostEqual(exp, act, delta=tol)

        print("> OK")

    def test_set_beams_axial_force(self) -> None:
        """
        < Test setting normal forces for all beams of model.
        """
        print(TestBeamSolver.test_set_beams_axial_force.__doc__.strip())  # type: ignore

        beams_normal_forces: ndarray = self.beam_solver.get_beams_normal_forces(
            gravity=10.0, accumulate=True
        )
        self.beam_solver.set_axial_forces(beams_normal_forces)

        print("   beam forces against set forces")
        for expected, beam in zip(beams_normal_forces, self.model.beams):
            assert isinstance(beam, PBeamPDelta), "model beam is not PBeamPDelta"
            self.assertAlmostEqual(expected, beam.force_x)

        print("> OK")

    def test_create_beam_solver_wrong_beam_type(self) -> None:
        """
        < Test fail of creation of CompBeamSolver due to unsupported beam type.
        """
        print(TestBeamSolver.test_create_beam_solver_wrong_beam_type.__doc__.strip())  # type: ignore

        model_file: Path = (
            Path(__file__).absolute().parent / "ut" / "wind_tower3_beam_orderI.json"
        )
        file_content: Dict[str, Any] = (
            JsonReader().set_file_name(str(model_file)).read()
        )
        beam_model: CompBeamModel = file_content["model"]

        with self.assertRaises(AttributeError) as context:
            CompBeamSolver(beam_model)
        print(f"   EXPECTED: {str(context.exception)}")

        print("> OK")


class TestDlubalBeam_I(TestCase):
    def setUp(self) -> None:

        self.model: CompBeamModel = get_dlubal_beam_model()
        self.eigen_solver: FlexEigenSolver = FlexEigenSolver()
        self.eigen_solver.set_gravity(9.81)
        self.eigen_solver.set_mode_count(5)
        self.eigen_solver.set_model(self.model)
        self.eigen_solver.set_normalize_shapes(True)
        self.eigen_solver.set_order(1)

        self.expected_frequency: List[float] = [1.235, 7.882, 22.323, 43.108, 64.147]
        self.delta: List[float] = [0.000664, 0.0006509, 0.0078642, 0.0473282, 0.1265796]

    def test_frequencies(self) -> None:
        """
        < Test frequency of dlubal beam, no pDelta effect
        """
        print(TestDlubalBeam_I.test_frequencies.__doc__.strip())  # type: ignore

        freq, _ = self.eigen_solver.solve()

        for exp, act, tol in zip(self.expected_frequency, freq, self.delta):
            print(f"    freq_exp={exp}, freq_act={act}, tol={tol}   -> ok")
            self.assertAlmostEqual(exp, act, delta=tol, msg=f"freq = {exp} != {act}")

        print("> OK")


class TestDlubalBeam_II(TestCase):
    def setUp(self) -> None:

        self.model: CompBeamModel = get_dlubal_beam_model()
        self.eigen_solver: FlexEigenSolver = FlexEigenSolver()
        self.eigen_solver.set_gravity(9.81)
        self.eigen_solver.set_mode_count(5)
        self.eigen_solver.set_model(self.model)
        self.eigen_solver.set_normalize_shapes(True)
        self.eigen_solver.set_order(2)

        self.expected_frequency: List[float] = [1.205, 7.855, 22.295, 43.08, 64.119]
        self.delta: List[float] = [0.00002, 0.00030, 0.00878, 0.04781, 0.12724]

    def test_frequencies(self) -> None:
        """
        < Test frequency of dlubal beam, with pDelta effect
        """
        print(TestDlubalBeam_II.test_frequencies.__doc__.strip())  # type: ignore

        freq, _ = self.eigen_solver.solve()

        for exp, act, tol in zip(self.expected_frequency, freq, self.delta):
            print(f"    freq_exp={exp}, freq_act={act}, tol={tol}   -> ok")
            self.assertAlmostEqual(exp, act, delta=tol, msg=f"freq = {exp} != {act}")

        print("> OK")


class TestTowerMunich_I(TestCase):
    def setUp(self) -> None:

        self.model: CompBeamModel = get_tower_munich_model()
        self.eigen_solver: FlexEigenSolver = FlexEigenSolver()
        self.eigen_solver.set_gravity(9.81)
        self.eigen_solver.set_mode_count(2)
        self.eigen_solver.set_model(self.model)
        self.eigen_solver.set_normalize_shapes(True)
        self.eigen_solver.set_order(1)

        self.expected_frequency: List[float] = [0.1857, 0.7629]
        self.delta: List[float] = [0.00025725, 0.02367003]

    def test_frequencies(self) -> None:
        """
        < Test frequency of radio tower munich, no pDelta effect
        """
        print(TestTowerMunich_I.test_frequencies.__doc__.strip())  # type: ignore

        freq, _ = self.eigen_solver.solve()

        for exp, act, tol in zip(self.expected_frequency, freq, self.delta):
            print(f"    freq_exp={exp}, freq_act={act}, tol={tol}   -> ok")
            self.assertAlmostEqual(exp, act, delta=tol, msg=f"freq = {exp} != {act}")

        print("> OK")


class TestTowerMunich_II(TestCase):
    def setUp(self) -> None:

        self.model: CompBeamModel = get_tower_munich_model()
        self.eigen_solver: FlexEigenSolver = FlexEigenSolver()
        self.eigen_solver.set_gravity(9.81)
        self.eigen_solver.set_mode_count(2)
        self.eigen_solver.set_model(self.model)
        self.eigen_solver.set_normalize_shapes(True)
        self.eigen_solver.set_order(2)

        self.expected_frequency: List[float] = [0.1796, 0.7572]
        self.delta: List[float] = [0.0002312408, 0.0229921733]

    def test_frequencies(self) -> None:
        """
        < Test frequency of radio tower munich, with pDelta effect
        """
        print(TestTowerMunich_II.test_frequencies.__doc__.strip())  # type: ignore

        freq, _ = self.eigen_solver.solve()

        for exp, act, tol in zip(self.expected_frequency, freq, self.delta):
            print(f"    freq_exp={exp}, freq_act={act}, tol={tol}   -> ok")
            self.assertAlmostEqual(exp, act, delta=tol, msg=f"freq = {exp} != {act}")

        print("> OK")


if __name__ == "__main__":
    main()
