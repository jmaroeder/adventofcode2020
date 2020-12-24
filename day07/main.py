import textwrap
from pathlib import Path
from typing import Any
from typing import Tuple

import advent
from day07.bag_rules import BagRules


def main(s: str) -> Tuple[Any, Any]:
    part1 = None
    part2 = None

    rules = BagRules(s)

    return part1, part2


SAMPLE_INPUT = textwrap.dedent(
    r"""
    light red bags contain 1 bright white bag, 2 muted yellow bags.
    dark orange bags contain 3 bright white bags, 4 muted yellow bags.
    bright white bags contain 1 shiny gold bag.
    muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
    shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
    dark olive bags contain 3 faded blue bags, 4 dotted black bags.
    vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
    faded blue bags contain no other bags.
    dotted black bags contain no other bags.
    """
)


if __name__ == "__main__":
    advent.test(
        main,
        advent.TestCase(
            input=SAMPLE_INPUT,
            expected_part_1=4,
            expected_part_2="",
        ),
    )

    input_file = Path(__file__).parent.absolute() / "input.txt"
    part1, part2 = main(input_file.read_text())
    if part1:
        print(f"Part 1: {part1}")
    if part2:
        print(f"Part 2: {part2}")
