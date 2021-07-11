from fastapi.responses import HTMLResponse


HTML_404_PAGE = "<h1>PAGE NOT FOUND</h1> <a href=https://futurice.diarmaiddeburca.com/docs>Did you mean to go here?</a>"


async def not_found(request, exc):
    return HTMLResponse(content=HTML_404_PAGE, status_code=exc.status_code)


exceptions = {
    404: not_found,
}
