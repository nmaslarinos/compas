import pytest
import math
import json
import compas

from compas.geometry import Frame
from compas.geometry import Polyline


@pytest.mark.parametrize(
    "points",
    [
        [],
        [[0, 0, 0]],
        [[0, 0, 0], [1, 0, 0]],
        [[0, 0, 0], [1, 0, 0], [2, 0, 0]],
    ],
)
def test_polyline_create(points):
    curve = Polyline(points)

    assert curve.frame == Frame.worldXY()


def test_polyline_create_with_frame():
    with pytest.raises(AttributeError):
        Polyline([], frame=Frame.worldXY())


# =============================================================================
# Data
# =============================================================================


def test_polyline_data():
    curve = Polyline([[0, 0, 0], [1, 0, 0]])
    other = Polyline.from_data(json.loads(json.dumps(curve.data)))

    assert curve.points == other.points

    if not compas.IPY:
        assert Polyline.validate_data(curve.data)
        assert Polyline.validate_data(other.data)


# =============================================================================
# Constructors
# =============================================================================

# =============================================================================
# Properties and Geometry
# =============================================================================


@pytest.mark.parametrize(
    "points",
    [
        [],
        [[0, 0, 0]],
        [[0, 0, 0], [1, 0, 0]],
        [[0, 0, 0], [1, 0, 0], [2, 0, 0]],
    ],
)
def test_polyline_properties(points):
    curve = Polyline(points)

    if len(points) == 0:
        with pytest.raises(IndexError):
            assert curve.start == curve.points[0]
            assert curve.end == curve.points[-1]

            assert curve.start == curve.lines[0][0]
            assert curve.end == curve.lines[-1][1]

            assert curve.start == curve.lines[0].start
            assert curve.end == curve.lines[-1].end

    elif len(points) == 1:
        assert curve.start == curve.points[0]
        assert curve.end == curve.points[-1]

        with pytest.raises(IndexError):
            assert curve.start == curve.lines[0][0]
            assert curve.end == curve.lines[-1][1]

            assert curve.start == curve.lines[0].start
            assert curve.end == curve.lines[-1].end

    else:
        assert curve.start == curve.points[0]
        assert curve.end == curve.points[-1]

        assert curve.start == curve.lines[0][0]
        assert curve.end == curve.lines[-1][1]

        assert curve.start == curve.lines[0].start
        assert curve.end == curve.lines[-1].end


# =============================================================================
# Accessors
# =============================================================================


@pytest.mark.parametrize(
    "points",
    [
        [],
        [[0, 0, 0]],
        [[0, 0, 0], [1, 0, 0]],
        [[0, 0, 0], [1, 0, 0], [2, 0, 0]],
    ],
)
def test_polyline_accessors(points):
    curve = Polyline(points)

    for i in range(len(points)):
        assert curve[i] == curve.points[i]


# =============================================================================
# Comparison
# =============================================================================

# =============================================================================
# Other Methods
# =============================================================================


@pytest.mark.parametrize(
    "coords,expected",
    [
        (
            [[0.0, 0.0, 0.0], [100.0, 0.0, 0.0]],
            [
                [0.0, 0.0, 0.0],
                [20.0, 0.0, 0.0],
                [40.0, 0.0, 0.0],
                [60.0, 0.0, 0.0],
                [80.0, 0.0, 0.0],
                [100.0, 0.0, 0.0],
            ],
        ),
        (
            [[0.0, 0.0, 0.0], [100.0, 0.0, 0.0], [300.0, 0.0, 0.0]],
            [
                [0.0, 0.0, 0.0],
                [60.0, 0.0, 0.0],
                [120.0, 0.0, 0.0],
                [180.0, 0.0, 0.0],
                [240.0, 0.0, 0.0],
                [300.0, 0.0, 0.0],
            ],
        ),
        (
            [
                [0.0, 0.0, 0.0],
                [200.0, 0.0, 0.0],
                [200.0, 200.0, 0.0],
                [0.0, 200.0, 0.0],
                [0.0, 0.0, 0.0],
            ],
            [
                [0.0, 0.0, 0.0],
                [160.0, 0.0, 0.0],
                [200.0, 120.0, 0.0],
                [120.0, 200.0, 0.0],
                [0.0, 160.0, 0.0],
                [0.0, 0.0, 0.0],
            ],
        ),
    ],
)
def test_polyline_divide(coords, expected):
    assert expected == Polyline(coords).divide(5)


@pytest.mark.parametrize(
    "coords,expected",
    [
        ([[0.0, 0.0, 0.0], [100.0, 0.0, 0.0]], [[0.0, 0.0, 0.0], [100.0, 0.0, 0.0]]),
        (
            [[0.0, 0.0, 0.0], [100.0, 0.0, 0.0], [300.0, 0.0, 0.0]],
            [[0, 0, 0], [100, 0, 0], [200, 0, 0], [300, 0, 0]],
        ),
        (
            [
                [0.0, 0.0, 0.0],
                [200.0, 0.0, 0.0],
                [200.0, 200.0, 0.0],
                [0.0, 200.0, 0.0],
                [0.0, 0.0, 0.0],
            ],
            [
                [0, 0, 0],
                [100, 0, 0],
                [200, 0, 0],
                [200, 100, 0],
                [200, 200, 0],
                [100.0, 200, 0],
                [0, 200, 0],
                [0, 100.0, 0],
                [0, 0, 0],
            ],
        ),
    ],
)
def test_polyline_divide_length(coords, expected):
    assert expected == Polyline(coords).divide_by_length(100)


@pytest.mark.parametrize(
    "coords,expected",
    [
        ([[0.0, 0.0, 0.0], [100.0, 0.0, 0.0]], [[0.0, 0.0, 0.0], [80.0, 0.0, 0.0]]),
    ],
)
def test_polyline_divide_length_strict1(coords, expected):
    assert expected == Polyline(coords).divide_by_length(80)


@pytest.mark.parametrize(
    "coords,expected",
    [
        (
            [[0.0, 0.0, 0.0], [100.0, 0.0, 0.0]],
            [[0.0, 0.0, 0.0], [80.0, 0.0, 0.0], [100.0, 0.0, 0.0]],
        ),
    ],
)
def test_polyline_divide_length_strict2(coords, expected):
    assert expected == Polyline(coords).divide_by_length(80, False)


@pytest.mark.parametrize(
    "coords,input,expected",
    [
        (
            [
                [0.0, 0.0, 0.0],
                [1.0, 0.0, 0.0],
                [1.0, 1.0, 0.0],
                [0.0, 1.0, 0.0],
                [0.0, 0.0, 0.0],
            ],
            math.pi / 2,
            [
                Polyline([[0.0, 0.0, 0.0], [1, 0.0, 0.0]]),
                Polyline([[1, 0.0, 0.0], [1, 1, 0.0]]),
                Polyline([[1, 1, 0.0], [0.0, 1, 0.0]]),
                Polyline([[0.0, 1, 0.0], [0.0, 0.0, 0.0]]),
            ],
        ),
    ],
)
def test_polyline_split_at_corners(coords, input, expected):
    assert expected == Polyline(coords).split_at_corners(input)


@pytest.mark.parametrize(
    "coords,segments_number,expected",
    [
        (
            [[0.0, 0.0, 0.0], [100.0, 0.0, 0.0]],
            5,
            [
                ([0.0, 0.0, 0.0], [20.0, 0.0, 0.0]),
                ([20.0, 0.0, 0.0], [40.0, 0.0, 0.0]),
                ([40.0, 0.0, 0.0], [60.0, 0.0, 0.0]),
                ([60.0, 0.0, 0.0], [80.0, 0.0, 0.0]),
                ([80.0, 0.0, 0.0], [100.0, 0.0, 0.0]),
            ],
        ),
        (
            [[0.0, 0.0, 0.0], [100.0, 0.0, 0.0], [300.0, 0.0, 0.0]],
            5,
            [
                ([0.0, 0.0, 0.0], [60.0, 0.0, 0.0]),
                ([60.0, 0.0, 0.0], [100.0, 0.0, 0.0], [120.0, 0.0, 0.0]),
                ([120.0, 0.0, 0.0], [180.0, 0.0, 0.0]),
                ([180.0, 0.0, 0.0], [240.0, 0.0, 0.0]),
                ([240.0, 0.0, 0.0], [300.0, 0.0, 0.0]),
            ],
        ),
        (
            [
                [0.0, 0.0, 0.0],
                [200.0, 0.0, 0.0],
                [200.0, 200.0, 0.0],
                [0.0, 200.0, 0.0],
                [0.0, 0.0, 0.0],
            ],
            5,
            [
                ([0.0, 0.0, 0.0], [160.0, 0.0, 0.0]),
                ([160.0, 0.0, 0.0], [200.0, 0.0, 0.0], [200.0, 120.0, 0.0]),
                ([200.0, 120.0, 0.0], [200.0, 200.0, 0.0], [120.0, 200.0, 0.0]),
                ([120.0, 200.0, 0.0], [0.0, 200.0, 0.0], [0.0, 160.0, 0.0]),
                ([0.0, 160.0, 0.0], [0.0, 0.0, 0.0]),
            ],
        ),
        ([[0.0, 0.0, 0.0], [100.0, 0.0, 0.0]], 1, [([0.0, 0.0, 0.0], [100.0, 0.0, 0.0])]),
        ([[0.0, 0.0, 0.0], [100.0, 0.0, 0.0]], 0, "error"),
    ],
)
def test_polyline_split(coords, segments_number, expected):
    if segments_number > 0:
        assert expected == Polyline(coords).split(segments_number)
    else:
        pytest.raises(ValueError)


@pytest.mark.parametrize(
    "coords,length,expected",
    [
        (
            [[0.0, 0.0, 0.0], [100.0, 0.0, 0.0]],
            70,
            [
                ([0.0, 0.0, 0.0], [70.0, 0.0, 0.0]),
                ([70.0, 0.0, 0.0], [100.0, 0.0, 0.0]),
            ],
        ),
        (
            [[0.0, 0.0, 0.0], [100.0, 0.0, 0.0], [300.0, 0.0, 0.0]],
            70,
            [
                ([0.0, 0.0, 0.0], [70.0, 0.0, 0.0]),
                ([70.0, 0.0, 0.0], [100.0, 0.0, 0.0], [140.0, 0.0, 0.0]),
                ([140.0, 0.0, 0.0], [210.0, 0.0, 0.0]),
                ([210.0, 0.0, 0.0], [280.0, 0.0, 0.0]),
                ([280.0, 0.0, 0.0], [300.0, 0.0, 0.0]),
            ],
        ),
        (
            [
                [0.0, 0.0, 0.0],
                [100.0, 0.0, 0.0],
                [100.0, 100.0, 0.0],
                [0.0, 100.0, 0.0],
                [0.0, 0.0, 0.0],
            ],
            70,
            [
                ([0.0, 0.0, 0.0], [70.0, 0.0, 0.0]),
                ([70.0, 0.0, 0.0], [100.0, 0.0, 0.0], [100.0, 40.0, 0.0]),
                ([100.0, 40.0, 0.0], [100.0, 100.0, 0.0], [90.0, 100.0, 0.0]),
                (
                    [90.0, 100.0, 0.0],
                    [20.0, 100.0, 0.0],
                ),
                ([20.0, 100.0, 0.0], [0.0, 100.0, 0.0], [0.0, 50.0, 0.0]),
                ([0.0, 50.0, 0.0], [0.0, 0.0, 0.0]),
            ],
        ),
        (
            [[0.0, 0.0, 0.0], [60.0, 0.0, 0.0]],
            70,
            "error",
        ),
        (
            [[0.0, 0.0, 0.0], [60.0, 0.0, 0.0]],
            0,
            "error",
        ),
    ],
)
def test_polyline_split_by_length_strict1(coords, length, expected):
    polyline = Polyline(coords)
    if length > 0 and length < polyline.length:
        assert expected == polyline.split_by_length(length, strict=False)
    else:
        pytest.raises(ValueError)


@pytest.mark.parametrize(
    "coords,expected",
    [
        (
            [[0.0, 0.0, 0.0], [100.0, 0.0, 0.0]],
            [
                ([0.0, 0.0, 0.0], [70.0, 0.0, 0.0]),
            ],
        ),
        (
            [[0.0, 0.0, 0.0], [100.0, 0.0, 0.0], [300.0, 0.0, 0.0]],
            [
                ([0.0, 0.0, 0.0], [70.0, 0.0, 0.0]),
                ([70.0, 0.0, 0.0], [100.0, 0.0, 0.0], [140.0, 0.0, 0.0]),
                ([140.0, 0.0, 0.0], [210.0, 0.0, 0.0]),
                ([210.0, 0.0, 0.0], [280.0, 0.0, 0.0]),
            ],
        ),
        (
            [
                [0.0, 0.0, 0.0],
                [100.0, 0.0, 0.0],
                [100.0, 100.0, 0.0],
                [0.0, 100.0, 0.0],
                [0.0, 0.0, 0.0],
            ],
            [
                ([0.0, 0.0, 0.0], [70.0, 0.0, 0.0]),
                ([70.0, 0.0, 0.0], [100.0, 0.0, 0.0], [100.0, 40.0, 0.0]),
                ([100.0, 40.0, 0.0], [100.0, 100.0, 0.0], [90.0, 100.0, 0.0]),
                (
                    [90.0, 100.0, 0.0],
                    [20.0, 100.0, 0.0],
                ),
                ([20.0, 100.0, 0.0], [0.0, 100.0, 0.0], [0.0, 50.0, 0.0]),
            ],
        ),
    ],
)
def test_polyline_split_by_length_strict2(coords, expected):
    assert expected == Polyline(coords).split_by_length(70, strict=True)


@pytest.mark.parametrize(
    "coords,input,expected",
    [
        ([[0.0, 0.0, 0.0], [100.0, 0.0, 0.0]], [50, 0, 0], [1.0, 0.0, 0.0]),
        (
            [[0.0, 0.0, 0.0], [50.0, 0.0, 0.0], [100.0, 100.0, 0.0]],
            [50, 0, 0],
            [1.0, 0.0, 0.0],
        ),
    ],
)
def test_polyline_tangent_at_point(coords, input, expected):
    assert expected == Polyline(coords).tangent_at_point(input)


@pytest.mark.parametrize(
    "coords,input,expected",
    [
        (
            [[0, 0, 0], [1, 0, 0], [2, 0, 0], [2, 2, 0]],
            1.5,
            [[0, 0, 0], [1, 0, 0], [2, 0, 0], [2, 3.5, 0]],
        ),
        (
            [[0, 0, 0], [1, 0, 0], [2, 0, 0], [2, 2, 0]],
            -2.5,
            [[0, 0, 0], [1, 0, 0], [2, 0, 0], [2, -0.5, 0]],
        ),
        (
            [[0, 0, 0], [1, 0, 0], [2, 0, 0], [2, 2, 0]],
            (2, 2),
            [[-2, 0, 0], [1, 0, 0], [2, 0, 0], [2, 4, 0]],
        ),
        (
            [[0, 0, 0], [1, 0, 0], [2, 0, 0], [2, 2, 0]],
            (2, 0),
            [[-2, 0, 0], [1, 0, 0], [2, 0, 0], [2, 2, 0]],
        ),
    ],
)
def test_polyline_extend(coords, input, expected):
    assert expected == Polyline(coords).extended(input)


@pytest.mark.parametrize(
    "coords,input,expected",
    [
        (
            [[0, 0, 0], [1, 0, 0], [2, 0, 0], [2, 2, 0]],
            0.5,
            [[0, 0, 0], [1, 0, 0], [2, 0, 0], [2, 1.5, 0]],
        ),
        (
            [[0, 0, 0], [1, 0, 0], [2, 0, 0], [2, 2, 0]],
            2,
            [[0, 0, 0], [1, 0, 0], [2, 0, 0]],
        ),
        (
            [[0, 0, 0], [1, 0, 0], [2, 0, 0], [2, 2, 0]],
            (0.5, 2.5),
            [[0.5, 0, 0], [1, 0, 0], [1.5, 0, 0]],
        ),
        ([[0, 0, 0], [1, 0, 0], [2, 0, 0], [2, 2, 0]], (1, 2), [[1, 0, 0], [2, 0, 0]]),
    ],
)
def test_polyline_shortened(coords, input, expected):
    assert expected == Polyline(coords).shortened(input)
