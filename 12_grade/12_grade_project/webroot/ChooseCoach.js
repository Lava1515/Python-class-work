const currentUsername = sessionStorage.getItem('username');

async function get_coaches(){
    let data = await fetch(`/get_coaches`, {
        method: 'Get',
    })
    data = await data.json();

    let container = document.getElementById('coachesContainer');
    // Iterate over the data list and create elements
    data.forEach(coach => {
        const coaches_containers = document.createElement('div');
        coaches_containers.className = 'coaches_containers'; // Changed from id to class
        const coachElement = document.createElement('h3');
        coachElement.textContent = coach;
        const submit = document.createElement('button');
        submit.innerHTML = "submit";
        coaches_containers.appendChild(coachElement);
        coaches_containers.appendChild(submit);
        container.appendChild(coaches_containers);
        submit.onclick = async function(){
            console.log(currentUsername, coach)
            let data = await fetch(`/SetCoach`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({"current_user": currentUsername, 'coach': coach})
            });
            const response = await data.json();
            console.log(response)
            if(response["Added"] == true){
                window.location.href = "index.html"
            }
            if(response["error"] == "this user already has a coach"){
                window.location.href = "index.html"
            }
        }
    });
    console.log(data);
}

get_coaches();
