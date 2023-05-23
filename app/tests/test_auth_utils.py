import pytest as pytest

from app.auth.auth import verify_password


@pytest.mark.parametrize(
    "a,b,expected",
    [
        (
            "password",
            "$2b$12$JwzVB1wx7PAcQo383dxPr.P5vU9dR6tmlWM/qDoYVRwWprgQIk.cS",
            True,
        ),
        (
            "password123",
            "$2b$12$JwzVB1wx7PAcQo383dxPr.P5vU9dR6tmlWM/qDoYVRwWprgQIk.cS",
            False,
        ),
    ],
)
def test_check_password(a: str, b: str, expected: bool):
    """Test check_password"""
    actual = verify_password(a, b)
    assert expected == actual
