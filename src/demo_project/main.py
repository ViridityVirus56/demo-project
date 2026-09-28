"""Main API application entrypoint with webhooks support."""

from fastapi import FastAPI
from demo_project.orders import router as orders_router
from demo_project.webhooks import router as webhooks_router

app = FastAPI(title="Demo Payment Service")
app.include_router(orders_router, prefix="/api/v1")
app.include_router(webhooks_router, prefix="/api/v1")


@app.get("/health")
def health():
    return {"status": "healthy"}
