"""Reading and writing of data from and to Excel by pandas.
"""
from pandas import DataFrame
from pandas import ExcelWriter as PExcelWriter  # type: ignore
from data_io.base import BaseWriter
from typing import Dict, Any, Optional


class ExcelWriter(BaseWriter):
    """Writes results stored in DataFrames to Excel."""

    def __init__(self) -> None:
        self._file_name: str = ""

    @property
    def file_name(self) -> str:
        """Returns the file name to write to.

        :return: File name to write to
        :rtype: str
        """
        return self._file_name

    def set_file_name(self, file_name: str) -> "ExcelWriter":
        """Sets the file name and returns self for chaining of calls.

        :param file_name: File name to write to
        :type file_name: str

        :raises ValueError: If file_name is None
        """
        if file_name is None:
            raise ValueError("Invalid file name None")
        self._file_name = file_name
        return self

    def write(self, **kwargs: Any) -> None:
        """Writes the data provided by arguments to an excel file.

        Supported kwargs are

        :freq: [DataFrame] -- Frequency data
        :msv: [DataFrame] -- Mode shape values
        :details: [Dict[str, DataFrame]] -- Information to the data saved

        :raises ValueError: If file_name is not set or freq or msv is None
        """
        freq: Optional[DataFrame] = kwargs.get("freq", None)
        msv: Optional[DataFrame] = kwargs.get("msv", None)
        details: Optional[Dict[str, DataFrame]] = kwargs.get("details", None)

        if self.file_name == "":
            raise ValueError("File name not set")
        if freq is None:
            raise ValueError("Frequency data undefined")
        if msv is None:
            raise ValueError("Mode shape values undefined")

        with PExcelWriter(  # pylint: disable=abstract-class-instantiated
            self._file_name
        ) as ew:

            if details is not None:
                for key, detail in details.items():
                    detail.to_excel(ew, sheet_name=key)     # type: ignore
            freq.to_excel(ew, sheet_name="frequencies")     # type: ignore
            msv.to_excel(ew, sheet_name="modes", engine="xlsxwriter")   # type: ignore

            sheet = ew.sheets["modes"]
            chart = ew.book.add_chart({"type": "scatter", "subtype": "straight"})
            chart.set_title({"name": "Mode Shapes"})
            sheet.insert_chart("G4", chart)
            num_msv: int = msv.shape[0]

            for col_idx in range(0, freq.shape[0]):
                chart.add_series(
                    {
                        "name": freq.index[col_idx],
                        "categories": ["modes", 1, 1, num_msv, 1],
                        "values": ["modes", 1, 2 + col_idx, num_msv, 2 + col_idx],
                        "line": {"width": 1},
                        "marker": {"type": "none"},
                    }
                )
