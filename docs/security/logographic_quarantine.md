# Semantic Token Quarantine — TOON + Lobster Trap Token Control

## Philosophy

Inspired by the principle of Semantic Token Constraints —where each symbol represents a complete unit of meaning, not just a sound— this architecture treats every token in the quarantine log as a compact, semantically complete representation of a security event. Lobster Trap, acting as a unified policy engine, inspects these "Semantic Token Constraints" to ensure structural integrity, prevent data leaks, and classify new failure patterns.

## The Concept

Traditional logging treats each entry as a sequence of fragmented data. The semantic constraint approach treats each TOON token as a miniature of the system's state. Just as the Chinese character `法` (law/method) encapsulates a complete concept, a TOON record like `R2_ACCION_SIN_SUJETO` captures the rule, the pipeline stage, and the structural violation in a single, auditable semantic unit.

## Architecture
Quarantine Event (Validation Failure)
↓
Serialized to TOON (compact, semantically rich)
↓
Lobster Trap Egress Rules inspect TOON "Semantic Token Constraints"
↓
┌────────────────────────────────────────────┐
│ [Semantic Decision Tree]    │
│ │
│ TOON_STRUCTURE_INVALID → QUARANTINE │
│ TOON_PII_LEAK → DENY │
│ TOON_NEW_PATTERN → INCUBATOR (V3) │
│ TOON_VALID → LOG │
└────────────────────────────────────────────┘
↓
Preference Dataset (for Fine-Tuning)

## Why TOON as the Semantic Token Unit

| Property | How it applies |
|:--|:--|
| 40-60% fewer tokens than JSON | Less storage, less cost for the fine-tuning dataset |
| Semantic headers (`[N]{field1,field2}`) | Each token is a "Semantic Token Constraint" encoding the schema structure |
| Lossless vs JSON | No semantic information is lost in the compression |
| Tabular format | Easy for Lobster Trap rules to inspect and validate |

## Lobster Trap Rules for Semantic Token Inspection

| Rule | Priority | Action | Conditions |
|:--|:--|:--|:--|
| toon_schema_integrity | 100 | QUARANTINE | TOON output fails to match expected schema structure |
| toon_pii_audit | 95 | DENY | TOON token contains previously undetected PII |
| toon_new_failure_pattern | 70 | LOG | rejection_reason is `NONE` but TOON structure is anomalous |
| toon_valid | 10 | ALLOW | TOON record passes all structural and security checks |

## Integration with the Flywheel (V3)

The semantic token quarantine feeds directly into the sovereign fine-tuning flywheel:

1. **Valid TOON Semantic Token Constraints**: Go directly to the preference dataset.
2. **Anomalous TOON Semantic Token Constraints**: Flagged for human review. Human decision (Approve/Discard) creates a new training pair.
3. **New failure Semantic Token Constraints**: Accumulated in the incubator. When enough samples exist, a new atomic rule (a new "Semantic Token Constraint") is proposed.

## Demo Narrative

"TridenGuard's quarantine system is based on the concept of Semantic Token Constraints: every token is a complete unit of meaning. We serialize every validation failure into TOON —a format where each record captures the rule, the stage, and the violation. Lobster Trap then inspects these 'Semantic Token Constraints', ensuring that each one is structurally valid, secure, and ready to train our sovereign model. This turns our error logs into a semantically rich, auditable, and efficient training dataset."