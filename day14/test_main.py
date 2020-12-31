from typing import Iterable

import pytest

from day14.vm import VM
from day14.vm import VM2


@pytest.mark.parametrize(
    ("value", "mask", "expected"),
    [
        (11, "XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X", 73),
        (101, "XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X", 101),
        (0, "XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X", 64),
    ]
)
def test_mask(value: int, mask: str, expected: int) -> None:
    vm = VM(mask=mask)
    assert vm.apply_mask(value) == expected


@pytest.mark.parametrize(
    ("address", "mask", "expected"),
    [
        (42, "000000000000000000000000000000X1001X", "000000000000000000000000000000X1101X"),
        (26, "00000000000000000000000000000000X0XX", "00000000000000000000000000000001X0XX"),
    ]
)
def test_address_mask(address: int, mask: str, expected: str) -> None:
    vm = VM2(mask=mask)
    assert vm.apply_address_mask(address) == expected


@pytest.mark.parametrize(
    ("masked_address", "addresses"),
    [
        ("000000000000000000000000000000X1101X", ("000000000000000000000000000000011010", "000000000000000000000000000000011011", "000000000000000000000000000000111010", "000000000000000000000000000000111011")),
    ]
)
def test_address_tree(masked_address: str, addresses: Iterable[str]) -> None:
    vm = VM2()
    assert tuple(vm.address_tree(masked_address)) == tuple(addresses)
