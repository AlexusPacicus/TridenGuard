#!/usr/bin/env python3
import json
import requests
import time

def main():
    print("==============================================================")
    print("🛡️  TridenGuard - Live Workflow Benchmark Runner")
    print("==============================================================")
    
    # Load benchmark cases
    try:
        with open("tests/benchmark_cuad_v1.json", "r") as f:
            cases = json.load(f)
    except Exception as e:
        print("❌ Error reading benchmark_cuad_v1.json: {}".format(e))
        return

    print("Loaded {} test cases successfully.".format(len(cases)))
    print("Target Webhook: http://localhost:5678/webhook/tridenguard")
    print("Sending requests...\n")

    headers = {
        "Content-Type": "application/json",
        "x-api-key": "tridenguard_secret_key_2026"
    }

    success_count = 0
    for idx, c in enumerate(cases, 1):
        case_id = c.get("id", "UNKNOWN")
        text = c.get("test_text_mutated", "")
        category = c.get("category", "UNKNOWN")
        rule = c.get("rule", "UNKNOWN")

        print("[{}/{}] ID: {} | Cat: {} | Expected: {}".format(idx, len(cases), case_id, category, rule))
        print("   Clause: \"{}\"".format(text))
        
        payload = {"text": text}
        start_time = time.time()
        try:
            response = requests.post(
                "http://localhost:5678/webhook/tridenguard",
                headers=headers,
                json=payload,
                timeout=10
            )
            elapsed = time.time() - start_time
            if response.status_code == 200:
                print("   ✅ Start Confirmation: {} (took {:.2f}s)".format(response.json(), elapsed))
                success_count += 1
            else:
                print("   ❌ Request failed: Status {} | {}".format(response.status_code, response.text))
        except Exception as e:
            print("   ❌ Network error: {}".format(e))
        print("-" * 60)
        
        # Pause slightly between requests to not overwhelm local Ollama
        time.sleep(0.5)

    print("\n==============================================================")
    print("🎯 Execution Finished: {}/{} requests successfully sent.".format(success_count, len(cases)))
    print("The local n8n workflow is executing the neuro-symbolic analysis")
    print("and Ollama is running the Phi-4 radical extraction in the background.")
    print("All results will be securely logged in your Validation Review Queue!")
    print("==============================================================")

if __name__ == "__main__":
    main()
