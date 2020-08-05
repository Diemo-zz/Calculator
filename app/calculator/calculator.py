import operator
from typing import List

operators = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.truediv,
}


def check_query(query_in: str) -> bool:
    """
    Validates the query string to ensure that a result can be found

    Calculator rules are as follows:
    Strip out all whitespace
    If at a number, you are allowed a number, a operator or a bracket
    If you are at a bracket or operator, you are allowed a number only
    The number of opening brackets and closing brackets have to be the same
    The only allowed characters are + - * / ( ) 1 2 3 4 5 6 7 8 9 0

    :param query_in: The query to evaluate
    :return: True/False
    """
    allowed_operators = set(operators.keys())
    query_in = "".join(query_in.split())
    previous_value = "+"  # You can always consider an equation x as 0 + x. As such, we always start on a +
    number_opening_brackets = 0
    number_closing_brackets = 0
    for character in query_in:
        if character.isdigit():  # digits can follow anything
            if previous_value == ")":
                return False  # We don't support bracket notation
        elif character == "(":  # Brackets can only come after an operator
            number_opening_brackets += 1
            if previous_value not in allowed_operators:
                return False
        elif character == ")":
            number_closing_brackets += 1
            if not (previous_value.isdigit() or previous_value == ")"):
                return False
        elif character in allowed_operators:
            if not (previous_value.isdigit() or previous_value in ["(", ")"]):
                return False
        else:
            return False
        previous_value = character
    return number_opening_brackets == number_closing_brackets


def split_query(query_in: str) -> List[str]:
    query_in = "".join(query_in.split())
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
    if current:
        split.append(current)
    split = [s for s in split if s]
    return split


def solve_query(query_in: str) -> float:
    """
    Takes a query and solves it

    Assumes that the query is valid. Solves as follows:
    1) Get all of the brackets and solve
    2) Solve the resulting string

    :param query_in: The query in
    :return: The solved number
    """
    query_in = "".join(query_in.split())
    query_in = query_in.lstrip("(").rstrip(")")
    res2 = split_query(query_in)
    new_r = []
    for r in res2:
        if r[0] == "(":
            value = str(solve_query(r))
        else:
            value = r
        new_r.append(value)
    res3 = "".join(new_r)
    res3 = (
        res3.replace("+", " + ")
        .replace("-", " - ")
        .replace("*", " * ")
        .replace("/", " / ")
    )
    res4 = res3.split()
    res5 = []
    previous_value = "+"
    for value in res4:
        if previous_value in ["*", "/"]:
            previous_number = res5.pop()
            new_number = operators.get(previous_value)(
                float(previous_number), float(value)
            )
            res5.append(new_number)
        elif value not in ["*", "/"]:
            res5.append(value)
        previous_value = value

    res_iter = iter(res5)
    initial_value = next(res_iter)
    while True:
        try:
            operator = next(res_iter)
            second_value = next(res_iter)
            initial_value = operators.get(operator)(
                float(initial_value), float(second_value)
            )
        except StopIteration:
            break
    return initial_value
