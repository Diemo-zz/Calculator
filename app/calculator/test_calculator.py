import unittest
from .calculator import (check_query, solve_query, split_query, clean_query, solve_bracketed_sub_equations,
                         solve_plus_minus, solve_multiplication_and_division)
import pytest


@pytest.mark.asyncio
async def test_solve_query_with_implicit_multiplication_of_two_bracketed_equations():
    query = "1+(2+1)(6)"
    res = await solve_query(query)
    assert 19.0 - res < 1e-7


@pytest.mark.asyncio
async def test_solve_bracked_subequations_single_bracket():
    query = "1+(1+1+1)+1"
    new_query = await solve_bracketed_sub_equations(query)
    expected = "1+3.0+1"
    assert expected == new_query


@pytest.mark.asyncio
async def test_solve_bracked_subequations_nested_brackets():
    query = "1+(1+1(1+1))+1"
    new_query = await solve_bracketed_sub_equations(query)
    expected = "1+3.0+1"
    assert expected == new_query


@pytest.mark.asyncio
async def test_solve_multiplication_and_division_with_single_multiply():
    query = "10*5+3"
    expected_result = "50.0+3"
    result = await solve_multiplication_and_division(query)
    assert expected_result == result


@pytest.mark.asyncio
async def test_multiplication_and_division_for_single_division():
    query = "10/2 +1"
    expected_result = "5.0+1"
    result = await solve_multiplication_and_division(query)
    assert expected_result == result

@pytest.mark.asyncio
async def test_plus_minus_with_only_plus():
    query = "2 + 3 + 4"
    expected_result = 9.0
    result = await solve_plus_minus(query)
    assert expected_result == result


@pytest.mark.asyncio
async def test_valid_query_with_plus():
    query = "1+2"
    val = await check_query(query)
    assert val is True


@pytest.mark.asyncio
async def test_valid_query_with_minus():
    query = "1 - 2"
    res = await check_query(query)
    assert res is True


@pytest.mark.asyncio
async def test_valid_query_with_multiply():
    query = "1 * 2"
    res = await check_query(query)
    assert res is True


@pytest.mark.asyncio
async def test_valid_query_with_divide():
    query = "1 / 2"
    res = await check_query(query)
    assert res is True


@pytest.mark.asyncio
async def test_valid_query_with_multiple():
    query = "1 +2 - 3 * 4 / 5"
    res = await check_query(query)
    assert res is True


@pytest.mark.asyncio
async def test_valid_query_with_brackets():
    query = "1 + (2 + 3 )"
    res = await check_query(query)
    assert res is True


@pytest.mark.asyncio
async def test_invalid_query_bad_values():
    query = "a + b"
    res = await check_query(query)
    assert res is False


@pytest.mark.asyncio
async def test_invalid_query_repeated_operators():
    query = "a ++ b"
    res = await check_query(query)
    assert res is False


@pytest.mark.asyncio
async def test_invalid_query_bad_brackets():
    query = "1 ( 1*1 ) + 2"
    res = await check_query(query)
    assert res is False


@pytest.mark.asyncio
async def test_invalid_query_bad_bracket_numbers():
    query = "1 + (4 + 5"
    res = await check_query(query)
    assert res is False


@pytest.mark.asyncio
async def test_valid_complicated_query():
    query = "1 + (1 + (1 + 2 + (5/6) + (12*32) - 7) +22)"
    res = await check_query(query)
    assert res is True


@pytest.mark.asyncio
async def test_solve_query_with_plus():
    query = "1 + 2"
    res = await solve_query(query)
    assert 3.0 == res


@pytest.mark.asyncio
async def test_solve_with_nested_brackets():
    query = "1 + (1 + 1 * 12 +(1 + 1) +1) + 12"
    res = await solve_query(query)
    assert 29.0 == res


@pytest.mark.asyncio
async def test_clean():
    query = "1(1 + 1)"
    res = await clean_query(query)
    assert "1*(1+1)" == res


@pytest.mark.asyncio
async def test_split_query():
    query = "1+(1+2)"
    expected = ["1+", "(1+2)"]
    res = await split_query(query)
    for e, gotten in zip(expected, res):
        assert e == gotten


@pytest.mark.asyncio
async def test_solve_without_brackets():
    query = "1 * 12 + 12"
    res = await solve_query(query)
    assert 24 == res


@pytest.mark.asyncio
async def test_solve_with_brackets():
    query = "2 * (12 + 12) + 10"
    res = await solve_query(query)
    assert 58 == res


@pytest.mark.asyncio
async def test_check_query_with_query():
    query = "2 * (23/(3*3))- 23 * (2*3)"
    res = await check_query(query)
    assert res is True


@pytest.mark.asyncio
async def test_check_query_with_nested_parenthesis_and_parenthesis_by_bracket():
    query = "2 * (23/(3*3))- 23 * (2*3)"
    res = await solve_query(query)
    assert abs(-132.888888888 - res) < 1e-6
    query = "15/6*(12+65/33+100 / (100*12/4+32*(33+1)))"
    res = await solve_query(query)
    assert abs(35.104357698 - res) < 1e-7


@pytest.mark.asyncio
async def test_check_query_with_dot():
    query = "4.5+2.3"
    res = await check_query(query)
    assert res is True


@pytest.mark.asyncio
async def test_check_query_with_bad_periods():
    query = "4.5.6 +2"
    res = await check_query(query)
    assert res is False


if __name__ == "__main__":
    unittest.main()
