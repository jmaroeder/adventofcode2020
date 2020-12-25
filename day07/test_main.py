import pytest

from day07.bag_rules import BagRules


@pytest.mark.parametrize(
    ("outer", "inner", "expected"),
    [
        ("bright white", "shiny gold", True),
        ("muted yellow", "shiny gold", True),
        ("dark orange", "bright white", True),
        ("dark orange", "muted yellow", True),
        ("dark orange", "shiny gold", True),
        ("light red", "bright white", True),
        ("light red", "muted yellow", True),
        ("light red", "shiny gold", True),
        ("dark olive", "shiny gold", False),
    ],
)
def test_can_contain(outer: str, inner: str, expected: bool, bag_rules: BagRules) -> None:
    assert bag_rules.can_contain(outer, inner) == expected


@pytest.mark.parametrize(
    ("outer", "expected"),
    [
        ("faded blue", 0),
        ("dotted black", 0),
        ("vibrant plum", 11),
        ("dark olive", 7),
        ("shiny gold", 32),
    ],
)
def test_count_inside(outer: str, expected: int, bag_rules: BagRules) -> None:
    assert bag_rules.count_inside(outer) == expected
