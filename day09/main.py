import functools
import itertools
import textwrap
from pathlib import Path
from typing import Any
from typing import Tuple

import advent


def main(s: str, preamble_length: int = 25) -> Tuple[Any, Any]:
    part1 = None
    part2 = None

    input_numbers = [int(line) for line in s.splitlines()]

    previous_numbers = input_numbers[:preamble_length]

    for input_number in input_numbers[preamble_length:]:
        valid = False
        for a, b in itertools.combinations(previous_numbers, 2):
            if a + b == input_number:
                valid = True
                break
        if not valid:
            part1 = input_number
            break
        previous_numbers.pop(0)
        previous_numbers.append(input_number)

    for i in range(len(input_numbers) - 1):
        tot = input_numbers[i]
        for j in range(i + 1, len(input_numbers)):
            tot += input_numbers[j]
            if tot > part1:
                break
            if tot == part1:
                part2 = min(input_numbers[i:j+1]) + max(input_numbers[i:j+1])
                break
        if part2:
            break
    return part1, part2


SAMPLE_INPUT = textwrap.dedent(
    r"""
    35
    20
    15
    25
    47
    40
    62
    55
    65
    95
    102
    117
    150
    182
    127
    219
    299
    277
    309
    576
    """
).strip()


if __name__ == "__main__":
    advent.setup()
    advent.test(
        functools.partial(main, preamble_length=5),
        advent.TestCase(
            input=SAMPLE_INPUT,
            expected_part_1=127,
            expected_part_2=62,
        ),
    )

    advent.execute(
        main,
        Path(__file__).parent.absolute() / "input.txt",
    )
