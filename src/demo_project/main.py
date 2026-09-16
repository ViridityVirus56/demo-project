"""Main API application entrypoint."""

from fastapi import FastAPI
from demo_project.orders import router as orders_router

app = FastAPI(title="Demo Payment Service")
app.include_router(orders_router, prefix="/api/v1")


@app.get("/health")
def health():
    return {"status": "healthy"}
