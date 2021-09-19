# -*- coding: utf-8 -*-
from unittest import TestCase
from pathlib import Path
from model.system import CompBeamModel
from model.entry import Spring
from solve.eigen import FlexEigenSolver
from model.elements import DOF
from data_io.json import JsonReader
from copy import deepcopy


class TestWindTower3(TestCase):
    def test_wind_tower3_BC(self) -> None:
        """
        < Test wind tower 3 with varying ground restraint - manually set.
        """
        print(TestWindTower3.test_wind_tower3_BC.__doc__.strip())  # type: ignore

        mdl_file: Path = (
            Path(__file__).parent.absolute() / "ut" / "wind_tower3_noBC.json"
        )
        print(f'reading wind tower model from "{str(mdl_file)}"')
        mode_count: int = 5

        base_model: CompBeamModel = (
            JsonReader().set_file_name(str(mdl_file)).read()["model"]
        )

        # -- stiff mount --
        model: CompBeamModel = deepcopy(base_model)
        model.attach_spring(
            model.start_node,
            Spring().set_value(DOF.W, 1.0e12).set_value(DOF.PHI, 1.0e12),
        )
        freq_stiff, _ = (
            FlexEigenSolver()
            .set_model(model)
            .set_mode_count(mode_count)
            .set_order(2)
            .set_normalize_shapes(True)
            .solve()
        )

        # -- soft mount --
        model = deepcopy(base_model)
        model.attach_spring(
            model.start_node,
            Spring().set_value(DOF.W, 3.0e8).set_value(DOF.PHI, 2.0e10),
        )
        freq_soft, _ = (
            FlexEigenSolver()
            .set_model(model)
            .set_mode_count(mode_count)
            .set_order(2)
            .set_normalize_shapes(True)
            .solve()
        )

        # -- infinite stiff mount --
        model = deepcopy(base_model)
        model.start_node.set_dof(DOF.W, 0.0)
        model.start_node.set_dof(DOF.PHI, 0.0)
        freq_inf_stiff, _ = (
            FlexEigenSolver()
            .set_model(model)
            .set_mode_count(mode_count)
            .set_order(2)
            .set_normalize_shapes(True)
            .solve()
        )

        print(f"    evaluating frequencies for mount: soft < stiff < infinite stiff")
        for soft, stiff, real_stiff in zip(freq_soft, freq_stiff, freq_inf_stiff):
            print(f"      {soft:.6f} < {stiff:.6f} < {real_stiff:.6f}")
            self.assertTrue(soft < stiff < real_stiff, f"{soft}, {stiff}, {real_stiff}")

        print("> OK")
