"""Fictional public demo data. No real customer or company information."""

PRODUCTS = [
    {
        "id": "BOT-001",
        "name": "Trail Bottle",
        "price_inr": 899,
        "description": "750 ml stainless steel bottle with double-wall insulation. Keeps drinks cold for up to 18 hours.",
        "materials": "Food-grade stainless steel; BPA-free lid",
        "colors": ["forest green", "sand", "navy"],
    },
    {
        "id": "BAG-002",
        "name": "Everyday Tote",
        "price_inr": 649,
        "description": "Reusable 12 L cotton canvas tote with an inside pocket. Suitable for daily errands.",
        "materials": "100% cotton canvas",
        "colors": ["natural", "black"],
    },
    {
        "id": "MUG-003",
        "name": "Desk Mug",
        "price_inr": 549,
        "description": "350 ml ceramic mug. Microwave-safe; hand washing is recommended.",
        "materials": "Glazed ceramic",
        "colors": ["cream", "terracotta"],
    },
]

POLICIES = [
    {
        "id": "POL-RETURNS",
        "title": "Returns",
        "text": "Unused items in original packaging may be requested for return within 7 days of delivery. A support agent must review eligibility and arrange the return.",
    },
    {
        "id": "POL-SHIPPING",
        "title": "Shipping",
        "text": "Orders usually dispatch within 1 to 2 business days. Delivery estimates depend on destination and are shown by the carrier after dispatch.",
    },
]

# Intentionally fictional fixtures for local demonstration only.
ORDERS = {
    "ORD-1001": {"status": "In transit", "carrier": "DemoShip", "estimated_delivery": "2026-11-05"},
    "ORD-1002": {"status": "Delivered", "carrier": "DemoShip", "estimated_delivery": "2026-10-29"},
}
