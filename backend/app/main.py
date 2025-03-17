from fastapi import FastAPI

from .routes import subsystems, production_statements, costs

app = FastAPI(title="SIN Dashboard API")

app.include_router(subsystems.router, prefix="/subsistemas", tags=["Subsistemas"])
app.include_router(
    production_statements.router, prefix="/balanco-energia", tags=["Balanço de Energia"]
)
app.include_router(costs.router, prefix="/cmo", tags=["Custo Marginal de Operação"])
