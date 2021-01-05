import functools
import logging
import re
from collections import defaultdict
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar
from typing import Dict
from typing import Iterable
from typing import List
from typing import Tuple


AND_MASK_TABLE = str.maketrans({"X": "1"})
OR_MASK_TABLE = str.maketrans({"X": "0"})
LOG = logging.getLogger(__name__)

@functools.cache
def calculate_bitmasks(mask: str) -> Tuple[int, int]:
    """Returns a tuple of ints that are meant to be & and |'d with a value."""
    return int(mask.translate(AND_MASK_TABLE), base=2), int(mask.translate(OR_MASK_TABLE), base=2)


@dataclass
class VM:
    mask_line_re: ClassVar = re.compile(r"mask = (?P<mask>[01X]{36})")
    mem_line_re: ClassVar = re.compile(r"mem\[(?P<address>\d+)] = (?P<value>\d+)")

    mask: str = "X" * 36
    mem: Dict[int, int] = field(default_factory=lambda: defaultdict(int))
    instructions: List[str] = field(default_factory=list)

    def update_mask(self, value: str) -> None:
        self.mask = value

    def apply_mask(self, value: int) -> int:
        """Applies the mask to the value."""
        and_mask, or_mask = self.bitmasks
        return value & and_mask | or_mask

    @property
    def bitmasks(self) -> Tuple[int, int]:
        return calculate_bitmasks(self.mask)

    def store(self, address: int, value: int) -> None:
        self.mem[address] = self.apply_mask(value)

    def sum_all_values(self) -> int:
        return sum(self.mem.values())

    def execute_line(self, s: str) -> None:
        match = self.mem_line_re.match(s)
        if match:
            self.store(int(match.group("address")), int(match.group("value")))
            return
        match = self.mask_line_re.match(s)
        if not match:
            raise Exception(f"Unable to parse line {s}")
        self.update_mask(match.group("mask"))

    def execute(self) -> None:
        for line in self.instructions:
            self.execute_line(line)


class VM2(VM):
    def apply_address_mask(self, value: int) -> str:
        """Applies the mask to the address"""
        s = f"{value:036b}"
        return "".join(
            c if c in ("X", "1") else s[idx]
            for idx, c in enumerate(self.mask)
        )

    def address_tree(self, address: str) -> Iterable[str]:
        if "X" not in address:
            yield address
            return
        yield from self.address_tree(address.replace("X", "0", 1))
        yield from self.address_tree(address.replace("X", "1", 1))

    def all_addresses(self, address: int) -> Iterable[int]:
        masked_address = self.apply_address_mask(address)
        # LOG.debug(f"Applying {masked_address}")
        yield from (int(s) for s in self.address_tree(masked_address))

    def store(self, address: int, value: int) -> None:
        for actual_address in self.all_addresses(address):
            # LOG.debug(f"Storing {value} at {actual_address}")
            self.mem[actual_address] = value

    def execute_line(self, s: str) -> None:
        super().execute_line(s)
