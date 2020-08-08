from .calculator.calculator import check_query, solve_query, clean_query
from fastapi import FastAPI, Response, status
from base64 import b64decode, b64encode
from binascii import Error

app = FastAPI()

@app.get("/")
async def root():
    return "HELOO"

@app.get("/calculus")
async def calculate(query: str, response: Response):
    query_in = query
    try:
        query = b64decode(query).decode("utf-8")
    except Error as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": f"Unable to decode the string {query}", "error": True}
    except UnicodeDecodeError as ue:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": f"{query} failed to be valid UTF-8"}
    query = await clean_query(query)
    valid = await check_query(query)
    if not valid:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {
            "error": True,
            "message": f"Invalid input string {query_in} - decoded to {query}",
        }

    result = await solve_query(query)
    response.status_code = 200
    return {"result": result}


if __name__ == "__main__":
    pass
