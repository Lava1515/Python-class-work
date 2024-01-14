const chatBox = document.getElementById('chat-box');
const Send = document.getElementById('Send');
const messageInput = document.getElementById('message-input');
const add_chat = document.getElementById('add_chat')
const x_btn = document.createElement("button")
const input = document.createElement("input");
const currentUsername = sessionStorage.getItem('username');
console.log(currentUsername)
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
    var add_chat_popup = document.getElementById("add_chat_popup")
    add_chat_popup.className += (" add_chat_popup_hover");
    while (add_chat_popup.firstChild) {
        add_chat_popup.removeChild(element.firstChild);
    }
    x_btn.innerHTML = "x"
    x_btn.className = "x_btn"
    add_chat_popup.appendChild(x_btn)
    const contact_button = document.createElement("button");
    const group_button = document.createElement("button");

    contact_button.innerHTML = "add contact"
    contact_button.className = "add_contacts"
    add_chat_popup.appendChild(contact_button)

    group_button.innerHTML = "add groups"
    group_button.className = "add_groups"
    add_chat_popup.appendChild(group_button)


    contact_button.onclick = add_contact
    group_button.onclick = addchat
}

x_btn.onclick = close_popup

function close_popup(){
    var element = document.getElementById("add_chat_popup");
    element.className = "add_chat_popup";
    const add_chat = document.getElementById("add_chat_popup")
    while (add_chat.firstChild) {
        add_chat.removeChild(add_chat.firstChild);
    }
    input.value = ""
}


function add_contact(){
    var add_chat_popup = document.getElementById("add_chat_popup");
    var submit_chat = document.createElement("button");
    while (add_chat_popup.firstChild) {
        add_chat_popup.removeChild(add_chat_popup.firstChild);
    }

    x_btn.innerHTML = "x";
    x_btn.className = "x_btn";
    add_chat_popup.appendChild(x_btn);

    input.setAttribute("type", "text"); 
    input.placeholder = "username:";
    input.className = "input_chat";
    add_chat_popup.appendChild(input);

    submit_chat.innerHTML = "submit";
    submit_chat.className = "submit_chat";
    add_chat_popup.appendChild(submit_chat);

    submit_chat.onclick = function(){
        fetch(`/add_friend`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({"user_to_add": input.value, "current_user": currentUsername})
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log('Message sent successfully:', data);
            if(data["Add_successfully"] == "false"){
                let not_user = document.createElement("h3")
                not_user.className = ""
                console.log("username not exixt")
            }
        })
        .catch(error => {
            console.error('Error sending message:', error);
        });
    }
}


function addchat(){
    var add_chat_popup = document.getElementById("add_chat_popup");
    var submit_chat = document.createElement("button");
    while (add_chat_popup.firstChild) {
        add_chat_popup.removeChild(add_chat_popup.firstChild);
    }
    x_btn.innerHTML = "x"
    x_btn.className = "x_btn"
    add_chat_popup.appendChild(x_btn)

    input.setAttribute("type", "text"); 
    input.placeholder = "Group name:"
    input.className = "input_chat"
    add_chat_popup.appendChild(input)

    submit_chat.innerHTML = "submit"
    submit_chat.className = "submit_chat"
    add_chat_popup.appendChild(submit_chat)

    submit_chat.onclick = function(){
        console.log("bruh")
        if(input.value != ""){
            var data = get_chat_id(input.value)
            create_chat(data["the_id"] ,input.value)
            close_popup()
        }
        else{
            console.log("the input has to be more then 0 ")
        }
    }
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

async function get_chat_id(name) {
    console.log("getid")
    fetch(`/get_id`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({"current_user": currentUsername , 'chat_name': name})
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
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
    await fetch(`/get_chats?${currentUsername}`, {
        method: 'Get',
    })
    .then(response => {
        return response.json();
    })
    .then(data => {
        console.log(data)
        for (const [id, data_] of Object.entries(data)) {
            if(data_["chat_name"] != undefined){
                console.log(data_["chat_name"])
                create_chat(id, data_["chat_name"])
            }
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
        body: JSON.stringify({"current_user": currentUsername , 'chat_id': current_chat, 'content': message })
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
