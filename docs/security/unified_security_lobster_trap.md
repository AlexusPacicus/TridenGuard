# Unified Security Layer — Lobster Trap + GBNF + Decision Tree

## Philosophy

Lobster Trap is not just an ingress firewall. In TridenGuard, it serves as the **single source of truth for security policy enforcement** across the entire pipeline. Every interaction —inbound, outbound, and quarantine classification— is governed by the same policy engine.

## Architecture
User Input
↓
[Lobster Trap — Ingress Rules]
↓ ALLOW
[Ollama + GBNF — Structured Generation]
↓ JSON Output
[Lobster Trap — Egress Rules]
↓ ALLOW
[Deterministic Validator — 8 Atomic Rules]
↓
┌─────────────────────────────────────────┐
│ [Lobster Trap — Quarantine Decision Tree] │
│ │
│ CRITICAL (R1-R3) → HUMAN_REVIEW │
│ WARNING (R5-R7) → LOG │
│ PII_LATE → DENY │
│ UNKNOWN → QUARANTINE │
└─────────────────────────────────────────┘
↓
Human Review Panel (Approve/Discard)
↓
Preference Dataset (TOON)
↓
Fine-Tuning (LoRA on Gemma 4 E2B)

## Layer 1: Ingress Inspection

**Purpose:** Block malicious or non-compliant prompts before they reach the LLM.

**Rules in use:**

| Rule | Priority | Action | Description |
|:--|:--|:--|:--|
| block_prompt_injection | 100 | DENY | Detects instruction override attempts |
| block_harm_violence | 98 | DENY | Blocks harmful/violent content requests |
| block_malware_request | 96 | DENY | Blocks malware/exploit generation |
| block_phishing_fraud | 94 | DENY | Blocks phishing/fraud content |
| block_data_exfiltration | 92 | DENY | Detects data exfiltration patterns |
| block_obfuscation_evasion | 90 | DENY | Blocks encoding/obfuscation attempts |
| review_role_impersonation | 86 | HUMAN_REVIEW | Flags privileged role assignment |
| block_pii_request | 82 | DENY | Blocks PII requests |
| block_dangerous_commands | 80 | DENY | Blocks system command injection |
| review_high_risk | 70 | HUMAN_REVIEW | High risk score triggers review |
| block_sensitive_paths | 85 | DENY | Blocks sensitive filesystem paths |
| log_code_execution | 30 | LOG | Logs code execution requests |

## Layer 2: Egress Inspection

**Purpose:** Validate the structural integrity of the LLM output before it enters the validation pipeline.

**Rules in use:**

| Rule | Priority | Action | Description |
|:--|:--|:--|:--|
| block_credential_leak | 100 | DENY | Blocks output containing credentials |
| block_pii_leak | 90 | DENY | Blocks output containing PII |
| schema_structure_check | 80 | HUMAN_REVIEW | Flags output that fails GBNF schema compliance |
> **Note:** GBNF integration is planned for V2. In the current MVP (V1), schema validation is handled by the Deterministic Validator and the Radical Grounding Check.
**Why Schema Check Matters:**
Even with GBNF constraining token generation, a structurally invalid output can slip through in edge cases (e.g., truncated generation, context overflow). The schema check acts as a safety net, ensuring that the Validator only processes well-formed JSON.

## Layer 3: Quarantine Decision Tree

**Purpose:** Classify every rejection from the Deterministic Validator and route it to the appropriate action.

**Rules:**

| Rule | Priority | Action | Conditions |
|:--|:--|:--|:--|
| quarantine_critical | 100 | HUMAN_REVIEW | `rejection_reason` matches `R[1-3]_` |
| quarantine_pii_late | 95 | DENY | `contains_pii == true` |
| quarantine_warning | 80 | LOG | `rejection_reason` matches `R[5-7]_` |
| quarantine_unknown_pattern | 50 | QUARANTINE | `rejection_reason == NONE` but risk score elevated |

**Routing Logic:**
Is rejection structural (R1-R3)?
→ CRITICAL. Red flag in panel. Human reviewer sees it first.

Is rejection contextual (R5-R7)?
→ WARNING. Yellow flag. Deferred review.

Is there PII the ingress layer missed?
→ Auto-block. No human needed.

Is this a new, unknown pattern?
→ QUARANTINE_UNKNOWN. Goes to the incubator. Candidate for V3 fine-tuning.


## Why Unified Lobster Trap

| Benefit | How it applies |
|:--|:--|
| Single policy language (YAML) | No fragmented security logic across n8n nodes |
| First-match-wins determinism | No ambiguity in rule priority |
| Audit trail native | Every action (ALLOW, DENY, HUMAN_REVIEW) is logged |
| Extensible per client | Plug policy packs for HIPAA, SOC2, or custom legal rules |
| Veea-aligned architecture | Lobster Trap is not an add-on. It is the backbone. |

## Demo Narrative

"Lobster Trap is not just our ingress firewall. It is the single source of truth for every security decision in TridenGuard. It inspects every incoming prompt for attacks. It validates every outgoing response for schema compliance. And when our Deterministic Validator rejects a structural failure, Lobster Trap classifies the rejection into a priority queue —critical, warning, or unknown— and routes it to the human reviewer. One policy engine. Three layers. Zero Trust across the entire pipeline."