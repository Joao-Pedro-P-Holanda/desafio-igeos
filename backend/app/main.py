from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routes import subsystems, production_statements, costs

app = FastAPI(title="SIN Dashboard API")

origins = ["http://localhost:3000", "http://localhost:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(subsystems.router, prefix="/subsistemas", tags=["Subsistemas"])
app.include_router(
    production_statements.router, prefix="/balanco-energia", tags=["Balanço de Energia"]
)
app.include_router(costs.router, prefix="/cmo", tags=["Custo Marginal de Operação"])
