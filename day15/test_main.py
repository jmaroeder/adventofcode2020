from typing import Iterable

import pytest

from day15.main import MemoryGame

@pytest.mark.parametrize(
    ("starting", "n", "expected"),
    [
        ("0,3,6", 4, 0),
        ("0,3,6", 5, 3),
        ("0,3,6", 6, 3),
        ("0,3,6", 7, 1),
        ("0,3,6", 8, 0),
        ("0,3,6", 9, 4),
        ("0,3,6", 10, 0),
        ("0,3,6", 30000000, 175594),
    ]
)
def test_nth_number(starting: str, n: int, expected: int) -> None:
    m = MemoryGame.from_string(starting)
    assert m.turn(n) == expected
