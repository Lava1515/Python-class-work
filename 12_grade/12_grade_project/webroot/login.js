function change(){
    if(document.getElementById("Login_register").innerHTML == "Login"){
        document.getElementById("Login_register").innerHTML = "Register"
        document.getElementById("title").innerHTML = "Login"
        document.getElementById("comfirm_pass_line").innerHTML = ""
        document.getElementById("comfirm_pass").className ="invisble"
        document.getElementById("eye2").className = ""
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

document.getElementById("submit").onclick = myfun

function myfun(){
    let name = document.getElementById("UsernameInput").value
    let pass = document.getElementById("password").value
    if (document.getElementById("title").innerHTML == "Login"){
        send_details("Login", name, pass)
    }
    else if (document.getElementById("title").innerHTML == "Register"){
        console.log("Register")
        if(pass != document.getElementById("comfirm_pass").value){
            let not_same = document.getElementById("pop_up") 
            not_same.innerHTML ="*The paswords are not matching*"
            not_same.className = "pop_up"
        }
        else{
            send_details("Register", name, pass)
        }
    }
}


function send_details(method_, name, pass) {
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
        if(data["can_login"] =="true"){
            sessionStorage.setItem('username', name);
            window.location.href = "index.html"
        }
        if (data["existing"] =="true"){
            let not_same = document.getElementById("pop_up") 
            not_same.innerHTML ="*User already exists*"
            not_same.className = "pop_up"
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
