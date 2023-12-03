const chatBox = document.getElementById('chat-box');
const submit = document.getElementById('submit');
const messageInput = document.getElementById('message-input');
const add_chat = document.getElementById('add_chat')
var chat_id = 0

submit.onclick = function (event) {
    console.log("click")
    event.preventDefault();
    const message = messageInput.value.trim();
    if (message !== '') {
        sendMessage(message);
        messageInput.value = '';
    }
};

add_chat.onclick = function() {
    // get_chat_id()
    // create_chat()
    var element = document.getElementById("add_chat_popup");
    element.className += (" add_chat_popup_hover");
}

function create_chat(){
    const chat = document.createElement("div");
    chat.innerHTML = "chat1"
    document.getElementById("chats").appendChild(chat);
}

function get_chat_id() {
    chat_id = Math.floor(Math.random() * 10000000) + 1000000;
    // chat_id = 10
    console.log(chat_id)
    ":todo check if id already taken if not creat chat"
    fetch(`/check_id`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ 'chat_id': chat_id})
    })
    .then(response => {
        console.log(response)
        return response.json();
    })
    .then(data => {
        console.log('Message sent successfully:', data);
        if(data["success"] == "false"){
            get_chat_id()
            console.log("the id aleady acupied")
        }
    })
    .catch(error => {
        console.error('Error sending message:', error);
    });
};

function sendMessage(message) {
    const chatId = 'chat1';  // Change this to the desired chat ID
    fetch(`/messages?chatid=${chatId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ 'chat_id': chatId, 'content': message })
    })
    .then(response => {
        console.log(response)
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        console.log(data)
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
