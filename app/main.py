from .calculator.calculator import check_query, solve_query, clean_query
from fastapi import FastAPI, Response, status
from fastapi.responses import JSONResponse
from base64 import b64decode
from binascii import Error
from pydantic import BaseModel

app = FastAPI()


class Result(BaseModel):
    result: float
    error: bool


class ErrorResponse(BaseModel):
    message: str
    error: bool


@app.get("/calculus", response_model=Result, responses={400: {"model": ErrorResponse}})
async def calculate(query: str):
    query_in = query
    try:
        query = b64decode(query).decode("utf-8")
    except Error as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": f"Unable to decode the string {query}", "error": True},
        )
    except UnicodeDecodeError as ue:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": f"{query} failed to be valid UTF-8", "error": True},
        )
    query = await clean_query(query)
    valid = await check_query(query)
    if not valid:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "message": f"Invalid input string {query_in} - decoded to {query}",
                "error": True,
            },
        )

    result = await solve_query(query)
    return {"result": result, "error": False}
