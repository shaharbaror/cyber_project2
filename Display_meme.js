const meme = document.getElementById("meme");
const capDiv = document.getElementById("cap-div1");
const caption1 = document.getElementById("caption1");

//create a stylesheet for the caption position
const sheet = new CSSStyleSheet();

const Input_field = document.getElementById("input-field");
const Input = document.getElementById("cp1");

function DisplayChange(id, type) {
  document.getElementById(id).style.display = type;
}


const ShowMeme = () => {
  const rnd = Math.floor(Math.random() * 6) + 1;

  //if the meme number is requireing a certin kind of display, this will change it
  //   switch (rnd) {
  //     case 3:
  //       DisplayFlex("meme");
  //       break;
  //     default:
  //       DisplayBlock("meme");
  //   }

  const data = useFetchinator("#","Get");

  DisplayChange("meme",data.displayType);
  
  meme.style.backgroundImage = `url(${data.image})`;
  meme.style.visibility = "visible";
  
  sheet.replaceSync(data.style);
  document.adoptedStyleSheets = [sheet];

  while(meme.lastChild !== meme.firstChild){
    meme.removeChild(meme.lastChild);
    Input_field.removeChild(Input_field.lastChild);
  }

  for (var i = 1; i<= data.caption_number; i++){
    let anotherInput = Input.cloneNode(true);
    let anotherCaption = capDiv.cloneNode(true);

    //make a new caption
    anotherCaption.id = `cap-div${i}`;
    anotherCaption.childNodes[1].innerHTML = `Caption ${i}`;
    anotherCaption.childNodes[1].id = `caption${i}`;
    anotherCaption.childNodes[1].className = `caption${i} caption-txt`;
    meme.appendChild(anotherCaption);

    //make a new input object for every caption
    anotherInput.value = `Caption${i}`;
    anotherInput.id = `cp${i}`;
    anotherInput.className = `za-inpudo`;
    Input_field.appendChild(anotherInput);

    //link every input with caption so that if the input change so does the caption

    LinkBetweenCaptions(`cp${i}`,`caption${i}`)
    
  }

};

const useFetchinator = (data, action) => {
  //creates the http request body
  let options = {
    method: action, //get or post
    headers: {
      "Content-Type": "application/json;charset=utf-8",
    },
    body: JSON.stringify(data), // what to send to the server
  };

  
  const rnd = Math.floor(Math.random() * 6) + 1;
  style =
    ".caption1 {margin-top: 60%;font-size: 25px;max-width: 300px;margin-left: 30%;} .caption2 {max-width: 300px;margin-left:5%; font-size: 30px;} #cap-div1 {width: 50%;}#cap-div2 {width: 50%;text-align: center;}";
  let retVal = {
    image: "./MemeBank/meme02.png",
    style,
    caption_number: 2,
    displayType: "flex",
    max_size:200
  };
  return retVal;
};

//if there are 2 captions create 2 inputs that are connected to the captions
