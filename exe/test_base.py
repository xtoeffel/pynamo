from unittest import TestCase
from exe.base import SingleRunFlexEigen
from pathlib import Path


class TestSingleRunFlexEigen(TestCase):
    def test_run(self) -> None:
        """
        < Test of single run computing frequencies and mode shapes. Read from JSON write to EXCEL.
        """
        print(TestSingleRunFlexEigen.test_run.__doc__.strip())  # type: ignore

        file_in: Path = Path(__file__).parent.absolute() / "ut" / "wind_tower_2.json"
        file_out: Path = (
            Path(__file__).parent.absolute() / "ut" / "test_out_single_run.xlsx"
        )

        print(f'    in : "{str(file_in)}"')
        print(f'    out: "{str(file_out)}"')

        run: SingleRunFlexEigen = SingleRunFlexEigen(str(file_in), str(file_out))

        run.execute()

        print("> OK")
