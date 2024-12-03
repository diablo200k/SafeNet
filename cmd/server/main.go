package main

import (
	"fmt"
	"log"
	"net/http"
	"github.com/gorilla/websocket"
	"os"
)

var upgrader = websocket.Upgrader{
	CheckOrigin: func(r *http.Request) bool {
		// Vérifie si l'origine est valide (à personnaliser si nécessaire)
		return true
	},
}

func handleConnection(conn *websocket.Conn) {
	defer conn.Close()
	fmt.Println("Nouveau client connecté:", conn.RemoteAddr())

	for {
		// Lire le message depuis le client
		_, msg, err := conn.ReadMessage()
		if err != nil {
			log.Println("Erreur de lecture du message:", err)
			break
		}

		// Affiche le message reçu
		fmt.Println("Message reçu:", string(msg))

		// Traitement des messages (par exemple audit, récupération des infos système)
		// Répondre au client
		err = conn.WriteMessage(websocket.TextMessage, []byte("Message reçu: "+string(msg)))
		if err != nil {
			log.Println("Erreur d'envoi de message:", err)
			break
		}
	}
}

func startServer() {
	http.HandleFunc("/ws", func(w http.ResponseWriter, r *http.Request) {
		conn, err := upgrader.Upgrade(w, r, nil)
		if err != nil {
			log.Println("Erreur de mise à niveau WebSocket:", err)
			return
		}
		handleConnection(conn)
	})

	port := "8080"
	fmt.Printf("Serveur WebSocket démarré sur ws://localhost:%s\n", port)
	err := http.ListenAndServe(":"+port, nil)
	if err != nil {
		log.Fatalf("Erreur de démarrage du serveur: %v\n", err)
	}
}

func main() {
	// Lancer le serveur WebSocket
	startServer()
}
