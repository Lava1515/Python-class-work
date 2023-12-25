const chatBox = document.getElementById('chat-box');
const Send = document.getElementById('Send');
const messageInput = document.getElementById('message-input');
const add_chat = document.getElementById('add_chat')
const x_btn = document.createElement("button")
const submit_chat = document.createElement("button");
const input = document.createElement("input");
input.maxLength = 20
let current_chat = "chat1"
var chat_id = 0

Send.onclick = function (event) {
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
    if(input.value != ""){
        get_chat_id(input.value)
        close_popup()
    }
    else{
        console.log("the input need to have value")
    }
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
    chat.addEventListener("click", function(){curront_chat_update(id)});
}

function curront_chat_update(id){
    console.log("update_chat" , id)
    current_chat = id
    fetchMessages();
}

function get_chat_id(name) {
    fetch(`/get_id`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ 'chat_name': name})
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        console.log('Message sent successfully:', data);
        create_chat(data["the_id"], name)
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
        return response.json();
    })
    .then(data => {
        console.log(data)
        for (const [id, data_] of Object.entries(data)) {
            console.log(data_["chat_name"])
            create_chat(id, data_["chat_name"])
        }
        return data
    })
    .catch(error => {
        console.error('Error sending message:', error);
    });
};

function sendMessage(message) {
    fetch(`/send_messages`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ 'chat_id': current_chat, 'content': message })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        console.log(response)
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
    fetch(`/get_messages?chat_id=${current_chat}`)
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
            // console.error('Error fetching messages:', error);
        });
}


// Fetch and display messages when the page loads
fetchMessages();
get_chats()

// Set up automatic message refresh every 0.5 seconds (adjust as needed)
setInterval(fetchMessages, 500);
