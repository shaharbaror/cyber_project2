const Submit = async() => {
    let username = document.getElementById("username").value;

    try {
        const response = await fetch("127.0.0.1/index?a=c",{
            method: "POST", //get or post
            headers: {"Content-Type": "application/json;charset=utf-8"},
            body:JSON.stringify(username)
        })
        if (response) {
            const data = await response.text();
            window.location.replace(`${data}/firstpage.html`);
        }
        
    } catch(e){
        console.log(e);
    }
}

const JoinLobby = () => {
    let username = document.getElementById("username").value;

    try {
        const response = fetch("127.0.0.1/index?a=j",{
            method: "POST", //get or post
            headers: {"Content-Type": "application/json;charset=utf-8"},
            body:JSON.stringify(username)
        })
        if (response) {
            window.location.replace(`/firstpage.html`);
        }
        
    } catch(e){
        console.log(e);
    }
}
