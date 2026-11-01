from typing import Any

from app.data import ORDERS
from app.retrieval import search_catalog


def get_order_status(order_id: str) -> dict[str, Any]:
    """Read status from fictional local fixtures; unknown IDs reveal no data."""
    normalized = order_id.strip().upper()
    if normalized not in ORDERS:
        return {"found": False, "message": "No demo order matched that ID."}
    return {"found": True, "order_id": normalized, **ORDERS[normalized]}


def create_handoff(reason: str) -> dict[str, Any]:
    """Return a handoff acknowledgement; this demo sends no external message."""
    safe_reason = " ".join(reason.split())[:240] or "Customer needs support"
    return {"created": True, "reference": "HANDOFF-DEMO", "reason": safe_reason}


TOOL_FUNCTIONS = {
    "search_catalog": search_catalog,
    "get_order_status": get_order_status,
    "create_handoff": create_handoff,
}

TOOL_SCHEMAS = [
    {
        "type": "function",
        "function": {
            "name": "search_catalog",
            "description": "Search fictional product and policy records. Use for product details, shipping, or return-policy questions.",
            "parameters": {"type": "object", "properties": {"query": {"type": "string", "description": "Short query describing the product or policy information needed"}}, "required": ["query"]},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_order_status",
            "description": "Look up a fictional demo order by ID. Read-only. Never guess an order ID.",
            "parameters": {"type": "object", "properties": {"order_id": {"type": "string", "description": "Order ID supplied by the customer, such as ORD-1001"}}, "required": ["order_id"]},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "create_handoff",
            "description": "Escalate a refund, cancellation, complaint, unsafe/uncertain answer, or request that needs a human. This only creates a local demo acknowledgement.",
            "parameters": {"type": "object", "properties": {"reason": {"type": "string", "description": "Brief explanation for the human support agent"}}, "required": ["reason"]},
        },
    },
]


def execute_tool(name: str, arguments: dict[str, Any]) -> dict[str, Any]:
    """Validate tool calls against a strict allowlist before execution."""
    if name not in TOOL_FUNCTIONS:
        raise ValueError(f"Tool is not allowed: {name}")
    if not isinstance(arguments, dict):
        raise ValueError("Tool arguments must be an object")
    if name == "search_catalog":
        query = arguments.get("query")
        if not isinstance(query, str) or not query.strip() or len(query) > 300:
            raise ValueError("query must be a non-empty string up to 300 characters")
        return {"results": search_catalog(query)}
    if name == "get_order_status":
        order_id = arguments.get("order_id")
        if not isinstance(order_id, str) or len(order_id) > 40:
            raise ValueError("order_id must be a string up to 40 characters")
        return get_order_status(order_id)
    reason = arguments.get("reason")
    if not isinstance(reason, str) or not reason.strip():
        raise ValueError("reason must be a non-empty string")
    return create_handoff(reason)
