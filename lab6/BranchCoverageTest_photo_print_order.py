"""Lab 6 - Branch coverage tests for photo_print_order.py

Every decision is exercised both True and False, including boundary values.

Run:
    coverage run --branch -m pytest BranchCoverageTest_photo_print_order.py
    coverage report -m
"""
import pytest
from photo_print_order import extra_print_charge, order_valid, dispatch_status


# ---------------- extra_print_charge: validation branches ----------------
def test_within_included_prints():
    assert extra_print_charge("4x6", 15, "matte", False) == 0


@pytest.mark.parametrize("size", ["11x14", "", "4X6"])
def test_unknown_print_size_raises(size):
    with pytest.raises(ValueError, match="unknown print size"):
        extra_print_charge(size, 10, "matte", False)


def test_negative_copies_raises():
    with pytest.raises(ValueError, match="invalid copies"):
        extra_print_charge("4x6", -1, "matte", False)


def test_zero_copies_is_valid():
    assert extra_print_charge("4x6", 0, "matte", False) == 0


# ---------------- membership branch (is_member and size != 8x10) ----------
def test_member_gets_bonus_on_4x6():
    # included 20 + 5 = 25 -> 5 extra * 4
    assert extra_print_charge("4x6", 30, "matte", True) == 20


def test_member_gets_bonus_on_5x7():
    # included 15 + 5 = 20 -> 5 extra * 4
    assert extra_print_charge("5x7", 25, "matte", True) == 20


def test_member_no_bonus_on_8x10():
    # is_member True but size == 8x10 -> included stays 10 -> 5 extra * 4
    assert extra_print_charge("8x10", 15, "matte", True) == 20


def test_non_member_no_bonus():
    # not a member -> included 20 -> 10 extra * 4
    assert extra_print_charge("4x6", 30, "matte", False) == 40


# ---------------- extra <= 0 boundary ----------------
def test_extra_exactly_zero():
    assert extra_print_charge("4x6", 20, "matte", False) == 0


def test_extra_exactly_one():
    assert extra_print_charge("4x6", 21, "matte", False) == 4


# ---------------- finish branch ----------------
def test_matte_rate():
    assert extra_print_charge("4x6", 30, "matte", False) == 40


def test_glossy_rate():
    assert extra_print_charge("5x7", 25, "glossy", False) == 70


def test_canvas_rate_without_bulk():
    # canvas but extra <= 50 -> plain rate 7
    assert extra_print_charge("4x6", 30, "canvas", False) == 70


# ---------------- bulk (extra > 50) branch ----------------
def test_bulk_boundary_50_extra_not_surcharged():
    # extra == 50 -> no surcharge, matte rate 4
    assert extra_print_charge("4x6", 70, "matte", False) == 200


def test_bulk_boundary_51_extra_surcharged():
    # extra == 51 -> rate 4 + 2 = 6
    assert extra_print_charge("4x6", 71, "matte", False) == 306


def test_bulk_glossy_surcharge():
    # extra 60 -> rate 7 + 2 = 9
    assert extra_print_charge("4x6", 80, "glossy", False) == 540


def test_bulk_canvas_surcharge():
    # extra 60 -> rate 7 + 2 + 5 = 14
    assert extra_print_charge("4x6", 80, "canvas", False) == 840


# ---------------- order_valid ----------------
def test_order_valid():
    assert order_valid(10, 100, False) is True


def test_rush_at_limit():
    assert order_valid(10, 50, True) is True


def test_rush_over_limit():
    assert order_valid(10, 51, True) is False


def test_rush_ignores_file_size():
    # rush path returns before the file-size check
    assert order_valid(100, 10, True) is True


def test_file_at_limit_valid():
    assert order_valid(25, 10, False) is True


def test_file_over_limit_invalid():
    assert order_valid(25.1, 10, False) is False


def test_copies_at_limit_valid():
    assert order_valid(10, 500, False) is True


def test_copies_over_limit_invalid():
    assert order_valid(10, 501, False) is False


# ---------------- dispatch_status ----------------
@pytest.mark.parametrize(
    "hours, framed, intl, expected",
    [
        # domestic, unframed -> cutoff 12
        (12, False, False, "on_time"),
        (11, False, False, "tight"),
        (6, False, False, "tight"),
        (5, False, False, "missed"),
        # domestic, framed -> cutoff 24
        (24, True, False, "on_time"),
        (23, True, False, "tight"),
        (18, True, False, "tight"),
        (17, True, False, "missed"),
        # international, unframed -> cutoff 36
        (36, False, True, "on_time"),
        (30, False, True, "tight"),
        (29, False, True, "missed"),
        # international, framed -> cutoff 48
        (48, True, True, "on_time"),
        (42, True, True, "tight"),
        (41, True, True, "missed"),
    ],
)
def test_dispatch_status(hours, framed, intl, expected):
    assert dispatch_status(hours, framed, intl) == expected
