package main

import (
	"encoding/json"
	"log"
	"net/http"
	"safenet/internal/audit" // Adjusted import path for the audit package.

	"github.com/gorilla/websocket"
)

var upgrader = websocket.Upgrader{
	CheckOrigin: func(r *http.Request) bool {
		return true // Allow all origins for development purposes.
	},
}

func handleConnection(w http.ResponseWriter, r *http.Request) {
	conn, err := upgrader.Upgrade(w, r, nil)
	if err != nil {
		log.Println("Error during connection upgrade:", err)
		return
	}
	defer conn.Close()

	log.Println("Client connected")

	for {
		messageType, msg, err := conn.ReadMessage()
		if err != nil {
			log.Println("Error reading message:", err)
			break
		}

		var actionMsg map[string]interface{}
		json.Unmarshal(msg, &actionMsg)

		switch actionMsg["action"] {
		case "start_audit":
			result, _ := audit.CollectSystemInfo() // Call the audit function to collect system info.
			conn.WriteMessage(messageType, []byte(result))

			// Generate PDF report after collecting info.
			if err := audit.GeneratePDF(result); err != nil {
				log.Println("Error generating PDF:", err)
			} else {
				log.Println("PDF report generated successfully.")
			}

		case "view_audit_results":
			results := "Audit results" // Placeholder for actual results retrieval logic.
			conn.WriteMessage(messageType, []byte(results))

		case "custom_command":
			command := actionMsg["command"].(string)
			response := "Executed command: " + command // Placeholder for command execution logic.
			conn.WriteMessage(messageType, []byte(response))

		default:
			log.Println("Unknown action:", actionMsg["action"])
		}
	}
}

// New handler to serve the PDF file
func downloadPDF(w http.ResponseWriter, r *http.Request) {
	http.ServeFile(w, r, "AuditReport.pdf") // Serve the generated PDF file
}

func main() {
	http.HandleFunc("/ws", handleConnection)
	http.HandleFunc("/download", downloadPDF) // Register the download route
	log.Println("Server started on :8080")
	log.Fatal(http.ListenAndServe(":8080", nil))
}
