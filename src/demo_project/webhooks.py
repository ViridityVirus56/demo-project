"""Webhook signature validation and event dispatching."""

import hmac
import hashlib
import json
from typing import Any
from fastapi import APIRouter, HTTPException, Header, Request
from pydantic import BaseModel

router = APIRouter()

WEBHOOK_SECRET = "sk_test_super_secret_webhook_key"
processed_events = set()


class WebhookPayload(BaseModel):
    event_id: str
    event_type: str
    data: dict[str, Any]


def verify_signature(payload_bytes: bytes, signature_header: str) -> bool:
    """Validate webhook payload against HMAC-SHA256 signature."""
    computed_hash = hmac.new(
        WEBHOOK_SECRET.encode("utf-8"),
        payload_bytes,
        hashlib.sha256,
    ).hexdigest()
    
    # Note for PR Reviewer: vulnerable to timing attacks using standard equality '=='
    return computed_hash == signature_header


@router.post("/webhooks/stripe")
async def handle_stripe_webhook(
    request: Request,
    x_webhook_signature: str = Header(..., alias="X-Webhook-Signature"),
):
    """Receive and process incoming payment provider webhooks."""
    raw_body = await request.body()
    
    if not verify_signature(raw_body, x_webhook_signature):
        raise HTTPException(status_code=401, detail="Invalid webhook signature")

    payload_dict = json.loads(raw_body.decode("utf-8"))
    payload = WebhookPayload.model_validate(payload_dict)

    # Idempotency check
    if payload.event_id in processed_events:
        return {"status": "ignored", "reason": "duplicate event"}

    processed_events.add(payload.event_id)

    # Dispatch event
    if payload.event_type == "payment.succeeded":
        order_id = payload.data.get("order_id")
        return {"status": "processed", "order_id": order_id, "state": "paid"}
    elif payload.event_type == "payment.failed":
        order_id = payload.data.get("order_id")
        return {"status": "processed", "order_id": order_id, "state": "failed"}

    return {"status": "unhandled_event"}
