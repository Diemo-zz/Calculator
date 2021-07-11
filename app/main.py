from calculator.calculator import check_query, solve_query, clean_query
from fastapi import FastAPI, status, Request
from fastapi.responses import JSONResponse
from base64 import b64decode
from binascii import Error
from pydantic import BaseModel
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.exception_handlers import http_exception_handler
from exceptions import four_oh_four_not_found

app = FastAPI()


@app.exception_handler(StarletteHTTPException)
async def my_custom_exception_handler(request: Request, exc: StarletteHTTPException):
    if exc.status_code == 404:
        return await four_oh_four_not_found(request, exc)
    else:
        # Just use FastAPI's built-in handler for other errors
        return await http_exception_handler(request, exc)


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
    except Error:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": f"Unable to decode the string {query}", "error": True},
        )
    except UnicodeDecodeError:
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
