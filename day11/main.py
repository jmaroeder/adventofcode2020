import collections
import functools
import logging
import re
import textwrap
from io import StringIO
from pathlib import Path
from typing import Any
from typing import Dict
from typing import Iterable
from typing import List
from typing import Mapping
from typing import Optional
from typing import Tuple

import advent

LOG = logging.getLogger(__name__)


STR_REP: Mapping[Optional[bool], str] = {
    True: "#",
    False: "L",
    None: ".",
}

DIRECTIONS = (
    (-1, -1), (-1, 0), (-1, 1),
    (0, -1), (0, 1),
    (1, -1), (1, 0), (1, 1),
)




class SeatMap:
    grid: Dict[Tuple[int, int], bool]

    def __init__(self, seat_positions: Iterable[Tuple[int, int]]) -> None:
        self.grid = {}
        self.height = 0
        self.width = 0
        for row, col in seat_positions:
            self.grid[row, col] = False
            self.height = max(self.height, row + 1)
            self.width = max(self.width, col + 1)

    def __repr__(self) -> str:
        ret = StringIO()
        for row in range(self.height):
            for col in range(self.width):
                ret.write(STR_REP[self.grid.get((row, col))])
            ret.write("\n")
        return ret.getvalue()

    @classmethod
    def from_str(cls, s: str) -> "SeatMap":
        seat_positions: List[Tuple[int, int]] = []
        for row, line in enumerate(s.splitlines()):
            seat_positions += [(row, m.start()) for m in re.finditer("L", line)]
        return cls(seat_positions)

    def tick(self) -> int:
        """Return the number of changes after a tick."""
        next_grid = self.grid.copy()
        changes = 0
        for row, col in self.grid.keys():
            adjacent_seats = self.count_occupied_adjacent_seats(row, col)
            if not self.grid[row, col] and adjacent_seats == 0:
                next_grid[row, col] = True
                changes += 1
            elif self.grid[row, col] and adjacent_seats >= 4:
                next_grid[row, col] = False
                changes += 1
        self.grid = next_grid
        return changes

    def count_occupied_adjacent_seats(self, row: int, col: int) -> int:
        ret = 0
        for i in (row-1, row, row+1):
            for j in (col-1, col, col+1):
                if i == row and j == col:
                    continue
                if self.grid.get((i, j)):
                    ret += 1
        return ret

    def count_occupied_seats(self) -> int:
        return collections.Counter(self.grid.values())[True]

    def run_until_stable(self) -> int:
        """Return the number of ticks until stable."""
        ticks = 0
        while True:
            changes = self.tick()
            LOG.debug(f"\n{self}")
            ticks += 1
            if changes == 0:
                break
        return ticks


class SeatMap2(SeatMap):
    def tick(self) -> int:
        """Return the number of changes after a tick."""
        next_grid = self.grid.copy()
        changes = 0
        for row, col in self.grid.keys():
            adjacent_seats = self.count_occupied_adjacent_visible_seats(row, col)
            if not self.grid[row, col] and adjacent_seats == 0:
                next_grid[row, col] = True
                changes += 1
            elif self.grid[row, col] and adjacent_seats >= 5:
                next_grid[row, col] = False
                changes += 1
        self.grid = next_grid
        return changes

    def count_occupied_adjacent_visible_seats(self, row: int, col: int) -> int:
        ret = 0

        for direction in DIRECTIONS:
            i, j = row + direction[0], col + direction[1]
            while i >= 0 and i < self.height and j >= 0 and j < self.width:
                if self.grid.get((i, j)):
                    ret += 1
                    break
                if (i, j) in self.grid:
                    break
                i += direction[0]
                j += direction[1]

        return ret




def main(s: str) -> Tuple[Any, Any]:
    part1 = None
    part2 = None

    seat_map = SeatMap.from_str(s)
    LOG.debug(f"\n{seat_map}")
    seat_map.run_until_stable()
    part1 = seat_map.count_occupied_seats()

    print("part 2")

    seat_map_2 = SeatMap2.from_str(s)
    seat_map_2.run_until_stable()
    part2 = seat_map_2.count_occupied_seats()
    return part1, part2



SAMPLE_INPUT = textwrap.dedent(
    r"""
    L.LL.LL.LL
    LLLLLLL.LL
    L.L.L..L..
    LLLL.LL.LL
    L.LL.LL.LL
    L.LLLLL.LL
    ..L.L.....
    LLLLLLLLLL
    L.LLLLLL.L
    L.LLLLL.LL
    """
).strip()


if __name__ == "__main__":
    advent.setup()
    advent.test(
        main,
        advent.TestCase(
            input=SAMPLE_INPUT,
            expected_part_1=37,
            expected_part_2=26,
        ),
    )

    advent.execute(
        main,
        Path(__file__).parent.absolute() / "input.txt",
    )
