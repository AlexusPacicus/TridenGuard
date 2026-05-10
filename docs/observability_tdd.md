Technical Implementation Document (TDD)
Observability and Telemetry — TridenGuard v1.5
Status: Ready for Hackathon

Scope: tridenguard.observability, lobstertrap.audit, n8n.webhook

Objective: Implement a deterministic system for logging, structuring, and analyzing Quarantine and Rejection events in the AI legal firewall.

1. SYSTEM DEFINITION

The system must:

Detect semantic failures (missing radicals) or malicious injections.

Generate structured events detailing the exact reason for rejection.

Persist events using TOON as a compact serialization format (40-60% smaller than JSON), reducing storage costs and tokens in the training pipeline.

Serve as a clean database for the human review dashboard (Approve/Discard).

2. MODELS (STRICT CONTRACT)

2.1 Enums

class PipelineStage(str, Enum):  
    DPI_INSPECTION = "DPI_INSPECTION"          # Lobster Trap Layer
    LLM_EXTRACTION = "LLM_EXTRACTION"          # Phi-4-mini Inference
    DETERMINISTIC_VALIDATION = "VALIDATION"    # 8-Radical JS Engine

class ReasonCode(str, Enum):  
    R1_SUBJECT_WITHOUT_ACTION = "R1_SUBJECT_WITHOUT_ACTION"
    R2_ACTION_WITHOUT_SUBJECT = "R2_ACTION_WITHOUT_SUBJECT"
    R3_OBJECT_WITHOUT_REFERENT = "R3_OBJECT_WITHOUT_REFERENT"
    R4_ORPHAN_METRIC = "R4_ORPHAN_METRIC"
    R5_CONDITION_WITHOUT_TRIGGER = "R5_CONDITION_WITHOUT_TRIGGER"
    R6_TEMPORAL_WITHOUT_ANCHOR = "R6_TEMPORAL_WITHOUT_ANCHOR"
    R7_INERT_SPATIAL = "R7_INERT_SPATIAL"
    R8_DEONTIC_WITHOUT_BEHAVIOR = "R8_DEONTIC_WITHOUT_BEHAVIOR"
    ERR_PROMPT_INJECTION = "ERR_PROMPT_INJECTION"
    ERR_HALLUCINATED_CITATION = "ERR_HALLUCINATED_CITATION"
    ERR_PII_LEAK = "ERR_PII_LEAK"

class SeverityLevel(str, Enum):  
    WARNING = "WARNING"         # Minor discrepancy, requires review
    QUARANTINE = "QUARANTINE"   # Direct block due to failed semantic integrity
    FATAL = "FATAL"             # Direct attack attempt or jailbreak

3. PERSISTENCE

3.1 Format

TOON as the primary serialization format, with export to JSONL for tools that do not natively support TOON.

Append-only. Only add, never delete, to maintain the audit chain of custody.

3.2 Conversion

The community node @tehw0lf/n8n-nodes-toon manages the conversion between JSON and TOON in the n8n flow without external dependencies.

3.3 Required Implementation

Synchronous writing. There must be no file corruption when logging simultaneous quarantines.

4. END-TO-END PIPELINE

TridenGuard Flow:

Prompt Input →

Lobster Trap (DPI) →

8-Radical Validation →

If fails: QuarantineEvent Generation →

TOON Serialization via n8n →

Persistence in quarantine_log.toon.

5. MINIMUM TESTS (HACKATHON MVP)

5.1 Validation Engine

Allowed case: Required radicals are present → No log is generated.

Blocked case: "Actor" radical is missing → R2_ACTION_WITHOUT_SUBJECT is generated.

5.2 Persistence

The file is created if it does not exist.

The event is added with a valid TOON format.

TOON→JSON back-conversion produces the same original object without loss.

6. VISUAL ANALYSIS FOR THE PITCH

Required script:

Load the TOON file.

Convert to JSON for visualization if necessary.

Group by reason_code.

Show it in the TridenGuard Frontend Panel (tridenguard_panel.html).

Show size comparison: same dataset in JSON vs TOON to demonstrate 40-60% savings.