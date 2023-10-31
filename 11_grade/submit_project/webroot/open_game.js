window.ip =  document.location.origin

function create_names() {
    const Div = document.createElement("div");
    for(let j = 0; j < names.length; j++) {
        const h3 = document.createElement("H3");
        let name = names[j].split(".")[0]
        h3.innerHTML = name
        Div.appendChild(h3);
        onlynames.push(name)
    }
    document.body.appendChild(Div)
}

async function Get_The_Names () {
    let data 
    console.log(window.ip + "/GET_Games_Names")
    let res = await fetch(window.ip +"/GET_Games_Names").then(async function(res){
        names = await res.json()
    })
    create_names()
}

function check_in_list(name ,lst ){
    for(let i = 0 ; i < lst.length; i++){
        console.log(lst[i])
        if(name == lst[i]){
            return true
            break
        }
    }
    return false
}

async function send_name() {
    let name = document.getElementById("name").value
    console.log(onlynames)
    if (check_in_list(name, onlynames)){
          await fetch(window.ip+"/set_name", {
            method: "POST", // GET, POST
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify(name), // body data type must match "Content-Type" header
          });
          console.log(name)

        document.getElementById("alert").innerHTML = ""
        window.location = "lobby.html?name=" + "&host=true"
    }
    else{
        document.getElementById("alert").innerHTML = "*NOT A VALID NAME"
    }
}

let names = []
onlynames = []
Get_The_Names()


document.getElementById("game_name").onclick = send_name