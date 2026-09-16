"""Unit tests for webhook processing and signature verification."""

import hmac
import hashlib
import json
from demo_project.webhooks import verify_signature, WEBHOOK_SECRET, WebhookPayload


def test_verify_signature():
    payload = json.dumps({"event_id": "evt_123", "event_type": "payment.succeeded", "data": {"order_id": "ord_1"}}).encode("utf-8")
    sig = hmac.new(WEBHOOK_SECRET.encode("utf-8"), payload, hashlib.sha256).hexdigest()
    
    assert verify_signature(payload, sig) is True
    assert verify_signature(payload, "invalid_signature") is False


def test_webhook_payload_validation():
    data = {
        "event_id": "evt_456",
        "event_type": "payment.failed",
        "data": {"order_id": "ord_2"},
    }
    payload = WebhookPayload.model_validate(data)
    assert payload.event_id == "evt_456"
    assert payload.event_type == "payment.failed"
