import operator
from typing import List
import re

operators = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.truediv,
}


async def check_query(query_in: str) -> bool:
    """
    Validates the query string to ensure that a result can be found

    Calculator rules are as follows:
    Strip out all whitespace
    If at a number, you are allowed a number, a operator or a bracket
    If you are at a bracket or operator, you are allowed a number only
    The number of opening brackets and closing brackets have to be the same
    The only allowed characters are + - * / ( ) 1 2 3 4 5 6 7 8 9 0 and .

    :param query_in: The query to evaluate
    :return: True/False
    """
    allowed_operators = set(operators.keys())
    query_in = "".join(query_in.split())
    previous_value = "+"  # You can always consider an equation x as 0 + x. As such, we always start on a +
    number_opening_brackets = 0
    number_closing_brackets = 0
    left_of_digital_point = False
    for character in query_in:
        if character.isdigit():
            if previous_value == ")":
                return False  # We don't support bracket notation at this point
        elif character == "(":  # Brackets can only come after an operator
            number_opening_brackets += 1
            if previous_value not in allowed_operators:
                return False
        elif character == ".":
            if left_of_digital_point or not previous_value.isdigit():
                return False
            left_of_digital_point = True
        elif character == ")":
            number_closing_brackets += 1
            if not (previous_value.isdigit() or previous_value == ")"):
                return False
        elif character in allowed_operators:
            left_of_digital_point = False
            if not (previous_value.isdigit() or previous_value in [")"]):
                return False
        else:
            return False
        previous_value = character
    return number_opening_brackets == number_closing_brackets


async def split_query(query_in: str) -> List[str]:
    """
    Takes in an input query and splits in up on brackets

    Given an equation with parentheses, we want to solve the parenthesis part of the equation first. This function will
    take in an equation in string form, and split it into brackets and non brackets -e.g.
    1 + (4*5) + (1+2) ==> ["1 + ", "(4*5)", "(1+2)"]
    :param query_in: The full equation in
    :return: A list of the equation parts
    """
    split = []
    current = ""
    inbracket = 0
    for character in query_in:
        if character == "(":
            if inbracket == 0:
                split.append(current)
                current = character
                inbracket += 1
            else:
                inbracket += 1
                current += character
        elif character == ")":
            inbracket -= 1
            if inbracket == 0:
                current += character
                split.append(current)
                current = ""
            else:
                current += character
        else:
            current += character
    if current:
        split.append(current)
    split = [s for s in split if s]
    return split


async def clean_query(query_in: str) -> str:
    """
    Takes in a query and removes whitespace, adds implicit multiplication signs
    :param query_in: string holding the mathematical equation
    :return: cleaned mathematical equation
    """
    query_in = "".join(query_in.split())
    implicit_multiplication_operators = re.findall(r"\d\(", query_in) + re.findall(
        r"\)\d", query_in
    )
    for implicit_operator in implicit_multiplication_operators:
        query_in = query_in.replace(
            implicit_operator, f"{implicit_operator[0]}*{implicit_operator[1]}"
        )
    return query_in


async def solve_query(query_in: str) -> float:
    """
    Takes in an equation and solves it

    Assumes that the euqation is valid - e.g that
    1) The only characters in the equation are parenthesises, operators, and numbers.
    2) That the equation has had any implicit multiplication signs added in

    Solves as follows:
    1) Get all of the brackets and solve each first
    2) Split the string up and iterate over, solving multiplication and division parts of the equation
    3) Iterate over the string again, solving the addition and subtraction parts

    :param query_in: The query in
    :return: The solved number
    """

    if query_in.startswith("("):
        query_in = query_in[1:-1]

    res2 = await split_query(query_in)
    new_r = []
    for r in res2:
        if r[0] == "(":
            value = str(await solve_query(r))
        else:
            value = r
        new_r.append(value)
    no_brackets_remaining = "".join(new_r)
    for operator in operators.keys():
        no_brackets_remaining = no_brackets_remaining.replace(operator, f" {operator} ")
    split_into_numbers_and_operators = no_brackets_remaining.split()
    previous_value = "+"
    solved_mult_and_div_numbers_and_operators = []
    for value in split_into_numbers_and_operators:
        if previous_value in ["*", "/"]:
            previous_number = solved_mult_and_div_numbers_and_operators.pop()
            new_number = operators.get(previous_value)(
                float(previous_number), float(value)
            )
            solved_mult_and_div_numbers_and_operators.append(new_number)
        elif value not in ["*", "/"]:
            solved_mult_and_div_numbers_and_operators.append(value)
        previous_value = value

    number_operator_iterator = iter(solved_mult_and_div_numbers_and_operators)
    initial_value = next(number_operator_iterator)
    while True:
        try:
            operator = next(number_operator_iterator)
            second_value = next(number_operator_iterator)
            initial_value = operators.get(operator)(
                float(initial_value), float(second_value)
            )
        except StopIteration:
            break
    return initial_value
