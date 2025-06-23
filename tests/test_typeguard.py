"""Test to verify typeguard is running and working correctly."""

import pytest
from typeguard import TypeCheckError

from econexyz import add_numbers


def test_typeguard_running():
    """Test that typeguard validates type annotations."""
    # This should work fine with correct types
    result = add_numbers(5, 3)
    assert result == 8


def test_typeguard_catches_type_errors():
    """Test that typeguard catches type errors at runtime."""
    # This should trigger a typeguard error if typeguard is working
    with pytest.raises(TypeCheckError):
        add_numbers("5", 3)  # type: ignore # Wrong type for first argument
