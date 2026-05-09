# 🎯 Construction Sprint: May 11 - May 15

## 🏁 Current Status (Pre-Sprint: May 9-10)
- **✅ Done**: Webhook REST, Lobster Trap DPI, 8-radical ontology, Data Tables structure.
- **🛠️ Prep Phase**: Preparing real court case datasets and defining rejection categories.

## 📅 Sprint Schedule (Execution Phase)

| Date | Goal | Tasks | Priority |
|------|------|-------|----------|
| **Mon May 11** | **Core Engine** | Replace UUIDs, Implement `rejection_reason` logic | 🔥 High |
| **Tue May 12** | **Stress Test** | Run 4 real court cases, refine radical rules | 🔥 High |
| **Wed May 13** | **Human-in-the-Loop** | Connect Frontend UI, Enable Approve/Discard flow | 🔥 High |
| **Thu May 14** | **Final Polish** | UI Aesthetics, Record 3-min Demo Video | 🟡 Medium |
| **Fri May 15** | **Submission** | Prepare 5-page Slide Deck, Final Audit | 🟢 Low |

## 🛠️ Task Breakdown

### 1. Motor & Data (Mon-Tue)
- Implement dynamic tagging for blockages: `hallucination`, `pii_violation`, `missing_actor`, `schema_mismatch`, `malicious_prompt`, `logic_error`.
- Ensure data persistence in n8n Data Tables with clean UUIDs.

### 2. Frontend (Wed)
- Simple panel to fetch "Quarantine" entries.
- POST requests to resolve entries (move to "Audit" or "Discard").

### 3. Demo (Thu)
- Show a real case being blocked.
- Show the human correcting/approving it.
- Show the "Audit Trail" updated.

## ❌ Post-V1 (The "Flywheel" Phase)
- `source_span` grounding.
- JSONL observability.
- Local Fine-tuning (TridenGemma).

---
*Last Updated: 2026-05-09*
