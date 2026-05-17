# TridenGuard — Architecture

## Overview

TridenGuard is a deterministic firewall enforcing Zero Trust for LLM outputs in legal and financial documents. It enforces a neuro-symbolic schema using 8 orthogonal atomic radicals and a human-in-the-loop quarantine system.

## Pipeline
User Input → n8n Webhook → Lobster Trap DPI → Information Extractor (Phi-4-mini)
→ Deterministic Validator (8 Rules)
→ Audit Table / Quarantine Table
→ Human Review Panel (Approve/Discard)

## Layers

| Layer | Technology | Function |
|:--|:--|:--|
| **Ingress Security** | Lobster Trap (Go, Veea) | Deep Prompt Inspection. Blocks injection, PII, exfiltration, malware. 12 ingress rules + 2 egress rules. |
| **Extraction** | Ollama + Phi-4-mini (3.8B) | Local LLM. Extracts 8 atomic radicals with GBNF-enforced schema. Temperature=0. No cloud. |
| **Validation** | Custom JS (n8n Code Node) | Deterministic. 8 orthogonal rules. No ML in the validator. Rejection with `rejection_reason` tagging. |
| **Persistence** | n8n Data Tables | Audit (validated) and Quarantine (rejected) tables. Append-only. |
| **Observability** | JSONL + TOON | Structured logging with `pipeline_stage`, `rule_id`, and `reason_code`. 40-60% size reduction via TOON. |
| **Human Review** | Panel HTML + n8n Webhooks | Approve/Discard. Real-time stats. Connected to `/webhook/approve` and `/webhook/discard`. |

## The 8 Atomic Rules

| Rule | Name | Condition |
|:--|:--|:--|
| R1 | Sujeto sin Acción | Actor/Deontic present, Action missing |
| R2 | Acción sin Sujeto | Action present, Actor missing |
| R3 | Objeto sin Referente | Object present, Actor and Action missing |
| R4 | Métrica Huérfana | Metric present, Actor and Object missing |
| R5 | Condición sin Gatillo | Condition present, Action missing |
| R6 | Temporal sin Anclaje | Temporal present, Actor and Action missing |
| R7 | Espacial Inerte | Spatial present, Actor and Action missing |
| R8 | Deóntico sin Conducta | Deontic present, Action missing |

## Roadmap

- **V1 (MVP):** Structural firewall. 100% local. REST API, DPI, 8 rules, Data Tables.
- **V2:** Observability (JSONL + TOON). Quarantine engine with Lobster Trap classification.
- **V3:** Local fine-tuning flywheel. Pydantic + GBNF + LoRA on Gemma 4 E2B. Sovereign AI.