window.ip =  document.location.origin

let i = 1

function addNew() {
  const before = document.getElementById("Div_btns");
  const Div = document.createElement("div");
  Div.className = "Div_look";
  Div.innerHTML = `Enter question number: ${i} - `;
  const inp_question = document.createElement("input");

  inp_question.id = `inp_question ${i}`
  inp_question.placeholder ="Enter question"
  inp_question.className = "inp_question"
  Div.appendChild(inp_question);

  for (let j = 1; j <= 4; j++) {
      let Div_answer = document.createElement("div");
      let inp_answer = document.createElement("input");
      let inp_right =document.createElement("input")

      inp_right.setAttribute("type", "checkbox")
      inp_answer.id =`inp_answer ${i} ${j}`
      inp_right.id =`inp_right ${i} ${j}`
      inp_answer.placeholder = `Answer ${j}`
      Div_answer.className = `look Div_answer${j}`

      Div_answer.appendChild(inp_answer);
      Div_answer.appendChild(inp_right);
      Div.appendChild(Div_answer)
  }
  i++;
  document.body.insertBefore(Div, before);
}


async function Send(){
  let ok = true
  for(let J = i - 1; J >= 1 ; J--) {
    if (document.getElementById(`inp_question ${J}`).value == ""){
      ok = false
    } 
    for(let k = 1; k <= 4 ; k++) {
      if (document.getElementById(`inp_answer ${J} ${k}`).value == ""){
        ok = false
      }
    }
  }
  console.log(ok)
  if(ok){
    let Name = document.getElementById("Name_input").value
    async function postData(url = "", data = {}) {
      const response = await fetch(url, {
        method: "POST", // GET, POST
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data), // body data type must match "Content-Type" header
      });
      return response; // parses JSON response into native JavaScript objects
    }
    
      let data = ""
      for (let j = 1 ; j < i ; j++) {
        data = data + "question number " + j + ": " +  document.getElementById(`inp_question ${j}`).value 
        for(let k = 1 ; k <= 4 ; k++){
          data = data + ", " + document.getElementById(`inp_answer ${j} ${k}`).value
          data = data + ", " + document.getElementById(`inp_right ${j} ${k}`).checked
        }
        data = data + " , "
    }
    let response_http = await postData(window.ip +"/create", { Game_Name: Name , The_data : data});
    document.getElementById("alert").innerHTML = ""
    window.location = "index.html"
  }
  else{
    document.getElementById("alert").innerHTML = "questions and answers canot be None"
  }

}


document.getElementById("addbtn").addEventListener("click", addNew);

document.getElementById("Submit").onclick = Send;

