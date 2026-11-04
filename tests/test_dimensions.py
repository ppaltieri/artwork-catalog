import pytest

from artwork_catalog.dimensions import Dimensions


def test_dimensions_all_values():
    dimensions = Dimensions(29, 21, 2, "cm")

    assert str(dimensions) == "29 x 21 x 2 cm"


def test_dimensions_none_depth():
    dimensions = Dimensions(29, 21, None, "cm")

    assert str(dimensions) == "29 x 21 cm"


def test_dimensions_zero_depth():
    dimensions = Dimensions(29, 21, 0, "cm")

    assert str(dimensions) == "29 x 21 cm"


def test_dimensions_default_arguments():
    dimensions = Dimensions(29, 21)

    assert str(dimensions) == "29 x 21 cm"


@pytest.mark.parametrize("height", [-1, 0])
def test_dimensions_negative_or_zero_height(height):
    with pytest.raises(ValueError):
        Dimensions(height, 21, 2, "cm")


@pytest.mark.parametrize("width", [-1, 0])
def test_dimensions_negative_or_zero_width(width):
    with pytest.raises(ValueError):
        Dimensions(29, width, 2, "cm")


@pytest.mark.parametrize("depth", [-1, -0.5])
def test_dimensions_negative_depth(depth):
    with pytest.raises(ValueError):
        Dimensions(29, 21, depth, "cm")


def test_dimensions_to_dict():
    dimensions = Dimensions(29, 21, 2, "cm")

    assert dimensions.to_dict() == {
        "height": 29,
        "width": 21,
        "depth": 2,
        "unit": "cm",
    }


def test_dimensions_to_dict_none_depth():
    dimensions = Dimensions(29, 21)

    assert dimensions.to_dict() == {
        "height": 29,
        "width": 21,
        "depth": None,
        "unit": "cm",
    }


def test_dimensions_whole_float_str_format():
    dimensions = Dimensions(29.0, 21.0, 2.0, "cm")

    assert str(dimensions) == "29 x 21 x 2 cm"


def test_dimensions_float_str_format():
    dimensions = Dimensions(29.5, 21.5, 2.5, "cm")

    assert str(dimensions) == "29.5 x 21.5 x 2.5 cm"