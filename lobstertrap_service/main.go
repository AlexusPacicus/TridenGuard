package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"os"
	"regexp"
	"strings"
)

/**
 * LOBSTER TRAP (Mock Stub) v1.1
 * Now with HTTP REST API support for Hackathon deployment.
 */

type InspectRequest struct {
	Text   string `json:"text"`
	Policy string `json:"policy"`
}

type InspectResponse struct {
	Action    string  `json:"action"`
	RiskScore float64 `json:"risk_score"`
	Reason    string  `json:"reason,omitempty"`
}

func main() {
	if len(os.Args) < 2 {
		printUsage()
		os.Exit(1)
	}

	command := os.Args[1]

	switch command {
	case "inspect":
		handleInspectCLI()
	case "serve":
		handleServe()
	case "version":
		fmt.Println("Lobster Trap v1.1-mock (Service Edition)")
	default:
		fmt.Printf("Unknown command: %s\n", command)
		printUsage()
		os.Exit(1)
	}
}

func printUsage() {
	fmt.Println("Usage:")
	fmt.Println("  lobstertrap inspect <prompt> --policy <file>   (CLI mode)")
	fmt.Println("  lobstertrap serve --port <number>              (HTTP Service mode)")
}

func handleInspectCLI() {
	prompt := ""
	for i, arg := range os.Args {
		if arg == "inspect" && i+1 < len(os.Args) {
			prompt = os.Args[i+1]
			break
		}
	}
	action, score, reason := analyze(prompt)
	fmt.Println("--- LOBSTER TRAP DPI ANALYSIS ---")
	fmt.Printf("Action: %s\n", action)
	if reason != "" {
		fmt.Printf("Reason: %s\n", reason)
	} else {
		fmt.Printf("Risk Score: %.2f (Safe)\n", score)
	}
	if action == "BLOCK" {
		os.Exit(1)
	}
}

func analyze(text string) (string, float64, string) {
    lower := strings.ToLower(text)
    
    // Prompt injection
    if strings.Contains(lower, "ignore previous instructions") ||
       strings.Contains(lower, "system override") ||
       strings.Contains(lower, "ignore all previous") {
        return "BLOCK", 0.95, "Potential Prompt Injection detected"
    }
    
    // PII Detection
    ssnPattern := regexp.MustCompile(`\b\d{3}-\d{2}-\d{4}\b`)
    emailPattern := regexp.MustCompile(`\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b`)
    phonePattern := regexp.MustCompile(`\b\d{3}[-.]?\d{3}[-.]?\d{4}\b`)
    dobPattern := regexp.MustCompile(`\bDOB\b.*\d{2}/\d{2}/\d{4}`)
    
    if ssnPattern.MatchString(text) || dobPattern.MatchString(lower) {
        return "BLOCK", 0.90, "PII detected (SSN, DOB)"
    }
    if emailPattern.MatchString(text) {
        return "BLOCK", 0.85, "PII detected (email)"
    }
    if phonePattern.MatchString(text) {
        return "BLOCK", 0.80, "PII detected (phone)"
    }
    
    // Data exfiltration
    if strings.Contains(lower, "https://") && 
       (strings.Contains(lower, "external") || strings.Contains(lower, "exfiltrat")) {
        return "BLOCK", 0.95, "Data exfiltration attempt detected"
    }
    
    return "ALLOW", 0.15, ""
}

func handleServe() {
	port := "8080"
	for i, arg := range os.Args {
		if arg == "--port" && i+1 < len(os.Args) {
			port = os.Args[i+1]
			break
		}
	}

	http.HandleFunc("/inspect", func(w http.ResponseWriter, r *http.Request) {
		if r.Method != http.MethodPost {
			http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
			return
		}

		var req InspectRequest
		if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
			http.Error(w, "Bad request", http.StatusBadRequest)
			return
		}

		action, score, reason := analyze(req.Text)
		
		w.Header().Set("Content-Type", "application/json")
		json.NewEncoder(w).Encode(InspectResponse{
			Action:    action,
			RiskScore: score,
			Reason:    reason,
		})
	})

	fmt.Printf("Lobster Trap Mock Service listening on port %s...\n", port)
	log.Fatal(http.ListenAndServe(":"+port, nil))
}

