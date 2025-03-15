from fastapi import FastAPI
from .routes import subsystems
import uvicorn

app = FastAPI(
    title="SIN Dashboard API",
)

app.include_router(subsystems.router, prefix="/subsistemas", tags=["Subsistemas"])
