TridenGuard: Intelligent Quarantine Engine (Roadmap V2)

Objective: Classify and prioritize rejections from the 8-Rule Validator
using Lobster Trap as a decision tree in the quarantine phase.

QUARANTINE STATES:

QUARANTINE_CRITICAL (R1, R2, R3)
  - Severe structural failure: missing Actor, Action, or Referent
  - Priority human review
  - Red in the dashboard

QUARANTINE_WARNING (R5, R6, R7)
  - Contextual failure: Condition, Temporal, or Spatial without anchor
  - Deferred review
  - Yellow in the dashboard

QUARANTINE_PII
  - PII detected during validation phase
  - Automatic blocking, no human review required

QUARANTINE_UNKNOWN
  - New pattern not covered by existing rules
  - Incubator for new rules (V3)
  - Accumulated for model fine-tuning

PLANNED LOBSTER TRAP RULES (EGRESS):

  quarantine_critical:
    priority: 100
    action: HUMAN_REVIEW
    conditions:
      - field: rejection_reason
        match_type: regex
        value: "R[1-3]_"

  quarantine_pii_late:
    priority: 95
    action: DENY
    conditions:
      - field: contains_pii
        match_type: boolean
        value: true

  quarantine_warning:
    priority: 80
    action: LOG
    conditions:
      - field: rejection_reason
        match_type: regex
        value: "R[5-7]_"

  quarantine_unknown:
    priority: 50
    action: QUARANTINE
    conditions:
      - field: rejection_reason
        match_type: exact
        value: "NONE"

BENEFIT: Full traceability. Every rejection has a reason, 
a priority, and a destination. The dashboard shows the queue 
ordered by criticality. The system learns from UNKNOWNs.