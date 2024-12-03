package audit

import (
	"bytes"
	"fmt"
	"net"
	"os/exec"

	"github.com/jung-kurt/gofpdf" // Import the PDF library
	"github.com/shirou/gopsutil/cpu"
	"github.com/shirou/gopsutil/disk"
	"github.com/shirou/gopsutil/mem"
	"github.com/yusufpapurcu/wmi"
)

// Application structure for WMI query
type InstalledApp struct {
	Name    string
	Version string
}

// CollectSystemInfo gathers various system information.
func CollectSystemInfo() (string, error) {
	var output bytes.Buffer

	output.WriteString("=== System Audit Report ===\n\n")

	// Get CPU Info
	cpuInfo, err := cpu.Info()
	if err != nil {
		return "", err
	}
	output.WriteString(fmt.Sprintf("CPU: %s\n", cpuInfo[0].ModelName))

	// Get Memory Info
	memInfo, err := mem.VirtualMemory()
	if err != nil {
		return "", err
	}
	output.WriteString(fmt.Sprintf("Total Memory: %.2f GB\n", float64(memInfo.Total)/1e9))

	// Get Disk Info
	diskInfo, err := disk.Usage("/")
	if err != nil {
		return "", err
	}
	output.WriteString(fmt.Sprintf("Total Disk Space: %.2f GB\n", float64(diskInfo.Total)/1e9))

	// Get OS Info
	cmd := exec.Command("wmic", "os", "get", "Caption")
	osVersion, err := cmd.Output()
	if err != nil {
		return "", err
	}
	output.WriteString(fmt.Sprintf("Operating System: %s\n", string(osVersion)))

	// Get Installed Applications using WMI
	var apps []InstalledApp
	query := "SELECT Name, Version FROM Win32_Product"
	if err := wmi.Query(query, &apps); err != nil {
		return "", err
	}

	output.WriteString("\nInstalled Applications:\n")
	for _, app := range apps {
		output.WriteString(fmt.Sprintf(" - %s (Version: %s)\n", app.Name, app.Version))
	}

	// Get IP Address and MAC Address
	output.WriteString("\nNetwork Interfaces:\n")
	interfaces, err := net.Interfaces()
	if err != nil {
		return "", err
	}

	for _, iface := range interfaces {
		if iface.Flags&net.FlagUp != 0 && iface.Flags&net.FlagLoopback == 0 {
			output.WriteString(fmt.Sprintf("Interface: %s\n", iface.Name))
			output.WriteString(fmt.Sprintf("MAC Address: %s\n", iface.HardwareAddr.String()))
			addrs, _ := iface.Addrs()
			for _, addr := range addrs {
				output.WriteString(fmt.Sprintf("IP Address: %s\n", addr.String()))
			}
			output.WriteString("\n")
		}
	}

	return output.String(), nil
}

// GeneratePDF creates a PDF report from the audit information.
func GeneratePDF(reportContent string) error {
	pdf := gofpdf.New("P", "mm", "A4", "")
	pdf.AddPage()
	pdf.SetFont("Arial", "B", 16)
	pdf.Cell(40, 10, "Audit Report")
	pdf.Ln(10)
	pdf.SetFont("Arial", "", 12)

	// Use MultiCell with correct parameters for line height and text wrapping.
	pdf.MultiCell(0, 10, reportContent, "", "", false)

	err := pdf.OutputFileAndClose("AuditReport.pdf")
	if err != nil {
		return err
	}

	return nil
}
