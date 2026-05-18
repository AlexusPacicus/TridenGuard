# Logographic Quarantine — TOON + Lobster Trap Token Control

> **Note:** TOON serialization and logographic token inspection are planned for **V2**. The current MVP (V1) uses JSONL logs. This document describes the target architecture.

## Philosophy

Inspired by logographic writing systems — where each symbol represents a complete unit of meaning, not just a sound — this architecture treats every quarantine event as a compact, semantically dense "logogram". Lobster Trap, acting as a unified policy engine, inspects these logograms to ensure structural integrity, detect anomalies, and classify new failure patterns.

The Chinese character `法` (law/method) encapsulates a complex concept in a single glyph. Similarly, a TOON record like `R2_ACTION_WITHOUT_SUBJECT` captures the rule, the pipeline stage, and the structural violation in one auditable unit.

## Architecture
Quarantine Event (Validation Failure)
↓
Serialized to TOON (compact, logographic)
↓
Lobster Trap Egress Rules inspect TOON logograms
↓
┌─────────────────────────────────────────────┐
│ [Logographic Decision Tree] │
│ │
│ TOON_STRUCTURE_INVALID → QUARANTINE │
│ TOON_PII_LEAK → DENY │
│ TOON_NEW_PATTERN → INCUBATOR (V3) │
│ TOON_VALID → LOG │
└─────────────────────────────────────────────┘
↓
Preference Dataset (for Fine-Tuning)

text

## Why TOON for Logographic Quarantine

| Property | How it applies |
| :--- | :--- |
| **40-60% fewer tokens than JSON** | Less storage, lower cost for fine-tuning datasets |
| **Semantic headers** (`[N]{field1,field2}`) | Each token encodes the schema structure — a true logogram |
| **Lossless vs JSON** | No semantic information is lost |
| **Tabular format** | Easy for Lobster Trap rules to inspect and validate |

## Lobster Trap Rules for Logographic Inspection (V3)

| Rule | Priority | Action | Condition |
| :--- | :--- | :--- | :--- |
| `toon_schema_integrity` | 100 | QUARANTINE | TOON structure does not match expected schema |
| `toon_pii_audit` | 95 | DENY | Logogram contains previously undetected PII |
| `toon_new_failure_pattern` | 70 | LOG | `rejection_reason = NONE` but TOON structure is anomalous |
| `toon_valid` | 10 | ALLOW | Passes all structural and security checks |

## Integration with the Sovereign Fine-Tuning Flywheel (V3)

The logographic quarantine feeds directly into the V3 flywheel:

1. **Valid logograms** → go directly to the preference dataset.
2. **Anomalous logograms** → flagged for human review. Each Approve/Discard creates a new training pair.
3. **New failure patterns** → accumulated in the incubator. When enough samples exist, a new atomic rule (a new logogram) is proposed.

## Demo Narrative (for V3 pitch)

> *"TridenGuard's quarantine system is logographic: every token is a complete unit of meaning. We serialize every validation failure into TOON, a format where each record captures the rule, the stage, and the violation in a single, compact symbol. Lobster Trap then inspects these logograms — ensuring each one is structurally valid, secure, and ready to train our sovereign model. This turns our error logs into a semantically rich, auditable, and efficient training dataset."*

## V1 Current Implementation

In the current MVP (V1), quarantine logs are stored as JSONL files in `tests/results/quarantine-log.csv`. The logographic TOON architecture is the planned evolution for V2 and V3.