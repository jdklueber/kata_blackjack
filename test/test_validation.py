import pytest
from blackjack.consoleio import validate_int


test_data = [
    ("10", 10, None, None),
    ("asdas", False, None, None),
    ("-10", -10, None, None),
    ("5", 5, 0, 10),
    ("-5", -5, -10, 10),
    ("11", False, 0, 10),
    ("-1", False, 0, 10),
]


@pytest.mark.parametrize("input_value, expected, min_value, max_value", test_data)
def test_validate_int(input_value, expected, min_value, max_value):
    assert validate_int(input_value, min_val=min_value, max_val=max_value) == expected
