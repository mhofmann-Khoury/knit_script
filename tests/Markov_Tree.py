import random
from enum import Enum
from typing import List, Optional, Dict, Tuple


class Directions(Enum):
    """
        Directions that a tree can branch
    """
    Left_Branch = "\\"
    Right_Branch = "/"
    Straight = "|"
    Left_Split = "\\|"
    Right_Split = "|/"

    def __hash__(self):
        return hash(self.name)


class Markov_Tree:
    """
        Generates a branching tree with random values
    """

    def __init__(self, width: int, height: int):
        self.height = height
        self.width = width
        self.tree: List[List[Optional[Directions]]] = [[None for _ in range(0, self.width)] for _ in range(0, height)]
        self.tree[0][int((width-1) / 2)] = Directions.Straight
        for r in range(0, self.height - 1):
            self._grow_row(r)

    def _growth_options(self, row: int, needle: int) -> Tuple[List[Directions], List[int]]:
        split_weight = self.height - row  # odds of branching drops off to 0
        continue_weight = (self.height - split_weight) + 1  # odds of continuing increases
        options: Dict[Directions, int] = {}
        if self.tree[row + 1][needle] is None:  # straight position is available, may branch or split
            options[Directions.Straight] = continue_weight
            if needle > 0 and self.tree[row + 1][needle - 1] is None:  # Left branch is available
                options[Directions.Left_Branch] = continue_weight
            if needle < self.width - 1 and self.tree[row + 1][needle + 1] is None:  # right branch is available
                options[Directions.Right_Branch] = continue_weight
            if Directions.Right_Branch in options: # right branch allows right split
                options[Directions.Right_Split] = split_weight
            if Directions.Left_Branch in options: # left branch allows left split
                options[Directions.Left_Split] = split_weight
        return [*options.keys()], [*options.values()]

    def _choose_growth(self, row: int, needle: int) -> Optional[Directions]:
        options, weights = self._growth_options(row, needle)
        if len(options) == 0:
            return None
        else:
            return random.choices(options, weights=weights, k=1)[0]

    def _grow_branch(self, row: int, needle: int):
        selection = self._choose_growth(row, needle)
        if selection in [Directions.Left_Branch, Directions.Left_Split]:
            self.tree[row + 1][needle - 1] = Directions.Left_Branch
        if selection in [Directions.Straight, Directions.Left_Split, Directions.Right_Split]:
            self.tree[row + 1][needle] = Directions.Straight
        if selection in [Directions.Right_Split, Directions.Right_Branch]:
            self.tree[row + 1][needle + 1] = Directions.Right_Branch

    def _grow_row(self, row: int):
        for needle, branch_point in enumerate(self.tree[row]):
            if branch_point is not None:
                self._grow_branch(row, needle)

    def _print_row(self, row: int) -> str:
        s = f"{row}: "
        for branch_point in self.tree[row]:
            if branch_point is None:
                s += "*"
            else:
                s += branch_point.value
        return s

    def __str__(self):
        s = ""
        for r in range(0, len(self.tree)):
            s = f"{self._print_row(r)}\n{s}"
        return s

    def __repr__(self):
        return str(self)


# random.seed(10)
# tree = Markov_Tree(10, 10)
# print(tree)
