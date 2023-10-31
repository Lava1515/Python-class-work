window.ip =  document.location.origin

const queryString = window.location.search
const urlParams = new URLSearchParams(queryString)
const name = urlParams.get('name')
const host = urlParams.get('host')

async function set_pin(){
    let res = await fetch(window.ip +"/GetIP").then(async function(res){
        PIN = await res.json()
    })
    document.getElementById("Pin_num").append(PIN)
}

async function Get_The_Names () {
    let data 
    let res = await fetch(window.ip +"/GETNames").then(async function(res){
        data = await res.json()
    })
    let h_names = document.getElementsByClassName("HNames")
    while(h_names[0]) {
        h_names[0].parentNode.removeChild(h_names[0]);
    }

    let Pnames = document.getElementById("Pnames")
    for (let i in data){
        let name = data[i]
        let HName = document.createElement("h1") //HName = header name 
        HName.id = name
        HName.innerHTML = name
        HName.className = "HNames"
        Pnames.append(HName)
    }
    setTimeout(Get_The_Names, 1000);
}

async function Move(){
    await fetch(window.ip+"/move_", {
    method: "POST",
    headers: {
        "Content-Type": "application/json",
    },
    body: JSON.stringify("True"), 
    })
}

async function Can_move(){

    let data
    let res = await fetch(window.ip +"/Can_move").then(async function(res){
        data = await res.json()
        console.log(data)
    })
    if (data == "Move"){
        window.location = "game.html?name="+ name  +"&host=" + host
    }
    setTimeout(Can_move, 1000);
}


set_pin()
Get_The_Names()
Can_move()

if (host=="true"){
    var btn = document.createElement("BUTTON")
    btn.innerHTML = "start game"
    btn.className = "look"
    document.body.appendChild(btn)
    btn.onclick = Move
}
