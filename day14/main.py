import logging
import textwrap
from functools import reduce
from pathlib import Path
from typing import Any
from typing import Sequence
from typing import Set
from typing import Tuple

import advent
from day14.vm import VM
from day14.vm import VM2

LOG = logging.getLogger(__name__)


def parse_input(s: str) -> Tuple[int, Sequence[int], Sequence[int]]:
    lines = s.splitlines()
    if len(lines) != 2:
        raise Exception(f"Unexpected # of lines of input ({len(lines)})")
    return int(lines[0]), [int(bus_id) for bus_id in lines[1].split(",") if bus_id != "x"], [idx for idx, bus_id in enumerate(lines[1].split(",")) if bus_id != "x"]


def main(s: str) -> Tuple[Any, Any]:
    part1 = None
    part2 = None

    vm = VM(instructions=s.splitlines())
    vm.execute()
    part1 = vm.sum_all_values()

    vm2 = VM2(instructions=s.splitlines())
    vm2.execute()
    part2 = vm2.sum_all_values()

    return part1, part2


SAMPLE_INPUT = textwrap.dedent(
    r"""
    mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
    mem[8] = 11
    mem[7] = 101
    mem[8] = 0
    """
).strip()

SAMPLE_INPUT_2 = textwrap.dedent(
    r"""
    mask = 000000000000000000000000000000X1001X
    mem[42] = 100
    mask = 00000000000000000000000000000000X0XX
    mem[26] = 1
    """
).strip()


if __name__ == "__main__":
    advent.setup()
    advent.test(
        main,
        # advent.TestCase(
        #     input=SAMPLE_INPUT,
        #     expected_part_1=165,
        #     expected_part_2=None,
        # ),
        advent.TestCase(
            input=SAMPLE_INPUT_2,
            expected_part_1=None,
            expected_part_2=208,
        ),
    )

    advent.execute(
        main,
        Path(__file__).parent.absolute() / "input.txt",
    )
