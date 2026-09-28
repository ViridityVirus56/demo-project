"""Order processing endpoints and state management."""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

orders_db = {}


class OrderCreate(BaseModel):
    item_id: str
    amount: float
    currency: str = "USD"


@router.post("/orders")
def create_order(order: OrderCreate):
    order_id = f"ord_{len(orders_db) + 1}"
    orders_db[order_id] = {
        "id": order_id,
        "item_id": order.item_id,
        "amount": order.amount,
        "status": "pending",
    }
    return orders_db[order_id]


@router.get("/orders/{order_id}")
def get_order(order_id: str):
    if order_id not in orders_db:
        raise HTTPException(status_code=404, detail="Order not found")
    return orders_db[order_id]
