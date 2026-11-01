# D2C Support Agent (Local Ollama)

A small, original portfolio project that demonstrates a grounded customer-support agent for a fictional D2C shop. It uses **Qwen 2.5 7B through Ollama**, a local catalogue/policy retriever, allowlisted tool calls, mock order lookup, and human handoff for sensitive or uncertain requests.

This repository is independent of any employer or internship project. All shop, customer, and order data are fictional. The order tool is read-only; no real purchases, refunds, or customer messages are performed.

The design applies concepts from agentic-AI study materials (tool calling, routing, human review, and evaluation); the implementation and demo data here are original.

## What it demonstrates

- Local LLM integration through Ollama's `/api/chat` API with tool calling.
- Retrieval grounding for product and policy questions using a transparent token-overlap ranker.
- An allowlisted tool loop with validated inputs, bounded iterations, and explicit tool results.
- A mock order-status tool and a human-handoff tool; refund/cancellation requests are escalated rather than executed.
- A small evaluation harness for expected tool use, escalation behavior, and answer signals.
- Per-turn latency and local prompt/completion token counts (token counts are not a dollar-cost estimate).
- FastAPI endpoints and structured request/response models.

## Architecture

```text
Client -> FastAPI /chat -> Ollama (Qwen 2.5 7B)
                         | tool call (allowlist only)
                         +-> search_catalog -> local products + policy docs
                         +-> get_order_status -> fictional read-only orders
                         +-> create_handoff -> local demo acknowledgement
```

The model may request a tool, but Python validates the tool name and arguments and executes only the three functions defined in `app/tools.py`. Retrieved catalogue and policy text is treated as untrusted data, not instructions. The model is told to answer only from tool evidence and to hand off when evidence is missing.

## Requirements

- Python 3.10+
- [Ollama](https://ollama.com/) running locally
- Qwen 2.5 7B model (for example, `qwen2.5:7b`)

## Run locally

```powershell
ollama pull qwen2.5:7b
ollama serve
```

In another terminal, from this project directory:

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000/docs` for the interactive API. `GET /health` checks whether the configured Ollama model is reachable. Set `OLLAMA_MODEL` or `OLLAMA_URL` if your local Ollama configuration differs.

Example request:

```json
{
  "message": "Is the Trail Bottle insulated?",
  "session_id": "demo-session"
}
```

Example order request (fictional IDs only):

```json
{
  "message": "Where is order ORD-1002?",
  "session_id": "demo-session"
}
```

## Run the evaluation harness

With Ollama running and the model available:

```powershell
python -m evals.run_evals
```

The harness prints per-case checks, latency, token counts, and aggregate pass rate. Cases live in `evals/cases.json` and cover product grounding, order lookup, unknown and missing IDs, deterministic refund escalation, a forbidden-tool check, and one Hinglish query. The checks are intentionally small and transparent; they are not a claim of production readiness or a substitute for human review. Expand with tool timeout simulations, prompt injection in retrieved records, ambiguous policies, and more reviewed Hinglish variants before deployment.

### Local evaluation run

Run on 2026-11-01 with `qwen2.5:7b` through local Ollama: **7/7 cases passed (100%)**. In the initial run, the first catalogue case took 56.1 seconds while the model loaded. In the final run, model-backed cases took 1.2–4.5 seconds, and deterministic refund escalations took under 1 ms. Ollama-reported prompt/completion token counts are included per response; they are not a dollar-cost estimate. These seven hand-written checks are a smoke-sized sample, not a quality guarantee. Re-run after changing the model, prompt, retrieval, or tools; report failures as well as passes.

## Design choices and production gaps

- Order data and policies are mock fixtures, not a live store integration.
- Retrieval uses lexical token overlap so the ranking behavior is easy to inspect and requires no embedding service. A production system should compare it with embedding retrieval and evaluate retrieval recall on representative queries.
- Refunds, cancellations, and address changes always require a human. No mutating commerce tools are exposed.
- The API does not persist conversations. Add authenticated identity, tenant isolation, privacy controls, rate limits, and secure session storage before handling real customers.
- Add production observability for tool success, groundedness, escalation rate, latency, and token/cost metrics. Avoid logging personal or payment data.
- Evaluate with a larger, reviewed dataset and adversarial cases before any customer-facing release.

## API

- `POST /chat`: run one support turn.
- `GET /health`: service and Ollama connectivity.

## License

MIT. See [LICENSE](LICENSE).
