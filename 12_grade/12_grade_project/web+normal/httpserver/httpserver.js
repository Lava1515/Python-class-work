let pesemtdata = document.getElementById("presntdata")

async function get_data() {
    console.log("get_data")
    let data = await fetch(`/get_data`, {
        method: 'Get',
    })
    data = await data.json();
    // todo sort data
    console.log(data)
    pesemtdata.innerHTML = data
};
get_data()
setInterval(get_data, 500)