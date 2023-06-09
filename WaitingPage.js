const timer = document.getElementById("timer");

const lobby = window.location.href.split("/")[3];
let counter = 120;

SetupWaiting();


async function SetupWaiting()  {
    const response = await fetch("waitingpage?a=setup");
    if (response){
        const data = await response.json();
        counter = data.time;
        timer.innerHTML = `${counter/60 < 10 ? `0${Math.floor(counter/60)}`:Math.floor(counter/60)}:${counter%60<10 ?" 0": ""}${counter%60}`;

        setInterval(() => {
            counter--;
            timer.innerHTML = `${counter/60 < 10 ? "0":""}${Math.floor(counter/60)}:${counter%60<10 ?" 0": ""}${counter%60}`;
            if (counter <= 0) {
                SeeIfRate();
            }
        },1000);

        setInterval(async () => {
            const response = await fetch("waitingpage?a=gettime");
            if (response){
                const data = await response.json();
                counter = data.time -1;
                
            }
        },5000);
    }
};

async function SeeIfRate() {
    const response = await fetch("waitingpage?a=rate");
    if (response) {
        const data = await response.text(); 
        if (data === "ok") {
            window.location.href = "/" + `${lobby}/ratememe.html`;
        }
    }
}

