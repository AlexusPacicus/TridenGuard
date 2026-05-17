# Neuro-Symbolic Isolation — TridenGuard Architecture

## Objective

Define the strict boundary between the probabilistic layer (LLM extraction) and the deterministic layer (validation & security). The LLM is responsible for form and type. The Validator is responsible for logic and safety. Never the reverse.

## The Isolation Principle

| Layer | Technology | Responsibility | What it does NOT do |
|:--|:--|:--|:--|
| **Neural (Extraction)** | Phi-4-mini / Gemma 4 E2B + Prompt | Produce structured JSON with 8 atomic radicals. Handle form and type. | It does NOT decide if the content is safe or complete. |
| **Symbolic (Validation)** | Custom JS Engine + 8 Atomic Rules | Apply deterministic exclusion rules. Check source integrity. Decide VALIDATED or QUARANTINED. | It does NOT use ML. It does NOT parse free text. |

## Why Isolation Matters

Most AI safety systems mix layers: they ask the LLM to validate its own output, or they use another LLM to check the first. This creates a probabilistic loop with no guarantee of correctness.

TridenGuard never asks the LLM to validate. The neurons propose. The rules dispose.

## Boundary Test

A valid TridenGuard deployment must pass this test:

1. **Input:** A legal text with a structural failure (e.g., Action without Actor).
2. **Neural Layer:** The Information Extractor produces a valid JSON with the extracted radicals. It does NOT flag the missing Actor — that is not its job.
3. **Symbolic Layer:** The Deterministic Validator detects the missing Actor via R2_ACTION_WITHOUT_SUBJECT and sets status to QUARANTINED.

If the LLM output is syntactically valid but semantically incomplete, the Validator catches it. If the LLM output is syntactically invalid, the Normalizer catches it. The LLM never decides safety.

## Implementation in TridenGuard

### Neural Layer
- **Information Extractor** (Ollama + Phi-4-mini / Gemma 4 E2B)
- Prompt with `must/must not` containment rules
- Output: `{"axiom": "...", "radicals": [...]}`

### Symbolic Layer
- **Normalizer**: Fixes malformed JSON (syntactic safety net)
- **Radical Grounding Check**: Verifies each radical exists literally in the source text
- **Deterministic Validator**: Applies 8 atomic exclusion rules + UNGROUNDED_RADICAL
- **Semantic Rule Engine**: Classifies errors by severity (CRITICAL / WARNING / UNKNOWN)

### What Never Happens
- The LLM never sees the validation rules
- The Validator never uses embeddings or probabilities
- A QUARANTINED case is never auto-corrected by the LLM

## Prompt Poda (Cognitive Offloading)

Following the isolation principle, the prompt does NOT include:
- Validation rules ("if Actor is missing, flag it")
- Safety instructions ("do not allow malicious content")
- Schema enforcement ("return JSON with these fields")

The prompt only instructs the LLM on what to extract and how to format it. The rest is handled by the symbolic layer.

## Acceptance Criteria

- [x] The LLM produces structured JSON without safety instructions in the prompt
- [x] 100% of extractions are validated by deterministic rules, not by another LLM
- [x] The Boundary Test passes: structural failures are caught by the Validator, not the Extractor
- [x] Source integrity is verified deterministically (literal match against source text)
- [x] The system can explain every rejection with a traceable `rejection_reason`

## Demo Narrative

"TridenGuard is built on a strict neuro-symbolic isolation principle. The LLM extracts. The rules validate. Never the reverse. This means we don't ask a probabilistic model to check its own homework. We trust the LLM to be good at language, and we trust deterministic logic to be good at safety. That's why our system can guarantee zero false negatives on structural failures — because the validator doesn't guess. It checks."