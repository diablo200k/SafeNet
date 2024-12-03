module safenet

go 1.23.3

require (
	github.com/gorilla/websocket v1.5.3 // For WebSocket support
	github.com/shirou/gopsutil v3.21.11+incompatible // For system information
)

require (
	github.com/go-ole/go-ole v1.2.6 // indirect; For Windows COM interaction
	github.com/stretchr/testify v1.10.0 // indirect
	github.com/tklauser/go-sysconf v0.3.14 // indirect; For system configuration
	github.com/tklauser/numcpus v0.8.0 // indirect; For CPU count
	github.com/yusufpapurcu/wmi v1.2.4 // indirect; For Windows Management Instrumentation
	golang.org/x/sys v0.27.0 // indirect; For low-level system calls
)

require github.com/jung-kurt/gofpdf v1.16.2 // indirect
