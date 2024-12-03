package utils

import (
	"os/exec"
	"strings"
)

func GetCPUUsage() (string, error) {
	out, err := exec.Command("wmic", "cpu", "get", "loadpercentage").Output() // Adjust for different OS
	if err != nil {
		return "", err
	}
	return strings.TrimSpace(string(out)), nil
}

func GetActiveProcesses() ([]string, error) {
	out, err := exec.Command("tasklist").Output() // Adjust for different OS
	if err != nil {
		return nil, err
	}
	return strings.Split(strings.TrimSpace(string(out)), "\n"), nil
}
