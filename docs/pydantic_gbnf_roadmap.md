# Pydantic + GBNF + TOON — Sovereign Fine-Tuning Roadmap (V3)

## Objective

Move from a fixed ontology to a **client-defined validation schema**. Each enterprise defines its own radicals, business rules, and compliance checks. The schema is enforced at the token level and the model is fine-tuned locally.

## Stack

| Component | Role |
|:--|:--|
| **Pydantic** | Client defines the schema (custom radicals, validation rules) |
| **GBNF** | Schema compiled to grammar. Forces the model to output only valid structures at the token level. No retries. No invalid output possible. |
| **TOON** | Compact serialization format. Reduces dataset size by 40-60% vs JSON. Lower token cost for fine-tuning. |
| **LoRA (MLX)** | Lightweight fine-tuning on Apple Silicon. Adapts Gemma 4 E2B to the client's terminology and document patterns. |
| **Preference Dataset** | Generated from Quarantine logs. Human decisions (Approve/Discard) become training pairs. Serialized in TOON for efficiency. |

## Flow
Client defines schema (Pydantic BaseModel)
↓
Schema compiled to GBNF grammar
↓
Ollama enforces grammar at inference (logit shaping)
↓
Model outputs only valid structures
↓
Quarantine logs → Preference Dataset (TOON)
↓
LoRA fine-tuning on Gemma 4 E2B (MLX, Apple Silicon)
↓
Fine-tuned model deployed locally. No data leaves the premises.

text

## Why TOON

| Format | Size | Tokens (1K entries) | Fine-tuning cost |
|:--|:--|:--|:--|
| JSON | Baseline | ~500K tokens | Baseline |
| TOON | -40 to -60% | ~200-300K tokens | ~50% reduction |

TOON compresses the preference dataset before fine-tuning. Less tokens = less compute = faster training on local hardware. The `@tehw0lf/n8n-nodes-toon` node handles conversion without external dependencies.

## Why GBNF + Pydantic

| Traditional Approach | GBNF + Pydantic |
|:--|:--|
| LLM generates free text | LLM constrained at token level |
| Validate with try/except | Validation before generation |
| Retries on JSONDecodeError | No retries. No invalid output possible. |
| Prompt engineering to fix format | Schema compiled to grammar. Deterministic. |

## The Moat

Every human decision (Approve/Discard) makes the local model smarter. Pydantic defines the contract. GBNF enforces it. TOON compresses the training data. LoRA personalizes the model. No cloud. No data leakage. Just a continuously improving, sovereign AI.