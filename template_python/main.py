from pathlib import Path
from typing import Any
from typing import Tuple

import advent


def main(s: str) -> Tuple[Any, Any]:
    part1 = None
    part2 = None

    return part1, part2


if __name__ == "__main__":
    advent.test(
        main,
        advent.TestCase(
            input="",
            expected_part_1="",
            expected_part_2="",
        ),
    )

    input_file = Path(__file__).parent.absolute() / "input.txt"
    part1, part2 = main(input_file.read_text())
    if part1:
        print(f"Part 1: {part1}")
    if part2:
        print(f"Part 2: {part2}")
