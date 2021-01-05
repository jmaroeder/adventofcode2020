import functools
import logging
import textwrap
from collections import defaultdict
from functools import reduce
from pathlib import Path
from typing import Any
from typing import Dict
from typing import Iterable
from typing import Mapping
from typing import Sequence
from typing import Set
from typing import Tuple
from typing import TypeVar

import advent

LOG = logging.getLogger(__name__)

T = TypeVar("T")


def rindex(lst, value):
    for i, v in enumerate(reversed(lst)):
        if v == value:
            return len(lst) - i - 1
    return None


class MemoryGame:
    def __init__(self, starting_numbers: Iterable[int]) -> None:
        self.numbers = list(starting_numbers)
        self.last_spoken: Dict[int, int] = defaultdict(int, {value: idx + 1 for idx, value in enumerate(self.numbers[:-1])})
        # self.spoken = set(self.numbers[:-1])

    def turn(self, n: int) -> int:
        while n > len(self.numbers):
            last_number = self.numbers[-1]
            if last_number not in self.last_spoken:
                self.numbers.append(0)
            else:
                self.numbers.append(len(self.numbers) - self.last_spoken[last_number])
            self.last_spoken[last_number] = len(self.numbers) - 1
        return self.numbers[n-1]

    @classmethod
    @functools.cache
    def from_string(cls, s: str) -> "MemoryGame":
        return cls(int(x) for x in s.split(","))



def main(s: str) -> Tuple[Any, Any]:
    part1 = None
    part2 = None

    m = MemoryGame.from_string(s)
    part1 = m.turn(2020)
    part2 = m.turn(30000000)

    return part1, part2


SAMPLE_INPUT = "0,3,6"

if __name__ == "__main__":
    advent.setup()
    # advent.test(
    #     main,
    #     advent.TestCase(
    #         input=SAMPLE_INPUT,
    #         expected_part_1=436,
    #         expected_part_2=175594,
    #     ),
    # )

    advent.execute(
        main,
        Path(__file__).parent.absolute() / "input.txt",
    )
