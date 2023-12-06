const serverUrl = 'http://localhost:12345';

// Fetch function to send messages to the server
async function sendMessage(recipient, message) {
    const data = {
        type: 'message',
        recipient,
        message,
    };

    await fetch(serverUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    });
}

// Fetch function to join the chat
async function joinChat(username) {
    const data = {
        type: 'join',
    };

    await fetch(serverUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    });
}

// Example of joining the chat
const username = prompt('Enter your username:');
joinChat(username);
