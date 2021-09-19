# -*- coding: utf-8 -*-
from unittest import TestCase
from model.elements import Node
from model.elements import by_axial_length
from model.core import AXIS, DOF
from typing import Tuple


class TestNode(TestCase):
    def test_distance(self) -> None:
        print(f"< test {Node.__name__}.{Node.distance.__name__}()")

        dofs: Tuple[DOF, ...] = (DOF.W, DOF.PHI)

        n1: Node = (
            Node(dofs).set_coord(AXIS.X, 7).set_coord(AXIS.Y, 4).set_coord(AXIS.Z, 3)
        )
        n2: Node = Node(dofs).set_coords({AXIS.X: 17, AXIS.Y: 6, AXIS.Z: 2})

        dist: float = n1.distance(n2)
        print(f"    distance: {dist} -- {n1} to {n2}")
        self.assertAlmostEqual(
            pow(105.0, 0.5), dist, delta=1.0e-10, msg=f"{n1} <-> {n2}"
        )
        self.assertAlmostEqual(
            pow(105.0, 0.5), n2.distance(n1), delta=1.0e-10, msg=f"{n2} <-> {n1}"
        )

        n1.set_coords({AXIS.X: 2, AXIS.Y: 3, AXIS.Z: 1})
        n2.set_coords({AXIS.X: 8, AXIS.Y: -5, AXIS.Z: 0})
        dist = n2.distance(n1)
        print(f"    distance: {dist} -- {n1} to {n2}")
        self.assertAlmostEqual(
            pow(101.0, 0.5), dist, delta=1.0e-10, msg=f"{n1} <-> {n2}"
        )
        self.assertAlmostEqual(
            pow(101.0, 0.5), n2.distance(n1), delta=1.0e-10, msg=f"{n2} <-> {n1}"
        )

        print("> OK")

    def test_offset(self) -> None:
        print("< test offset of node")

        dofs: Tuple[DOF, ...] = (DOF.W, DOF.PHI)

        n1: Node = Node(dofs, {AXIS.X: 7, AXIS.Y: 4, AXIS.Z: 3})
        print(f"    node: {n1}")

        n1.offset({AXIS.X: 12.4})
        print(f"    offset x-axis -- new node: {n1}")
        self.assertAlmostEqual(
            19.4, n1.get_coord(AXIS.X), delta=1.0e-9, msg="x offset by 12.4 to 19.4"
        )

        n1.offset({AXIS.Y: 2.3})
        print(f"    offset y-axis -- new node: {n1}")
        self.assertAlmostEqual(
            6.3, n1.get_coord(AXIS.Y), delta=1.0e-9, msg="y offset by 2.3 to 6.3"
        )

        n1.offset({AXIS.Z: 8.1})
        print(f"    offset z-axis -- new node: {n1}")
        self.assertAlmostEqual(
            11.1, n1.get_coord(AXIS.Z), delta=1.0e-9, msg="y offset by 8.1 to 11.1"
        )

        n1.offset({AXIS.Z: 0.9, AXIS.X: 1.3, AXIS.Y: -3.4})
        print(f"    offset [x,y,z]-axis -- new node: {n1}")
        self.assertAlmostEqual(20.7, n1.get_coord(AXIS.X), delta=1.0e-9, msg="x offset")
        self.assertAlmostEqual(2.9, n1.get_coord(AXIS.Y), delta=1.0e-9, msg="y offset")
        self.assertAlmostEqual(12.0, n1.get_coord(AXIS.Z), delta=1.0e-9, msg="y offset")

        print("    fail due to empty vector (dictionary)")
        with self.assertRaises(ValueError) as context:
            n1.offset({})
        print(f"    EXPECTED: {context.exception}")

        print("> OK")

    def test_by_axial_length(self) -> None:
        print("< test creation of nodes by axial length")

        dofs: Tuple[DOF, ...] = (DOF.W, DOF.PHI)
        n1: Node
        n2: Node
        (n1, n2) = by_axial_length(dofs, 2.343)

        self.assertAlmostEqual(
            2.343, n1.distance(n2), delta=1.0e-12, msg="distance n1 to n2 = 2.343"
        )
        print("> OK")
