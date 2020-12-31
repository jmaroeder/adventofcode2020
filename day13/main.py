import logging
import textwrap
from functools import reduce
from pathlib import Path
from typing import Any
from typing import Sequence
from typing import Set
from typing import Tuple

import advent

LOG = logging.getLogger(__name__)


def parse_input(s: str) -> Tuple[int, Sequence[int], Sequence[int]]:
    lines = s.splitlines()
    if len(lines) != 2:
        raise Exception(f"Unexpected # of lines of input ({len(lines)})")
    return int(lines[0]), [int(bus_id) for bus_id in lines[1].split(",") if bus_id != "x"], [idx for idx, bus_id in enumerate(lines[1].split(",")) if bus_id != "x"]


def main(s: str) -> Tuple[Any, Any]:
    part1 = None
    part2 = None

    earliest_timestamp, bus_ids, offsets = parse_input(s)

    current_timestamp = earliest_timestamp
    while True:
        for bus_id in bus_ids:
            if current_timestamp % bus_id == 0:
                part1 = bus_id * (current_timestamp - earliest_timestamp)
                break
        if part1 is not None:
            break
        current_timestamp += 1

    LOG.debug(f"offsets: {offsets}")
    part2 = chinese_remainder(bus_ids, [-offset for offset in offsets])

    return part1, part2


def chinese_remainder(n, a):
    sum = 0
    prod = reduce(lambda a, b: a*b, n)
    for n_i, a_i in zip(n, a):
        p = prod // n_i
        sum += a_i * mul_inv(p, n_i) * p
    return sum % prod


def mul_inv(a, b):
    b0 = b
    x0, x1 = 0, 1
    if b == 1: return 1
    while a > 1:
        q = a // b
        a, b = b, a%b
        x0, x1 = x1 - q * x0, x0
    if x1 < 0: x1 += b0
    return x1


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
