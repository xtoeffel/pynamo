"""IO for JSON"""
from typing import Type
from typing import Any
from typing import Dict
from pathlib import Path
from data_io.base import FileTypeError
from data_io.base import BaseReader
from utils.strings import require_non_empty
from model.system import CompBeamModel
from model.elements import by_axial_length
from model.elements import Node
from model.entry import Mass
from model.entry import Spring
from model.core import DOF
from model.core import DOF_TYPE
from model.beams import ABeam
from model.beams import BeamB_2DOF
from model.beams import BeamB_2DOF_II
from json import load
from copy import deepcopy


class JsonReader(BaseReader):
    @staticmethod
    def _get_dof(identifier: str) -> DOF:
        """Get DOF from identifier.

        :param identifier: identifier for DOF, either 'DOF.W' or 'W' where W can be any supported entry
        :type identifier: str

        :return: DOF for identifier
        :rtype: DOF

        :raise KeyError: if identifier is invalid
        """
        try:
            return DOF[identifier.upper()]
        except KeyError:
            try:
                return DOF[identifier.split(".")[1].upper()]
            except KeyError:
                raise KeyError(f'Invalid entry "{identifier}"')

    @staticmethod
    def _get_beam_type(identifier: str) -> Type[ABeam]:
        """Get beam type from identifier.

        :param identifier: beam type identifier (usually class name)
        :type identifier: str

        :return: beam type
        :rtype: Type[ABeam]

        :raises TypeError: if there is no beam type for identifier
        """
        id_upper: str = identifier.upper()
        if id_upper == "B_2DOF":
            return BeamB_2DOF
        elif id_upper == "B_2DOF_II" or id_upper == "B_2DOF_pDelta":
            return BeamB_2DOF_II
        else:
            raise TypeError(f'Unsupported beam type "{identifier}"')

    @staticmethod
    def _get_mass(definition: Dict[str, float]) -> Mass:
        """Creates a mass from a dictionary.

        :param definition: dictionary to create mass from
        :type definition: Dict[str, float]

        :return: mass created from dictionary
        :rtype: Mass

        :raises ValueError: if values are invalid
        :raises KeyError: if entries (keys) are not supported
        """
        mass: Mass = Mass()
        for key, value in definition.items():
            if key == "x":
                continue
            elif key.lower() == "mass":
                mass.set_mass(value)
            else:
                dof: DOF = JsonReader._get_dof(key)
                if dof.dof_type != DOF_TYPE.ROT:
                    raise KeyError(f'Invalid entry "{key}" for mass element')
                mass.set_mmoi(dof, value)

        return mass

    @staticmethod
    def _to_model(model_data: Dict[str, Any]) -> CompBeamModel:
        """Extracts the beam model from the read json data.

        :param json_data: dictionary of model data read from JSON file, this is the "model" entry
        :type json_data: Dict[str, Any]

        :return: beam model extracted from json_data
        :rtype: CompBeamModel

        :raises KeyError: if any required key does not exist
        :raises ValueError: if beam type is not supported
        """

        beam_type: Type[ABeam] = JsonReader._get_beam_type(model_data["beam_type"])

        model: CompBeamModel = CompBeamModel()
        for idx, beam in enumerate(model_data["beams"]):
            if idx == 0:
                beam_no_length: Dict[str, Any] = deepcopy(beam)
                beam_no_length.pop("length")
                model.add(
                    beam_type(
                        # mypy cannot detect that static method get_dofs() exists for all beam type classes
                        *by_axial_length(beam_type.get_dofs(), beam["length"]),  # type: ignore
                        **beam_no_length,
                    )
                )
            else:
                model.append(**beam)

        if "masses" in model_data and len(model_data["masses"]) > 0:
            for mass_dict in model_data["masses"]:
                mass: Mass = JsonReader._get_mass(mass_dict)
                model.assign_mass(mass, mass_dict["x"])

        if "dofs" in model_data and len(model_data["dofs"]) > 0:
            for dof in model_data["dofs"]:
                dof_node: Node = model.get_node_by_height(dof["x"])
                for key, value in dof.items():
                    if key != "x":
                        dof_node.set_dof(JsonReader._get_dof(key), value)

        if "springs" in model_data and len(model_data["springs"]) > 0:
            for spring in model_data["springs"]:
                spring_node: Node = model.get_node_by_height(spring["x"])
                new_spring: Spring = Spring()
                for key, value in spring.items():
                    if key != "x":
                        new_spring.set_value(JsonReader._get_dof(key), value)
                model.attach_spring(spring_node, new_spring)

        return model

    def __init__(self) -> None:
        self._file_name: str = ""

    @property
    def file_name(self) -> str:
        """Name of JSON file to read from.

        :return: name of JSON file
        :rtype: str
        """
        return self._file_name

    def set_file_name(self, file_name: str) -> "JsonReader":
        """Sets the file name of the JSON file to read from.

        :param file_name: name of JSON file
        :type file_name: str

        :raises ValueError: if file_name is None or empty
        """
        require_non_empty(file_name, "file name")
        self._file_name = file_name
        return self

    def read(self) -> Dict[str, Any]:
        """Reads the model and additional parameters from the file set to the model reader.

        The reader will inspect for entry with key "model" and convert that to a CompBeamModel.
        Thus the entry with key "model" will be a CompBeamModel.
        All other entries are mapped from the JSON file content into the returned dictionary.

        :return: dictionary of model and additional parameters read from JSON
        :rtype: Dict[str, Any]

        :raises KeyError: if any required key does not exist
        :raises ValueError: file name is not set, if beam type is not supported
        :raises FileTypeError: if file extension is not .json
        """
        require_non_empty(self._file_name, "json file name")
        file_path: Path = Path(self._file_name)
        if file_path.suffix != ".json":
            raise FileTypeError.by_path(self._file_name, ".json")

        with open(self._file_name, "r") as json_file:
            content: Dict[str, Any] = load(json_file)
            content["model"] = JsonReader._to_model(content["model"])
            return content
