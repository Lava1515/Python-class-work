let pesemtdata = document.getElementById("presntdata");

const socket = new WebSocket("ws://localhost:5000");

socket.onopen = () => {
    console.log("WebSocket connection established.");
    sendData(); // Initial request after WebSocket connection is established
};

socket.onmessage = (event) => {
    let data = JSON.parse(event.data);
    console.log(data);
    pesemtdata.innerHTML = data;
};

socket.onerror = (error) => {
    console.error("WebSocket error:", error);
};

function sendData() {
    console.log("Sending data request...");
    socket.send("get_data");
}

