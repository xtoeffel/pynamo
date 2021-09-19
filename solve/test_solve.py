# -*- coding: utf-8 -*-
"""Some testing that is not related to real implementations, this is just for fun."""

from unittest import TestCase
from model.beams import BeamB_2DOF
from model.beams import BeamB_3DOF
from model.beams import BeamB_2DOF_II
from model.beams import ABeam
from model.beams import Type
from model.system import CompBeamModel
from solve.eigen import FlexEigenSolver
from math import pi
from math import sqrt
from copy import deepcopy
from pandas import DataFrame
from pandas import ExcelWriter
from data_io.excel import ExcelWriter
from typing import List
from typing import Dict
from typing import Any
from typing import Final
from typing import Tuple
from model.elements import by_axial_length
from model.entry import Mass
from model.entry import Spring
from model.core import DOF
from pathlib import Path
from json import load


# control writing of results to Excel files
write_results: Final[bool] = False


class TestEigenSolve(TestCase):
    @staticmethod
    def read_CompBeamModel(
        file_name: str, beam_type: Type[ABeam] = BeamB_2DOF
    ) -> CompBeamModel:
        """Reads a model defined in json file into a CompBeamModel w/ BeamB_2DOF beam elements.

        This only reads the beams, not the ground restraints or additional masses.
        """
        with open(file_name, "r") as json_file:
            json_data: Dict[str, Any] = load(json_file)

        model: CompBeamModel = CompBeamModel()
        for idx, beam in enumerate(json_data["model"]):
            if idx == 0:
                model.add(
                    beam_type(
                        *by_axial_length(beam_type.get_dofs(), beam["length"]),  # type: ignore
                        mass=beam["mass"],
                        area=beam["area"],
                        area_moi=beam["area_moi"],
                        e_modul=beam["e_modul"],
                    )
                )
            else:
                model.append(
                    length=beam["length"],
                    mass=beam["mass"],
                    area=beam["area"],
                    area_moi=beam["area_moi"],
                    e_modul=beam["e_modul"],
                )
        return model

    def test_solver_3DOF(self) -> None:
        print(
            "< test {CompBeamModel.__name__} with 42 uniform"
            " {BeamB_3DOF.__name__}-beams"
        )

        beam_template: BeamB_3DOF = BeamB_3DOF(
            *by_axial_length(BeamB_3DOF.get_dofs(), 2.9),
            e_modul=2.1e11,
            area_moi=0.615773774261056,
            area=0.268920331147286,
            mass=6121.97133856797,
        )
        model: CompBeamModel = CompBeamModel().add(beam_template)
        for _ in range(0, 41):
            model.append(
                2.9,
                e_modul=2.1e11,
                area_moi=0.615773774261056,
                area=0.268920331147286,
                mass=6121.97133856797,
            )

        # boundary conditions
        assert model.start_node is not None
        model.start_node.set_dof(DOF.W, 0.0).set_dof(DOF.PHI, 0.0).set_dof(DOF.U, 0.0)

        freq: DataFrame
        msv: DataFrame

        freq, msv = FlexEigenSolver.to_dataframe(
            *FlexEigenSolver()
            .set_model(model)
            .set_mode_count(3)
            .set_pref_positive_lat_msv(False)
            .set_normalize_shapes(True)
            .solve()
        )
        print(f"freq: {freq.shape}, msv: {msv.shape}")
        print("... done")

        if write_results:
            file_name: str = str(
                Path(__file__).parent.absolute()
                / "ut"
                / "test_out_model_uniform_3dof.xlsx"
            )
            print(f'write results to "{file_name}"')
            ExcelWriter().set_file_name(file_name).write(freq=freq, msv=msv)
            print(f"... done")

        # unit tests
        tol: float = 1.0e-4
        print(f"testing frequencies with tolerance {tol}")
        print(f"1st mode frequency: {0.29519003579169}")
        self.assertAlmostEqual(
            0.29519003579169, freq.iat[0, 0], delta=tol, msg="freq first mode"
        )
        print(f"2nd mode frequency: {1.85005789851337}")
        self.assertAlmostEqual(
            1.85005789851337, freq.iat[1, 0], delta=tol, msg="freq second mode"
        )
        tol = 3.5e-4
        print(f"tolerance lower for 3rd mode, tolerance = {tol}")
        print(f"3rd mode frequency: {5.18073679022478}")
        self.assertAlmostEqual(
            5.18073679022478, freq.iat[2, 0], delta=tol, msg="freq third mode"
        )
        print("> OK")

    def test_solver_2DOF(self) -> None:
        print(
            "< test {CompBeamModel.__name__} with 42 uniform"
            " {BeamB_2DOF.__name__}-beams"
        )

        beam_template: BeamB_2DOF = BeamB_2DOF(
            *by_axial_length(BeamB_2DOF.get_dofs(), 2.9),
            e_modul=2.1e11,
            area_moi=0.615773774261056,
            area=0.268920331147286,
            mass=6121.97133856797,
        )
        model: CompBeamModel = CompBeamModel()
        model.add(beam_template)
        for _ in range(0, 41):
            model.append(
                2.9,
                e_modul=2.1e11,
                area_moi=0.615773774261056,
                area=0.268920331147286,
                mass=6121.97133856797,
            )

        # boundary conditions
        assert model.start_node is not None
        model.start_node.set_dof(DOF.W, 0.0).set_dof(DOF.PHI, 0.0)

        freq: DataFrame
        msv: DataFrame

        freq, msv = FlexEigenSolver.to_dataframe(
            *FlexEigenSolver()
            .set_model(model)
            .set_mode_count(3)
            .set_pref_positive_lat_msv(False)
            .set_normalize_shapes(True)
            .solve()
        )
        print(f"freq: {freq.shape}, msv: {msv.shape}")
        print("... done")

        if write_results:
            file_name: str = str(
                Path(__file__).parent.absolute()
                / "ut"
                / "test_out_model_uniform_2dof.xlsx"
            )
            print(f'write results to "{file_name}"')
            ExcelWriter().set_file_name(file_name).write(freq=freq, msv=msv)
            print(f"... done")

        # unit tests
        tol: float = 1.0e-4
        print(f"testing frequencies with tolerance {tol}")
        print(f"1st mode frequency: {0.29519003579169}")
        self.assertAlmostEqual(
            0.29519003579169, freq.iat[0, 0], delta=tol, msg="freq first mode"
        )
        print(f"2nd mode frequency: {1.85005789851337}")
        self.assertAlmostEqual(
            1.85005789851337, freq.iat[1, 0], delta=tol, msg="freq second mode"
        )
        tol = 3.5e-4
        print(f"tolerance lower for 3rd mode, tolerance = {tol}")
        print(f"3rd mode frequency: {5.18073679022478}")
        self.assertAlmostEqual(
            5.18073679022478, freq.iat[2, 0], delta=tol, msg="freq third mode"
        )
        print("> OK")

    def test_petersen_11_3_5(self) -> None:
        print("< Test results from Petersen, Baudynamik, Kapitel 11.3.5")

        # use of 2DOF
        model: CompBeamModel = CompBeamModel()
        model.add(
            BeamB_2DOF(
                *by_axial_length(BeamB_2DOF.get_dofs(), 5.0),
                mass=168 * 5.0,
                area=0.0,
                area_moi=11905 / 100 ** 4,
                e_modul=21000 * 1000 * 100 ** 2,
            )
        )
        model.append(
            5.0,
            mass=168 * 5.0,
            area=0.0,
            area_moi=11905 / 100 ** 4,
            e_modul=21000 * 1000 * 100 ** 2,
        )

        # boundary conditions
        assert model.start_node is not None
        model.start_node.set_dof(DOF.W, 0.0).set_dof(DOF.PHI, 0.0)

        freq, _ = (
            FlexEigenSolver()
            .set_model(model)
            .set_mode_count(4)
            .set_normalize_shapes(True)
            .solve()
        )

        print("solution w/ 2 elements (2DOF beams)")
        print(f"actual frequencies: {freq}")
        expected: List[float] = [2.159, 13.643, 46.143, 133.93]
        print(f"expected frequencies: {expected}")
        tol: float = 0.00206
        print(f"tolerance: {tol}")
        for a, e in zip(freq, expected):
            self.assertAlmostEqual(e, a, delta=tol, msg=f"expected: {e}, actual: {a}")
        print("> OK")

        # now model with 20 elements to fit to real frequencies
        print("more accurate solution w/ 20 elements (2DOF beams)")
        expected = [2.158, 13.528, 37.879, 74.229]
        beam = BeamB_2DOF(
            *by_axial_length(BeamB_2DOF.get_dofs(), 0.5),
            mass=168 * 0.5,
            area=0.0,
            area_moi=11905 / 100 ** 4,
            e_modul=21000 * 1000 * 100 ** 2,
        )
        model = CompBeamModel().add(beam)
        for _ in range(0, 19):
            model.append(
                0.5,
                mass=168 * 0.5,
                area=0.0,
                area_moi=11905 / 100 ** 4,
                e_modul=21000 * 1000 * 100 ** 2,
            )
        # boundary conditions
        assert model.start_node is not None
        model.start_node.set_dof(DOF.W, 0.0).set_dof(DOF.PHI, 0.0)

        freq, _ = (
            FlexEigenSolver()
            .set_model(model)
            .set_mode_count(4)
            .set_normalize_shapes(True)
            .solve()
        )
        print(f"actual frequencies: {freq}")
        print(f"expected frequencies: {expected}")
        tol = 0.00454
        print(f"tolerance: {tol}")
        for a, e in zip(freq, expected):
            self.assertAlmostEqual(e, a, delta=tol, msg=f"expected: {e}, actual: {a}")
        print("> OK")

    def test_wind_tower1_2ndOrder(self) -> None:
        """
        < Test wind tower 1 w/ p-delta effects (2nd order) frequency and mode shapes.
        """
        print(TestEigenSolve.test_wind_tower1_2ndOrder.__doc__.strip())  # type: ignore

        mdl_file: Path = Path(__file__).parent.absolute() / "ut" / "wind_tower1.json"
        print(f'reading wind tower model from "{str(mdl_file)}"')

        # read model and append beams
        model: CompBeamModel = TestEigenSolve.read_CompBeamModel(
            str(mdl_file), BeamB_2DOF_II
        )
        assert model.start_beam is not None
        assert isinstance(
            model.start_beam, BeamB_2DOF_II
        ), "unexpected beam type for 2nd order frequency model"

        # tower top mass
        model.append(2.02, mass=0.1, area=0, area_moi=10, e_modul=210000000000)
        assert model.end_node is not None
        model.add_mass(
            model.end_node, Mass().set_mass(169100).set_mmoi(DOF.PHI, 5.00e05)
        )

        # boundary conditions
        assert model.start_node is not None
        model.start_node.set_dof(DOF.W, 0.0).set_dof(DOF.PHI, 0.0)

        # compute frequencies 1st and 2nd order
        freq1, _ = (
            FlexEigenSolver()
            .set_model(model)
            .set_order(1)
            .set_mode_count(3)
            .set_normalize_shapes(True)
            .solve()
        )
        freq2, _ = (
            FlexEigenSolver()
            .set_model(model)
            .set_order(2)
            .set_mode_count(3)
            .set_normalize_shapes(True)
            .solve()
        )

        print(f"model mass: {model.mass}")
        print(f"freq1: {freq1} -- w/o p-Delta effects")
        print(f"freq2: {freq2} -- w/  p-Delta effects")

        print(f"compare to 1st order results, condition: 2nd order < 1st order")
        for e, a in zip(freq2, freq1):
            print(f"frequency: {e} < {a}")
            assert e < a, f"frequency: {e} < {a} -- failed"

        print("> OK")

    def test_wind_tower1_point_mass(self) -> None:
        """
        < Test wind tower 1 w/ point mass at top (mass and mmoi) and infinite stiff mount.
        """
        print(TestEigenSolve.test_wind_tower1_point_mass.__doc__.strip())  # type: ignore

        mdl_file: Path = Path(__file__).parent.absolute() / "ut" / "wind_tower1.json"
        print(f'reading wind tower model from "{str(mdl_file)}"')

        # read model and append beams
        model: CompBeamModel = TestEigenSolve.read_CompBeamModel(str(mdl_file))

        # tower top mass
        model.append(2.02, mass=0.1, area=0, area_moi=10, e_modul=210000000000)
        assert model.end_node is not None
        model.add_mass(
            model.end_node, Mass().set_mass(169100).set_mmoi(DOF.PHI, 5.00e05)
        )

        # boundary conditions
        assert model.start_node is not None
        model.start_node.set_dof(DOF.W, 0.0).set_dof(DOF.PHI, 0.0)

        freq, msv = (
            FlexEigenSolver()
            .set_model(model)
            .set_mode_count(4)
            .set_normalize_shapes(True)
            .solve()
        )

        print(f"model mass: {model.mass}")

        print(f"evaluate computed frequencies against expected")
        print(f"computed: {freq}")
        print(f"expected: {[0.28061, 1.99591, 5.66893, 11.1852]}")
        self.assertAlmostEqual(0.28061, freq[0], delta=0.00237809378069995)
        self.assertAlmostEqual(1.99591, freq[1], delta=0.0311910819077)
        self.assertAlmostEqual(5.66893, freq[2], delta=0.0994734547246003)
        self.assertAlmostEqual(11.1852, freq[3], delta=0.253804828022899)
        print("> OK")

        if write_results:
            print()
            out_file: str = str(
                Path(__file__).parent.absolute()
                / "ut"
                / "test_out_windtower1_point_mass.xlsx"
            )
            print(f'writing result to: "{out_file}"')
            freq, msv = FlexEigenSolver.to_dataframe(freq, msv)
            ExcelWriter().set_file_name(out_file).write(freq=freq, msv=msv)

    def test_wind_tower1_application_BC(self) -> None:
        """
        < Test wind tower 1 w/ point mass and mmoi at top for spring ground restraints (soft BC).
        """
        print(TestEigenSolve.test_wind_tower1_application_BC.__doc__.strip())  # type: ignore

        mdl_file: Path = Path(__file__).parent.absolute() / "ut" / "wind_tower1.json"
        print(f'reading wind tower model from "{str(mdl_file)}"')

        # read model and append beams
        model: CompBeamModel = TestEigenSolve.read_CompBeamModel(str(mdl_file))

        # foundation mass
        assert model.start_node is not None
        model.add_mass(
            model.start_node, Mass().set_mass(1.0e6).set_mmoi(DOF.PHI, 5.0e7)
        )

        # tower top mass
        model.append(2.02, mass=0.1, area=0.0, area_moi=10.0, e_modul=210000000000)
        assert model.end_node is not None
        model.add_mass(
            model.end_node, Mass().set_mass(169100).set_mmoi(DOF.PHI, 5.00e05)
        )

        # boundary conditions, spring
        assert (
            model.start_node is not None
        ), "undefined start node tower1, application BC"
        model.attach_spring(
            model.start_node,
            Spring().set_value(DOF.W, 3.1e8).set_value(DOF.PHI, 1.0e11),
        )

        freq, msv = (
            FlexEigenSolver()
            .set_model(model)
            .set_mode_count(4)
            .set_normalize_shapes(True)
            .solve()
        )

        print(f"model mass: {model.mass}")

        print(f"evaluate computed frequencies against expected")
        print(f"computed: {freq}")
        print(f"expected: {[0.270723, 1.81915, 2.74306, 5.27814]}")
        self.assertAlmostEqual(0.270723, freq[0], delta=0.00201)
        self.assertAlmostEqual(1.81915, freq[1], delta=0.0248)
        self.assertAlmostEqual(2.74306, freq[2], delta=0.0062)
        self.assertAlmostEqual(5.27814, freq[3], delta=0.07552)

        print("> OK")

        if write_results:
            print()
            out_file: str = str(
                Path(__file__).parent.absolute() / "ut" / "test_out_windtower1_BC.xlsx"
            )
            print(f'writing result to: "{out_file}"')
            freq, msv = FlexEigenSolver.to_dataframe(freq, msv)
            ExcelWriter().set_file_name(out_file).write(freq=freq, msv=msv)

    def test_wind_tower2_point_mass(self) -> None:
        """
        < Test wind tower 2 with point mass with boundary conditions: stiff (infinite) at base
        """
        print(TestEigenSolve.test_wind_tower2_point_mass.__doc__.strip())  # type: ignore

        mdl_file: Path = Path(__file__).parent.absolute() / "ut" / "wind_tower2.json"
        print(f'reading wind tower model from "{str(mdl_file)}"')

        # read model and append beams
        model: CompBeamModel = TestEigenSolve.read_CompBeamModel(str(mdl_file))

        # tower top mass
        model.append(2.02, mass=0.1, area=0, area_moi=10, e_modul=210000000000)
        assert model.end_node is not None
        model.add_mass(
            model.end_node, Mass().set_mass(165000).set_mmoi(DOF.PHI, 5.00e05)
        )

        # boundary conditions
        assert model.start_node is not None
        model.start_node.set_dof(DOF.W, 0.0).set_dof(DOF.PHI, 0.0)

        freq, msv = (
            FlexEigenSolver()
            .set_model(model)
            .set_mode_count(5)
            .set_normalize_shapes(True)
            .solve()
        )

        print(f"model mass: {model.mass}")

        # unit test
        print("testing results")
        print(f"computed: {freq}")
        print(f"expected: {[0.262103, 2.12672, 5.96088, 11.6763, 18.5397]}")
        self.assertAlmostEqual(0.262103, freq[0], delta=0.000653)
        self.assertAlmostEqual(2.12672, freq[1], delta=0.0244)
        self.assertAlmostEqual(5.96088, freq[2], delta=0.0743)
        self.assertAlmostEqual(11.6763, freq[3], delta=0.2)
        self.assertAlmostEqual(18.5397, freq[4], delta=0.584)

        if write_results:
            print()
            out_file: str = str(
                Path(__file__).parent.absolute()
                / "ut"
                / "test_out_windtower2_point_mass.xlsx"
            )
            print(f'writing result to: "{out_file}"')
            freq, msv = FlexEigenSolver.to_dataframe(freq, msv)
            ExcelWriter().set_file_name(out_file).write(freq=freq, msv=msv)

        print("> OK")

    def test_wind_tower2_application_BC(self) -> None:
        """
        < Test wind tower 2 with soft ground restraint.
        """
        print(TestEigenSolve.test_wind_tower2_application_BC.__doc__.strip())  # type: ignore

        mdl_file: Path = Path(__file__).parent.absolute() / "ut" / "wind_tower2.json"
        print(f'reading wind tower model from "{str(mdl_file)}"')

        # read model and append beams
        model: CompBeamModel = TestEigenSolve.read_CompBeamModel(str(mdl_file))

        # foundation mass
        assert model.start_node is not None
        model.add_mass(
            model.start_node, Mass().set_mass(1.0e6).set_mmoi(DOF.PHI, 5.0e7)
        )

        # tower top mass
        model.append(2.02, mass=0.1, area=0, area_moi=10, e_modul=210000000000)
        assert model.end_node is not None
        model.add_mass(
            model.end_node, Mass().set_mass(165000).set_mmoi(DOF.PHI, 5.00e05)
        )

        # boundary conditions, spring
        model.attach_spring(
            model.start_node,
            Spring().set_value(DOF.W, 3.1e8).set_value(DOF.PHI, 1.0e11),
        )

        freq, msv = (
            FlexEigenSolver()
            .set_model(model)
            .set_mode_count(5)
            .set_normalize_shapes(True)
            .solve()
        )

        print(f"model mass: {model.mass}")

        print("evalute computed against expected results")
        print(f"computed: {freq}")
        print(f"expected: {[0.254552, 1.95146, 2.77028, 5.5222, 8.0054]}")
        self.assertAlmostEqual(0.254552, freq[0], delta=0.000645)
        self.assertAlmostEqual(1.95146, freq[1], delta=0.019713)
        self.assertAlmostEqual(2.77028, freq[2], delta=0.00405)
        self.assertAlmostEqual(5.5222, freq[3], delta=0.05319)
        self.assertAlmostEqual(8.0054, freq[4], delta=0.036235)

        if write_results:
            print()
            out_file: str = str(
                Path(__file__).parent.absolute()
                / "ut"
                / "test_out_windtower2_applicationBC.xlsx"
            )
            print(f'writing result to: "{out_file}"')
            freq, msv = FlexEigenSolver.to_dataframe(freq, msv)
            ExcelWriter().set_file_name(out_file).write(freq=freq, msv=msv)

        print("> OK")
