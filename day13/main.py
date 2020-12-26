import logging
import textwrap
from pathlib import Path
from typing import Any
from typing import Set
from typing import Tuple

import advent

LOG = logging.getLogger(__name__)


def parse_input(s: str) -> Tuple[int, Set[int]]:
    lines = s.splitlines()
    if len(lines) != 2:
        raise Exception(f"Unexpected # of lines of input ({len(lines)})")
    return int(lines[0]), {int(bus_id) for bus_id in lines[1].split(",") if bus_id != "x"}


def main(s: str) -> Tuple[Any, Any]:
    part1 = None
    part2 = None

    bus_ids: str
    earliest_timestamp, bus_ids = parse_input(s)

    current_timestamp = earliest_timestamp
    while True:
        for bus_id in bus_ids:
            if current_timestamp % bus_id == 0:
                part1 = bus_id * (current_timestamp - earliest_timestamp)
                break
        if part1 is not None:
            break
        current_timestamp += 1

    return part1, part2


SAMPLE_INPUT = textwrap.dedent(
    r"""
    939
    7,13,x,x,59,x,31,19
    """
).strip()


if __name__ == "__main__":
    advent.setup()
    advent.test(
        main,
        advent.TestCase(
            input=SAMPLE_INPUT,
            expected_part_1=295,
            expected_part_2=None,
        ),
    )

    advent.execute(
        main,
        Path(__file__).parent.absolute() / "input.txt",
    )
