from fastapi.responses import HTMLResponse
from fastapi import Request
from starlette.exceptions import HTTPException as StarletteHTTPException


HTML_404_PAGE = "<h1>PAGE NOT FOUND</h1> <a href=https://futurice.diarmaiddeburca.com/docs>Did you mean to go here?</a>"


async def four_oh_four_not_found(request: Request, exc: StarletteHTTPException):
    return HTMLResponse(content=HTML_404_PAGE, status_code=exc.status_code)
