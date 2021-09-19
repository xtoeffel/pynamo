# -*- coding: utf-8 -*-
from model.test_utils import TestBaseCase
from model.system import CompBeamModel
from model.elements import Node
from model.elements import by_axial_length
from model.beams import BeamB_3DOF
from model.beams import BeamB_2DOF
from model.core import AXIS, DOF
from model.entry import Mass
from numpy import ndarray
from numpy import array
from typing import List
from typing import Dict
from typing import Any
from data_io.json import JsonReader
from pathlib import Path


class TestCompBeamModel(TestBaseCase):
    def test_K(self) -> None:
        print(f">> test {CompBeamModel.__name__}.{CompBeamModel.get_K.__name__}()")

        m: CompBeamModel = CompBeamModel()
        m.add(
            BeamB_3DOF(
                *by_axial_length(BeamB_3DOF.get_dofs(), 2.9),
                e_modul=2.1e11,
                area_moi=0.615773774261056,
                area=0.268920331147286,
                mass=6121.97133856797,
            )
        )
        m.add(
            BeamB_3DOF(
                m._beams[-1].node2,
                Node(
                    BeamB_3DOF.get_dofs(),
                    {AXIS.X: m._beams[-1].node2.get_coord(AXIS.X) + 2.9},
                ),
                e_modul=2.1e11,
                area_moi=0.615773774261056,
                area=0.268920331147286,
                mass=6121.97133856797,
            )
        )
        m.add(
            BeamB_3DOF(
                m._beams[-1].node2,
                Node(
                    BeamB_3DOF.get_dofs(),
                    {AXIS.X: m._beams[-1].node2.get_coord(AXIS.X) + 2.9},
                ),
                e_modul=2.1e11,
                area_moi=0.615773774261056,
                area=0.268920331147286,
                mass=6121.97133856797,
            )
        )
        m.add(
            BeamB_3DOF(
                m._beams[-1].node2,
                Node(
                    BeamB_3DOF.get_dofs(),
                    {AXIS.X: m._beams[-1].node2.get_coord(AXIS.X) + 2.9},
                ),
                e_modul=2.1e11,
                area_moi=0.615773774261056,
                area=0.268920331147286,
                mass=6121.97133856797,
            )
        )
        m.add(
            BeamB_3DOF(
                m._beams[-1].node2,
                Node(
                    BeamB_3DOF.get_dofs(),
                    {AXIS.X: m._beams[-1].node2.get_coord(AXIS.X) + 2.9},
                ),
                e_modul=2.1e11,
                area_moi=0.615773774261056,
                area=0.268920331147286,
                mass=6121.97133856797,
            )
        )

        expected: ndarray = array(
            [
                [
                    19473541221.0104,
                    0.0000,
                    0.0000,
                    -19473541221.0104,
                    0.0000,
                    0.0000,
                    0.0000,
                    0.0000,
                    0.0000,
                    0.0000,
                    0.0000,
                    0.0000,
                    0.0000,
                    0.0000,
                    0.0000,
                    0.0000,
                    0.0000,
                    0.000,
                ],
                [
                    0.0000,
                    63624991231.2051,
                    92256237285.2474,
                    0.0000,
                    -63624991231.2051,
                    92256237285.2474,
                    0.0000,
                    0.0000,
                    0.0000,
                    0.0000,
                    0.0000,
                    0.0000,
                    0.0000,
                    0.0000,
                    0.0000,
                    0.0000,
                    0.0000,
                    0.000,
                ],
                [
                    0.0000,
                    92256237285.2474,
                    178362058751.4780,
                    0.0000,
                    -92256237285.2474,
                    89181029375.7392,
                    0.0000,
                    0.0000,
                    0.0000,
                    0.0000,
                    0.0000,
                    0.0000,
                    0.0000,
                    0.0000,
                    0.0000,
                    0.0000,
                    0.0000,
                    0.000,
                ],
                [
                    -19473541221.0104,
                    0.0000,
                    0.0000,
                    38947082442.0208,
                    0.0000,
                    0.0000,
                    -19473541221.0104,
                    0.0000,
                    0.0000,
                    0.0000,
                    0.0000,
                    0.0000,
                    0.0000,
                    0.0000,
                    0.0000,
                    0.0000,
                    0.0000,
                    0.000,
                ],
                [
                    0.0000,
                    -63624991231.2051,
                    -92256237285.2474,
                    0.0000,
                    127249982462.4100,
                    0.0000,
                    0.0000,
                    -63624991231.2051,
                    92256237285.2474,
                    0.0000,
                    0.0000,
                    0.0000,
                    0.0000,
                    0.0000,
                    0.0000,
                    0.0000,
                    0.0000,
                    0.000,
                ],
                [
                    0.0000,
                    92256237285.2474,
                    89181029375.7392,
                    0.0000,
                    0.0000,
                    356724117502.9570,
                    0.0000,
                    -92256237285.2474,
                    89181029375.7392,
                    0.0000,
                    0.0000,
                    0.0000,
                    0.0000,
                    0.0000,
                    0.0000,
                    0.0000,
                    0.0000,
                    0.000,
                ],
                [
                    0.0000,
                    0.0000,
                    0.0000,
                    -19473541221.0104,
                    0.0000,
                    0.0000,
                    38947082442.0208,
                    0.0000,
                    0.0000,
                    -19473541221.0104,
                    0.0000,
                    0.0000,
                    0.0000,
                    0.0000,
                    0.0000,
                    0.0000,
                    0.0000,
                    0.000,
                ],
                [
                    0.0000,
                    0.0000,
                    0.0000,
                    0.0000,
                    -63624991231.2051,
                    -92256237285.2474,
                    0.0000,
                    127249982462.4100,
                    0.0000,
                    0.0000,
                    -63624991231.2051,
                    92256237285.2474,
                    0.0000,
                    0.0000,
                    0.0000,
                    0.0000,
                    0.0000,
                    0.000,
                ],
                [
                    0.0000,
                    0.0000,
                    0.0000,
                    0.0000,
                    92256237285.2474,
                    89181029375.7392,
                    0.0000,
                    0.0000,
                    356724117502.9570,
                    0.0000,
                    -92256237285.2474,
                    89181029375.7392,
                    0.0000,
                    0.0000,
                    0.0000,
                    0.0000,
                    0.0000,
                    0.000,
                ],
                [
                    0.0000,
                    0.0000,
                    0.0000,
                    0.0000,
                    0.0000,
                    0.0000,
                    -19473541221.0104,
                    0.0000,
                    0.0000,
                    38947082442.0208,
                    0.0000,
                    0.0000,
                    -19473541221.0104,
                    0.0000,
                    0.0000,
                    0.0000,
                    0.0000,
                    0.000,
                ],
                [
                    0.0000,
                    0.0000,
                    0.0000,
                    0.0000,
                    0.0000,
                    0.0000,
                    0.0000,
                    -63624991231.2051,
                    -92256237285.2474,
                    0.0000,
                    127249982462.4100,
                    0.0000,
                    0.0000,
                    -63624991231.2051,
                    92256237285.2474,
                    0.0000,
                    0.0000,
                    0.000,
                ],
                [
                    0.0000,
                    0.0000,
                    0.0000,
                    0.0000,
                    0.0000,
                    0.0000,
                    0.0000,
                    92256237285.2474,
                    89181029375.7392,
                    0.0000,
                    0.0000,
                    356724117502.9570,
                    0.0000,
                    -92256237285.2474,
                    89181029375.7392,
                    0.0000,
                    0.0000,
                    0.000,
                ],
                [
                    0.0000,
                    0.0000,
                    0.0000,
                    0.0000,
                    0.0000,
                    0.0000,
                    0.0000,
                    0.0000,
                    0.0000,
                    -19473541221.0104,
                    0.0000,
                    0.0000,
                    38947082442.0208,
                    0.0000,
                    0.0000,
                    -19473541221.0104,
                    0.0000,
                    0.000,
                ],
                [
                    0.0000,
                    0.0000,
                    0.0000,
                    0.0000,
                    0.0000,
                    0.0000,
                    0.0000,
                    0.0000,
                    0.0000,
                    0.0000,
                    -63624991231.2051,
                    -92256237285.2474,
                    0.0000,
                    127249982462.4100,
                    0.0000,
                    0.0000,
                    -63624991231.2051,
                    92256237285.2474,
                ],
                [
                    0.0000,
                    0.0000,
                    0.0000,
                    0.0000,
                    0.0000,
                    0.0000,
                    0.0000,
                    0.0000,
                    0.0000,
                    0.0000,
                    92256237285.2474,
                    89181029375.7392,
                    0.0000,
                    0.0000,
                    356724117502.9570,
                    0.0000,
                    -92256237285.2474,
                    89181029375.7392,
                ],
                [
                    0.0000,
                    0.0000,
                    0.0000,
                    0.0000,
                    0.0000,
                    0.0000,
                    0.0000,
                    0.0000,
                    0.0000,
                    0.0000,
                    0.0000,
                    0.0000,
                    -19473541221.0104,
                    0.0000,
                    0.0000,
                    19473541221.0104,
                    0.0000,
                    0.000,
                ],
                [
                    0.0000,
                    0.0000,
                    0.0000,
                    0.0000,
                    0.0000,
                    0.0000,
                    0.0000,
                    0.0000,
                    0.0000,
                    0.0000,
                    0.0000,
                    0.0000,
                    0.0000,
                    -63624991231.2051,
                    -92256237285.2474,
                    0.0000,
                    63624991231.2051,
                    -92256237285.2474,
                ],
                [
                    0.0000,
                    0.0000,
                    0.0000,
                    0.0000,
                    0.0000,
                    0.0000,
                    0.0000,
                    0.0000,
                    0.0000,
                    0.0000,
                    0.0000,
                    0.0000,
                    0.0000,
                    92256237285.2474,
                    89181029375.7392,
                    0.0000,
                    -92256237285.2474,
                    178362058751.478,
                ],
            ]
        )
        print(f'expected [K] size: {"x".join(map(str, expected.shape))}')
        tol: float = 1.0e-3
        print(f"tolerance: {tol}")
        self.assertAlmostEqualMatrix(expected, m.get_K(), tol=tol, msg="[K]")
        print(" > OK")

    def test_M(self) -> None:
        print(f">> test {CompBeamModel.__name__}.{CompBeamModel.get_K.__name__}()")

        m: CompBeamModel = CompBeamModel()
        m.add(
            BeamB_3DOF(
                *by_axial_length(BeamB_3DOF.get_dofs(), 2.9),
                e_modul=2.1e11,
                area_moi=0.615773774261056,
                area=0.268920331147286,
                mass=6121.97133856797,
            )
        )
        m.add(
            BeamB_3DOF(
                m._beams[-1].node2,
                Node(
                    BeamB_3DOF.get_dofs(),
                    {AXIS.X: m._beams[-1].node2.get_coord(AXIS.X) + 2.9},
                ),
                e_modul=2.1e11,
                area_moi=0.615773774261056,
                area=0.268920331147286,
                mass=6121.97133856797,
            )
        )
        m.add(
            BeamB_3DOF(
                m._beams[-1].node2,
                Node(
                    BeamB_3DOF.get_dofs(),
                    {AXIS.X: m._beams[-1].node2.get_coord(AXIS.X) + 2.9},
                ),
                e_modul=2.1e11,
                area_moi=0.615773774261056,
                area=0.268920331147286,
                mass=6121.97133856797,
            )
        )
        m.add(
            BeamB_3DOF(
                m._beams[-1].node2,
                Node(
                    BeamB_3DOF.get_dofs(),
                    {AXIS.X: m._beams[-1].node2.get_coord(AXIS.X) + 2.9},
                ),
                e_modul=2.1e11,
                area_moi=0.615773774261056,
                area=0.268920331147286,
                mass=6121.97133856797,
            )
        )
        m.add(
            BeamB_3DOF(
                m._beams[-1].node2,
                Node(
                    BeamB_3DOF.get_dofs(),
                    {AXIS.X: m._beams[-1].node2.get_coord(AXIS.X) + 2.9},
                ),
                e_modul=2.1e11,
                area_moi=0.615773774261056,
                area=0.268920331147286,
                mass=6121.97133856797,
            )
        )

        expected: ndarray = array(
            [
                [
                    2040.657113,
                    0,
                    0,
                    1020.328556,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                ],
                [
                    0,
                    2273.875069,
                    929.9565986,
                    0,
                    787.1106007,
                    -549.5198082,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                ],
                [
                    0,
                    929.9565986,
                    490.340752,
                    0,
                    549.5198082,
                    -367.755564,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                ],
                [
                    1020.328556,
                    0,
                    0,
                    4081.314226,
                    0,
                    0,
                    1020.328556,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                ],
                [
                    0,
                    787.1106007,
                    549.5198082,
                    0,
                    4547.750137,
                    0,
                    0,
                    787.1106007,
                    -549.5198082,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                ],
                [
                    0,
                    -549.5198082,
                    -367.755564,
                    0,
                    0,
                    980.6815039,
                    0,
                    549.5198082,
                    -367.755564,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                ],
                [
                    0,
                    0,
                    0,
                    1020.328556,
                    0,
                    0,
                    4081.314226,
                    0,
                    0,
                    1020.328556,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                ],
                [
                    0,
                    0,
                    0,
                    0,
                    787.1106007,
                    549.5198082,
                    0,
                    4547.750137,
                    0,
                    0,
                    787.1106007,
                    -549.5198082,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                ],
                [
                    0,
                    0,
                    0,
                    0,
                    -549.5198082,
                    -367.755564,
                    0,
                    0,
                    980.6815039,
                    0,
                    549.5198082,
                    -367.755564,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                ],
                [
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    1020.328556,
                    0,
                    0,
                    4081.314226,
                    0,
                    0,
                    1020.328556,
                    0,
                    0,
                    0,
                    0,
                    0,
                ],
                [
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    787.1106007,
                    549.5198082,
                    0,
                    4547.750137,
                    0,
                    0,
                    787.1106007,
                    -549.5198082,
                    0,
                    0,
                    0,
                ],
                [
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    -549.5198082,
                    -367.755564,
                    0,
                    0,
                    980.6815039,
                    0,
                    549.5198082,
                    -367.755564,
                    0,
                    0,
                    0,
                ],
                [
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    1020.328556,
                    0,
                    0,
                    4081.314226,
                    0,
                    0,
                    1020.328556,
                    0,
                    0,
                ],
                [
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    787.1106007,
                    549.5198082,
                    0,
                    4547.750137,
                    0,
                    0,
                    787.1106007,
                    -549.5198082,
                ],
                [
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    -549.5198082,
                    -367.755564,
                    0,
                    0,
                    980.6815039,
                    0,
                    549.5198082,
                    -367.755564,
                ],
                [
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    1020.328556,
                    0,
                    0,
                    2040.657113,
                    0,
                    0,
                ],
                [
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    787.1106007,
                    549.5198082,
                    0,
                    2273.875069,
                    -929.9565986,
                ],
                [
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    -549.5198082,
                    -367.755564,
                    0,
                    -929.9565986,
                    490.340752,
                ],
            ]
        )
        print(f'expected [M] size: {"x".join(map(str, expected.shape))}')
        tol: float = 1.0e-6
        print(f"tolerance: {tol}")
        self.assertAlmostEqualMatrix(expected, m.get_M(), tol=tol, msg="[M]")
        print(" > OK")

    def test_fail_add(self) -> None:
        print(f">> test {CompBeamModel.__name__}.{CompBeamModel.add}()")

        m: CompBeamModel = CompBeamModel()
        b1: BeamB_3DOF = BeamB_3DOF(
            *by_axial_length(BeamB_3DOF.get_dofs(), 2.9),
            e_modul=2.1e11,
            area_moi=0.615773774261056,
            area=0.268920331147286,
            mass=6121.97133856797,
        )
        m.add(b1)
        m.add(
            BeamB_3DOF(
                m._beams[-1].node2,
                Node(
                    BeamB_3DOF.get_dofs(),
                    {AXIS.X: m._beams[-1].node2.get_coord(AXIS.X) + 2.9},
                ),
                e_modul=2.1e11,
                area_moi=0.615773774261056,
                area=0.268920331147286,
                mass=6121.97133856797,
            )
        )

        print(f"add beam of same identity")
        with self.assertRaises(ValueError) as context:
            m.add(b1)
        print(f" > EXPECTED: {context.exception}")

        print(f"add wrong type of beam")
        with self.assertRaises(TypeError) as c:
            m.add(
                BeamB_2DOF(
                    *by_axial_length(BeamB_2DOF.get_dofs(), 2.9),
                    e_modul=2.1e11,
                    area_moi=0.615773774261056,
                    area=0.268920331147286,
                    mass=6121.97133856797,
                )
            )
        print(f" > EXPECTED: {c.exception}")

    def test_get_coords(self) -> None:
        print(f">> test {CompBeamModel.get_coords.__name__}()")
        print(f"NOTE: nodes are set to their location manually.")
        m: CompBeamModel = CompBeamModel()
        m.add(
            BeamB_3DOF(
                *by_axial_length(BeamB_3DOF.get_dofs(), 2.9),
                e_modul=2.1e11,
                area_moi=0.615773774261056,
                area=0.268920331147286,
                mass=6121.97133856797,
            )
        )
        assert m.start_node is not None, "Start node is undefined"
        m.start_node.set_coord(AXIS.X, 12.334)
        assert m.end_node is not None, "End node is undefined"
        m.end_node.set_coord(AXIS.X, 12.334 + 2.9)
        m.add(
            BeamB_3DOF(
                m._beams[-1].node2,
                Node(
                    BeamB_3DOF.get_dofs(),
                    {AXIS.X: m._beams[-1].node2.get_coord(AXIS.X) + 2.9},
                ),
                e_modul=2.1e11,
                area_moi=0.615773774261056,
                area=0.268920331147286,
                mass=6121.97133856797,
            )
        )
        m.add(
            BeamB_3DOF(
                m._beams[-1].node2,
                Node(
                    BeamB_3DOF.get_dofs(),
                    {AXIS.X: m._beams[-1].node2.get_coord(AXIS.X) + 2.9},
                ),
                e_modul=2.1e11,
                area_moi=0.615773774261056,
                area=0.268920331147286,
                mass=6121.97133856797,
            )
        )
        m.add(
            BeamB_3DOF(
                m._beams[-1].node2,
                Node(
                    BeamB_3DOF.get_dofs(),
                    {AXIS.X: m._beams[-1].node2.get_coord(AXIS.X) + 2.9},
                ),
                e_modul=2.1e11,
                area_moi=0.615773774261056,
                area=0.268920331147286,
                mass=6121.97133856797,
            )
        )
        m.add(
            BeamB_3DOF(
                m._beams[-1].node2,
                Node(
                    BeamB_3DOF.get_dofs(),
                    {AXIS.X: m._beams[-1].node2.get_coord(AXIS.X) + 2.9},
                ),
                e_modul=2.1e11,
                area_moi=0.615773774261056,
                area=0.268920331147286,
                mass=6121.97133856797,
            )
        )

        x_coords: List[float] = m.get_coords(AXIS.X)
        expected: List[float] = [
            12.334,
            12.334 + 2.9,
            12.334 + 2.9 + 2.9,
            12.334 + 2.9 + 2.9 + 2.9,
            12.334 + 2.9 + 2.9 + 2.9 + 2.9,
            12.334 + 2.9 + 2.9 + 2.9 + 2.9 + 2.9,
        ]

        print(f"number of x-coordinates: {len(expected)}")
        self.assertEqual(len(expected), len(x_coords), msg="length of x-coords")
        print(f"values of x-coordinates")
        for e, a in zip(expected, x_coords):
            self.assertAlmostEqual(e, a, delta=1.0e-12, msg=f"x-coord: {e}")
        print("> OK")

    def test_offset(self) -> None:
        print(f">> test {CompBeamModel.offset.__name__}()")
        m: CompBeamModel = CompBeamModel()
        m.add(
            BeamB_3DOF(
                *by_axial_length(BeamB_3DOF.get_dofs(), 2.9),
                e_modul=2.1e11,
                area_moi=0.615773774261056,
                area=0.268920331147286,
                mass=6121.97133856797,
            )
        )
        m.add(
            BeamB_3DOF(
                m._beams[-1].node2,
                Node(
                    BeamB_3DOF.get_dofs(),
                    {AXIS.X: m._beams[-1].node2.get_coord(AXIS.X) + 2.9},
                ),
                e_modul=2.1e11,
                area_moi=0.615773774261056,
                area=0.268920331147286,
                mass=6121.97133856797,
            )
        )
        m.add(
            BeamB_3DOF(
                m._beams[-1].node2,
                Node(
                    BeamB_3DOF.get_dofs(),
                    {AXIS.X: m._beams[-1].node2.get_coord(AXIS.X) + 2.9},
                ),
                e_modul=2.1e11,
                area_moi=0.615773774261056,
                area=0.268920331147286,
                mass=6121.97133856797,
            )
        )
        m.add(
            BeamB_3DOF(
                m._beams[-1].node2,
                Node(
                    BeamB_3DOF.get_dofs(),
                    {AXIS.X: m._beams[-1].node2.get_coord(AXIS.X) + 2.9},
                ),
                e_modul=2.1e11,
                area_moi=0.615773774261056,
                area=0.268920331147286,
                mass=6121.97133856797,
            )
        )
        m.add(
            BeamB_3DOF(
                m._beams[-1].node2,
                Node(
                    BeamB_3DOF.get_dofs(),
                    {AXIS.X: m._beams[-1].node2.get_coord(AXIS.X) + 2.9},
                ),
                e_modul=2.1e11,
                area_moi=0.615773774261056,
                area=0.268920331147286,
                mass=6121.97133856797,
            )
        )

        vec: Dict[AXIS, float] = {AXIS.X: 12.334, AXIS.Y: -0.6788, AXIS.Z: 1.48473}
        print(f"offset vector: {vec}")
        m.offset(vec)

        x_coords: List[float] = m.get_coords(AXIS.X)
        y_coords: List[float] = m.get_coords(AXIS.Y)
        z_coords: List[float] = m.get_coords(AXIS.Z)

        expected_x: List[float] = [
            12.334,
            12.334 + 2.9,
            12.334 + 2.9 + 2.9,
            12.334 + 2.9 + 2.9 + 2.9,
            12.334 + 2.9 + 2.9 + 2.9 + 2.9,
            12.334 + 2.9 + 2.9 + 2.9 + 2.9 + 2.9,
        ]
        expected_y: List[float] = [-0.6788, -0.6788, -0.6788, -0.6788, -0.6788, -0.6788]
        expected_z: List[float] = [1.48473, 1.48473, 1.48473, 1.48473, 1.48473, 1.48473]

        print(f"x-coordinates: {expected_x}")
        for e, a in zip(expected_x, x_coords):
            self.assertAlmostEqual(e, a, delta=1.0e-12, msg=f"x-coord: {e}")

        print(f"y-coordinates: {expected_y}")
        for e, a in zip(expected_y, y_coords):
            self.assertAlmostEqual(e, a, delta=1.0e-12, msg=f"y-coord: {e}")

        print(f"z-coordinates: {expected_z}")
        for e, a in zip(expected_z, z_coords):
            self.assertAlmostEqual(e, a, delta=1.0e-12, msg=f"z-coord: {e}")

        print("> OK")

    def test_mass_add(self) -> None:
        print(
            f">> test {CompBeamModel.__name__}.{CompBeamModel.add_mass.__name__}() --"
            " 2DOF beams"
        )

        m: CompBeamModel = CompBeamModel()
        m.add(
            BeamB_2DOF(
                *by_axial_length(BeamB_2DOF.get_dofs(), 2.9),
                e_modul=2.1e11,
                area_moi=0.615773774261056,
                area=0.268920331147286,
                mass=6121.97133856797,
            )
        )
        m.add(
            BeamB_2DOF(
                m._beams[-1].node2,
                Node(
                    BeamB_2DOF.get_dofs(),
                    {AXIS.X: m._beams[-1].node2.get_coord(AXIS.X) + 2.9},
                ),
                e_modul=2.1e11,
                area_moi=0.615773774261056,
                area=0.268920331147286,
                mass=6121.97133856797,
            )
        )
        m.add(
            BeamB_2DOF(
                m._beams[-1].node2,
                Node(
                    BeamB_2DOF.get_dofs(),
                    {AXIS.X: m._beams[-1].node2.get_coord(AXIS.X) + 2.9},
                ),
                e_modul=2.1e11,
                area_moi=0.615773774261056,
                area=0.268920331147286,
                mass=6121.97133856797,
            )
        )
        m.add(
            BeamB_2DOF(
                m._beams[-1].node2,
                Node(
                    BeamB_2DOF.get_dofs(),
                    {AXIS.X: m._beams[-1].node2.get_coord(AXIS.X) + 2.9},
                ),
                e_modul=2.1e11,
                area_moi=0.615773774261056,
                area=0.268920331147286,
                mass=6121.97133856797,
            )
        )
        m.add(
            BeamB_2DOF(
                m._beams[-1].node2,
                Node(
                    BeamB_2DOF.get_dofs(),
                    {AXIS.X: m._beams[-1].node2.get_coord(AXIS.X) + 2.9},
                ),
                e_modul=2.1e11,
                area_moi=0.615773774261056,
                area=0.268920331147286,
                mass=6121.97133856797,
            )
        )

        nodes: List[Node] = m.nodes
        print("adding masses to nodes")
        m.add_mass(nodes[3], Mass().set_mass(1832.9).set_mmoi(DOF.PHI, 1.7834e9))
        m.add_mass(nodes[3], Mass().set_mass(834.23).set_mmoi(DOF.PHI, 2.343e3))
        assert m.end_node is not None, "end node is None"
        assert m.start_node is not None, "start node is None"
        m.add_mass(m.end_node, Mass().set_mass(122233.23).set_mmoi(DOF.PHI, 1.3643e8))
        m.add_mass(m.start_node, Mass().set_mass(887828.23).set_mmoi(DOF.PHI, 1.23e7))
        m.add_mass(nodes[1], Mass().set_mass(8234.3234))

        print(f"number of mass {m.mass_count()}")
        self.assertEqual(5, m.mass_count(), msg="mass count")
        print(f"number of mass node 3 {m.mass_count(nodes[3])}")
        self.assertEqual(2, m.mass_count(nodes[3]), msg="mass count node 3")
        print(f"number of mass node 1 {m.mass_count(nodes[1])}")
        self.assertEqual(1, m.mass_count(nodes[1]), msg="node 1")
        print(f"number of mass end node {m.mass_count(m.end_node)}")
        self.assertEqual(1, m.mass_count(nodes[-1]), msg="end node")
        print(f"number of mass start node {m.mass_count(m.start_node)}")
        self.assertEqual(1, m.mass_count(nodes[0]), msg="start node")

        print(f"mass(mass, moi) 1 at node 3 {m.get_masses_of_node(nodes[3])[1]}")
        self.assertEqual(
            834.23,
            m.get_masses_of_node(nodes[3])[1].get_value(DOF.W),
            msg="2nd mass.mass node 3",
        )
        self.assertEqual(
            2.343e3,
            m.get_masses_of_node(nodes[3])[1].get_value(DOF.PHI),
            msg="2nd mass.moi node 3",
        )

        print("mass matrix w/ point masses")
        expected_M: ndarray = array(
            [
                [
                    890102.105068611,
                    929.956598572944,
                    787.110600673025,
                    -549.519808247649,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                ],
                [
                    929.956598572944,
                    12300490.340752,
                    549.519808247649,
                    -367.755563981119,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                ],
                [
                    787.110600673025,
                    549.519808247649,
                    12782.0735372219,
                    0,
                    787.110600673025,
                    -549.519808247649,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                ],
                [
                    -549.519808247649,
                    -367.755563981119,
                    0,
                    980.681503949651,
                    549.519808247649,
                    -367.755563981119,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                ],
                [
                    0,
                    0,
                    787.110600673025,
                    549.519808247649,
                    4547.75013722192,
                    0,
                    787.110600673025,
                    -549.519808247649,
                    0,
                    0,
                    0,
                    0,
                ],
                [
                    0,
                    0,
                    -549.519808247649,
                    -367.755563981119,
                    0,
                    980.681503949651,
                    549.519808247649,
                    -367.755563981119,
                    0,
                    0,
                    0,
                    0,
                ],
                [
                    0,
                    0,
                    0,
                    0,
                    787.110600673025,
                    549.519808247649,
                    7214.88013722192,
                    0,
                    787.110600673025,
                    -549.519808247649,
                    0,
                    0,
                ],
                [
                    0,
                    0,
                    0,
                    0,
                    -549.519808247649,
                    -367.755563981119,
                    0,
                    1783403323.6815,
                    549.519808247649,
                    -367.755563981119,
                    0,
                    0,
                ],
                [
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    787.110600673025,
                    549.519808247649,
                    4547.75013722192,
                    0,
                    787.110600673025,
                    -549.519808247649,
                ],
                [
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    -549.519808247649,
                    -367.755563981119,
                    0,
                    980.681503949651,
                    549.519808247649,
                    -367.755563981119,
                ],
                [
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    787.110600673025,
                    549.519808247649,
                    124507.105068611,
                    -929.956598572944,
                ],
                [
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    -549.519808247649,
                    -367.755563981119,
                    -929.956598572944,
                    136430490.340752,
                ],
            ]
        )
        self.assertAlmostEqualMatrix(
            expected_M, m.get_M(), tol=1.0e-5, msg="mass matrix w/ point masses"
        )
        # TODO: test the computation of frequency with mass and inertia for 2DOF

        print("> OK")

    def test_mass_add_3DOF(self) -> None:
        print(
            f"< test {CompBeamModel.__name__}.{CompBeamModel.add_mass.__name__}() --"
            " 3DOF beams"
        )

        m: CompBeamModel = CompBeamModel()
        m.add(
            BeamB_3DOF(
                *by_axial_length(BeamB_3DOF.get_dofs(), 2.9),
                e_modul=2.1e11,
                area_moi=0.615773774261056,
                area=0.268920331147286,
                mass=6121.97133856797,
            )
        )
        m.add(
            BeamB_3DOF(
                m._beams[-1].node2,
                Node(
                    BeamB_3DOF.get_dofs(),
                    {AXIS.X: m._beams[-1].node2.get_coord(AXIS.X) + 2.9},
                ),
                e_modul=2.1e11,
                area_moi=0.615773774261056,
                area=0.268920331147286,
                mass=6121.97133856797,
            )
        )
        m.add(
            BeamB_3DOF(
                m._beams[-1].node2,
                Node(
                    BeamB_3DOF.get_dofs(),
                    {AXIS.X: m._beams[-1].node2.get_coord(AXIS.X) + 2.9},
                ),
                e_modul=2.1e11,
                area_moi=0.615773774261056,
                area=0.268920331147286,
                mass=6121.97133856797,
            )
        )
        m.add(
            BeamB_3DOF(
                m._beams[-1].node2,
                Node(
                    BeamB_3DOF.get_dofs(),
                    {AXIS.X: m._beams[-1].node2.get_coord(AXIS.X) + 2.9},
                ),
                e_modul=2.1e11,
                area_moi=0.615773774261056,
                area=0.268920331147286,
                mass=6121.97133856797,
            )
        )
        m.add(
            BeamB_3DOF(
                m._beams[-1].node2,
                Node(
                    BeamB_3DOF.get_dofs(),
                    {AXIS.X: m._beams[-1].node2.get_coord(AXIS.X) + 2.9},
                ),
                e_modul=2.1e11,
                area_moi=0.615773774261056,
                area=0.268920331147286,
                mass=6121.97133856797,
            )
        )

        nodes: List[Node] = m.nodes
        print("adding masses to nodes")
        m.add_mass(nodes[3], Mass().set_mass(1832.9).set_mmoi(DOF.PHI, 1.7834e9))
        m.add_mass(nodes[3], Mass().set_mass(834.23).set_mmoi(DOF.PHI, 2.343e3))
        assert m.end_node is not None, "end node is None"
        assert m.start_node is not None, "start node is None"
        m.add_mass(m.end_node, Mass().set_mass(122233.23).set_mmoi(DOF.PHI, 1.3643e8))
        m.add_mass(m.start_node, Mass().set_mass(887828.23).set_mmoi(DOF.PHI, 1.23e7))
        m.add_mass(nodes[1], Mass().set_mass(8234.3234))

        print(f"number of mass {m.mass_count()}")
        self.assertEqual(5, m.mass_count(), msg="mass count")
        print(f"number of mass node 3 {m.mass_count(nodes[3])}")
        self.assertEqual(2, m.mass_count(nodes[3]), msg="mass count node 3")
        print(f"number of mass node 1 {m.mass_count(nodes[1])}")
        self.assertEqual(1, m.mass_count(nodes[1]), msg="node 1")
        print(f"number of mass end node {m.mass_count(m.end_node)}")
        self.assertEqual(1, m.mass_count(nodes[-1]), msg="end node")
        print(f"number of mass start node {m.mass_count(m.start_node)}")
        self.assertEqual(1, m.mass_count(nodes[0]), msg="start node")

        print(f"mass(mass, moi) 1 at node 3 {m.get_masses_of_node(nodes[3])[1]}")
        self.assertEqual(
            834.23,
            m.get_masses_of_node(nodes[3])[1].get_value(DOF.W),
            msg="2nd mass.mass node 3",
        )
        self.assertEqual(
            2.343e3,
            m.get_masses_of_node(nodes[3])[1].get_value(DOF.PHI),
            msg="2nd mass.moi node 3",
        )

        print("mass matrix w/ point masses")
        expected_M: ndarray = array(
            [
                [
                    889868.887112856,
                    0,
                    0,
                    1020.328556428,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                ],
                [
                    0,
                    890102.105068611,
                    929.956598572944,
                    0,
                    787.110600673025,
                    -549.519808247649,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                ],
                [
                    0,
                    929.956598572944,
                    12300490.340752,
                    0,
                    549.519808247649,
                    -367.755563981119,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                ],
                [
                    1020.328556428,
                    0,
                    0,
                    12315.637625712,
                    0,
                    0,
                    1020.328556428,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                ],
                [
                    0,
                    787.110600673025,
                    549.519808247649,
                    0,
                    12782.0735372219,
                    0,
                    0,
                    787.110600673025,
                    -549.519808247649,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                ],
                [
                    0,
                    -549.519808247649,
                    -367.755563981119,
                    0,
                    0,
                    980.681503949651,
                    0,
                    549.519808247649,
                    -367.755563981119,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                ],
                [
                    0,
                    0,
                    0,
                    1020.328556428,
                    0,
                    0,
                    4081.31422571198,
                    0,
                    0,
                    1020.328556428,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                ],
                [
                    0,
                    0,
                    0,
                    0,
                    787.110600673025,
                    549.519808247649,
                    0,
                    4547.75013722192,
                    0,
                    0,
                    787.110600673025,
                    -549.519808247649,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                ],
                [
                    0,
                    0,
                    0,
                    0,
                    -549.519808247649,
                    -367.755563981119,
                    0,
                    0,
                    980.681503949651,
                    0,
                    549.519808247649,
                    -367.755563981119,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                ],
                [
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    1020.328556428,
                    0,
                    0,
                    6748.44422571198,
                    0,
                    0,
                    1020.328556428,
                    0,
                    0,
                    0,
                    0,
                    0,
                ],
                [
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    787.110600673025,
                    549.519808247649,
                    0,
                    7214.88013722192,
                    0,
                    0,
                    787.110600673025,
                    -549.519808247649,
                    0,
                    0,
                    0,
                ],
                [
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    -549.519808247649,
                    -367.755563981119,
                    0,
                    0,
                    1783403323.6815,
                    0,
                    549.519808247649,
                    -367.755563981119,
                    0,
                    0,
                    0,
                ],
                [
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    1020.328556428,
                    0,
                    0,
                    4081.31422571198,
                    0,
                    0,
                    1020.328556428,
                    0,
                    0,
                ],
                [
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    787.110600673025,
                    549.519808247649,
                    0,
                    4547.75013722192,
                    0,
                    0,
                    787.110600673025,
                    -549.519808247649,
                ],
                [
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    -549.519808247649,
                    -367.755563981119,
                    0,
                    0,
                    980.681503949651,
                    0,
                    549.519808247649,
                    -367.755563981119,
                ],
                [
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    1020.328556428,
                    0,
                    0,
                    124273.887112856,
                    0,
                    0,
                ],
                [
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    787.110600673025,
                    549.519808247649,
                    0,
                    124507.105068611,
                    -929.956598572944,
                ],
                [
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    -549.519808247649,
                    -367.755563981119,
                    0,
                    -929.956598572944,
                    136430490.340752,
                ],
            ]
        )
        self.assertAlmostEqualMatrix(
            expected_M, m.get_M(), tol=1.0e-5, msg="mass matrix w/ point masses"
        )

        print("> OK")

    def test_assign_mass(self) -> None:
        """Test assign_mass() to add masses at any z-coordinate in the model between start_node.z and end_node.z.
        The model is read from file, random masses assigned at z and nodes tested for masses to be present.
        Nodes are accessed by index for the unit tests.
        The masses are random, their values are only relevant for unit tests. Only DOF.W values are set.
        """
        print(TestCompBeamModel.test_assign_mass.__doc__)

        model_file: Path = (
            Path(__file__).parent.absolute()
            / ".."
            / "data_io"
            / "ut"
            / "model_definition.json"
        )
        read_data: Dict[str, Any] = JsonReader().set_file_name(str(model_file)).read()

        model: CompBeamModel = read_data["model"]
        assert model.start_node is not None
        assert model.end_node is not None

        # assign some masses
        # masses at nodes
        model.assign_mass(Mass().set_mass(2534.2334), 8.599)  # node 4
        model.assign_mass(Mass().set_mass(8233.23), 52.82)  # node 25
        model.assign_mass(Mass().set_mass(9293.83), 98.92)  # end node
        model.assign_mass(Mass().set_mass(28947.2323), 0.0)  # start node
        # masses at center between nodes
        model.assign_mass(
            Mass().set_mass(823.384), (43.945 + 46.715) / 2.0
        )  # assigned to 20
        model.assign_mass(
            Mass().set_mass(32983.4), (70.495 + 70.600) / 2.0
        )  # assigned to 31
        # masses at random locations
        model.assign_mass(Mass().set_mass(2341.123), 85.0)  # node 38
        model.assign_mass(Mass().set_mass(985.39043), 17.0)  # node 9
        model.assign_mass(Mass().set_mass(939834.28934), 39.0)  # node 18

        # test masses at nodes
        print("test masses at nodes")
        print("start node")
        masses: List[Mass] = model.get_masses_of_node(model.start_node)
        self.assertEqual(len(masses), 2)
        self.assertEqual(masses[1].get_value(DOF.W), 28947.2323)
        print("end node")
        masses = model.get_masses_of_node(model.end_node)
        self.assertEqual(len(masses), 2)
        self.assertEqual(masses[1].get_value(DOF.W), 9293.83)

        # cache nodes of model
        print("at node locations")
        nodes: List[Node] = model.nodes
        print("x = 8.599")
        masses = model.get_masses_of_node(nodes[4])
        self.assertEqual(len(masses), 1)
        self.assertEqual(masses[0].get_value(DOF.W), 2534.2334)
        print("x = 52.82")
        masses = model.get_masses_of_node(nodes[25])
        self.assertEqual(len(masses), 1)
        self.assertEqual(masses[0].get_value(DOF.W), 8233.23)

        print("center between nodes, assigned to lower")
        print(f"x = {(43.945 + 46.715)/2.0}")
        masses = model.get_masses_of_node(nodes[20])
        self.assertEqual(len(masses), 1)
        self.assertEqual(masses[0].get_value(DOF.W), 823.384)
        print(f"x = {(70.495 + 70.600)/2.0}")
        masses = model.get_masses_of_node(nodes[31])
        self.assertEqual(len(masses), 1)
        self.assertEqual(masses[0].get_value(DOF.W), 32983.4)

        print("other random nodes")
        print("x = 85.0")
        masses = model.get_masses_of_node(nodes[38])
        self.assertEqual(len(masses), 1)
        self.assertEqual(masses[0].get_value(DOF.W), 2341.123)
        print("x = 17.0")
        masses = model.get_masses_of_node(nodes[9])
        self.assertEqual(len(masses), 1)
        self.assertEqual(masses[0].get_value(DOF.W), 985.39043)
        print("x = 39.0")
        masses = model.get_masses_of_node(nodes[18])
        self.assertEqual(len(masses), 1)
        self.assertEqual(masses[0].get_value(DOF.W), 939834.28934)

        print("> OK")
