# 🛡️ TridenGuard

**Deterministic firewall for LLM hallucinations in legal and financial documents.**

## Problem

In 2025-2026, courts sanctioned lawyers for filing AI-hallucinated citations:
- *Lacey v. State Farm*: $31,100 sanctions
- *Russell v. Mells*: Referral to Florida Bar
- *Flycatcher v. Affable*: Default judgment

LLMs cannot distinguish contract text from malicious instructions (LegalPwn).

## Solution

TridenGuard enforces a strict schema using 6 atomic radicals:
- **Obligation** | **Metric** | **Contingency** | **Risk** | **Asset** | **Exception**

If the LLM hallucinates or fails schema validation, the vector goes to QUARANTINE for human review.

## Architecture
Telegram → Lobster Trap (DPI) → n8n → Ollama/Gemini → Cartesian Validator (Set()) → AND Gate
↓ ↓
Quarantine ←─────────────────────── Block

## Tech Stack

- n8n (orchestration)
- Lobster Trap (prompt inspection)
- Ollama + Phi-4-mini (local inference)
- Telegram (human-in-the-loop)
- Google Sheets (audit trail)

## Roadmap

- **V1 (MVP)**: n8n + Lobster Trap (current)
- **V2**: LangGraph for parallel execution
- **V3**: ADK for native observability

## Demo

[Link to video]

## Repository Structure
├── n8n-workflow/
│ └── triden_guard_v1.json
├── docs/
│ └── cases.md (real court cases)
└── README.md

## License

MIT
