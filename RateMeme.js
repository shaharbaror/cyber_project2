const sheet = new CSSStyleSheet();


setInterval(() => {
    FetchImages()
},1000)

const FetchImages = async () => {
    let data
    let response = await fetch("127.0.0.1/ratememe/getmeme");
    if (response) {
        data = await response.json()
        console.log(data)
    }
    /* data:
    {
        "style":"",
        "captions": num,
        "content": ["",""],
        "user": ""
    }
    */ 

    //get the style for the meme and captions
    sheet.replaceSync(data.styles);
    document.adoptedStyleSheets = [sheet];

    const captionDiv = document.createElement("div");
    const caption = document.createElement("textarea");
    captionDiv.appendChild(caption);
    console.log(captionDiv);

    const meme = document.getElementById("meme");
    
    //clear the captions of the previus meme
    if (meme.hasChildNodes()) {
        while (meme.lastChild !== meme.firstChild) {
            console.log(meme.lastChild);
            meme.removeChild(meme.lastChild);
            //inputDiv.removeChild(inputDiv.lastChild);
            console.log("earased")
        }
    }

    for (var i =0; i< data.captions; i++) {
        let cdClone = captionDiv.cloneNode(true);
        //cdClone.appendChild(document.createElement("textarea"));
        cdClone.id = `c${i}d`;
        cdClone.childNodes[0].id = `caption${i}`;
        cdClone.childNodes[0].className = `meme_caption${i}`;
        console.log(data.content[i]);
        cdClone.childNodes[0].value = data.content[i];
        cdClone.childNodes[0].readonly = true;
        meme.appendChild(cdClone);
    }

    //set up a working timer
    let time = 20;
    setInterval(async () => {
        document.getElementById("time").innerHTML = `00:${time > 10? time: "0" + time}`;
        time -= 1;
    },1000);
   

}