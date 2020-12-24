from dataclasses import dataclass
from typing import Any
from typing import Optional


@dataclass
class TestCase:
    input: str
    expected_part_1: Optional[Any]
    expected_part_2: Optional[Any]
