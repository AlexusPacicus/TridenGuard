#!/bin/bash

# TridenGuard Test Runner
# Use this script to run the 8 atomic rules tests.

echo "🛡️ TridenGuard Test Suite"
echo "------------------------"
echo "IMPORTANT: n8n test webhooks only accept ONE request per execution."
echo "Please click 'Execute Workflow' in the n8n UI before each case."
echo ""

ENDPOINT="http://localhost:5678/webhook-test/tridenguard"
DATA_FILE="tests/test_data.json"

for i in {0..7}; do
  id=$(jq -r ".test_cases[$i].id" "$DATA_FILE")
  text=$(jq -r ".test_cases[$i].text" "$DATA_FILE")
  
  echo ">>> Case [$((i+1))/8]: $id"
  echo "Input: $text"
  read -p "Press Enter after clicking 'Execute Workflow' in n8n..."
  
  curl -s -X POST "$ENDPOINT" \
    -H "Content-Type: application/json" \
    -d "{\"text\": \"$text\"}"
  
  echo -e "\n------------------------\n"
done

echo "✅ All tests completed."
