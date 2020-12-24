from typing import Any
from typing import Callable
from typing import Tuple

from advent.test_case import TestCase

import pytest


def test(main: Callable[[str], Tuple[Any, Any]], *test_cases: TestCase) -> None:
    pytest.register_assert_rewrite()
    for test_case in test_cases:
        part1, part2 = main(test_case.input)
        if test_case.expected_part_1:
            assert part1 == test_case.expected_part_1, f"part1 failed (got {part1}, expected {test_case.expected_part_1})"
        if test_case.expected_part_2:
            assert part2 == test_case.expected_part_2, f"part2 failed (got {part2}, expected {test_case.expected_part_2})"
