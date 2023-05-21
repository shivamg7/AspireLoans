import pytest as pytest

from app.auth.auth import get_hashed_password, verify_password


def test_get_hashed_password() -> None:
    # test same passwords create the same hash
    password_1 = "password"
    password_hashed_1 = get_hashed_password(password_1)

    password_2 = "password"
    password_hashed_2 = get_hashed_password(password_2)

    assert password_hashed_2 == password_hashed_1


@pytest.mark.parametrize(
    "a,b,expected",
    [
        (
            "password",
            "b109f3bbbc244eb82441917ed06d618b9008dd09b3befd1b5e07394c706a8bb980b1d7785e5976ec049b46df5f1326af5a2ea6d103fd07c95385ffab0cacbc86",
            True
        ),
        (
            "password",
            "wrong_password",
            False
        )
    ]
)
def test_check_password(a: str, b: str, expected: bool):
    """Test check_password"""
    actual = verify_password(a, b)
    assert expected == actual