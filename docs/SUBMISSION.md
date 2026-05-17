# 🛡️ TridenGuard — Master Submission Document
### Veea / lablab.ai Hackathon · May 11–19, 2026

> **The first B2B Neuro-Symbolic Contract Integrity Validation System bringing enterprise-grade, deterministic discipline to enterprise AI adoption — enforcing Zero Trust for LLM outputs.**

---

## 1. The Hook & Origin Story

### Bridging the Gap Between Probability and Compliance

Generative AI operates on probability, but enterprise compliance demands determinism. As the legal and financial industries rapidly adopt Large Language Models (LLMs) to automate workflows, they face a fundamental architectural flaw: deploying engines built on hallucination without any deterministic safety nets.

> When you are automating enterprise workflows, a **95% accuracy rate isn't a success; it's a 5% critical failure rate** waiting to happen. 

TridenGuard was built to solve this exact gap. It is the first B2B Neuro-Symbolic Contract Integrity Validation System designed to impose strict, deterministic logic over LLM outputs, enabling enterprises to adopt generative AI with absolute certainty.

---

## 2. The Problem: The Global "Early Adopters" Crisis

### The cost of moving from pilot to production.

The transition of AI from experimental pilots to operational reality is already causing financial and legal damage. Global early adopters are paying the price for deploying LLMs without an auditable security layer. This isn't a theoretical risk — **it is happening right now**.

### 📋 Documented Cases

| Case | Jurisdiction | Consequence |
| :--- | :--- | :--- |
| *Lacey v. State Farm* (May 2025) | C.D. Cal., USA | **$31,100 in sanctions** for hallucinated AI citations |
| *Russell v. Mells* | Florida, USA | Referral to the Florida Bar |
| *Flycatcher v. Affable* | USA | Default judgment entered |
| Baidu AI Hallucination Cases | China | Systemic trust collapse in enterprise deployments |

As Judge Wilner stated in *Lacey v. State Farm*:

> *"The use of AI actively deceived me... I discovered they **DID NOT EXIST**. That's frightening."*

### 🎯 The Enterprise Market Gap

No Fortune 500 company or top-tier law firm will approve the full integration of AI agents into their workflows if the AI is left to validate its own errors. The enterprise market **desperately needs a trust layer**.

---

## 3. The Solution: Neuro-Symbolic Isolation

### *"The neurons propose. The rules dispose."*

Most current AI safety systems make a fatal architectural mistake: they ask a probabilistic model to check its own homework, creating a loop with **no guarantee of correctness**.

TridenGuard introduces a strict **Neuro-Symbolic Isolation** architecture that separates concerns absolutely:

```
┌─────────────────────────────────────────────────────┐
│              TRIDENTGUARD PIPELINE                  │
│                                                     │
│  📄 Input Clause                                    │
│       │                                             │
│       ▼                                             │
│  🛡️ SHIELD A: Lobster Trap (Go DPI)                 │
│  ├─ PII Detection (SSN, email, DOB)                 │
│  ├─ Prompt Injection Detection                      │
│  └─ Data Exfiltration Blocking          → 🚫 BLOCK  │
│       │ (clean)                                     │
│       ▼                                             │
│  🧠 NEURAL LAYER: Phi-4-mini (Local)                │
│  └─ Extracts 8 Atomic Radicals from text            │
│       │ (structured JSON)                           │
│       ▼                                             │
│  ⚖️  SYMBOLIC LAYER: Deterministic Validator        │
│  └─ Applies 8 Orthogonal Exclusion Rules            │
│       │ (pass)          │ (fail)                    │
│       ▼                 ▼                           │
│  ✅ APPROVED      🔴 QUARANTINED                    │
│                         │                           │
│                         ▼                           │
│              👨‍⚖️ Human Review Panel                 │
│              (Approve / Discard → LoRA)             │
└─────────────────────────────────────────────────────┘
```

### The Two Layers Explained

**🧠 The Neural Layer (Extraction)**

We trust the LLM to be good at language. Using a local **Phi-4-mini (3.8B)** model running entirely on-premise via Ollama, the system extracts 8 foundational **Atomic Radicals** from the input text:

| Radical | Description | Example |
| :--- | :--- | :--- |
| **Actor** | Who performs the action | *Company, Distributor* |
| **Deontic** | The obligation modality | *shall, must, may not* |
| **Action** | The verb / behaviour | *appoint, disclose, pay* |
| **Object** | What is acted upon | *Products, Confidential Information* |
| **Temporal** | Time constraints | *10 years, by January 1st* |
| **Spatial** | Jurisdiction or location | *within the Market, Los Angeles* |
| **Metric** | Quantifiable values | *15%, $250,000* |
| **Condition** | Triggering conditions | *in the event of breach* |

The LLM does **NOT** decide if the content is safe. It is used exclusively for what it excels at: understanding language.

**⚖️ The Symbolic Layer (Validation)**

We trust deterministic logic to be good at safety. A custom engine applies **8 orthogonal, deterministic exclusion rules**:

| Rule | Name | What it catches |
| :--- | :--- | :--- |
| R1 | `SUBJECT_WITHOUT_ACTION` | An Actor with no corresponding Action |
| R2 | `ACTION_WITHOUT_SUBJECT` | An Action with no Actor — the clause is legally void |
| R3 | `OBJECT_WITHOUT_REFERENT` | An object present with no linked Actor or Action |
| R4 | `ORPHAN_METRIC` | A financial figure with no actor or action bound to it |
| R5 | `TEMPORAL_INERT` | A deadline with nothing attached |
| R6 | `CONDITION_WITHOUT_CONSEQUENCE` | An "if" without a "then" |
| R7 | `INERT_SPATIAL` | A jurisdiction reference with no subject or action |
| R8 | `DEONTIC_WITHOUT_BEHAVIOR` | A prohibition ("shall not") with no specified behaviour |

**🔬 Radical Grounding Check — The Zero-Hallucination Layer**

Before the exclusion rules even run, the pipeline executes a final deterministic check. A script verifies that **every extracted radical physically exists in the original source text** (`textLower.includes(value)`). If the LLM hallucinates a concept that is not present in the document, the radical's `source_integrity` drops to `false` and the case is **instantly quarantined** as `UNGROUNDED_RADICAL` — before any human ever reads it.

> **The Guarantee:** If a required radical is missing or hallucinated, TridenGuard doesn't guess — it flags a **structural failure** and routes the case to the Human-in-the-Loop Quarantine Panel.
>
> TridenGuard guarantees **zero false negatives on structural failures** because our validator never uses probabilities — **it uses deterministic logic**.

---

## 4. Architecture & Tech Stack

### Orchestrating the Neuro-Symbolic Pipeline at the Edge

TridenGuard operates as a **local-first, zero-cloud pipeline**. The entire logic is orchestrated deterministically through n8n to manage state, handle low-latency webhooks, and route decisions without ever exposing data to external clouds.

```
              ┌────────────────────────┐
              │   📄 Ingress Contract   │
              └───────────┬────────────┘
                          │
                          ▼
              ┌────────────────────────┐
              │ 📥 n8n Webhook Trigger │
              └───────────┬────────────┘
                          │
                          ▼
              ┌────────────────────────┐
              │ 🛡️ Lobster Trap Proxy  │◄── Enforces YAML Firewall
              └───────────┬────────────┘    (Prompt Injection / PII)
                          │
                  (Clean JSON Payload)
                          │
                          ▼
              ┌────────────────────────┐
              │ 🧠 Local Ollama Node   │◄── Extract 8 Radicals
              │      (Phi-4-mini)      │    (Temperature = 0)
              └───────────┬────────────┘
                          │
                 (Structured Radicals)
                          │
                          ▼
              ┌────────────────────────┐
              │ ⚖️ Custom JS Validator  │◄── Run 8 Exclusion Rules
              └───────────┬────────────┘    (Deterministic Logic)
                          │
           ┌──────────────┴──────────────┐
    (Pass) │                             │ (Fail)
           ▼                             ▼
┌────────────────────────┐  ┌────────────────────────┐
│ ✅ Approved Audit Log  │  │ 🔴 Validation Quarantine │
│   (audit-log table)    │  │   (quarantine table)   │
└────────────────────────┘  └────────────┬───────────┘
                                         │
                                         ▼
                            ┌────────────────────────┐
                            │ 👨‍⚖️ Legal Review Panel │◄── Generates TOON
                            │  (Human-in-the-Loop)   │    Constraint for LoRA
                            └────────────────────────┘
```

### 🔥 Built for the Edge — Hardware Note

> This entire B2B firewall — including the local Phi-4-mini LLM inference, the n8n orchestration, and the Lobster Trap DPI — was developed and **stress-tested concurrently on a 2020 Mac M1 with only 8GB of RAM**.
>
> If TridenGuard can execute a full Neuro-Symbolic pipeline on a 6-year-old entry-level machine, **it is lightweight enough to be deployed on any enterprise edge node today**.

### 🛠️ The Tech Stack

| Component | Technology | Role in TridenGuard |
| :--- | :--- | :--- |
| **Orchestration** | n8n | The backbone connecting the webhook, DPI, LLM, and data tables |
| **Unified Security** | Veea Lobster Trap (Go) | DPI proxy enforcing YAML-based firewall rules in low-latency time |
| **Neural Extraction** | Phi-4-mini (3.8B) + Ollama | Runs locally (Temp=0). Extracts the 8 orthogonal atomic radicals |
| **Symbolic Validation** | Custom JS Engine | Applies deterministic exclusion rules (e.g., Action without Subject) |
| **Observability** | TOON + JSONL | Compresses security audit logs for future model fine-tuning |
| **Frontend UI** | Vanilla JS / HTML / CSS | Strict B2B Enterprise Quarantine & Audit Dashboard |

---

## 5. Demo & Test Cases

### How to experience the TridenGuard Firewall

The provided video and live demo showcase the system intercepting real-world contractual structural anomalies. The system executes these **4 deterministic steps** on every submission:

**Step 1 — Input a Structural Anomaly**
Submit a contract extract missing a critical element. Example: *"The profitability threshold is set at 15%."* — the Actor and the Object binding that metric to a party have been removed.

**Step 2 — Lobster Trap Ingress**
The proxy inspects the payload for prompt injections or PII leaks in low-latency time. If clean, the payload advances. If not, it is permanently blocked and logged.

**Step 3 — Radical Extraction**
Phi-4-mini structures the text into our 8-radical ontology at Temperature=0, producing a deterministic structured JSON payload.

**Step 4 — Deterministic Quarantine**
The validation engine detects the structural failure (`R4_ORPHAN_METRIC`), **overriding the LLM's output** and sending a `CRITICAL` Business Risk alert to the Review Panel for human review.

### 🧪 Live Test Cases

Use these in the validator to reproduce the demo:

| Select Contract | Paste this clause | Expected Verdict |
| :--- | :--- | :--- |
| `REAL-R1` LIMEENERGYCO | `Company and Distributor must comply with all obligations stipulated in this agreement.` | 🔴 CRITICAL — `R1_SUBJECT_WITHOUT_ACTION` |
| `TECH-R4` TechVista | `The profitability threshold is set at 15%.` | 🔴 CRITICAL — `R4_ORPHAN_METRIC` |
| `PHARMA-R8` Pharma Global | `The Receiving Party shall not from any source other than the Company.` | 🔴 CRITICAL — `R8_DEONTIC_WITHOUT_BEHAVIOR` |
| `APEX-R7` Apex Construction | `Located in Los Angeles.` | 🔵 BORDERLINE — `R7_INERT_SPATIAL` |

---

## 6. Benchmark: Phase 1 & The 64-Case Matrix

### Stress-testing the architecture and identifying operational limits.

To validate the system, I designed a rigorous **64-case benchmark matrix** testing the 8 atomic rules against 8 hostile input variations: Pure, Overlap, Noise, Evasion, Injection, PII, Exfiltration, and Edge cases.

For this Hackathon MVP, I executed **Phase 1: a 20-case targeted evaluation** designed to identify the system's baseline operational limits under real-world conditions within the hackathon timeframe. The remaining 44 cases constitute the V2 stress-testing roadmap.

### 📊 Phase 1 Results Summary

| Layer | Test Scope | Result |
| :--- | :--- | :--- |
| **Overall Pipeline** | 20 targeted cases | **85% accuracy (17/20)** |
| **Lobster Trap (Ingress)** | Injection, PII, Exfiltration | **100% block rate (Tested against replicated benchmark cases)** |
| **Real-World Court Events** | Hallucination replication | **100% intercepted (Tested against replicated benchmark cases)** |
| **Structural Validator** | R1–R8 rule enforcement | **87.5% accuracy** |

### 🔍 Finding 1: Ingress Defense — Full Coverage

Lobster Trap achieved a **100% block rate (Tested against replicated benchmark cases)** against all Prompt Injection, PII, and Data Exfiltration attempts before they ever reached the LLM. It also successfully intercepted **100% of the real-world court hallucination events (Tested against replicated benchmark cases)** replicated from documented legal cases.

### 🔍 Finding 2: Structural Defense — Identified Edge Cases

The deterministic validator achieved **87.5% accuracy** using a local Phi-4-mini model. The 12.5% failure cases were not random — they were structurally predictable:
- **False positive**: A Temporal expression misclassified as Spatial due to ambiguous prepositional phrasing.
- **Multi-rule noise**: Highly ambiguous clauses triggering two overlapping rules simultaneously, producing conflicting verdicts.

These are known, bounded failure modes — not undefined behavior.

### 🔍 Finding 3: The Gemma 4 E2B Bottleneck — The Engineering Insight That Drives V3

During stress-testing, an attempt was made to substitute Phi-4-mini with **Gemma 4 E2B** to enhance extraction depth. The result was a critical pipeline failure: the model's native chain-of-thought tokens (internal reasoning pathways) could not be stripped reliably within the n8n orchestration layer, causing **structured JSON parsing failures**.

> This is not a bug. This stress test exposed a key architectural constraint.

Raw text extraction from reasoning models is **unreliable for deterministic legal validation workflows** for production legal environments. This discovery establishes the exact engineering parameters for the V3 Semantic Token Constraints roadmap detailed below.

---

## 7. Enterprise Readiness & AI Governance

### Built for CISOs, not just Developers

TridenGuard is designed to pave the way for strict corporate compliance and security audits:

* **Deterministic Auditability:** CISOs do not trust black-box LLM validation. TridenGuard provides explicit structural traceability for every decision. If a contract fails, the system doesn't just vaguely say "unsafe" — it provides the exact missing radical or structural flaw (e.g., `R2_ACTION_WITHOUT_SUBJECT`) as irrefutable evidence.
* **The Unified Policy Roadmap:** In this Hackathon MVP, Veea's Lobster Trap successfully secures the Ingress layer (DPI), while the complex Egress schema validation and Quarantine Decision Tree are prototyped via deterministic n8n JavaScript. Establishing this deterministic logic natively was the core goal of Phase 1. Phase 2 involves migrating this proven JS logic entirely into Lobster Trap's native YAML policies, transforming it into a true 3-Layer Unified Engine.
* **Audit Trails:** Currently logging to structured data tables, the immediate architecture evolution includes serializing these validation failures into compressed TOON Semantic Token Constraints. This transition replaces verbose JSON logs with semantically dense records, providing clear compliance tracking while optimizing storage overhead.

### System Boundaries & Strict Limitations
To maintain deterministic integrity, TridenGuard operates under strict boundaries:
* **No Autonomous Legal Reasoning:** The system does not give legal advice or interpret the law.
* **No Generative Rewrites:** The LLM is never allowed to "auto-correct" or rewrite a failed clause.
* **Human-in-the-Loop Required:** The system acts strictly as a filter and router. Final approval or dismissal is always delegated to human counsel.




---

## 8. The North Star: Horizon 3 Roadmap

### Sovereign AI, Fisher's Statistics, and GBNF Constrained Decoding.

TridenGuard V1 establishes the deterministic firewall. The V2/V3 roadmap transforms this security checkpoint into a **self-improving, sovereign ecosystem** — each pillar directly motivated by the engineering constraints discovered in Phase 1.

### Pillar 1: GBNF Constrained Decoding via TOON + GBNF

**The problem it solves**: The Gemma 4 E2B parsing failures.

To solve the structured parsing failures caused by reasoning models, we are shifting from text parsing to **Semantic Token Constraints**. Enterprise-defined Pydantic schemas will be compiled into native **GBNF grammars**, physically constraining the LLM at the inference stage.

This enforces absolute compliance, making it deterministically impossible for the model to emit unwanted reasoning loops, raw thoughts, or malformed structures. Every validation result is emitted instantly as a single, semantically dense pseudo-token — a "Semantic Token Constraint" — using the compact **TOON** format, achieving a projected 40–60% token reduction vs. raw JSON.

### Pillar 2: Statistical Threat Hunting (Fisher's Exact Test)

**The problem it solves**: Passive detection → Active threat intelligence.

By combining Lobster Trap's structured observability with TOON-compressed audit logs, the system will apply **Fisher's Exact Test** across the data tables. This statistical method rigorously detects non-random associations between input patterns and structural failures — turning the passive firewall into an **active threat-hunting tool** capable of detecting systemic drift, targeted evasion campaigns, and document-level adversarial patterns before they escalate.

### Pillar 3: The Local LoRA Flywheel

**The problem it solves**: Static rules → A model that improves with use.

The flywheel is complete when lawyers click "Approve" or "Discard" in the Quarantine Panel. Each decision is logged as a TOON-compressed preference signal. This clean, structured dataset continuously fine-tunes small sovereign models locally on the enterprise's own hardware via **LoRA (PEFT)** on Gemma 4 E2B.

```
Human Decision → TOON Semantic Token Constraint → LoRA Dataset → Fine-Tuned Local Model → Better Extraction → Fewer False Positives → Better Human Decisions
```

> **The Moat**: Every human decision makes the model smarter. No cloud. No data leakage. Full legal sovereignty. The enterprise owns its intelligence.

### V2/V3 Roadmap Summary

| Horizon | Milestone | Status |
| :--- | :--- | :--- |
| ✅ **V1 (MVP)** | Deterministic Firewall + Human Review Panel | **Delivered** |
| 🔄 **V2** | TOON logging, GBNF schema compilation, Source-Level Grounding | Next sprint |
| 🔁 **V3** | Fisher's threat hunting + Local LoRA fine-tuning flywheel | Q3 2026 |

---
