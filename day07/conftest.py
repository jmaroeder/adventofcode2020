import pytest

from day07.bag_rules import BagRules
from day07.main import SAMPLE_INPUT


@pytest.fixture(scope="session")
def bag_rules() -> BagRules:
    return BagRules(SAMPLE_INPUT)
