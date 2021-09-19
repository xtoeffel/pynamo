# Input

The run configuration is defined in a _JSON_ file.
That includes project data, computation settings and the engineering model.

## Model Definition
A simple _JSON_ definition can look like this (compact formatting):
```json
{
    "header": {
        "user": "Jane Doe",
        "project": "example user manual",
        "site": "The fallen Rocks",
        "state": "Wyoming"
    },
    "parameters": {
        "p_delta": true,
        "prefer_positive_lateral_mode_shape_values": false,
        "number_of_modes": 5,
        "normalize_mode_shapes": true,
        "gravity": 9.81
    },    
    "model": {
        "beam_type": "B_2DOF_II",
        "dofs": [{"x": 0.0, "w": 0.0, "phi": 0.0}],
        "springs": [{"x": 0.0, "w": 1.2e6, "phi": 5.0e7}],
        "masses": [
            {"x": 1.0, "mass": 4000.0}, {"x": 2.0, "mass": 4000.0}, 
            {"x": 3.0, "mass": 4000.0}, {"x": 4.0, "mass": 4000.0}, 
            {"x": 5.0, "mass": 4000.0}
        ],
        "beams": [
            {"length":1.0, "area":0.0, "area_moi":8.356e-5, "mass":2.5, "e_modul": 2.1e+11},
            {"length":1.0, "area":0.0, "area_moi":8.356e-5, "mass":2.5, "e_modul": 2.1e+11},
            {"length":1.0, "area":0.0, "area_moi":8.356e-5, "mass":2.5, "e_modul": 2.1e+11},
            {"length":1.0, "area":0.0, "area_moi":8.356e-5, "mass":2.5, "e_modul": 2.1e+11},
            {"length":1.0, "area":0.0, "area_moi":8.356e-5, "mass":2.5, "e_modul": 2.1e+11}
        ]
    }
}
```
The object structure of the above example must be followed. 

## Parameters
Computation parameters control the computation and
are defined by the `"parameters"` entry. 

Following parameters are supported:

- `"p_delta"`: `true` to include *pDelta* effects
  for computation of mode shapes and frequencies, otherwise `false`
- `"prefer_positive_lateral_mode_shape_values"`: `true` to prefer
  positive mode shapes (e.g. the normalized first modes maximum phi will be `1.0` instead of `-1.0`), otherwise `false`
- `"number_of_modes"`: number of modes for which to compute mode shapes
  and frequencies
- `"normalize_mode_shapes"`: `true` to normalize mode shapes to `1.0`,
  otherwise `false`
- `"gravity"`: earth acceleration

## Model Definition
The model definition, `"model"`, is split in sub-entries:

- `"beam_type"` defines the beam type
- `"dofs"` are the boundary conditions
- `"springs"` is used to define springs
- `"beams"` defines the beams in order
  
Springs and boundary conditions are optional, however at 
least one must be provided.

## User Entries
In the JSON example `"header"` is an _optional_ user entry.
These entries serve the purpose of writing meta information
into the result file for better traceability.
The following rules apply to user entries:

- Data of user entries will not be used in the computation
- All sub-entries in a user entry can only be *name*, *value*
  pairs
- Theoretically, there is no limitation on the number 
  of user entries.

A sheet will be included in the result file for each user entry
with a simple *name*, *value* table. 
This table will be included in sheet the `"header"` for the above 
_JSON_ file:

|    |	value |
| --- | ------ |
| user | Jane Doe |
| project | user manual |
| site | The fallen Rocks |
| state | Wyoming |
