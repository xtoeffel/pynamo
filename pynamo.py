#!/usr/bin/env python
"""Main program for execution of Pynamo.
"""

# TODO: clean out old format wind_tower#.json test files
# TODO: fix wind_tower3.json which fails w/ insufficient boundary conditions
# TODO: if above is for testing than hint in filename
# TODO: add function to get default json file from tool or document online


from argparse import ArgumentParser
from typing import Final
from pathlib import Path
from exe.base import SingleRunFlexEigen


class Pynamo:
    @staticmethod
    def _show_message(msg: str) -> None:
        print(f"   {msg}")

    def __init__(self) -> None:
        self.version: Final[str] = "1.0.0"
        self._overwrite_existing_file: bool = False
        self._json_input: str = ""
        self._excel_output: str = ""

    def _check_file_overwriteable(self, file: str) -> None:
        if self._overwrite_existing_file:
            return

        if Path(file).exists():
            raise FileExistsError(file)

    def _read_JSON_compute_write_Excel(self) -> None:
        run: SingleRunFlexEigen = SingleRunFlexEigen(
            self._json_input, self._excel_output
        )
        run.set_notifier(Pynamo._show_message)
        run.execute()

    def execute(self) -> None:
        if self._json_input != "" and self._excel_output != "":
            print(f"JSON input: {self._json_input}")
            print(f"Excel output: {self._excel_output}")
            self._check_file_overwriteable(self._excel_output)

            print("Executing:")
            self._read_JSON_compute_write_Excel()

        else:
            raise ValueError("Insufficient arguments, use -h for details")


def _print_error_header():
    print()
    print("!An error occurred!")


def main() -> None:
    pynamo: Pynamo = Pynamo()

    parser = ArgumentParser(
        prog="Pynamo",
        description=(
            "Compute flexural mode shapes and frequency for "
            "composite beam models."
        ),
    )

    parser.add_argument(
        "-v", "--version", action="version", version=f"{pynamo.version}"
    )
    parser.add_argument(
        "-o",
        "--overwrite",
        action="store_true",
        dest="overwrite_existing_file",
        help="Overwrite existing files instead of raising an error.",
    )
    parser.add_argument(
        type=str,
        action="store",
        default="",
        metavar="<json_input_file>",
        dest="json_input_file",
        help="Path to JSON input file with beam model and configuration.",
    )
    parser.add_argument(
        type=str,
        action="store",
        default="",
        metavar="<excel_output_file>",
        dest="excel_output_file",
        help="Path to Excel file to write computation results to.",
    )
    args = parser.parse_args()

    pynamo._overwrite_existing_file = args.overwrite_existing_file
    pynamo._json_input = args.json_input_file
    pynamo._excel_output = args.excel_output_file

    try:
        pynamo.execute()

    except FileNotFoundError as err:
        _print_error_header()
        print("Following file does not exist")
        print(err)

    except FileExistsError as err:
        _print_error_header()
        print(f'Existing file: "{err}"')
        print("Use [-o, --overwrite] to overwrite existing files.")

    except ValueError as err:
        _print_error_header()
        print(err)

    else:
        print("Done!")


if __name__ == "__main__":
    main()
