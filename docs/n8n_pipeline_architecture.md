# 📄 n8n Pipeline Architecture — TridenGuard v1.5

**Date:** May 18, 2026  
**Workflow:** `TridenGuard_v1`  
**Based on:** `TridenGuard.json`

This document provides a technical breakdown of the core nodes within the TridenGuard n8n orchestration pipeline. The system operates as a deterministic, local-first state machine.

---

## 1. Ingress & Pre-Processing

| Node | Type | Function |
| :--- | :--- | :--- |
| **Frontend Webhook** | Webhook | Primary entry point. Listens for POST requests at `/webhook/tridenguard` containing the raw contract clause. |
| **Auth Gate** | IF Node | Validates the `x-api-key` header against `tridenguard_secret_key_2026`. Drops unauthorized payloads immediately. |
| **Source Truth Anchor** | Code Node | Caches the raw incoming text into `source_truth` and `source_hash`. Critical for the downstream `Radical Grounding Check`. |

---

## 2. Shield Layer (DPI)

| Node | Type | Function |
| :--- | :--- | :--- |
| **HTTP Request** | HTTP Request | Sends the raw payload to the Veea Lobster Trap proxy at `http://host.docker.internal:8080/inspect`. |
| **DPI Gate** | IF Node | Evaluates the Lobster Trap response. If `action: "ALLOW"`, the pipeline continues. Otherwise, routes to `Respond to Webhook1` (blocked) and logs to `dpi-block-log`. |

---

## 3. Neural Extraction Layer

| Node | Type | Function |
| :--- | :--- | :--- |
| **Ollama Chat Model** | LM Chat (Ollama) | Local Phi-4-mini (3.8B) model. Temperature forced to 0. Format forced to JSON. |
| **Information Extractor** | Information Extractor | Passes the text with a strict system prompt (8 atomic radicals). Extracts `axiom`, `radicals`, and `falsabilidad` as structured JSON. |
| **Normalizer** | Code Node | Syntactic safety net. Cleans malformed JSON (e.g., extra quotes, missing brackets) and normalizes radical objects to `{radical, value}` format. |

---

## 4. Symbolic Validation Layer

| Node | Type | Function |
| :--- | :--- | :--- |
| **Radical Grounding Check** | Code Node | Performs a strict `.includes()` check comparing every extracted radical value against the original text (cached in `Source Truth Anchor`). Sets `source_integrity: true/false` and logs `ungrounded_radicals`. |
| **Deterministic Validator** | Code Node | Applies the **8 Cartesian Exclusion Rules** (R1–R8). Also checks for `EMPTY_EXTRACTION`, `UNGROUNDED_RADICAL`, `DUPLICATE_DEONTIC`, and `METRIC_WITHOUT_CONTEXT`. Outputs `status` (VALIDATED / QUARANTINED) and `rejection_reason`. |
| **Semantic Rule Engine** | Code Node | Classifies errors by severity: `has_critical` (R1–R4, R8, UNGROUNDED, EMPTY), `has_warning` (R5–R7), `has_borderline`, `has_unknown`, `has_validated`. |

---

## 5. Routing & Persistence

| Node | Type | Function |
| :--- | :--- | :--- |
| **Switch** | Switch Node | Routes the payload based on `has_validated`, `has_critical`, `has_warning`, `has_borderline`, `has_unknown`, and `UNGROUNDED_RADICAL`. |
| **Save to Audit Table** | Data Table | Persists validated cases to `audit-log` (n8n Data Table). |
| **Save to Quarantine Table** | Data Table | Persists quarantined cases to `quarantine-log` (n8n Data Table). |
| **Save to dpi-block-log** | Data Table | Persists blocked DPI cases (prompt injection, PII, exfiltration). |

---

## 6. Human-in-the-Loop (HITL)

| Node | Type | Function |
| :--- | :--- | :--- |
| **Webhook (approve)** | Webhook | Listens for POST requests at `/webhook/approve` from the frontend panel. |
| **Update row(s) (approve)** | Data Table | Updates the status of a case in `quarantine-log` to `APPROVED`. |
| **Webhook (discard)** | Webhook | Listens for POST requests at `/webhook/discard` from the frontend panel. |
| **Update row(s) (discard)** | Data Table | Updates the status of a case in `quarantine-log` to `DISCARDED`. |

---

## 7. Response Nodes

| Node | Type | Function |
| :--- | :--- | :--- |
| **Respond to Webhook (Unauthorized)** | Respond to Webhook | Returns `401 Unauthorized` if the API key is missing or invalid. |
| **Respond to Webhook1 (DPI Block)** | Respond to Webhook | Returns security violation message when Lobster Trap blocks a prompt. |
| **Respond to Webhook3 (Discard)** | Respond to Webhook | Confirms discard action back to the frontend panel. |
| **Respond to Webhook4 (Approve)** | Respond to Webhook | Confirms approval action back to the frontend panel. |
| **Respond to Webhook (Audit)** | Respond to Webhook | Returns validation result for approved cases. |
| **Respond to Webhook (Quarantine)** | Respond to Webhook | Returns rejection reason and severity for quarantined cases. |

---

## 📊 Pipeline Summary

| Stage | Key Nodes | Data Tables |
| :--- | :--- | :--- |
| **Ingress** | Webhook, Auth Gate, Source Truth Anchor | — |
| **Shield (DPI)** | HTTP Request (Lobster Trap), DPI Gate | `dpi-block-log` |
| **Extraction** | Ollama, Information Extractor, Normalizer | — |
| **Validation** | Radical Grounding Check, Deterministic Validator, Semantic Rule Engine | — |
| **Routing** | Switch | `audit-log`, `quarantine-log` |
| **HITL** | Approve/Discard webhooks + updates | `quarantine-log` (update) |

---

## 🔧 Key Design Decisions

| Decision | Why |
| :--- | :--- |
| **Data Tables instead of Supabase/Postgres** | Local-first, zero-cloud, no external dependencies. |
| **Source Truth Anchor as a separate node** | Ensures the original text is immutable and accessible to downstream validators. |
| **Radical Grounding Check before Deterministic Validator** | Allows the validator to differentiate between missing radicals (structural failure) and hallucinated radicals (grounding failure). |
| **Semantic Rule Engine as a separate node** | Decouples severity classification from validation logic. Easier to modify thresholds without touching validation rules. |
| **Approve/Discard webhooks as separate paths** | Clean separation of concerns; each action has its own audit trail. |

---

## 📝 Document Version

- **v1.5** — Based on `TridenGuard.json` as of May 18, 2026.
- **Next update** — When TOON + GBNF integration is added (V2).

---
