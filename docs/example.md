# Example

This example illustrates how to run the tool.

## Download Model File
Input is a file from the repo: 
[wind_tower_2.json](https://github.com/xtoeffel/pynamo/master/exe/ut/wind_tower_2.json)

Download that file to a folder on your computer.
We assume for this example `C:\temp\wind_tower_2.json` as location.

## Run Computation
The output will be written to `C:\temp\wind_tower_2_out.xlsx`.

If you run the _Windows_ executable call:
```bash
pynamo.exe C:\temp\wind_tower_2.json C:\temp\wind_tower_2_out.xlsx
```
If you run over the _Python_ interpreter call:
```bash
python pynamo.py C:\temp\wind_tower_2.json C:\temp\wind_tower_2_out.xlsx
```

The output looks similar to this:
```code
JSON input: C:\temp\wind_tower_2.json
Excel output: C:\temp\wind_tower_2_out.xlsx
Executing:
   Verifying Files
   Reading "C:\temp\wind_tower_2.json"
   Computing frequencies and mode shapes
   Writing "C:\temp\wind_tower_2_out.xlsx"
Done!
```

> __Note__: Output might deviate depending on the tool version.

_That's it!_
Open the output file and review the results.
