function change(){
    if(document.getElementById("Login_register").innerHTML == "Login"){
        document.getElementById("Login_register").innerHTML = "Register"
        document.getElementById("title").innerHTML = "Login"
        document.getElementById("forgot_pass").innerHTML = ""
        document.getElementById("forgot_pass_line").className ="invisble"
        document.getElementById("eye2").className = ""
    }

    else if(document.getElementById("Login_register").innerHTML == "Register"){
        document.getElementById("Login_register").innerHTML = "Login"
        document.getElementById("title").innerHTML = "Register"
        document.getElementById("forgot_pass").innerHTML = "Comfirm password"
        document.getElementById("forgot_pass_line").className ="login_register_mesagebox"
        document.getElementById("eye2").className = "fa fa-eye"
    }
}


function change_eye_slash1(){
    document.getElementById("eye1").className = "fa fa-eye-slash"
    document.getElementById("pass1").type = "text"
}
function change_eye1(){
    document.getElementById("eye1").className = "fa fa-eye"
    document.getElementById("pass1").type="password"
}

function change_eye_slash2(){
    document.getElementById("eye2").className = "fa fa-eye-slash"
    document.getElementById("forgot_pass_line").type = "text"
}
function change_eye2(){
    document.getElementById("eye2").className = "fa fa-eye"
    document.getElementById("forgot_pass_line").type="password"
}

document.getElementById("submit").onclick = myfun

function myfun(){
    if (document.getElementById("title").innerHTML == "Login"){
        console.log("Login")
    }
    else if (document.getElementById("title").innerHTML == "Register"){
        console.log("Register")
    }
}







