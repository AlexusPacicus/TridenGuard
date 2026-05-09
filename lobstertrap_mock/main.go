package main

import (
	"fmt"
	"os"
	"strings"
)

/**
 * LOBSTER TRAP (Mock Stub) v1.0
 * This is a simulated security engine for TridenGuard.
 * Used for demo portability when the full DPI binary is not available.
 */

func main() {
	if len(os.Args) < 2 {
		fmt.Println("Usage: lobstertrap inspect <prompt> --policy <file>")
		os.Exit(1)
	}

	command := os.Args[1]

	switch command {
	case "inspect":
		handleInspect()
	case "version":
		fmt.Println("Lobster Trap v1.0-mock (Hackathon Edition)")
	default:
		fmt.Printf("Unknown command: %s\n", command)
		os.Exit(1)
	}
}

func handleInspect() {
	// Look for the prompt in the arguments
	prompt := ""
	for i, arg := range os.Args {
		if arg == "inspect" && i+1 < len(os.Args) {
			prompt = os.Args[i+1]
			break
		}
	}

	// Simple heuristic security check
	isUnsafe := strings.Contains(strings.ToLower(prompt), "ignore previous instructions") ||
		strings.Contains(strings.ToLower(prompt), "system override")

	fmt.Println("--- LOBSTER TRAP DPI ANALYSIS ---")
	if isUnsafe {
		fmt.Println("Action: BLOCK")
		fmt.Println("Reason: Potential Prompt Injection detected (Mock Logic)")
		os.Exit(1) // Exit with error code to trigger block in n8n
	} else {
		fmt.Println("Action: ALLOW")
		fmt.Println("Risk Score: 0.15 (Safe)")
	}
}
