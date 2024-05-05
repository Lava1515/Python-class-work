function change_eye_slash1(){
    document.getElementById("eye1").className = "fa fa-eye-slash"
    document.getElementById("password").type = "text"
}
function change_eye1(){
    document.getElementById("eye1").className = "fa fa-eye"
    document.getElementById("password").type="password"
}

function change_eye_slash2(){
    document.getElementById("eye2").className = "fa fa-eye-slash"
    document.getElementById("comfirm_pass").type = "text"
}
function change_eye2(){
    document.getElementById("eye2").className = "fa fa-eye"
    document.getElementById("comfirm_pass").type="password"
}

document.getElementById("submit").onclick = function(){
    let name = document.getElementById("UsernameInput").value
    let pass = document.getElementById("password").value
    let pop_up = document.getElementById("pop_up")
    if(name == ""){
        pop_up.innerHTML = "No username provided"
        pop_up.className = "alert_pop_up"
    }
    else if(pass == ""){
        pop_up.innerHTML = "Password is needed"
        pop_up.className = "alert_pop_up"
    }
    else{
        send_details( name, pass)
    }
}


function send_details(name, pass) {
    console.log("send_details" , name , pass)
    fetch(`/AdminRegister`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ 'name': name, 'pass': pass })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        console.log(response)
        return response.json();
    })
    .then(data => {
        let pop_up = document.getElementById("pop_up")
        if(data["can_login"] =="true"){
            sessionStorage.setItem('username', name);
            window.location.href = "index.html"
        }
        else if(data["can_login"] =="false"){
            pop_up.innerHTML = "Username or pasword are not matching"
            pop_up.className = "alert_pop_up"
        }
        if (data["existing"] =="true"){
            pop_up.innerHTML ="*User already exists*"
            pop_up.className = "alert_pop_up"
        }
        else if (data["existing"] =="false"){
            sessionStorage.setItem('username', name);
            window.location.href = "index.html"
        }
        console.log(data)
        console.log('Message sent successfully:', data);
    })
    .catch(error => {
        console.error('Error sending message:', error);
    });
}
