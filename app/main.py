from fastapi import FastAPI

from app.core.logging import setup_logging
from app.api.v1.lots import router as lots_router
from app.api.v1.vehicles import router as vehicles_router
from app.api.v1.accesses import router as accesses_router


setup_logging()
app = FastAPI(title="Estacionamento API")

# Routers v1
app.include_router(lots_router)
app.include_router(vehicles_router)
app.include_router(accesses_router)


@app.get("/health")
def health():
    return {"status": "ok"}
