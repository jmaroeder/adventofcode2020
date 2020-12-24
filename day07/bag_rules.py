import re
from dataclasses import dataclass
from dataclasses import field
from typing import Dict
from typing import List
from typing import Tuple
from typing import overload


@dataclass
class Bag:
    adj: str
    color: str
    contains: List[Tuple[int, "Bag"]] = field(default_factory=list)


class BagRules:
    bag_re = re.compile(r'(?P<adj>\w+) (?P<color>\w+)')
    line_re = re.compile(rf'{bag_re} bags contain (?P<contents>.*).')
    content_re = re.compile(rf'(?P<number>\d+) {bag_re} bags?')

    def __init__(self, input: str) -> None:
        self.bags: Dict[Tuple[str, str], Bag] = {}
        for line in input.splitlines():
            self.parse_line(line)

    def can_contain(self, outer: str, inner: str) -> bool:
        outer_bag = self.bag(outer)
        inner_bag = self.bag(inner)

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
