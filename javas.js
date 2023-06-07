let playerplayer;
const player = document.getElementById("player-1");
playerplayer = document.getElementById("player_stash");

//Right after the load:

//get the first caption to work

document.querySelector(`#cp1`).addEventListener("input", async (event) => {
  caption1.innerHTML = event.target.value;
});

//change how the caption looks like
const ReworkSize = (object, data) => {
  let response = "";
  let words = data.split(" ");
  //go through all of the words in the input, and if there is a word that passes the limit, then go down a line
  for (var j = 1; j <= words.length; j++) {
    let newWord = words[j - 1];
    for (var i = 1; i < words[j - 1].length / data.min_words; i++) {
      //reformat the word that is too long so it will go down a line
      newWord =
        newWord.slice(0, i * data.min_words - 1) +
        " " +
        newWord.slice(i * data.min_words - 1, newWord.length - 1);
    }
    response += newWord + (j != words.length ? " " : "");
  }
  return response;
  //caption.style.fontSize = `${valueLength >= 50 ? 250 - valueLength: 250 }%`
};

const LinkBetweenCaptions = (inputId, captionId) => {
  let caption = document.getElementById(captionId);
  document
    .querySelector(`#${inputId}`)
    .addEventListener("input", async (event) => {
      let valueLength = event.target.value.length;
      if (valueLength <= 250) {
        let content = ReworkSize(caption, event.target.value);
        caption.innerHTML = content;
      }
      event.target.value = caption.innerHTML;
    });
};

//The functions:

function PlayerPlayerPlayerPlayer(playerplayerplayer) {
  playerplayer.appendChild(playerplayerplayer);
}

function SubmitMeme() {
  alert(
    "MEME HAS BEEN SUBMITTED YOU WRETCHED WEAKLING!! BOW BEFORE YOUR CREATOR, GOD(ME) ALMIGHTY!!!!!"
  );
}

for (var i = 0; i < 4; i++) {
  let playerplayerplayer = player.cloneNode(true);
  playerplayerplayer.id = `player${i}`;
  if (i % 2 === 0) {
    playerplayerplayer.style.backgroundColor = "lightgray";
  }
  PlayerPlayerPlayerPlayer(playerplayerplayer);
}
