function change(){
    if(document.getElementById("Login_register").innerHTML == "Login"){
        document.getElementById("Login_register").innerHTML = "Register"
        document.getElementById("title").innerHTML = "Login"
        document.getElementById("comfirm_pass_line").innerHTML = ""
        document.getElementById("comfirm_pass").className ="invisble"
        document.getElementById("eye2").className = ""
        document.getElementById("pop_up").innerHTML = ""
    }

    else if(document.getElementById("Login_register").innerHTML == "Register"){
        document.getElementById("Login_register").innerHTML = "Login"
        document.getElementById("title").innerHTML = "Register"
        document.getElementById("comfirm_pass_line").innerHTML = "Comfirm password"
        document.getElementById("comfirm_pass").className ="login_register_mesagebox"
        document.getElementById("eye2").className = "fa fa-eye"
    }
}


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

document.getElementById("submit").onclick = submit

function submit(){
    let name = document.getElementById("UsernameInput").value
    let pass = document.getElementById("password").value
    let pop_up = document.getElementById("pop_up")
    if (document.getElementById("title").innerHTML == "Login"){
        if(name == ""){
            pop_up.innerHTML = "No username provided"
            pop_up.className = "pop_up"
        }
        else if(pass == ""){
            pop_up.innerHTML = "Password is needed"
            pop_up.className = "pop_up"
        }
        else{
            send_details("Login", name, pass)
        }
    }
    else if (document.getElementById("title").innerHTML == "Register"){
        console.log("Register")
        if(pass != document.getElementById("comfirm_pass").value){ 
            pop_up.innerHTML ="*The paswords are not matching*"
            pop_up.className = "pop_up"
        }
        else{
            if(name == ""){
                pop_up.innerHTML = "Username must be given"
                pop_up.className = "pop_up"
            }
            else if(pass == ""){
                pop_up.innerHTML = "Do u think this password is suitble?"
                pop_up.className = "pop_up"
            }
            else{
                send_details("Register", name, pass)
            }
        }
    }
}


function send_details(method_, name, pass) {
    console.log("send_details" , method_ , name , pass)
    fetch(`/send_details_${method_}`, {
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
            pop_up.className = "pop_up"
        }
        if (data["existing"] =="true"){
            pop_up.innerHTML ="*User already exists*"
            pop_up.className = "pop_up"
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
