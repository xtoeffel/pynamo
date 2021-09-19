# -*- coding: utf-8 -*-
"""Unit test for new version of beam with nodes on both ends."""
from unittest import TestCase
from model.beams import BeamB_2DOF
from model.beams import BeamB_3DOF
from model.beams import BeamB_2DOF_II
from model.elements import Node
from model.elements import by_axial_length
from model.core import AXIS
from numpy import ndarray
from numpy import array
from numpy import allclose


class TestBeam_Generic(TestCase):
    def test_beamB_2DOF(self) -> None:
        print(f"< test: {BeamB_2DOF.__name__}")
        beam_2dof: BeamB_2DOF = BeamB_2DOF(
            Node(BeamB_2DOF.get_dofs()),
            Node(BeamB_2DOF.get_dofs(), {AXIS.X: 2.34}),
            0.232,
            0.234,
            2.1e11,
            2345.8787,
        )
        print(f"     beam: {beam_2dof}")

        print("     evaluating properties")
        print(f"     order = {beam_2dof.order}")
        self.assertAlmostEqual(1, beam_2dof.order, delta=1.0e-12, msg="beam order")
        print(f"     length = {beam_2dof.length}")
        self.assertAlmostEqual(2.34, beam_2dof.length, delta=1.0e-12, msg="beam length")
        print(f"     area = {beam_2dof.area}")
        self.assertAlmostEqual(0.232, beam_2dof.area, delta=1.0e-12, msg="beam area")
        print(f"     area_moi = {beam_2dof.area_moi}")
        self.assertAlmostEqual(
            0.234, beam_2dof.area_moi, delta=1.0e-12, msg="beam area_moi"
        )
        print(f"     e_modul = {beam_2dof.e_modul}")
        self.assertAlmostEqual(
            2.1e11, beam_2dof.e_modul, delta=1.0e-12, msg="beam e_modul"
        )
        print(f"     mass = {beam_2dof.mass}")
        self.assertAlmostEqual(
            2345.8787, beam_2dof.mass, delta=1.0e-12, msg="beam mass"
        )

        print("> OK")

    def test_beamB_3DOF(self) -> None:
        print(f"< test: {BeamB_3DOF.__name__}")
        beam_3dof: BeamB_3DOF = BeamB_3DOF(
            Node(BeamB_3DOF.get_dofs()),
            Node(BeamB_3DOF.get_dofs(), {AXIS.X: 2.34}),
            0.232,
            0.234,
            2.1e11,
            2345.8787,
        )
        print(f"     beam: {beam_3dof}")

        print("     evaluating properties")
        print(f"     order = {beam_3dof.order}")
        self.assertAlmostEqual(1, beam_3dof.order, delta=1.0e-12, msg="beam order")
        print(f"     length = {beam_3dof.length}")
        self.assertAlmostEqual(2.34, beam_3dof.length, delta=1.0e-12, msg="beam length")
        print(f"     area = {beam_3dof.area}")
        self.assertAlmostEqual(0.232, beam_3dof.area, delta=1.0e-12, msg="beam area")
        print(f"     area_moi = {beam_3dof.area_moi}")
        self.assertAlmostEqual(
            0.234, beam_3dof.area_moi, delta=1.0e-12, msg="beam area_moi"
        )
        print(f"     e_modul = {beam_3dof.e_modul}")
        self.assertAlmostEqual(
            2.1e11, beam_3dof.e_modul, delta=1.0e-12, msg="beam e_modul"
        )
        print(f"     mass = {beam_3dof.mass}")
        self.assertAlmostEqual(
            2345.8787, beam_3dof.mass, delta=1.0e-12, msg="beam mass"
        )

        print("> OK")

    def test_beamB_2DOF_2ndOrder(self) -> None:
        print(f"< test 2nd Order: {BeamB_2DOF_II.__name__}")
        beam_2dof: BeamB_2DOF_II = BeamB_2DOF_II(
            Node(BeamB_2DOF.get_dofs()),
            Node(BeamB_2DOF.get_dofs(), {AXIS.X: 2.34}),
            0.232,
            0.234,
            2.1e11,
            2345.8787,
        )
        print(f"     beam: {beam_2dof}")

        print("     evaluating properties")
        print(f"     order = {beam_2dof.order}")
        self.assertAlmostEqual(2, beam_2dof.order, delta=1.0e-12, msg="beam order")
        print(f"     length = {beam_2dof.length}")
        self.assertAlmostEqual(2.34, beam_2dof.length, delta=1.0e-12, msg="beam length")
        print(f"     area = {beam_2dof.area}")
        self.assertAlmostEqual(0.232, beam_2dof.area, delta=1.0e-12, msg="beam area")
        print(f"     area_moi = {beam_2dof.area_moi}")
        self.assertAlmostEqual(
            0.234, beam_2dof.area_moi, delta=1.0e-12, msg="beam area_moi"
        )
        print(f"     e_modul = {beam_2dof.e_modul}")
        self.assertAlmostEqual(
            2.1e11, beam_2dof.e_modul, delta=1.0e-12, msg="beam e_modul"
        )
        print(f"     mass = {beam_2dof.mass}")
        self.assertAlmostEqual(
            2345.8787, beam_2dof.mass, delta=1.0e-12, msg="beam mass"
        )

        print("> OK")

    def test_beamB_fails(self) -> None:
        print("< testing fails for creation of beams")

        print("    fail due to unequal DOFs in nodes")
        with self.assertRaises(ValueError) as context:
            BeamB_2DOF(
                Node(BeamB_3DOF.get_dofs()),
                Node(BeamB_2DOF.get_dofs(), {AXIS.X: 2.34}),
                0.232,
                0.234,
                2.1e11,
                2345.8787,
            )
        print(f"    EXPECTED: {context.exception}")

        print("    Test verify(): fail due to invalid properties")

        beam_b_2dof: BeamB_2DOF = BeamB_2DOF(
            *by_axial_length(BeamB_2DOF.get_dofs(), 2.30458),
            0.958435,
            0.2485,
            2.1e11,
            234.08,
        )
        print("    verify with all properties set -- no fail")
        beam_b_2dof.verify()

        # reset some properties
        print("    reset some properties to invalid values -- fail")
        beam_b_2dof.set_mass(-1.45)
        with self.assertRaises(ValueError) as context:
            beam_b_2dof.verify()
        print(f"    EXPECTED: {context.exception}")
        beam_b_2dof.set_mass(2344.34734)
        beam_b_2dof.set_area_moi(-0.032493434)
        with self.assertRaises(ValueError) as context:
            beam_b_2dof.verify()
        print(f"    EXPECTED: {context.exception}")

        print("> OK")


class TestBeamB_3DOF(TestCase):
    def test_beam_MassMatrix(self) -> None:
        print("< test mass matrix for 3DOF bernoulli beam")

        beam_b_3dof: BeamB_3DOF = BeamB_3DOF(
            *by_axial_length(BeamB_3DOF.get_dofs(), 2.9),
            e_modul=2.1e11,
            area_moi=0.615773774261056,
            area=0.268920331147286,
            mass=6121.97133856797,
        )

        m_mass: ndarray = beam_b_3dof.get_M()

        m_mass_expected: ndarray = array(
            [
                [2040.657112856, 0, 0, 1020.328556428, 0, 0],
                [0, 2273.875068611, 929.9565985729, 0, 787.110600673, -549.5198082476],
                [0, 929.9565985729, 490.3407519748, 0, 549.5198082476, -367.7555639811],
                [1020.328556428, 0, 0, 2040.657112856, 0, 0],
                [0, 787.110600673, 549.5198082476, 0, 2273.875068611, -929.9565985729],
                [
                    0,
                    -549.5198082476,
                    -367.7555639811,
                    0,
                    -929.9565985729,
                    490.3407519748,
                ],
            ]
        )

        # unit tests
        self.assertTrue(
            allclose(m_mass_expected, m_mass, rtol=0.0, atol=1.0e-10),
            msg="mass matrix 6x6, beam bernoulli 3 DOF",
        )

        print("> OK")

    def test_StiffnessMatrix(self) -> None:
        print("< test stiffness matrix 3DOF bernoulli beam")
        print(
            "    Note: most values are > 1.0e+10, therefore accuracy is limited to"
            " 1.0e-3"
        )

        beam_b_3dof: BeamB_3DOF = BeamB_3DOF(
            *by_axial_length(BeamB_3DOF.get_dofs(), 2.9),
            e_modul=2.1e11,
            area_moi=0.615773774261056,
            area=0.268920331147286,
            mass=6121.97133856797,
        )
        m_stiff: ndarray = beam_b_3dof.get_K()
        m_stiff_expected: ndarray = array(
            [
                [19473541221.0104, 0.0, 0.0, -19473541221.0104, 0.0, 0.0],
                [
                    0.0,
                    63624991231.2051,
                    92256237285.2474,
                    0.0,
                    -63624991231.2051,
                    92256237285.2474,
                ],
                [
                    0.0,
                    92256237285.2474,
                    178362058751.478,
                    0.0,
                    -92256237285.2474,
                    89181029375.7392,
                ],
                [-19473541221.0104, 0.0, 0.0, 19473541221.0104, 0.0, 0.0],
                [
                    0.0,
                    -63624991231.2051,
                    -92256237285.2474,
                    0.0,
                    63624991231.2051,
                    -92256237285.2474,
                ],
                [
                    0.0,
                    92256237285.2474,
                    89181029375.7392,
                    0.0,
                    -92256237285.2474,
                    178362058751.478,
                ],
            ]
        )
        self.assertTrue(
            allclose(m_stiff_expected, m_stiff, rtol=0.0, atol=1.0e-3),
            msg="stiffness matrix 6x6, beam bernoulli 3 DOF",
        )

        print("    test [K]/E as secondary test w/ higher accuracy of 1.0e-10")
        m_stiff = beam_b_3dof.get_K() / beam_b_3dof.e_modul
        m_stiff_expected = array(
            [
                [0.0927311487, 0.0, 0.0, -0.0927311487, 0.0, 0.0],
                [0.0, 0.3029761487, 0.4393154156, 0.0, -0.3029761487, 0.4393154156],
                [0.0, 0.4393154156, 0.8493431369, 0.0, -0.4393154156, 0.4246715685],
                [-0.0927311487, 0.0, 0.0, 0.0927311487, 0.0, 0.0],
                [0.0, -0.3029761487, -0.4393154156, 0.0, 0.3029761487, -0.4393154156],
                [0.0, 0.4393154156, 0.4246715685, 0.0, -0.4393154156, 0.8493431369],
            ]
        )
        self.assertTrue(
            allclose(m_stiff_expected, m_stiff, rtol=0.0, atol=1.0e-10),
            msg="stiffness matrix 6x6 -- [K]/E, beam bernoulli 3 DOF",
        )
        print("> OK")


class TestBeamB_2DOF(TestCase):
    def test_M(self):
        print("< test mass matrix for 2DOF bernoulli beam")

        beam_b_2DOF: BeamB_2DOF = BeamB_2DOF(
            *by_axial_length(BeamB_2DOF.get_dofs(), 2.9),
            e_modul=2.1e11,
            area_moi=0.615773774261056,
            area=0.268920331147286,
            mass=6121.97133856797,
        )
        m_mass: ndarray = beam_b_2DOF.get_M()
        m_mass_expected: ndarray = array(
            [
                [2273.875068611, 929.9565985729, 787.110600673, -549.5198082476],
                [929.9565985729, 490.3407519748, 549.5198082476, -367.7555639811],
                [787.110600673, 549.5198082476, 2273.875068611, -929.9565985729],
                [-549.5198082476, -367.7555639811, -929.9565985729, 490.3407519748],
            ]
        )

        self.assertTrue(
            allclose(m_mass_expected, m_mass, rtol=0.0, atol=1.0e-10),
            msg="mass matrix 4x4, beam bernoulli 2 DOF",
        )

        print("> OK")

    def test_K(self):
        print("< test stiffness matrix 2DOF bernoulli beam")
        print(
            "    Note: most values are > 1.0e+10, therefore accuracy is limited to"
            " 1.0e-3"
        )

        beam_b_2dof: BeamB_2DOF = BeamB_2DOF(
            *by_axial_length(BeamB_2DOF.get_dofs(), 2.9),
            e_modul=2.1e11,
            area_moi=0.615773774261056,
            area=0.268920331147286,
            mass=6121.97133856797,
        )
        m_stiff: ndarray = beam_b_2dof.get_K()
        m_stiff_expected: ndarray = array(
            [
                [
                    63624991231.2051,
                    92256237285.2474,
                    -63624991231.2051,
                    92256237285.2474,
                ],
                [
                    92256237285.2474,
                    178362058751.478,
                    -92256237285.2474,
                    89181029375.7392,
                ],
                [
                    -63624991231.2051,
                    -92256237285.2474,
                    63624991231.2051,
                    -92256237285.2474,
                ],
                [
                    92256237285.2474,
                    89181029375.7392,
                    -92256237285.2474,
                    178362058751.478,
                ],
            ]
        )
        self.assertTrue(
            allclose(m_stiff_expected, m_stiff, rtol=0.0, atol=1.0e-3),
            msg="stiffness matrix 4x4, beam bernoulli 2 DOF",
        )

        print("    test [K]/E as secondary test w/ higher accuracy of 1.0e-10")
        m_stiff = beam_b_2dof.get_K() / beam_b_2dof.e_modul
        m_stiff_expected = array(
            [
                [0.3029761487, 0.4393154156, -0.3029761487, 0.4393154156],
                [0.4393154156, 0.8493431369, -0.4393154156, 0.4246715685],
                [-0.3029761487, -0.4393154156, 0.3029761487, -0.4393154156],
                [0.4393154156, 0.4246715685, -0.4393154156, 0.8493431369],
            ]
        )
        self.assertTrue(
            allclose(m_stiff_expected, m_stiff, rtol=0.0, atol=1.0e-10),
            msg="stiffness matrix 4x4 -- [K]/E, beam bernoulli 2 DOF",
        )
        print("> OK")

    def test_K2(self) -> None:
        print("< test stiffness matrix 2DOF bernoulli beam, including p-Delta effects")
        print(
            "    Note: most values are > 1.0e+10, therefore accuracy is limited to"
            " 1.0e-3"
        )

        beam_b_2dof: BeamB_2DOF_II = BeamB_2DOF_II(
            *by_axial_length(BeamB_2DOF.get_dofs(), 2.9),
            e_modul=2.1e11,
            area_moi=0.615773774261056,
            area=0.268920331147286,
            mass=6121.97133856797,
        )
        beam_b_2dof.set_force_x(-2000.0)
        print("    first order (no p-Delta) stiffness matrix")
        m_stiff: ndarray = beam_b_2dof.get_K1()
        m_stiff1_expected: ndarray = array(
            [
                [
                    63624991231.2051,
                    92256237285.2474,
                    -63624991231.2051,
                    92256237285.2474,
                ],
                [
                    92256237285.2474,
                    178362058751.478,
                    -92256237285.2474,
                    89181029375.7392,
                ],
                [
                    -63624991231.2051,
                    -92256237285.2474,
                    63624991231.2051,
                    -92256237285.2474,
                ],
                [
                    92256237285.2474,
                    89181029375.7392,
                    -92256237285.2474,
                    178362058751.478,
                ],
            ]
        )
        self.assertTrue(
            allclose(m_stiff1_expected, m_stiff, rtol=0.0, atol=1.0e-3),
            msg="stiffness matrix 4x4, beam bernoulli 2 DOF",
        )

        print("    test [K(1)]/E as secondary test w/ higher accuracy of 1.0e-10")
        m_stiff = beam_b_2dof.get_K1() / beam_b_2dof.e_modul
        m_stiff1_expected_high_acc: ndarray = array(
            [
                [0.3029761487, 0.4393154156, -0.3029761487, 0.4393154156],
                [0.4393154156, 0.8493431369, -0.4393154156, 0.4246715685],
                [-0.3029761487, -0.4393154156, 0.3029761487, -0.4393154156],
                [0.4393154156, 0.4246715685, -0.4393154156, 0.8493431369],
            ]
        )
        self.assertTrue(
            allclose(m_stiff1_expected_high_acc, m_stiff, rtol=0.0, atol=1.0e-10),
            msg="stiffness matrix 4x4 -- [K1]/E, beam bernoulli 2 DOF",
        )

        print("stiffness matrix of ONLY 2nd order (p-Delta effects) - [K2]")
        m_stiff = beam_b_2dof.get_K2()
        # original values were computed with: D/(60L)*[...] as documented in Petersen Baudynamik
        # however, that is incorrect - correct is: D/(30L)*[...]
        m_stiff2_expected: ndarray = array(
            [
                [
                    2.0 * -413.793103448276,
                    2.0 * -100,
                    2.0 * 413.793103448276,
                    2.0 * -100,
                ],
                [
                    2.0 * -100,
                    2.0 * -386.666666666667,
                    2.0 * 100,
                    2.0 * 96.6666666666667,
                ],
                [2.0 * 413.793103448276, 2.0 * 100, 2.0 * -413.793103448276, 2.0 * 100],
                [
                    2.0 * -100,
                    2.0 * 96.6666666666667,
                    2.0 * 100,
                    2.0 * -386.666666666667,
                ],
            ]
        )
        self.assertTrue(
            allclose(m_stiff2_expected, m_stiff, rtol=0.0, atol=1.0e-10),
            msg=(
                "stiffness matrix 4x4 -- [K2] -- only 2nd order (p-Delta), beam"
                " bernoulli 2 DOF"
            ),
        )

        print("    second order (with p-Delta effects) stiffness matrix")
        m_stiff = beam_b_2dof.get_K(2)
        m_stiff_SYS_expected: ndarray = m_stiff1_expected + m_stiff2_expected
        self.assertTrue(
            allclose(m_stiff_SYS_expected, m_stiff, rtol=0.0, atol=1.0e-3),
            msg=(
                "stiffness matrix 2nd order (with p-Delta effects) 4x4, beam bernoulli"
                " 2 DOF"
            ),
        )
        print("> OK")
