package main

import (
	"fmt"
	"log"
	"time"

	"github.com/gorilla/websocket"
)

func main() {
	// Connect to the WebSocket server
	conn, _, err := websocket.DefaultDialer.Dial("ws://localhost:8080/ws", nil)
	if err != nil {
		log.Fatal("Error connecting to server:", err)
	}
	defer conn.Close()

	for {
		// Example of sending a message to the server
		err := conn.WriteMessage(websocket.TextMessage, []byte("Hello Server!"))
		if err != nil {
			log.Println("Error sending message:", err)
			return
		}
		time.Sleep(1 * time.Second)

		// Read messages from the server
		_, msg, err := conn.ReadMessage()
		if err != nil {
			log.Println("Error reading message:", err)
			return
		}
		fmt.Printf("Received from server: %s\n", msg)
	}
}
