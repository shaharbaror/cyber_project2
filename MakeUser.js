let url = window.location.href;
let lobby = url.split("/")[3];
console.log(lobby);

const Submit = async() => {
    let username = document.getElementById("username").value;

    try {
        const response = await fetch("makeuser/index?a=c",{
            method: "POST", //get or post
            headers: {"Content-Type": "application/json;charset=utf-8"},
            body:JSON.stringify(username)
        })
        if (response) {
            const data = await response.text();            
            window.location.href = "/" + `${data}/firstpage.html`;
        }
        
    } catch(e){
        console.log(e);
    }
}

const JoinLobby = () => {
    let username = document.getElementById("username").value;

    try {
        const response = fetch("makeuser/index?a=j",{
            method: "POST", //get or post
            headers: {"Content-Type": "application/json;charset=utf-8"},
            body:JSON.stringify(username)
        })
        if (response) {
            console.log(lobby);
            window.location.href = "/" + `${lobby}/firstpage.html`;
        }
        
    } catch(e){
        console.log(e);
    }
}

if (lobby.length == 8) {
    const button = document.createElement("button");
    button.className = "join_lobby";
    button.id = "joinLobby";
    button.onclick = JoinLobby;
    button.innerHTML = "join Lobby";
    const buttonDiv = document.getElementById("submitDiv");
    console.log(button);
    buttonDiv.appendChild(button);
    console.log(buttonDiv);
}
