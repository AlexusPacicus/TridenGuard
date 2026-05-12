from flask import Flask, request, jsonify
import requests
import json
import uuid
from datetime import datetime
from models import ExtractionResult, ValidationResult
from validator import validate_extraction

app = Flask(__name__)

OLLAMA_URL = "http://localhost:11434/api/generate"

SYSTEM_PROMPT = """Role: Senior AI Engineer / Legal Ontologist.

Task: Extract foundational facts (axioms) and their atomic components (radicals) from legal or technical text.

Atomic radicals (ontology of 8):
- Actor: entity explicitly named as performing the action. who.
- Action: the core activity or verb explicitly stated. does what.
- Object: the target or entity explicitly affected by the action. to what/whom.
- Deontic: the nature of the rule (obligation, permission, prohibition). must/may/must not.
- Condition: prerequisites or triggers explicitly stated. if.
- Temporal: time constraints, deadlines, periods explicitly stated. when.
- Spatial: geographic or location constraints explicitly stated. where.
- Metric: measurable values, thresholds, limits explicitly stated. how much.

Must:
1. only extract radicals that are explicitly stated in the text.
2. if no actor is explicitly named, omit the actor radical.
3. prioritize Action as the core radical. if there is no Action, keep radicals to a minimum.
4. prefer fewer radicals over inventing one. 2 radicals is better than 4 with one invented.
5. if a radical type is uncertain, omit it.
6. every radical object must have exactly two keys: "radical" and "value".
7. return valid JSON only. no markdown. no explanation.

Must not:
1. invent a radical that is not explicitly in the text.
2. extract Metric from a Temporal expression, or Temporal from a Spatial one.
3. extract Deontic and Action as the same radical.
4. use the radical name as a key directly.
5. pad the output to reach a higher number of radicals.
6. include your thinking process, reasoning, or explanations in the output.

Examples of correct extraction:

Text: "The contractor must complete the installation within 30 days."
Output: {"axiom": "Contractor must complete installation within 30 days.", "radicals": [{"radical": "Actor", "value": "contractor"}, {"radical": "Deontic", "value": "must"}, {"radical": "Action", "value": "complete the installation"}, {"radical": "Object", "value": "the installation"}, {"radical": "Temporal", "value": "30 days"}]}

Text: "The report must be submitted before Friday."
Output: {"axiom": "The report must be submitted before Friday.", "radicals": [{"radical": "Action", "value": "submit the report"}, {"radical": "Object", "value": "the report"}, {"radical": "Deontic", "value": "must"}, {"radical": "Temporal", "value": "before Friday"}]}

Text: "Any act violating the regulation is strictly prohibited."
Output: {"axiom": "Any act violating the regulation is strictly prohibited.", "radicals": [{"radical": "Deontic", "value": "prohibited"}, {"radical": "Object", "value": "any act violating the regulation"}]}

Text: "The profitability threshold is set at 15%."
Output: {"axiom": "The profitability threshold is set at 15%.", "radicals": [{"radical": "Metric", "value": "15%"}]}

Text: "Whenever the index exceeds 3.5% for two consecutive quarters."
Output: {"axiom": "Whenever the index exceeds 3.5% for two consecutive quarters.", "radicals": [{"radical": "Condition", "value": "whenever the index exceeds 3.5%"}, {"radical": "Temporal", "value": "two consecutive quarters"}]}

Only output the JSON object. No additional text."""

@app.route('/validate', methods=['POST'])
def validate():
    data = request.json
    if not data or 'text' not in data:
        return jsonify({"error": "Missing 'text' in payload"}), 400
        
    source_text = data['text']
    
    payload = {
        "model": "phi4-mini:3.8b",
        "prompt": source_text,
        "system": SYSTEM_PROMPT,
        "format": "json",
        "stream": False
    }
    
    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=60)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Ollama connection failed: {str(e)}"}), 502
        
    try:
        ollama_data = response.json()
        llm_response_text = ollama_data.get("response", "{}")
        extracted_json = json.loads(llm_response_text)
    except (json.JSONDecodeError, ValueError) as e:
        return jsonify({"error": f"Failed to parse Ollama JSON response: {str(e)}"}), 502
        
    try:
        extraction = ExtractionResult(**extracted_json)
    except Exception as e:
        return jsonify({"error": f"Validation of extraction failed: {str(e)}"}), 422
        
    validation_dict = validate_extraction(extraction, source_text)
    
    status = "VALIDATED" if validation_dict["has_validated"] else "QUARANTINED"
    rejection_reason = "Passed all checks" if validation_dict["has_validated"] else f"Failed validation: {', '.join(validation_dict['errors'])}"
    
    result = ValidationResult(
        case_id=str(uuid.uuid4()),
        timestamp=datetime.utcnow().isoformat() + "Z",
        source_text=source_text,
        extraction=extraction,
        status=status,
        rejection_reason=rejection_reason,
        errors=validation_dict["errors"],
        source_integrity=validation_dict["source_integrity"],
        ungrounded_radicals=validation_dict["ungrounded_radicals"],
        has_critical=validation_dict["has_critical"],
        has_warning=validation_dict["has_warning"],
        has_unknown=validation_dict["has_unknown"],
        has_validated=validation_dict["has_validated"],
        error_count=validation_dict["error_count"]
    )
    
    return jsonify(result.model_dump())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
