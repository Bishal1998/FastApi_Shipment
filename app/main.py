from contextlib import asynccontextmanager

from fastapi import FastAPI
from scalar_fastapi import get_scalar_api_reference

from app.api.router import router

from .database.session import create_db_and_tables


@asynccontextmanager
async def lifespan_handler(app: FastAPI):
   await create_db_and_tables()
   yield

app = FastAPI(lifespan=lifespan_handler)

app.include_router(router)

@app.get("/")
def get_root():
    return {"message": "Hello, World!"}

@app.get("/scalar", include_in_schema=False)
def get_scalar_docs():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title="Scalar API",
        #  this here
        servers=[
            {
                "url": "http://localhost:8000",
                "description": "Local server",
            },
        ]
    )