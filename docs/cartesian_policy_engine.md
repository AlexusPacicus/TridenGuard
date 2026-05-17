# Cartesian Policy Engine — Lobster Trap + Tuple-Based Rules

## Objective

Replace fragile keyword-based detection with a **cartesian policy engine** that evaluates structured metadata using tuple algebra. Each rule is defined as an incompatibility between fields (factors) and their values (levels). Lobster Trap enforces these rules with first-match-wins determinism.

## Inspiration

Inspired by formal verification techniques in safety-critical systems, each extracted radical becomes a tuple `(radical_type, radical_value)`, and Lobster Trap evaluates incompatibilities between them:

```python
exclusion_matrix = [
    frozenset([("Factor_A", "Level_1"), ("Factor_B", "Level_2")])
]
```

## Tuple Translation

### LLM Extraction → Cartesian Tuples

```json
{
  "radicals": [
    {"radical": "Actor", "value": "contractor"},
    {"radical": "Deontic", "value": "must"},
    {"radical": "Action", "value": "complete installation"}
  ]
}
```

Translates to:

```
("Actor", "contractor")
("Deontic", "must")
("Action", "complete installation")
```

### Rule Definition (YAML)

```yaml
- name: rule_action_without_subject
  description: "Action present but Actor missing → structural failure R2"
  priority: 100
  action: QUARANTINE
  conditions:
    - field: has_action
      match_type: boolean
      value: true
    - field: has_actor
      match_type: boolean
      value: false
  logic: AND
```

### Rule Definition (Cartesian Tuples — V3)

```yaml
- name: incompatible_radicals
  description: "Block combinations where Action exists but Actor is missing"
  priority: 100
  action: QUARANTINE
  incompatible_tuples:
    - [("Action", "*"), ("Actor", null)]
  logic: REQUIRES_PAIR
```

## Early Pruning

When a rule fires, Lobster Trap stops evaluating subsequent rules. This is equivalent to **Early Pruning (Backtracking)** in formal verification constraint solvers:

> "Si la intersección matemática con la matriz de exclusión es positiva, el motor descarta la evaluación actual y no evalúa las condiciones restantes."

In TridenGuard terms: if `has_action = true AND has_actor = false`, the case goes to QUARANTINE immediately. No further rules are checked.

## Why This Matters for Veea

| Traditional Approach | Cartesian Policy Engine |
|:--|:--|
| Regex on free text | Tuple matching on structured metadata |
| Fragile across languages | Language-independent |
| Hard to audit | Every rule is a YAML declaration |
| One layer only | Same engine governs Ingress, Egress, and Quarantine |

## Integration with TridenGuard

### Current State (MVP)
- Lobster Trap evaluates boolean fields (`has_action`, `has_actor`, etc.)
- Rules defined in `configs/egress/pre_validation.yaml`
- First-match-wins logic active

### V3 Vision
- Lobster Trap evaluates cartesian tuples natively
- Rules defined as incompatible pairs `[("field", "value"), ("field", "value")]`
- Automatic rule suggestion from quarantine logs (semantic token constraint inspection)

## Demo Narrative

"Lobster Trap doesn't just scan for keywords. It evaluates structured metadata using a cartesian policy engine. Each extracted radical becomes a tuple — a point in our validation space. Rules are defined as incompatibilities between these points. When a rule fires, the system prunes the evaluation tree immediately. First-match-wins. Deterministic. Auditable."