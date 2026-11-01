import re
from collections import Counter
from typing import Any

from app.data import POLICIES, PRODUCTS

STOP_WORDS = {"a", "an", "and", "are", "can", "do", "does", "for", "how", "i", "is", "it", "me", "my", "of", "on", "or", "the", "to", "what", "where", "with"}


def _tokens(text: str) -> list[str]:
    return [token for token in re.findall(r"[a-z0-9]+", text.lower()) if token not in STOP_WORDS]


def _score(query: list[str], document: str) -> int:
    counts = Counter(_tokens(document))
    return sum(min(counts[token], 2) for token in set(query))


def search_catalog(query: str, limit: int = 4) -> list[dict[str, Any]]:
    """Retrieve the most relevant fictional product or policy records."""
    terms = _tokens(query)
    docs: list[tuple[int, dict[str, Any]]] = []
    for product in PRODUCTS:
        score = _score(terms, " ".join(str(v) for v in product.values()))
        docs.append((score, {"type": "product", **product}))
    for policy in POLICIES:
        score = _score(terms, " ".join(str(v) for v in policy.values()))
        docs.append((score, {"type": "policy", **policy}))
    docs.sort(key=lambda item: item[0], reverse=True)
    return [doc for score, doc in docs[:limit] if score > 0]
