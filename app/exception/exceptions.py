from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse


class BadCredential(Exception):

    def __init__(self, message: str = "Bad credentials"):
        self.message = message


async def bad_credential_handler(request: Request, e: BadCredential):
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"detail": e.message},
        headers={"WWW-Authenticate": "Bearer"}
    )
