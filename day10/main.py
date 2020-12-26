import collections
import logging
import textwrap
from collections import defaultdict
from pathlib import Path
from typing import Any
from typing import Dict
from typing import Sequence
from typing import Tuple

import advent

LOG = logging.getLogger(__name__)


def main(s: str) -> Tuple[Any, Any]:
    part1 = None
    part2 = None

    input_numbers = [int(line) for line in s.splitlines()]

    sorted_adapters = sorted(input_numbers)
    sorted_adapters.append(sorted_adapters[-1] + 3)

    current_voltage = 0
    differences: Dict[int, int] = defaultdict(int)
    for adapter in sorted_adapters:
        difference = adapter - current_voltage
        differences[difference] += 1
        current_voltage = adapter

    part1 = differences[1] * differences[3]

    dp: Dict[int, int] = defaultdict(int)
    dp[0] = 1
    for adapter in sorted_adapters:
        dp[adapter] = dp[adapter-1] + dp[adapter-2] + dp[adapter-3]

    part2 = dp[sorted_adapters[-1]]

    return part1, part2


def diffs(numbers: Sequence[int]) -> Sequence[int]:
    return [number - prev_number for number, prev_number in zip(numbers[1:], numbers)]


SAMPLE_INPUT_1 = textwrap.dedent(
    r"""
    16
    10
    15
    5
    1
    11
    7
    19
    6
    12
    4
    """
).strip()

SAMPLE_INPUT_2 = textwrap.dedent(
    r"""
    28
    33
    18
    42
    31
    14
    46
    20
    48
    47
    24
    23
    49
    45
    19
    38
    39
    11
    1
    32
    25
    35
    8
    17
    7
    9
    4
    2
    34
    10
    3
    """
).strip()


if __name__ == "__main__":
    advent.setup()
    advent.test(
        main,
        advent.TestCase(
            input=SAMPLE_INPUT_1,
            expected_part_1=35,
            expected_part_2=8,
        ),
        advent.TestCase(
            input=SAMPLE_INPUT_2,
            expected_part_1=220,
            expected_part_2=19208,
        ),
    )

    advent.execute(
        main,
        Path(__file__).parent.absolute() / "input.txt",
    )
