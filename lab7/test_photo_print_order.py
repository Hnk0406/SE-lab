import math

from hypothesis import given, strategies as st
from photo_print_order import parse_order, file_size_average, payable_amount


@given(st.text() | st.none())
def test_parse_order_no_crash(s):
    try:
        parse_order(s)
    except Exception as e:
        assert False, f"parse_order crashed with: {e!r} for input {s!r}"


@given(st.text() | st.none())
def test_file_size_average_no_crash(s):
    try:
        file_size_average(s)
    except Exception as e:
        assert False, f"file_size_average crashed with: {e!r} for input {s!r}"


@given(st.text() | st.none())
def test_payable_amount_no_crash(s):
    try:
        payable_amount(s)
    except Exception as e:
        assert False, f"payable_amount crashed with: {e!r} for input {s!r}"


# ---- Extra property checks: the output must also be sensible ----

@given(st.text() | st.none())
def test_parse_order_output_shape(s):
    result = parse_order(s)
    assert result is None or (
        isinstance(result, tuple)
        and isinstance(result[0], str)
        and isinstance(result[1], int)
        and result[1] > 0
    )


@given(st.text() | st.none())
def test_file_size_average_output_is_non_negative_number(s):
    result = file_size_average(s)
    assert isinstance(result, (int, float)) and result >= 0


@given(st.text() | st.none())
def test_payable_amount_is_finite_and_non_negative(s):
    result = payable_amount(s)
    assert isinstance(result, (int, float))
    assert math.isfinite(result) and result >= 0


# ---- Valid inputs must still work after hardening ----

@given(st.integers(1, 10**6), st.integers(1, 10**6))
def test_parse_order_valid(w, c):
    assert parse_order(f"{w}x6:{c}") == (f"{w}X6", c)


@given(st.lists(st.integers(0, 10**6), min_size=1, max_size=50))
def test_file_size_average_valid(values):
    csv = ",".join(map(str, values))
    assert file_size_average(csv) == sum(values) // len(values)


@given(st.integers(0, 10**6), st.integers(0, 10**6))
def test_payable_amount_valid(amount, discount):
    expected = max(amount * 1.18 - discount, 0)
    assert math.isclose(payable_amount(f"{amount}|{discount}"), expected)