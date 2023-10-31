window.ip =  document.location.origin

const queryString = window.location.search
const urlParams = new URLSearchParams(queryString)
const host = urlParams.get('host')
const name = urlParams.get('name')


function get(object, key, default_value) {
    var result = object[key];
    return (typeof result !== "undefined") ? result : default_value;
}

function rst_Board(question_data) {
    if (i < data.length){
        question_data = question_data.split(",")
        document.getElementById("question").innerHTML =question_data[0]
        document.getElementById("question").className = "look"
        let Div = document.getElementById("questions")
        Div.innerHTML = ""
        for (let j = 1 ; j <= 8; j ++) {
            if (question_data[j] != " ") {
                let btn = document.createElement("BUTTON")
                btn.innerHTML = question_data[j]
                Div.appendChild(btn)
                btn.id = j
                btn.className = `answer_buttons${j}`
            }
            j++
        } 
        document.getElementById("1").onclick = function() {GET_true_false(1)}
        document.getElementById("3").onclick = function() {GET_true_false(3)}
        document.getElementById("5").onclick = function() {GET_true_false(5)}
        document.getElementById("7").onclick = function() {GET_true_false(7)}
    }
    else{
        let data_
        async function do_fetch(){
            let res = await fetch(window.ip +"/get_names_and_ranks").then(async function(res){
                data_ = await res.json()
            })
            console.log("GETNames")
            if(set_lead_Board == false){
                Div = document.getElementById("game")
                Div.innerHTML = ""
                lead_Board = document.createElement("h1")
                lead_Board.innerHTML = "The leaderboard :"
                lead_Board.className = "UP_BIG"
                Div.appendChild(lead_Board)
                for(let i = 1 ; i<= data_.length ; i++){
                    if (i == 1){
                        bord = document.createElement("h1")
                    }
                    else if (i == 2){
                        bord = document.createElement("h2")
                    }
                    else {
                        bord = document.createElement("h3")
                    }
                    bord.innerHTML = i + " : " + data_[i - 1]
                    Div.appendChild(bord)
                }
                set_lead_Board = true
            }
        
        }
        async function return_to_home_page(){
            await fetch(window.ip +"/back_to_home_page", {
                method: "POST", // GET, POST
                headers: {
                "Content-Type": "application/json",
                },
                body: JSON.stringify("data"),
            });
            console.log("bruhhh")
            window.location = "index.html"
        }
        do_fetch()
        let return_ = document.createElement("h1")
        return_.innerHTML = "Back to home page"
        return_.href = "index.html"
        return_.className = "Bottom_right"
        return_.style = "position: absolute; top:90%;"
        document.body.appendChild(return_)
        return_.addEventListener("click", return_to_home_page);
    }
}

async function GET_game_info () {
    let res = await fetch(window.ip +"/GETGameInfo").then(async function(res){
        data = await res.json()
    })
    let name = get(data,"Game_Name","nothing")
    data = get(data,"The_data","nothing")
    data = data.split("question number")
    rst_Board(data[i])
}

async function GET_true_false (n) {
    corrent = data[i].split(",")[n]
    console.log("GET_true_false")
    if(host == "false"){
        let t_f
        console.log(corrent)
        let res = await fetch(window.ip +"/GET_true_false" + corrent + " " + i + " " + name +" "+seconds).then(async function(res){
            t_f = await res.json()
            console.log(t_f)
        })
        document.getElementById("question").innerHTML = t_f
        document.getElementById("question").className = t_f
        document.getElementById("questions").innerHTML = ""
    }
}

async function next_Q() {
    console.log(i)
    console.log("next")
    await fetch(window.ip+"/move_Qs" + i, {
        method: "POST", // GET, POST
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify("True"), 
        })
}

async function timer(){
    var now = new Date().getTime();
    var distance = now - before;
    let data_ 

    seconds = Math.floor((distance % (1000 * 60)) / 1000);
    seconds = 30 - seconds
    document.getElementById("timer").innerHTML = seconds + "s ";
   
    if (distance < 0) {
      clearInterval(x);
      document.getElementById("timer").innerHTML = "EXPIRED";
    }

    let res = await fetch(window.ip +"/move_to_next" + i).then(async function(res){
        data_ = await res.json()
        console.log(data_)
    })

    if(data_ == "Move"){
        i++;
        rst_Board(data[i])
        before = new Date().getTime()
    }
    
    if(seconds == 0){
        before = new Date().getTime();
        next_Q()
        if(i < data.length ){
            timer()
        }
        console.log("times up")
    }
    else{
        setTimeout(timer,1000)
    }
}


let i = 1
let data
var seconds
var before = new Date().getTime();
set_lead_Board = false

if ((host == "true")){
    console.log("host")
    let btn = document.createElement("BUTTON")
    btn.id = "Next_Qu"
    btn.innerHTML = "Next question"
    document.getElementById("game").appendChild(btn)

    document.getElementById("Next_Qu").onclick = next_Q
}

if (i == 1){
    GET_game_info()
}

timer()

document.getElementById("1").onclick = function() {GET_true_false(1)}
document.getElementById("3").onclick = function() {GET_true_false(3)}
document.getElementById("5").onclick = function() {GET_true_false(5)}
document.getElementById("7").onclick = function() {GET_true_false(7)}




