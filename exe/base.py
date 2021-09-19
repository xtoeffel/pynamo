# -*- coding: utf-8 -*-
"""Base classes for execution of computation runs.

Classes must take over the complete execution process including data IO.
"""
from typing import Callable
from typing import Dict
from typing import Any
from typing import Optional
from typing import Tuple
from typing import cast
from pathlib import Path
from utils.strings import require_non_empty
from data_io.base import FileTypeError
from data_io.base import BaseWriter
from data_io.base import BaseReader
from data_io.json import JsonReader
from data_io.excel import ExcelWriter
from solve.eigen import FlexEigenSolver
from model.system import CompBeamModel
from numpy import ndarray
from pandas import DataFrame
from data_io.compile import df_comp_beam_model
from data_io.compile import df_node_masses
from data_io.compile import df_dofs
from data_io.compile import df_springs


class BaseRun:
    """Base class to define the class structure for runs.

    Runs are defined by the steps pre-processing, reading data, running, writing results
    and post-processing represented by hook methods pre(), read(), run(), write() and post().
    The main method is execute() - which is not a hook.

    Readers and writers must be set and their concrete use implemented in the hook methods
    read_execute() and write_execute(). Setter and getter methods for reader and writer
    might be overridden to handle specific types.
    """

    def __init__(self) -> None:
        self._notifier: Optional[Callable[[str], None]] = None
        self._writer: Optional[BaseWriter] = None
        self._reader: Optional[BaseReader] = None

    def set_notifier(self, notifier: Callable[[str], None]) -> "BaseRun":
        """Sets notifier function for passing messages of execution to a notification system.

        :param notifier: notifier function
        :type notifier: Callable[[str], None]

        :return: self for chaining of calls
        :rtype: BaseRun
        """
        self._notifier = notifier
        return self

    def _send_msg(self, msg: str) -> None:
        """Sends a message to the notifier function, if set, or ignores if not set.

        :param msg: message to send to notifier
        :type msg: str
        """
        if self._notifier is not None and msg is not None and len(msg) > 0:
            self._notifier(msg)

    def set_reader(self, reader: BaseReader) -> "BaseRun":
        """Sets the reader.

        :param reader: reader for run configuration, this is model and other run setup
        :type reader: BaseReader

        :returns: self for chaining of calls
        :rtype: BaseRun
        """
        self._reader = reader
        return self

    @property
    def reader(self) -> BaseReader:
        """Reader of run configuration.

        :return: reader of run configuration
        :rtype: BaseReader

        :raises ValueError: if reader is not set (undefined)
        """
        if self._reader is None:
            raise ValueError("Undefined reader")
        return self._reader

    def set_writer(self, writer: BaseWriter) -> "BaseRun":
        """Sets the writer.

        :param writer: writer for computation results
        :type writer: BaseWriter

        :return: self for chaining of calls
        :rtype: BaseRun
        """
        self._writer = writer
        return self

    @property
    def writer(self) -> BaseWriter:
        """Writer for results.

        :return: writer for computation results
        :rtype: BaseWriter
        """
        if self._writer is None:
            raise ValueError("Undefined writer")
        return self._writer

    # hook methods
    def pre_execute(self) -> None:
        """First hook method to be called by execute() for setup of execution."""
        pass

    def read_execute(self) -> None:
        """Hook method for reading of data required to run execution."""
        pass

    def run_execute(self) -> None:
        """Hook method for main or core execution."""
        pass

    def write_execute(self) -> None:
        """Hook method for writing of results or output data."""
        pass

    def post_execute(self) -> None:
        """Hook method for closing of execution process."""
        pass

    # main execution method
    def execute(self) -> None:
        """Execute run in the order of calling hook methods:
        pre_execute(), read_execute(), run_execute(), write_execute(), post_execute().
        """
        self.pre_execute()
        self.read_execute()
        self.run_execute()
        self.write_execute()
        self.post_execute()


class SingleRunFlexEigen(BaseRun):
    """Single run of model with control paramters for flexural eigenvalues and frequencies."""

    def __init__(self, file_in: str, file_out: str) -> None:
        """Create a new single run object to compute flexural frequencies and mode shapes.

        :param file_in: path of JSON file to read model data and config from
        :type file_in: str
        :param file_out: path of Excel file to write results to
        :type file_out: str

        :raise ValueError: if file_in or file_out is None or empty
        """
        require_non_empty(file_in, "input file name")
        require_non_empty(file_out, "output file name")

        super().__init__()
        super().set_reader(JsonReader().set_file_name(file_in))
        super().set_writer(ExcelWriter().set_file_name(file_out))
        self._solver: FlexEigenSolver = FlexEigenSolver()
        self._config: Dict[str, Any] = {}
        self._model: Optional[CompBeamModel] = None
        self._results: Optional[Tuple[ndarray, ndarray]] = None

    def set_reader(self, reader: BaseReader) -> "SingleRunFlexEigen":
        """Setting the reader is not supported for this run.

        :raises NotImplementedError: on call, setting is reader not supported
        """
        raise NotImplementedError(
            f"Reader cannot be set on {SingleRunFlexEigen.__name__}"
        )

    @property
    def reader(self) -> JsonReader:
        """Json reader for run configuration data.

        :return: JSON reader for run configuration
        :rtype: JsonReader
        """
        return cast(JsonReader, super().reader)

    def set_writer(self, writer: BaseWriter) -> "SingleRunFlexEigen":
        """Setting the writer is not supported.

        :raises NotImplementedError: on call, setting writer is not supported
        """
        raise NotImplementedError(
            f"Writer cannot be set on {SingleRunFlexEigen.__name__}"
        )

    @property
    def writer(self) -> ExcelWriter:
        """Excel writer for calculation results.

        :return: Excel writer for calculation results
        :rtype: Excel
        """
        return cast(ExcelWriter, super().writer)

    @property
    def file_in(self) -> str:
        """Input file name."""
        return self.reader.file_name

    @property
    def file_out(self) -> str:
        """Output file name."""
        return self.writer.file_name

    def pre_execute(self) -> None:
        """Verify properties and input file.

        :raises FileNotFoundError: if input file does not exist
        :raises FileTypeError: on invalid file suffixes, required is *.json for input, *.xlsx for output
        """
        self._send_msg("Verifying Files")

        file_in_path: Path = Path(self.file_in)
        file_out_path: Path = Path(self.file_out)

        if not file_in_path.exists():
            raise FileNotFoundError(self.file_in)
        if file_in_path.suffix != ".json":
            raise FileTypeError.by_path(self.file_in, ".json")
        if file_out_path.suffix != ".xlsx":
            raise FileTypeError.by_path(self.file_out, ".xlsx")

    def read_execute(self) -> None:
        """Read the model and run configuration."""
        self._send_msg(f'Reading "{self.file_in}"')
        read_data: Dict[str, Any] = self.reader.read()
        model: CompBeamModel = read_data["model"]
        self._model = model

        default_parameters = {
            "gravity": 9.81,
            "p_delta": False,
            "normalize_mode_shapes": True,
            "number_of_modes": 2,
            "prefer_positive_lateral_mode_shape_values": False,
        }

        parameters: Dict[str, Any] = read_data.get("parameters", default_parameters)
        header: Optional[Dict[str, Any]] = read_data.get("header", None)

        self._solver.set_model(model)
        if parameters.get("p_delta", False):
            self._solver.set_order(2)
        self._solver.set_pref_positive_lat_msv(
            parameters.get("prefer_positive_lateral_mode_shape_values", False)
        )
        self._solver.set_normalize_shapes(parameters.get("normalize_mode_shapes", True))
        self._solver.set_mode_count(parameters.get("number_of_modes", 2))
        self._solver.set_gravity(parameters.get("gravity", 9.81))

        # save config and detailed data
        self._config["model"] = df_comp_beam_model(model)
        if model.mass_count() > 0:
            self._config["masses"] = df_node_masses(model.node_masses)
        if any(n.has_set_dofs for n in model.nodes):
            self._config["bc"] = df_dofs(model.nodes)
        if model.spring_count > 0:
            self._config["springs"] = df_springs(model.springs)
        self._config["parameters"] = DataFrame.from_dict(
            parameters, orient="index", columns=["value"]
        )
        if header is not None:
            self._config["header"] = DataFrame.from_dict(
                header, orient="index", columns=["value"]
            )

    def run_execute(self) -> None:
        """Computes the frequencies and modes shapes."""
        self._send_msg(f"Computing frequencies and mode shapes")
        self._results = self._solver.solve()

    def write_execute(self) -> None:
        """Writes the results to Excel file."""
        self._send_msg(f'Writing "{self.file_out}"')
        assert self._results is not None
        freq, msv = FlexEigenSolver.to_dataframe(*self._results)
        self.writer.write(freq=freq, msv=msv, details=self._config)
