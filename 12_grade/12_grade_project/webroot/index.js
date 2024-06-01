const ip = document.location.origin.split(":")[1];
console.log(ip);
const webSocket = new WebSocket("ws:" + ip + ":8765")
console.log("ws:" + ip + ":8765")
const currentUsername = sessionStorage.getItem('username')
let target_username = currentUsername;
const copen_chat = document.getElementById('open_chat')
const chat_div = document.getElementById("chat_div")
const selectElement = document.getElementById("dates")
const trainers_select = document.getElementById("trainers_select")
const the_chat = document.getElementById("messages")
const ctx = document.getElementById('myChart').getContext('2d');
const numColumns = 100;
let startIndex = 0;
let currentChatId = "";

// Generate labels from 100 to 1 (assuming numColumns is 100)
const labels = Array.from({ length: numColumns }, (_, i) => numColumns - i);

let dataList = []

GetPermissions()
document.getElementById('loged_as').innerHTML = "looged in as " + currentUsername
SetDates()

const chart = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: labels,
        datasets: [{
            label: 'beats per minute',
            data: getDataSlice(),
            backgroundColor: 'rgba(255, 98, 0, 0.65)',
            borderColor: 'rgba(255, 189, 0, 1)',
            borderWidth: 1
        }]
    },
    options: {
        scales: {
            x: {
                reverse: true // Option to reverse the x-axis
            },
            y: {
                beginAtZero: true
            }
        }
    }
});



selectElement.addEventListener('change', () => {
    const selectedValue = selectElement.value;
    console.log('Selected date:', selectedValue);
    startIndex = 0;
    get_date_bpms(selectedValue)
});

trainers_select.addEventListener('change', () => {
    const selectedValue = trainers_select.value;
    target_username = selectedValue;
    for (var i = selectElement.options.length - 1; i > 0; i--) {
        selectElement.remove(i);
    }
    SetDates()
});  

document.getElementById('logout').onclick = function(){
    sessionStorage.setItem('username',  null);
    window.location.href = "login.html"
};

webSocket.onopen = function(event) {
    console.log("WebSocket connection established.");
    webSocket.send(currentUsername);
};

// webSocket.onmessage = function(event) {
//     const messageDiv = document.createElement("div");
//     messageDiv.textContent = event.data;
//     console.log(messageDiv.textContent )
//     document.getElementById("messages").appendChild(messageDiv);
// };

// function sendMessage(sendto) {
//     const messageInput = document.getElementById("messageInput");
//     const message = {"FromUser":currentUsername, "SendTo": sendto , "message": messageInput.value}
//     webSocket.send(message);
//     messageInput.value = "";
// }

// // Add event listener for Enter key press
// document.getElementById("messageInput").addEventListener("keypress", function(event) {
//     if (event.key === "Enter") {
//         sendMessage();
//     }
// });


document.getElementById('next').addEventListener('click', () => {
    if (startIndex > 0) {
        startIndex -= 10;
        updateChart();
    }
});

document.getElementById('prev').addEventListener('click', () => {
    if (startIndex < dataList.length) {
        startIndex += 10;
        updateChart();
    }
});

document.getElementById('chat_settings_button').addEventListener('click', () => {
    const popup_div = document.createElement("div");
    create_popup(popup_div)
    const add_contact = document.createElement("button");
    const leave_group = document.createElement("button");
    add_contact.innerHTML = "add contact"
    leave_group.innerHTML = "leave groupp"
    add_contact.className = "add_contact"
    leave_group.className = "leave_group"
    popup_div.appendChild(add_contact);
    popup_div.appendChild(leave_group);
    add_contact.onclick= async function(){
        console.log("add_contact")
        const pop_up = create_middle_popup()
        createDropdown(pop_up)
    }
    leave_group.onclick= async function(){
        console.log("leave_group")
        const pop_up = create_middle_popup()
    }
});

document.getElementById('add_button').onclick = function(){
    const popup_div = document.createElement("div");
    create_popup(popup_div)
    const add_contact = document.createElement("button");
    const create_group = document.createElement("button");
    add_contact.innerHTML = "add contact"
    create_group.innerHTML = "create group"
    add_contact.className = "add_contact"
    create_group.className = "create group"
    popup_div.appendChild(add_contact);
    popup_div.appendChild(create_group);
    add_contact.onclick= async function(){
        console.log("add_contact")
        add_middle_popup("add_contact")
    }
    create_group.onclick= async function(){
        console.log("create_group")
        add_middle_popup("create_group")
    }
    console.log(chat_div.children);
}


document.getElementById("Send").onclick = async function(){
    let message = document.getElementById("message-input")
    console.log(currentChatId)
    console.log(message.value)
    create_message(message.value, currentUsername, get_time())
    let data = await fetch(`send_message`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({"id": currentChatId,"current_user": currentUsername, "message":message.value})
    });
    const response = await data.json();
    console.log(response)
}

document.getElementById("open_arduino").onclick = function(){
    const random_str = generateRandomString()
    webSocket.send("random_str: " + random_str)
    const LocalWebSocket = new WebSocket('ws://127.0.0.1:8080');

    LocalWebSocket.onopen = function(event) {
        console.log("WebSocket connection established.");
        LocalWebSocket.send(currentUsername + ip + ":8765" +"//" +  random_str);

    };
    
    LocalWebSocket.onmessage = function(event) {
        console.log(event.data);
    };
    LocalWebSocket.onerror = function(event) {
        alert('Couldnt connect to Arduino');
    };
}

copen_chat.onclick = function(){
    const existingPopup = document.querySelector('.middle_popup');
    // If it exists, remove it
    if(existingPopup) {
        existingPopup.parentNode.removeChild(existingPopup);
    }
    for (let i = 0; i < chat_div.children.length; i++) {
        if (chat_div.children[i].className === "add_popup") {
            exists = true;
            chat_div.removeChild(chat_div.children[i]);
            break;
        }
    }
    if (chat_div.style.display === "none") {
        chat_div.style.display = "block";
        copen_chat.classList.remove("chatbuttonslideOutToRight")
        chat_div.classList.remove("slideOutToRight")
        copen_chat.classList.add("chatbuttonslideInFromRight")
        chat_div.classList.add("slideInFromRight")
    } else {
        copen_chat.classList.remove("chatbuttonslideInFromRight")
        chat_div.classList.remove("slideInFromRight")
        copen_chat.classList.add("chatbuttonslideOutToRight")
        chat_div.classList.add("slideOutToRight")
        setTimeout(() => {
            chat_div.style.display = "none";
        }, 1000);
    }
    getChats()
}

function create_popup(popup_div){
    popup_div.className = "add_popup"; // Corrected: popup_div instead of div
    let exists = false;
    // Check if popup_div already exists as a child of chat_div
    for (let i = 0; i < chat_div.children.length; i++) {
        if (chat_div.children[i].className === "add_popup") {
            exists = true;
            chat_div.removeChild(chat_div.children[i]);
            break;
        }
    }
    if(!exists){
        chat_div.appendChild(popup_div);
    }
}

//Functions 
async function GetPermissions(){
    let data = await fetch(`/get_Permissions`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({"current_user": currentUsername})
    });

    const response = await data.json();
    console.log(response);

    if (response["Permissions"] === "Coach"){
        let trainer_list = await GetTrainers();  // Use await here
        console.log(trainer_list);

        if (Array.isArray(trainer_list)) {
            trainers_select.style.display = "block";
            trainer_list.forEach(name => {
                const newOption = document.createElement('option');
                newOption.value = name;
                newOption.text = name;
                trainers_select.appendChild(newOption);
            });
        } else {
            console.error('GetTrainers did not return an array');
        }
    }
}

async function GetTrainers(){
    let data = await fetch(`/get_trainers`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({"current_user": currentUsername})
    });

    const response = await data.json();
    console.log(response)
    return response["Trainers"];
}
async function GetBpmsDates(){
    let data = await fetch(`get_bpms_dates`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({"current_user": target_username})
    });
    
    const response = await data.json();
    console.log(response)
    return response
}
async function SetDates(){
    console.log()
    dates = await GetBpmsDates()
    dates = dates["dates"]
    console.log(dates)
    dates.forEach(date => {
        const newOption = document.createElement('option');
        newOption.value = date;
        newOption.text = date;
        selectElement.appendChild(newOption);
    });
}
async function get_date_bpms(Value){
    let data = await fetch(`get_date_bpms`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({"current_user": target_username , "date": Value})
    });
    console.log(data)
    const response = await data.json();
    dataList = response["bpms"]
    updateChart()
    console.log(dataList)
    console.log(startIndex)
}
function generateRandomString(length = 50) {
    const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*';
    let randomString = '';
    for (let i = 0; i < length; i++) {
        const randomIndex = Math.floor(Math.random() * characters.length);
        randomString += characters[randomIndex];
    }
    return randomString;
}
function add_middle_popup(type) {
    // Check if .middle_popup already exists
    dict = {"add_contact": "Contact name" , "create_group": "Group name"}
    
    const pop_up = create_middle_popup();
    const input = document.createElement("input");
    input.className = "pop_up_input"
    input.type = "text";
    input.placeholder = dict[type]
    pop_up.appendChild(input);
    const submitButton = document.createElement("button");
    pop_up.appendChild(submitButton);
    submitButton.type = "button"; // Set type to "button" to prevent form submission
    submitButton.textContent = "Submit";
    submitButton.addEventListener("click", async () => {
        const inputValue = input.value.trim(); // Get input value and remove leading/trailing spaces
        if (inputValue) {
            const data = await fetch(`/${type}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({"current_user": currentUsername, 'chat_name': inputValue})
            });
            const response = await data.json();
            console.log(response)
            // Handle response as needed
            try{
                if(response["added_chat"] == "true"){
                    create_chat(inputValue, response["id"]);
                }
            }catch(error){
                console.log(error);
            }
        } else {
            // Handle case where input is empty
            alert("Please enter a value before submitting.");
        }
    });
}
function create_middle_popup(){
    const existingPopup = document.querySelector('.middle_popup');
    const x_btn = document.createElement("button")
    // If it exists, remove it
    if(existingPopup) {
        existingPopup.parentNode.removeChild(existingPopup);
    }
    // Create and append new .middle_popup element
    const pop_up = document.createElement("div");
    pop_up.className = "middle_popup";
    
    x_btn.innerHTML = "x";
    x_btn.className = "x_btn";
    x_btn.onclick= function(){
        const existingPopup = document.querySelector('.middle_popup');
        // If it exists, remove it
        if(existingPopup) {
            existingPopup.parentNode.removeChild(existingPopup);
        }
    }
    pop_up.appendChild(x_btn);
    document.body.appendChild(pop_up);
    return pop_up;
}
function getDataSlice() {
    console.log(dataList.slice(startIndex - numColumns, startIndex))
    return dataList.reverse().slice(startIndex , startIndex + numColumns);
}
function updateChart() {
    chart.data.datasets[0].data = getDataSlice();
    chart.update();
}
async function getChats(){
    let data = await fetch(`get_chats`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({"current_user": currentUsername})
    });
    const response = await data.json();
    console.log(response)
    create_chats(response)
}
function create_chats(chat_dict) {
    // Get the element with id "chats"
    const chats = document.getElementById("chats");

    // Iterate through the keys (chat IDs) in the chat_dict
    for (const id in chat_dict) {
        if (chat_dict.hasOwnProperty(id)) {
            // Check if a chat with this ID already exists
            if (!document.getElementById(id)) {
                // Get the chat name corresponding to the current ID
                const chatname = chat_dict[id];
                create_chat(chatname, id)
            }
        }
    }
}
function create_chat(chatname, id) {
     // Create a new div element for the chat
     const chat = document.createElement("div");
     // Set the inner HTML to the chat name
     chat.innerHTML = chatname;
     // Set the class name for styling
     chat.className = "chat";
     // Set a unique ID for the chat
     chat.id = id;
     // Append the chat element to the chats container
     chats.appendChild(chat);
     // Add a click event listener to switch chats
     chat.addEventListener("click", function() {
         switch_chat(id); // Pass the id to the switch_chat function
         document.getElementById("chat_name").innerHTML = chat.innerHTML;
    });
}
async function switch_chat(id) {
    console.log("Switching to chat:", id);
    currentChatId = id
    const backButton = document.getElementById("back_button");
    const chats_container = document.getElementById("chats_container")
    const in_chat_container =  document.getElementById("in_chat_container")
    in_chat_container.style.display = "block";
    chats_container.style.display = "none";
    add_messages()
    backButton.onclick = function(){
        chats_container.style.display = "block";
        in_chat_container.style.display = "none";
    }
}
async function get_messages(){
    let data = await fetch(`get_messages`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({"id": currentChatId})
    });
    const response = await data.json();
    console.log(response)
    return response
}
async function add_messages(){
    remove_messages()
    let messages = await get_messages()
    console.log(messages)
    for (const [_date, data] of Object.entries(messages)) {
        console.log(data)
        _message = data.split("|")[0];
        _name = data.split("|")[1];
        console.log(_message);
        create_message(_message, _name,  _date.split(" ")[1].split(";").slice(0, 2).join(":"));
    }
}
function remove_messages() {
    while (the_chat.lastChild) {
        the_chat.removeChild(the_chat.lastChild);
      }
}
function create_message(msg, name, _date){
    let message_container = document.createElement("div");
    let message = document.createElement("h5");
    let date = document.createElement("i");
    let name_ = document.createElement("i");

    message_container.className = "message_container";

    message.innerHTML = msg;
    message.className = "message";
    message_container.appendChild(name_); // Name should be on top
    message_container.appendChild(message);
    message_container.appendChild(date); // Date should be on bottom
    
    date.innerHTML = _date;
    date.className = "date";
    name_.innerHTML = name;
    name_.className = "name";
    
    console.log(name);
    if (name == currentUsername){
        message_container.classList.add("MyMessage-container"); // Add class for current user messages
    }
    the_chat.appendChild(message_container);
    the_chat.scrollTop = the_chat.scrollHeight;
}
function get_time(){
    // Create a new Date object
    let now = new Date();

    // Get the current hours and minutes
    let hours = now.getHours();
    let minutes = now.getMinutes();

    // Format the hours and minutes to always have two digits
    if (hours < 10) {
        hours = '0' + hours;
    }
    if (minutes < 10) {
        minutes = '0' + minutes;
    }

    // Combine hours and minutes into the desired format
    let currentTime = hours + ':' + minutes;

    // Display the current time
    console.log(currentTime);
    return currentTime
}
// Function to get contacts
async function get_contacts(){
    let data = await fetch('get_contacts', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({"current_user": currentUsername})
    });
    const response = await data.json();
    return response.names;
}

// Function to create the dropdown elements and populate them
async function createDropdown(pop_up) {
    // Wait for contacts to be fetched
    const names = await get_contacts();

    // Create dropdown div
    const dropdownDiv = document.createElement('div');
    dropdownDiv.className = 'dropdown';

    // Create search input
    const searchInput = document.createElement('input');
    searchInput.type = 'text';
    searchInput.id = 'searchInput';
    searchInput.placeholder = 'Search for names...';
    searchInput.onkeyup = filterNames;

    // Create select element
    const select = document.createElement('select');
    select.id = 'namesSelect';
    select.size = '5';

    // Create submit button
    const submit = document.createElement('button');
    submit.innerHTML = 'Submit';

    // Append search input, select, and submit button to dropdown div
    dropdownDiv.appendChild(searchInput);
    dropdownDiv.appendChild(select);
    dropdownDiv.appendChild(submit);

    // Append dropdown div to the specified container (pop_up)
    pop_up.appendChild(dropdownDiv);

    // Now call populateSelect after the select element has been appended
    populateSelect(names, select, submit);
}

// Function to populate the select element with names
function populateSelect(names, select, submit) {
    names.forEach(name => {
        const option = document.createElement('option');
        option.value = name;
        option.text = name;
        select.appendChild(option);

        // Attach click event to option to set up submit button's functionality
        option.onclick = function() {
            submit.onclick = function() {
                add_chat_for_contact(name)
            };
        };
    });
}

// Function to filter names based on the search input
function filterNames() {
    const input = document.getElementById('searchInput');
    const filter = input.value.toLowerCase();
    const select = document.getElementById('namesSelect');
    const options = select.options;

    for (let i = 0; i < options.length; i++) {
        const txtValue = options[i].text;
        if (txtValue.toLowerCase().indexOf(filter) > -1) {
            options[i].style.display = '';
        } else {
            options[i].style.display = 'none';
        }
    }
}

async function add_chat_for_contact(name){
    let data = await fetch('add_chat_for_contact', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({"chat_id": currentChatId,"contact_name" : name})
    });
    const response = await data.json();
    console.log(response)
}

// Initialize dropdown on DOMContentLoaded

// const chatBox = document.getElementById('chat-box');
// const Send = document.getElementById('Send');
// const messageInput = document.getElementById('message-input');
// const add_chat = document.getElementById('add_chat')
// const x_btn = document.createElement("button")
// const input = document.createElement("input");
// input.maxLength = 20
// let current_chat = "chat1"
// var chat_id = 0

// Send.onclick = function (event) {
//     event.preventDefault();
//     const message = messageInput.value.trim();
//     if (message !== '') {
//         sendMessage(message);
//         messageInput.value = '';
//     }
// };

// add_chat.onclick = function() {
//     var add_chat_popup = document.getElementById("add_chat_popup")
//     add_chat_popup.className += (" add_chat_popup_hover");
//     while (add_chat_popup.firstChild) {
//         add_chat_popup.removeChild(element.firstChild);
//     }
    

//     x_btn.innerHTML = "x"
//     x_btn.className = "x_btn"
//     add_chat_popup.appendChild(x_btn)
//     const contact_button = document.createElement("button");
//     const group_button = document.createElement("button");

//     contact_button.innerHTML = "add contact"
//     contact_button.className = "add_contacts"
//     add_chat_popup.appendChild(contact_button)

//     group_button.innerHTML = "add groups"
//     group_button.className = "add_groups"
//     add_chat_popup.appendChild(group_button)


//     contact_button.onclick = add_contact
//     group_button.onclick = addchat
// }

// x_btn.onclick = close_popup

// function close_popup(){
//     var element = document.getElementById("add_chat_popup");
//     element.className = "add_chat_popup";
//     const add_chat = document.getElementById("add_chat_popup")
//     while (add_chat.firstChild) {
//         add_chat.removeChild(add_chat.firstChild);
//     }
//     input.value = ""
// }


// function add_contact(){
//     var add_chat_popup = document.getElementById("add_chat_popup");
//     var submit_chat = document.createElement("button");
//     while (add_chat_popup.firstChild) {
//         add_chat_popup.removeChild(add_chat_popup.firstChild);
//     }

//     x_btn.innerHTML = "x";
//     x_btn.className = "x_btn";
//     add_chat_popup.appendChild(x_btn);

//     input.setAttribute("type", "text"); 
//     input.placeholder = "username:";
//     input.className = "input_chat";
//     add_chat_popup.appendChild(input);

//     submit_chat.innerHTML = "submit";
//     submit_chat.className = "submit_chat";
//     add_chat_popup.appendChild(submit_chat);

//     submit_chat.onclick = function(){
//         fetch(`/add_friend`, {
//             method: 'POST',
//             headers: {
//                 'Content-Type': 'application/json'
//             },
//             body: JSON.stringify({"user_to_add": input.value, "current_user": currentUsername})
//         })
//         .then(response => {
//             if (!response.ok) {
//                 throw new Error(`HTTP error! Status: ${response.status}`);
//             }
//             return response.json();
//         })
//         .then(data => {
//             console.log('Message sent successfully:', data);
//             if(data["Add_successfully"] == "false"){
//                 let not_user = document.createElement("h3")
//                 not_user.className = ""
//                 console.log("username does not exixt")
//             }
//         })
//         .catch(error => {
//             console.error('Error sending message:', error);
//         });
//     }
// }


// function addchat(){
//     var add_chat_popup = document.getElementById("add_chat_popup");
//     var submit_chat = document.createElement("button");
//     while (add_chat_popup.firstChild) {
//         add_chat_popup.removeChild(add_chat_popup.firstChild);
//     }
//     x_btn.innerHTML = "x"
//     x_btn.className = "x_btn"
//     add_chat_popup.appendChild(x_btn)

//     input.setAttribute("type", "text"); 
//     input.placeholder = "Group name:"
//     input.className = "input_chat"
//     add_chat_popup.appendChild(input)

//     submit_chat.innerHTML = "submit"
//     submit_chat.className = "submit_chat"
//     add_chat_popup.appendChild(submit_chat)

//     submit_chat.onclick = async function () {
//         if (input.value !== "") {
//             try {
//                 let data = await get_chat_id(input.value);
//                 console.log(data);
//                 create_chat(data["the_id"], input.value);
//                 close_popup();
//             } catch (error) {
//                 console.error("Error fetching chat ID:", error);
//             }
//         } else {
//             console.log("the input has to be more than 0 ");
//         }
//     };
// }

// function create_chat(id , chatname){
//     const chat = document.createElement("div");
//     chat.innerHTML = chatname
//     chat.className = "allchats"
//     chat.id = id
//     document.getElementById("chats").appendChild(chat);
//     chat.addEventListener("click", function(){curront_chat_update(id)});
// }

// function curront_chat_update(id){
//     console.log("update_chat" , id)
//     current_chat = id
//     fetchMessages();
// }

// async function get_chat_id(name) {
//     console.log("getid")
//     let data = await fetch(`/get_id`, {
//         method: 'POST',
//         headers: {
//             'Content-Type': 'application/json'
//         },
//         body: JSON.stringify({"current_user": currentUsername, 'chat_name': name})
//     });

//     let x = await data.json();
//     return x;
// }


// async function get_chats(name) {
//     let data = await fetch(`/get_chats?${currentUsername}`, {
//         method: 'Get',
//     })
//     data = await data.json();
//     // todo sort data
//     console.log(data)
//     // let data_ = sortObjectByTime(data)
//     // console.log(data_)
//     for(const [id,data_] of Object.entries(data)) {
//         if(data_["chat_name"] != undefined){
//             console.log(data_["chat_name"])
//             create_chat(id, data_["chat_name"])
//         }
//     }
// };

// // function sortObjectByTime(inputObject) {
// //     console.log(inputObject)
// //     const entries = Object.entries(inputObject);
// //     entries.sort((a, b) => {
// //         const timeA = new Date(a[1].time);
// //         const timeB = new Date(b[1].time);
// //         return timeA.getTime() - timeB.getTime();
// //     });
// //     console.log(entries)
// //     const sortedObject = entries
// //     console.log(sortedObject)
// //     return sortedObject;
// // }
// function sendMessage(message) {
//     fetch(`/send_messages`, {
//         method: 'POST',
//         headers: {
//             'Content-Type': 'application/json'
//         },
//         body: JSON.stringify({"current_user": currentUsername , 'chat_id': current_chat, 'content': message })
//     })
//     .then(response => {
//         if (!response.ok) {
//             throw new Error(`HTTP error! Status: ${response.status}`);
//         }
//         console.log(response)
//         return response.json();
//     })
//     .then(data => {
//         console.log(data)
//         console.log('Message sent successfully:', data);
//     })
//     .catch(error => {
//         console.error('Error sending message:', error);
//     });
// }

// function displayMessage(message) {
//     const messageElement = document.createElement('p');
//     messageElement.textContent = message;
//     messageElement.className = "messageElement"
//     chatBox.appendChild(messageElement);
//     chatBox.scrollTop = chatBox.scrollHeight; // Auto-scroll to the bottom
// }

// function fetchMessages() {
//     fetch(`/get_messages?chat_id=${current_chat}`)
//         .then(response => {
//             if (!response.ok) {
//                 throw new Error(`HTTP error! Status: ${response.status}`);
//             }
//             return response.json();
//         })
//         .then(data => {
//             // Clear the chat box before displaying new messages
//             chatBox.innerHTML = '';
//             data.forEach(message => displayMessage(message.content));
//         })
//         .catch(error => {
//             // console.error('Error fetching messages:', error);
//         });
// }


// // Fetch and display messages when the page loads
// fetchMessages();
// get_chats()

// // Set up automatic message refresh every 0.5 seconds (adjust as needed)
// setInterval(fetchMessages, 500);
