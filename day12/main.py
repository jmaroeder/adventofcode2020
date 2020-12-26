import collections
import enum
import functools
import logging
import re
import textwrap
from io import StringIO
from pathlib import Path
from typing import Any
from typing import ClassVar
from typing import Dict
from typing import Iterable
from typing import List
from typing import Mapping
from typing import Optional
from typing import Tuple

import advent

LOG = logging.getLogger(__name__)


class Direction(int, enum.Enum):
    E = 0
    S = 90
    W = 180
    N = 270


DIRECTION_DXY = {
    Direction.E: (1, 0),
    Direction.N: (0, 1),
    Direction.W: (-1, 0),
    Direction.S: (0, -1),
}


class Ship:
    instruction_re: ClassVar[re.Pattern] = re.compile(r"(?P<action>[NSEWLRF])(?P<value>\d+)")
    action_method_map: ClassVar[Mapping[str, str]] = {
        "N": "north",
        "S": "south",
        "E": "east",
        "W": "west",
        "L": "left",
        "R": "right",
        "F": "forward",
    }

    heading = Direction.E
    x = 0
    y = 0

    def go_direction(self, direction: Direction, value: int) -> None:
        dxy = DIRECTION_DXY[direction]
        self.x += dxy[0] * value
        self.y += dxy[1] * value

    def forward(self, value: int) -> None:
        self.go_direction(self.heading, value)

    def left(self, value: int) -> None:
        self.right(-value)

    def right(self, value: int) -> None:
        self.heading = Direction((self.heading + value) % 360)

    def north(self, value: int) -> None:
        self.go_direction(Direction.N, value)

    def south(self, value: int) -> None:
        self.go_direction(Direction.S, value)

    def east(self, value: int) -> None:
        self.go_direction(Direction.E, value)

    def west(self, value: int) -> None:
        self.go_direction(Direction.W, value)

    def follow_instruction(self, s: str) -> None:
        match = self.instruction_re.match(s)
        if match is None:
            raise Exception(f"Unable to parse instruction: {s}")
        getattr(self, self.action_method_map[match.group("action")])(int(match.group("value")))

    @property
    def manhattan_distance(self) -> int:
        return abs(self.x) + abs(self.y)


class ActualShip(Ship):
    waypoint_x = 10
    waypoint_y = 1

    def go_direction(self, direction: Direction, value: int) -> None:
        """Move waypoint instead of ship."""
        dxy = DIRECTION_DXY[direction]
        self.waypoint_x += dxy[0] * value
        self.waypoint_y += dxy[1] * value

    def forward(self, value: int) -> None:
        """Move ship to waypoint."""
        self.x += self.waypoint_x * value
        self.y += self.waypoint_y * value

    def right(self, value: int) -> None:
        """Rotate the waypoint around the ship."""
        value %= 360
        if value == 90:
            self.waypoint_x, self.waypoint_y = self.waypoint_y, -self.waypoint_x
        elif value == 180:
            self.waypoint_x, self.waypoint_y = -self.waypoint_x, -self.waypoint_y
        elif value == 270:
            self.waypoint_x, self.waypoint_y = -self.waypoint_y, self.waypoint_x

    def __repr__(self) -> str:
        return f"ship=({self.x}, {self.y}), waypoint=({self.waypoint_x}, {self.waypoint_y})"

def main(s: str) -> Tuple[Any, Any]:
    ship = Ship()
    actual_ship = ActualShip()
    LOG.debug(actual_ship)
    for line in s.splitlines():
        # ship.follow_instruction(line)
        actual_ship.follow_instruction(line)
        LOG.debug(actual_ship)

    # part1 = ship.manhattan_distance
    part1 = None
    part2 = actual_ship.manhattan_distance

    return part1, part2



SAMPLE_INPUT = textwrap.dedent(
    r"""
    F10
    N3
    F7
    R90
    F11
    """
).strip()


if __name__ == "__main__":
    advent.setup()
    advent.test(
        main,
        advent.TestCase(
            input=SAMPLE_INPUT,
            # expected_part_1=25,
            expected_part_1=None,
            expected_part_2=286,
        ),
    )

    advent.execute(
        main,
        Path(__file__).parent.absolute() / "input.txt",
    )
