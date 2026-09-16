"""Unit tests for orders."""

from demo_project.orders import create_order, OrderCreate, orders_db


def test_create_order():
    orders_db.clear()
    order = create_order(OrderCreate(item_id="item_1", amount=99.99))
    assert order["id"] == "ord_1"
    assert order["amount"] == 99.99
    assert order["status"] == "pending"
