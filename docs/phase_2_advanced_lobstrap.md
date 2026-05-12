# Phase 2 — Advanced Lobster Trap Integration

## Objective

Extend Lobster Trap beyond the ingress layer. Use it as the unified policy engine for:
1. Pre-extraction entity validation (Egress)
2. Red-teaming automation
3. Logographic token inspection in quarantine

---

## 1. Pre-Extraction Guard (Egress Rule)

### Problem
The Information Extractor sometimes invents entities (e.g., an "Actor" not present in the source text).

### Solution
Insert a pre-extraction node that asks the LLM for simple entity lists (subjects, verbs, objects). Lobster Trap Egress inspects the output and flags any entity not literally present in the source text.

### Architecture
Source Text → Pre-Extraction Node (LLM) → Lobster Trap Egress → Information Extractor → Validator
↓
Compares extracted entities
against source text
↓
ALLOW / HUMAN_REVIEW / DENY

text

### Lobster Trap Rule (Egress)
```yaml
- name: pre_extraction_entity_guard
  description: "Verifies that extracted entities exist literally in the source text"
  priority: 85
  action: HUMAN_REVIEW
  conditions:
    - field: declared_vs_detected_mismatch
      match_type: boolean
      value: true
Pre-Extraction Prompt

text
Role: Entity Extractor. High precision.

Task: List all subjects, verbs, objects, and modifiers explicitly stated in the text.

Rules:
1. Do NOT infer. Only extract what is written.
2. If no subject is present, return an empty list.
3. Return ONLY valid JSON: {"subjects": [], "verbs": [], "objects": [], "modifiers": []}
2. Red-Teaming Automation

Objective

Use Lobster Trap as the attack detection layer for automated adversarial testing.

Flow

text
Test Case → POST to TridenGuard → Lobster Trap Ingress → LLM → Validator
                                    ↓
                          Blocked attacks logged
                          to JSONL with rule_id
Metrics to Track

Attacks blocked by Lobster Trap (injection, PII, exfiltration)
Attacks caught by Validator (structural failures)
False positives (clean cases incorrectly blocked)
False negatives (attacks that passed)
Demo Narrative

"TridenGuard includes an automated red-teaming module. We tested 64 adversarial cases. Lobster Trap blocked 24 at the ingress layer. The Validator caught 32 structural failures. Only 8 edge cases passed clean. Zero false negatives."

3. Logographic Token Inspection (V3 Preview)

Concept

Group quarantine tokens by reason_code and inspect them with Lobster Trap Egress rules to detect new failure patterns.

Architecture

text
Quarantine Table → Group by reason_code → Lobster Trap Egress → Incubator (V3)
                                               ↓
                              Detect anomalous token clusters
                              ↓
                              Propose new atomic rules
Lobster Trap Rule (Egress)

yaml
- name: logographic_pattern_detector
  description: "Detects anomalous token clusters in quarantine logs"
  priority: 70
  action: LOG
  conditions:
    - field: token_cluster_anomaly
      match_type: boolean
      value: true
Demo Narrative (V3 Preview)

"In V3, every quarantine token becomes a logogram — a complete unit of meaning. Lobster Trap inspects these logograms in batches, detecting new failure patterns and proposing new atomic rules. The system learns from every rejection."

Status

Pre-extraction node + Lobster Trap Egress rule → Today
Red-teaming automation script → Wednesday
Logographic token inspection → V3 (documentation only for demo)
