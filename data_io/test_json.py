from unittest import TestCase
from data_io.json import JsonReader
from model.system import CompBeamModel
from model.beams import BeamB_2DOF
from model.entry import Mass
from model.core import DOF
from model.core import DOF_TYPE
from pathlib import Path
from typing import Dict, Any, List


class TestJsonReader(TestCase):
    def test_read_from_JSON(self) -> None:
        """
        < Reads header, parameters and model from JSON, tests data structure.
        """
        print(TestJsonReader.test_read_from_JSON.__doc__.strip())  # type: ignore

        json_file: Path = (
            Path(__file__).parent.absolute() / "ut" / "model_definition.json"
        )

        print(f'reading data from "{str(json_file)}"')
        file_content: Dict[str, Any] = JsonReader().set_file_name(str(json_file)).read()
        model: CompBeamModel = file_content["model"]

        print()
        print(f"    beam type = {model.beam_type}")
        self.assertTrue(isinstance(model.start_beam, BeamB_2DOF))
        self.assertTrue(isinstance(model.end_beam, BeamB_2DOF))

        print()
        print("    generic properties")
        print(f"    length = {model.length}")
        self.assertAlmostEqual(98.92, model.length, delta=1.0e-13)
        print(f"    mass beams = {model.total_mass_beams}")
        print(f"    note, mass 0.1 of link beam at top is included")
        self.assertAlmostEqual(
            252669.192053125 + 0.1, model.total_mass_beams, delta=1.0e-6
        )
        print(f"    average I = {0.880236640176015}")
        print("    note, area moi 10 for link beam at top is included")
        self.assertAlmostEqual(
            0.880236640176015,
            sum(b.area_moi for b in model._beams) / model.count,
            delta=1.0e-7,
        )

        print(f'   mass at start node: each DOF_TYPE.DIST must have same value')
        assert model.start_node is not None
        start_node_masses: List[Mass] = model.get_masses_of_node(model.start_node)
        assert len(start_node_masses) == 1, 'number of masses at start node is not 1'
        start_mass: Mass = model.get_masses_of_node(model.start_node)[0]
        mass_value: float = start_mass.get_value(DOF.U)
        for dof in DOF.get_by_type(DOF_TYPE.DISP):
            self.assertEqual(mass_value, start_mass.get_value(dof), msg=f'mass value {dof.name}')

        print()
        print("    other data in file")
        print(f'"header"')
        header: Dict[str, Any] = {
            "designator": "wind tower 2",
            "project": "Behind the Hills 4",
            "version": "0",
            "user": "christof dittmar",
            "description": "a nice day to compute some modes shapes",
            "note": "some note or maybe not",
        }
        self.assertTrue("header" in file_content)
        self.assertEqual(header, file_content["header"])

        print(f'"parameters"')
        parameters: Dict[str, Any] = {
            "p_delta": False,
            "prefer_positive_lateral_mode_shape_values": False,
            "number_of_modes": 3,
            "normalize_mode_shapes": True,
            "gravity": 9.81,
        }
        self.assertTrue("parameters" in file_content)
        self.assertEqual(parameters, file_content["parameters"])

        print("> OK")
