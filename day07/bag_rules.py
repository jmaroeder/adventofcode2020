import functools
import re
from dataclasses import dataclass
from dataclasses import field
from typing import Dict
from typing import List
from typing import Set
from typing import Tuple
from typing import Union
from typing import overload


@dataclass(frozen=True)
class Bag:
    adj: str
    color: str
    contains: List[Tuple[int, "Bag"]] = field(default_factory=list, repr=False, compare=False)

    @functools.cached_property
    def contains_set(self) -> Set["Bag"]:
        return set(bag for _, bag in self.contains)


class BagRules:
    bag_re = re.compile(r"(?P<adj>\w+) (?P<color>\w+)")
    line_re = re.compile(rf"{bag_re.pattern} bags contain (?P<contents>.*).")
    content_re = re.compile(rf"(?P<number>\d+) {bag_re.pattern} bags?")

    _cycle_check = Dict[Bag, Set[Bag]]

    def __init__(self, input: str) -> None:
        self.bags: Dict[Tuple[str, str], Bag] = {}
        for line in input.splitlines():
            self.parse_line(line)

    @functools.lru_cache(maxsize=None)
    def can_contain(self, outer: Union[str, Bag], inner: Union[str, Bag]) -> bool:
        if not isinstance(outer, Bag):
            outer = self.bag(outer)
        if not isinstance(inner, Bag):
            inner = self.bag(inner)
        if inner in outer.contains_set:
            return True
        return any(self.can_contain(content, inner) for content in outer.contains_set)

    @functools.lru_cache(maxsize=None)
    def count_inside(self, outer: Union[str, Bag]) -> int:
        if not isinstance(outer, Bag):
            outer = self.bag(outer)
        total = 0
        for quantity, bag in outer.contains:
            total += quantity * (1 + self.count_inside(bag))
        return total

    @overload
    def bag(self, desc: str) -> Bag:
        ...

    @overload
    def bag(self, adj: str, color: str) -> Bag:
        ...

    def bag(self, adj: str, color: str = None) -> Bag:
        if color is None:
            match = self.bag_re.match(adj)
            if not match:
                raise Exception(f"Unable to parse bag: {adj}")
            adj = match.group("adj")
            color = match.group("color")

        if (adj, color) not in self.bags:
            self.bags[adj, color] = Bag(adj, color)
        return self.bags[adj, color]

    def parse_line(self, line: str) -> None:
        match = self.line_re.match(line)
        if not match:
            raise Exception(f"Unable to parse line: {line}")
        bag = self.bag(match.group("adj"), match.group("color"))
        contents = match.group("contents")
        if contents == "no other bags":
            return
        for content in contents.split(", "):
            match = self.content_re.match(content)
            inner_bag = self.bag(match.group("adj"), match.group("color"))
            bag.contains.append((int(match.group("number")), inner_bag))
