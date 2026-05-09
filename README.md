# 🛡️ TridenGuard

**Deterministic firewall for LLM hallucinations in legal and financial documents.**

## Problem

In 2025-2026, courts sanctioned lawyers for filing AI-hallucinated citations:
- *Lacey v. State Farm*: $31,100 sanctions
- *Russell v. Mells*: Referral to Florida Bar
- *Flycatcher v. Affable*: Default judgment

LLMs cannot distinguish contract text from malicious instructions (LegalPwn) and often "invent" clauses or metrics that don't exist.

## Real Court Cases (2025-2026)

| Case | Sanction | Key Finding |
|------|----------|-------------|
| **Lacey v. State Farm** | $31,100 | Lawyer filed 9 incorrect citations, 2 hallucinated |
| **Lexos Media v. Overstock** | Show cause order | Lawyer admitted no verification of AI output |
| **Russell v. Mells** | Florida Bar referral | Completely invented case citation |

## Solution: The 8-Radical Ontology

TridenGuard enforces a strict, neuro-symbolic schema using 8 orthogonal atomic radicals:
- **Actor** | **Deontic** | **Action** | **Object** | **Temporal** | **Spatial** | **Metric** | **Condition**

If the LLM fails semantic completeness (e.g., extracting an Action without an Actor) or fails schema validation, the entry is automatically **QUARANTINED** for human review.

## Architecture

```mermaid
graph TD
    A[Frontend UI] -->|REST POST| B[n8n Webhook]
    B -->|DPI Inspection| C[Lobster Trap Engine]
    C -->|Secure Prompt| D[Ollama / Phi-4-mini]
    D -->|8-Radical Extraction| E[Deterministic Validator v2.1]
    E -->|Validation Success| F[n8n Data Table: AUDIT]
    E -->|Validation Fail| G[n8n Data Table: QUARANTINE]
    F -->|JSON Response| A
    G -->|JSON Response| A
```

## Tech Stack

- **n8n**: Orchestration, state management, and native **Data Tables**.
- **Lobster Trap (Go)**: Deep Prompt Inspection (DPI) and PII filtering.
- **Ollama (Phi-4-mini)**: Local inference for zero-latency data residency.
- **Deterministic Validator**: Custom JS engine enforcing semantic completeness rules (Guardian Logic).

## 🗺️ Roadmap & The "Flywheel" Moat

- **V1/V2 (Current MVP)**: n8n Orchestration + Lobster Trap (DPI) + Local UI + Deterministic Logic (8-Radicals).
- **V3 (TridenGemma & Local MLOps)**: The Data Flywheel. We utilize the corrected local quarantine logs (Rejected vs. Chosen outputs securely stored in n8n Data Tables) to fine-tune **Google's Gemma 4 (Apache 2.0)**.
  - Leveraging our proprietary `gemma-tuner-multimodal` pipeline (custom-patched for PEFT and optimized for Apple Silicon/MPS), we train a hyper-specialized edge model (`TridenGemma`).
  - **The Result**: A lightweight, on-premise model capable of zero-shot 8-radical extraction with near-zero hallucination rates.

## 🚀 Quick Start

1. `docker-compose up -d`
2. Import `n8n-workflows/triden_guard_v1.json` into your n8n instance.
3. Ensure Ollama is running with `phi4-mini:3.8b`.
4. Send a test POST to `http://localhost:5678/webhook/tridenguard`.

## Repository Structure

```mermaid
graph LR
    Root[TridenGuard]
    Root --> Workflows[n8n-workflows]
    Root --> Logic[Deterministic Validator]
    Root --> Research[I+D / Code Engine]
    
    Workflows --> W1[triden_guard_v1.json]
    Research --> R1[triden_guard_code_engine_v4.json]
```

## License

MIT License - Copyright (c) 2026 AlexusPacicus
