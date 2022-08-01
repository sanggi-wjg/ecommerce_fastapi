import logging

import uvicorn as uvicorn
from fastapi import FastAPI

from app.core.config import get_settings
from app.database.database import Base, Engine
from app.exception.exceptions import bad_credential_handler, BadCredential
from app.router import user, auth

settings = get_settings()


def create_app():
    app = FastAPI(
        debug=settings.debug,
    )

    Base.metadata.create_all(bind=Engine)
    logging.basicConfig()
    logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

    # exception
    app.add_exception_handler(BadCredential, bad_credential_handler)

    # router
    app.include_router(user.router)
    app.include_router(auth.router)
    return app


app = create_app()

if __name__ == '__main__':
    uvicorn.run(
        "main:app",
        port=settings.port,
        reload=settings.reload
    )
