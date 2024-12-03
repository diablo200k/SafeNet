package logger

import (
	"log"
	"os"
)

var logger *log.Logger

func InitLogger() {
	file, _ := os.OpenFile("app.log", os.O_CREATE|os.O_WRONLY|os.O_APPEND, 0666)
	logger = log.New(file, "", log.Ldate|log.Ltime|log.Lshortfile)
}

func Log(message string) {
	logger.Println(message)
}
