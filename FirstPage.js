const sheet = new CSSStyleSheet();
let url = window.location.href;
console.log(url)
const lobby = url.split("/")[3]
console.log(lobby)
const player_id = localStorage.getItem("playerID");
localStorage.removeItem("playerID");
const username = "shahar";
let memeInfo = {
    cContent:[],
    rollsLeft:5
}



AtStart();



function AtStart() {
    FetchFirstData();
    //AssignCaptions("caption1", "input1");
}

// async function UpdateDone() {
//     const players_done = setInterval(async () => {
//         let response = await fetch(`127.0.0.1/firstpage?s=f&a=getplayersdone`);
//         if (response) {
//             let data = response.text();
//             data = (await data).split("\n");
//             console.log(data)
//             document.getElementById("players_done").innerHTML = data[1];
//             if (data[0] === data[1]) {
//                 SubmitMeme();
//             }
            
//         }
//     },1000);
// }

async function FetchFirstData(){
    var data;
    
    var response = await fetch(`firstpage?s=f&a=startgame`);
    data = await response.json();
    if (data.send) {
        window.location.replace(`/makeuser.html`);
        console.log("it works");
    }
    console.log(data);

    let timer = 320;
    if (data){
        timer = data.time;
    }
    
    const inter = setInterval(function(){
        timer = CountTime(timer);
        if (timer <= -1){
            SubmitMeme();
            clearInterval(inter);
        }
    }, 1000);
    //UpdateDone();
    ReRollMeme(data.is_ok, data.memeIndex, data.captions, data.styles)

} 

function CountTime(timer) {
    let seconds = timer % 60;
    let minutes = Math.floor(timer / 60);
    document.getElementById("timer").innerHTML = `${minutes < 10 ? `0${minutes}`: minutes}: ${seconds < 10 ? `0${seconds}`:seconds}`;
    return timer -1;
}

//Assigning an EventListener to a caption and an input so that when i change the input the caption will change too
// function AssignCaptions(captionId,inputId){
//     let caption1 = document.getElementById(captionId)
//     console.log("hi");
//     document.querySelector(`#${inputId}`).addEventListener("input", async (event) => {
//         if (event.target.value.length >= 100){
//             event.target.value = caption1.value;
//         }
//         else {  
//             console.log(event.target.value)
//             caption1.value = event.target.value;
//             if (caption1.value.length >= 50){ //if the text reached over 50 characters then change the text size
//                 caption1.style.fontSize = `${1.25 - caption1.value.length/200}vw`;
//                 event.target.style.fontSize = `${1.25 - event.target.value.length/200}vw`;
//             }
//         }
       
//     })
// }

async function ReRollMeme(is_ok = null, memeIndex = null, captions = null, styles = null) {
    //fetch the meme id and the caption amount, also make sure that if the meme is changed manualy the server wont give the mene
    
    if (memeInfo.rollsLeft > 0) {
        let response,data;
        if (!(memeIndex && captions && styles)){
            response = await fetch(`firstpage?s=f&a=newmeme`);
            if (response){
                data = await response.json();
            }
        } else {
            data = {
                is_ok,
                memeIndex,
                captions,
                styles,
            }
        }
        console.log(data)
        if (data.is_ok) {
            //because we reroll the meme we need to reset the data about the meme
            memeInfo = {
                ...memeInfo,
                cContent : [],
                rollsLeft: memeInfo.rollsLeft -1,
                ...data,
                
            };


            //assign all of the inputs to the captions with event listiners
            //let inputDiv = document.getElementById("inputDiv");
            let meme = document.getElementById("meme");
            let cd = document.getElementById("c1d");
            //let inputField = document.getElementById("input1");
        
            sheet.replaceSync(data.styles);
            document.adoptedStyleSheets = [sheet];

            while (meme.lastChild !== meme.firstChild) {
                console.log(meme.lastChild);
                meme.removeChild(meme.lastChild);
                //inputDiv.removeChild(inputDiv.lastChild);
                console.log("earased")
            }

            for (var i =1; i<= data.captions; i++) {
                let cdClone = cd.cloneNode(true);
                cdClone.id = `c${i}d`;
                cdClone.childNodes[1].id = `caption${i}`;
                cdClone.childNodes[1].className = `meme_caption`;
                cdClone.childNodes[1].value = `Caption ${i}`;
                meme.appendChild(cdClone);

                // let inputClone = inputField.cloneNode(true);
                // inputClone.innerHTML = `Caption ${i}`;
                // inputClone.id = `input${i}`;
                // inputDiv.appendChild(inputClone);

                // AssignCaptions(`caption${i}`,`input${i}`);

            }
        } else {
            console.log("o hell no buddy you aint getting another one if theese jewcy memes!");
        }
    }

}

function SubmitMeme() {
    let post = {
        index:memeInfo.memeIndex,
        captions:[],
    
    }
    //add all of the text from the captions to the meme info
    for (var i =1; i <= memeInfo.captions; i++){
        post.captions.push(`${document.getElementById(`caption${i}`).value} \n`);
    }
    console.log(post);

    try{
        console.log(`firstpage?s=t&i=${memeInfo.memeIndex}&c=[${memeInfo.cContent}]`);
        fetch(`firstpage?s=t`,{
            method: "POST", //get or post
            headers: {"Content-Type": "application/json;charset=utf-8"},
            body:JSON.stringify(post)
        }).then(response => {if(response.ok){window.location.replace("WaitingPage.html")}});
        
    }catch(err){
        console.log(err);
    }
    //create a var for post request which contains everything that is needed so that the server will keep the meme
    //example:
    // var finalMeme = {
    //     memeNumer,
    //     url:`${MemeUrl}`,
    //     text: [`${caption1.innerHTML}`, `${caption2.innerHTML}`]
    // };

    //fetch the post request and transfer user to the waiting page
    //window.location.replace("WaitingPage.html");
}