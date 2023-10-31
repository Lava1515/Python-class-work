window.ip =  document.location.origin

async function Send(){
    let Name = document.getElementById("Client_Name_input").value
    async function postData(url = "", data = {}) {
    try{
        const response = await fetch(url, {
          method: "POST", // GET, POST
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(data),
        });
        return response;
        }
      catch{}
      }
    console.log(window.ip +"/players")
    let response_http = await postData(window.ip +"/players", { "Client_Name" : Name });
    console.log(response_http)
  }

 function Submit(){
    console.log(window.ip + "/GetIP")
    let res =  fetch(window.ip +"/GetIP").then(async function(res){
        PIN =  res.json()
    })
    let data = document.getElementById("PIN_box_P").value
    if ((data == "87654321" || data == PIN)&&(data != ""))
    {
      let Name = document.getElementById("Client_Name_input").value
      window.location = "lobby.html?name=" + Name + "&host=false"
      return true
    }
    else{
      document.getElementById("alert").innerHTML = "*NOT A VALID PIN"
    }
    return false
  }

  document.getElementById("Submit_").onclick = function(){
    if(Submit()){
      Send()
    }
  };
