from pathlib import Path
from typing import Any
from typing import Callable
from typing import Tuple


def execute(main: Callable[[str], Tuple[Any, Any]], input_file: Path) -> None:
    part1, part2 = main(input_file.read_text().strip())
    if part1 is not None:
        print(f"Part 1: {part1}")
    if part2 is not None:
        print(f"Part 2: {part2}")
