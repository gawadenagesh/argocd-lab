import logging

from fastapi import FastAPI
from pydantic import BaseModel

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("argocd-lab")

app = FastAPI(title="argocd-lab")


class HealthResponse(BaseModel):
    status: str
    version: str


@app.get("/", response_model=HealthResponse)
def read_root() -> HealthResponse:
    logger.info("root endpoint called")
    return HealthResponse(status="ok", version="2.0.0")


@app.get("/health", response_model=HealthResponse)
def health_check() -> HealthResponse:
    return HealthResponse(status="ok", version="2.0.0")
