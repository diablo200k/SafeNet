const socket = new WebSocket("ws://localhost:8080/ws");

socket.onopen = function() {
    console.log("Connected to the server");
};

socket.onmessage = function(event) {
    const resultsDiv = document.getElementById("audit-results");
    resultsDiv.innerHTML += `<p>${event.data}</p>`;
};

socket.onclose = function(event) {
    console.log(`Connection closed: ${event.code} - ${event.reason}`);
    if (event.code === 1001) {
        alert("The connection was closed because the server is going away.");
        // Optionally, you could try to reconnect here
        // setTimeout(() => { location.reload(); }, 5000); // Reload after 5 seconds
    }
};

function startAudit() {
    socket.send(JSON.stringify({ action: "start_audit" }));
}

function downloadAudit() {
    window.location.href = "/download"; // Redirects to download the PDF
}

function sendCustomCommand() {
    const command = prompt("Enter your command:");
    if (command) {
        socket.send(JSON.stringify({ action: "custom_command", command }));
    }
}