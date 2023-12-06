const chatBox = document.getElementById('chat-box');
const submit = document.getElementById('submit');
const messageInput = document.getElementById('message-input');
const add_chat = document.getElementById('add_chat')
const x_btn = document.createElement("button")
const submit_chat = document.createElement("button");
const input = document.createElement("input");
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
    var element = document.getElementById("add_chat_popup");
    element.className += (" add_chat_popup_hover");
    while (element.firstChild) {
        element.removeChild(element.firstChild);
    }
    all_addchat()
}

x_btn.onclick = close_popup

submit_chat.onclick = function(){
    console.log("bruh")
    get_chat_id(input.value)
    create_chat(input.value)
    close_popup()
}

function close_popup(){
    var element = document.getElementById("add_chat_popup");
    element.className = ("add_chat_popup");
    const add_chat = document.getElementById("add_chat_popup")
    while (add_chat.firstChild) {
        add_chat.removeChild(add_chat.firstChild);
    }
    input.value = ""
}

function all_addchat(){
    const add_chat = document.getElementById("add_chat_popup")
    x_btn.innerHTML = "x"
    x_btn.className = "x_btn"
    add_chat.appendChild(x_btn)

    input.setAttribute("type", "text"); 
    input.placeholder = "Group name:"
    input.className = "input_chat"
    add_chat.appendChild(input)

    submit_chat.innerHTML = "submit"
    submit_chat.className = "submit_chat"
    add_chat.appendChild(submit_chat)
}

function create_chat(id , chatname){
    const chat = document.createElement("div");
    chat.innerHTML = chatname
    chat.className = "allchats"
    chat.id = id
    document.getElementById("chats").appendChild(chat);
}

async function get_chat_id(name) {
    await fetch(`/check_id?chat_name=${name}`, {
        method: 'Get',
    })
    .then(response => {
        console.log(response)
        return response.json();
    })
    .then(data => {
        console.log('Message sent successfully:', data);
        return data
    })
    .catch(error => {
        console.error('Error sending message:', error);
    });
};

async function get_chats(name) {
    await fetch(`/get_chats`, {
        method: 'Get',
    })
    .then(response => {
        console.log(response)
        return response.json();
    })
    .then(data => {
        console.log('Message sent successfully:', data);
        for (const [id, name] of Object.entries(data)) {
            console.log(id, name);
            create_chat(id, name)
        }
        return data
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
    messageElement.className = "messageElement"
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
get_chats()

// Set up automatic message refresh every 0.5 seconds (adjust as needed)
setInterval(fetchMessages, 500);
