from fastapi import FastAPI

from app.api.v1.endpoints.items.item_route import router as item_router
from app.api.v1.endpoints.auth_route import router as auth_router

app = FastAPI(
    title="FastAPI PostgreSQL App",
    version="1.0"
)

app.include_router(auth_router)
app.include_router(item_router)