import unittest
from .calculator import check_query, solve_query, split_query


class MyTestCase(unittest.TestCase):
    def test_valid_query_with_plus(self):
        query = "1+2"
        self.assertTrue(check_query(query))

    def test_valid_query_with_minus(self):
        query = "1 - 2"
        self.assertTrue(check_query(query))

    def test_valid_query_with_multiply(self):
        query = "1 * 2"
        self.assertTrue(check_query(query))

    def test_valid_query_with_divide(self):
        query = "1 / 2"
        self.assertTrue(check_query(query))

    def test_valid_query_with_multiple(self):
        query = "1 +2 - 3 * 4 / 5"
        self.assertTrue(check_query(query))

    def test_valid_query_with_brackets(self):
        query = "1 + (2 + 3 )"
        self.assertTrue(query)

    def test_invalid_query_bad_values(self):
        query = "a + b"
        self.assertFalse(check_query(query))

    def test_invalid_query_repeated_operators(self):
        query = "a ++ b"
        self.assertFalse(check_query(query))

    def test_invalid_query_bad_brackets(self):
        query = "1 ( 1*1 ) + 2"
        self.assertFalse(check_query(query))

    def test_invalid_query_bad_bracket_numbers(self):
        query = "1 + (4 + 5"
        self.assertFalse(check_query(query))

    def test_valid_complicated_query(self):
        query = "1 + (1 + (1 + 2 + (5/6) + (12*32) - 7) +22)"
        self.assertTrue(check_query(query))

    def test_solve_query_with_plus(self):
        query = "1 + 2"
        print(solve_query(query))
        self.assertEqual(3.0, solve_query(query))

    def test_solve_with_nested_brackets(self):
        query = "1 + (1 + 1 * 12 +(1 + 1) +1) + 12"
        self.assertEqual(29.0, solve_query(query))

    def test_split_query(self):
        query = "1 + (1 + 2)"
        expected = ["1+", "(1+2)"]
        self.assertListEqual(expected, split_query(query))

    def test_solve_without_brackets(self):
        query = "1 * 12 + 12"
        self.assertEqual(24, solve_query(query))

    def test_solve_with_brackets(self):
        query = "2 * (12 + 12) + 10"
        self.assertEqual(58, solve_query(query))

    def test_check_query_with_query(self):
        query = "2 * (23/(3*3))- 23 * (2*3)"
        self.assertTrue(check_query(query))

    def test_check_query_with_nested_parenthesis_and_parenthesis_by_bracket(self):
        query = "2 * (23/(3*3))- 23 * (2*3)"
        self.assertAlmostEqual(-132.888888888, solve_query(query), 6)
        query = "15/6*(12+65/33+100 / (100*12/4+32*(33+1)))"
        self.assertAlmostEqual(35.104357698, solve_query(query), 7)


if __name__ == "__main__":
    unittest.main()
