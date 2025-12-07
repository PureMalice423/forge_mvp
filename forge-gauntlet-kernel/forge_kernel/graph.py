# File: forge_kernel/graph.py

from __future__ import annotations

from typing import Callable, List

from .state import ForgeState
from .nodes import (
    intake_node,
    fixer_node,
    gauntlet_node,
    linearizer_node,
    vault_prep_node,
)


class ForgeGraph:
    """
    Minimal pipeline-style "graph" so we don't depend on external libraries yet.
    It just runs a list of node functions in order.
    """

    def __init__(self, steps: List[Callable[[ForgeState], ForgeState]]) -> None:
        self._steps = steps

    def invoke(self, initial_state: ForgeState) -> ForgeState:
        """
        Run the state through each node, in order.
        """
        state: ForgeState = dict(initial_state)  # shallow copy
        for step in self._steps:
            state = step(state)
        return state


FORGE_GRAPH = ForgeGraph(
    [
        intake_node,
        fixer_node,
        gauntlet_node,
        linearizer_node,
        vault_prep_node,
    ]
)
