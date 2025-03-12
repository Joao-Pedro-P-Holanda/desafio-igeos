from fastapi import FastAPI
from .routes import auth, subsystems
import uvicorn

app = FastAPI(
    title="SIN Dashboard API",
)


app.include_router(auth.router, tags=["Autenticação"])
app.include_router(subsystems.router, prefix="/subsistemas", tags=["Subsistemas"])
