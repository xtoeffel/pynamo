"""Functions and classes for compilation of data to write to targets.
"""
from typing import Dict, List, Tuple
from model.system import CompBeamModel
from pandas import DataFrame
from model.elements import Node
from model.core import AXIS, DOF
from model.entry import Mass, Spring


def df_comp_beam_model(model: CompBeamModel) -> DataFrame:
    """Compiles a DataFrame from a CompBeamModel.

    :param model: model to compile DataFrame for
    :type model: CompBeamModel

    :return: DataFrame of model
    :rtype: DataFrame

    :raises ValueError: if model is empty
    """
    if model.is_empty:
        raise ValueError("Empty model")

    return DataFrame(
        [
            [
                beam.__class__.__name__,
                beam.node1.get_coord(AXIS.X),
                beam.node2.get_coord(AXIS.X),
                beam.length,
                beam.area,
                beam.area_moi,
                beam.e_modul,
                beam.mass,
            ]
            for beam in model.beams
        ],
        columns=[
            "type",
            f"{AXIS.X.lower}1",
            f"{AXIS.X.lower}2",
            "length",
            "area",
            "area_moi",
            "e_modul",
            "mass",
        ],
    )


def df_node_masses(node_masses: Dict[Node, List[Mass]]) -> DataFrame:
    """Compiles a DataFrame form a dict of mass lists.

    :param node_masses: dict of list of mass per node
    :type node_masses: Dict[Node, List[Mass]]

    :return: DataFrame with flatmapped node.x, dof, mass_value
    :rtype: DataFrame

    :raises ValueError: if node_masses is empty
    """
    if len(node_masses) == 0:
        raise ValueError("Empty dict of node masses")

    header_dof: List[str] = [dof.name.lower() for dof in DOF]

    return DataFrame(
        [
            [node.get_coord(AXIS.X), *[val for key, val in mass.values().items()]]
            for node, mass_list in node_masses.items()
            for mass in mass_list
        ],
        columns=[AXIS.X.lower, *header_dof],
    )


def df_dofs(nodes: List[Node]) -> DataFrame:
    """Compiles a list of DOF for a list of nodes.

    :param nodes: nodes to get DOFs for - only nodes with DOF set will be considered
    :type nodes: List[Node]

    :return: DataFrame of DOF of nodes
    :rtype: DataFrame

    :raises ValueError: if nodes is empty
    """
    if len(nodes) == 0:
        raise ValueError("Empty list of nodes")

    filtered_nodes: List[Node] = [n for n in nodes if n.has_set_dofs]
    return DataFrame(
        [
            [n.get_coord(AXIS.X), dof.name.lower(), n.get_dof(dof)]
            for n in filtered_nodes
            for dof in n.set_dofs
        ],
        columns=[AXIS.X.lower, "dof", "value"],
    )


def df_springs(springs: Dict[Node, Spring]) -> DataFrame:
    """Compiles a DataFrame of springs.

    :param springs: dictionary of springs
    :type springs: Dict[Node, Spring]

    :return: DataFrame of springs
    :rtype: DataFrame

    :raise ValueError: if springs is empty
    """
    if len(springs) == 0:
        raise ValueError("Empty dict of springs")
    return DataFrame(
        [
            [node.get_coord(AXIS.X), dof.name.lower(), spring.get_value(dof)]
            for node, spring in springs.items()
            for dof in spring.dofs
        ],
        columns=[AXIS.X.lower, "dof", "spring"],
    )
