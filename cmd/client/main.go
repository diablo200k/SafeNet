package main

import (
	"fmt"
	"log"
	"github.com/gorilla/websocket"
	"os"
)

func connectToServer() {
	serverURL := "ws://localhost:8080/ws"
	fmt.Printf("Connexion au serveur WebSocket à %s...\n", serverURL)

	// Se connecter au serveur WebSocket
	conn, _, err := websocket.DefaultDialer.Dial(serverURL, nil)
	if err != nil {
		log.Fatalf("Erreur de connexion: %v\n", err)
		os.Exit(1)
	}
	defer conn.Close()

	fmt.Println("Connecté au serveur WebSocket")

	// Envoyer un message initial
	message := "Hello, serveur WebSocket!"
	err = conn.WriteMessage(websocket.TextMessage, []byte(message))
	if err != nil {
		log.Println("Erreur lors de l'envoi du message:", err)
		return
	}

	// Lire la réponse du serveur
	_, response, err := conn.ReadMessage()
	if err != nil {
		log.Println("Erreur lors de la lecture du message:", err)
		return
	}
	fmt.Printf("Réponse du serveur: %s\n", response)
}

func main() {
	// Se connecter au serveur WebSocket
	connectToServer()
}
