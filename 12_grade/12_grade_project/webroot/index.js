const chatBox = document.getElementById('chat-box');
const submit = document.getElementById('submit');
const messageInput = document.getElementById('message-input');

submit.addEventListener('click', function (event) {
    console.log("click")
    event.preventDefault();
    const message = messageInput.value.trim();
    if (message !== '') {
        sendMessage(message);
        messageInput.value = '';
    }
});

function sendMessage(message) {
    const chatId = 'chat1';  // Change this to the desired chat ID
    fetch(`/messages?chat_id=${chatId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ 'chat_id': chatId, 'content': message })
    })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log('Message sent successfully:', data);
        })
        .catch(error => {
            console.error('Error sending message:', error);
        });
}

function displayMessage(message) {
    const messageElement = document.createElement('p');
    messageElement.textContent = message;
    chatBox.appendChild(messageElement);
    chatBox.scrollTop = chatBox.scrollHeight; // Auto-scroll to the bottom
}

function fetchMessages() {
    const chatId = 'chat1';  // Change this to the desired chat ID
    fetch(`/messages?chat_id=${chatId}`)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            // Clear the chat box before displaying new messages
            chatBox.innerHTML = '';
            data.forEach(message => displayMessage(message.content));
        })
        .catch(error => {
            console.error('Error fetching messages:', error);
        });
}

// Fetch and display messages when the page loads
fetchMessages();

// Set up automatic message refresh every 0.5 seconds (adjust as needed)
setInterval(fetchMessages, 500);
