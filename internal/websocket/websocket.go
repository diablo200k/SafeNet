package websocket

import (
	"github.com/gorilla/websocket"
)

type WebSocketManager struct {
	clients map[*websocket.Conn]bool
}

func NewWebSocketManager() *WebSocketManager {
	return &WebSocketManager{
		clients: make(map[*websocket.Conn]bool),
	}
}

func (manager *WebSocketManager) AddClient(conn *websocket.Conn) {
	manager.clients[conn] = true
}

func (manager *WebSocketManager) RemoveClient(conn *websocket.Conn) {
	delete(manager.clients, conn)
}
