from page_analyzer import validator
import pytest

CASES = (
    ("a" * 256, None, "URL превышает 255 символов"),
    ("abc", None, "Некорректный URL"),
    ("ftp://www.rbc.r", None, "Некорректный URL"),
    ("http://www.rbc.ru/new", "http://www.rbc.ru", None),
)


@pytest.mark.parametrize("url, res, err", CASES)
def test_validate(url, res, err):
    assert validator.validate(url) == (res, err)
