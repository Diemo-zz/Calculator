from calculator.calculator import check_query, solve_query
from fastapi import FastAPI
from base64 import b64decode, encode
from binascii import Error

app = FastAPI()

@app.get("/")
async def root():
    return "HELOO"

@app.get("/calculus")
async def calculate(query: str):
    try:
        query = b64decode(query).decode("utf-8")
    except Error as e:
        return {"message": f"Unable to decode the string {query}, {type(query)}", "error": True, "e": e}, 400
    valid = check_query(query)
    if not valid:
        return {"error": True, "message": f"Invalid input string {query}, {type(query)}"}, 400
    result = solve_query(query)
    return {"result": result}, 200


if __name__ == "__main__":
    pass