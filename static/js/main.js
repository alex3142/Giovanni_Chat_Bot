/*  ----------------------------------  */
/*  -------  Speech Synthesis  -------  */
/*  ----------------------------------  */

var ourVoice = speechSynthesis.getVoices().filter(function(voice) { 
    return voice.name == "Google UK English Male"; 
})[0];

var speaker = document.querySelector('.speak');
var speakerOn = false;

toggleSpkColor = function() {
    if (speaker.style.color == "") {
        speaker.style.color = "#6A40C2";
        speaker.firstElementChild.classList.toggle("fa-volume-off");
        speaker.firstElementChild.classList.toggle("fa-volume-up");
        speakerOn = true;
    } else {
        speaker.style.color = "";
        speaker.firstElementChild.classList.toggle("fa-volume-up");
        speaker.firstElementChild.classList.toggle("fa-volume-off");
        speakerOn = false;
    }
}

speaker.addEventListener("click",toggleSpkColor);

function readOutLoud2(msg) {
    var speech = new SpeechSynthesisUtterance();
    speech.text = msg;
    speech.volume = 1;
    speech.rate = 1;
    speech.pitch = 1;
    speech.voice = ourVoice;


    window.speechSynthesis.speak(speech);
}

function readOutLoud(msg) {
    responsiveVoice.speak(msg, "Italian Female", {pitch:0.5});
}

/*  ----------------------------------  */
/*  -------  Main Interaction  -------  */
/*  ----------------------------------  */

var xmlhttpR = new XMLHttpRequest();
window.onload = function() {
    xmlhttpR.open("GET","/new_session");
    xmlhttpR.send();
}

var msg = document.querySelector('.messages')
var textInput = document.querySelector('.message-input textarea');
var submitBtn = document.querySelector('.submit');
var msgList = document.querySelector('.messages ul');

var xmlhttp = new XMLHttpRequest();
xmlhttp.onreadystatechange = function() {
    if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
        response = JSON.parse(xmlhttp.response);
        appendMessage(response.response,"received");
        if (speakerOn) {
            readOutLoud(response.response);
        }
    }
    return false;
}  

appendMessage = function(message,who) {
    var nodeP = document.createElement("p");
    nodeP.innerHTML = message;
    var nodeA = nodeP.querySelector('a')
    if (nodeA) {
        nodeA.target="_blank";
    }
    var nodeLi = document.createElement('li');
    nodeLi.className = who;
    nodeLi.appendChild(nodeP);
    msgList.appendChild(nodeLi);
    msg.scroll(0,msg.scrollHeight);
}

giovanniSays = function (sentence) {
    xmlhttp.open("POST", "/run_pipeline");
    xmlhttp.setRequestHeader('content-type', 
        'application/x-www-form-urlencoded;charset=UTF-8'); 
    xmlhttp.send("sentence="+sentence);
}

sendMessage = function(msg) {
    if (msg) {
        appendMessage(msg,"sent");
        giovanniSays(msg);
        return true;
    } else {
        return false;
    }
}

onSubmit = function(e) {
    var caca = sendMessage(textInput.value);
    if (caca) {
        textInput.value = "";
    }
}
submitBtn.addEventListener("click",onSubmit);

onEnter = function(e) {
    var charCode = (e.which) ? e.which : e.keyCode
    if (charCode == 13) { // enter key
        e.preventDefault();
        var caca = sendMessage(textInput.value);
        if (caca) {
            textInput.value = "";
        }
    }
}
textInput.addEventListener('keydown', onEnter);

var dbg = document.querySelector('.messages.debug');
var infoBtn = document.querySelector('#infoBtn');
toggleDebugger = function () {
    if (dbg.style.display) {
        dbg.removeAttribute("style");
        msg.classList.add('side');
        infoBtn.style.color="#6A40C2";
    } else {
        dbg.style.display="None";
        msg.classList.remove('side');
        infoBtn.style.color="";
    }
}

infoBtn.addEventListener("click",toggleDebugger);

// appendMessage("Hej u hungry?","received");

/*  ------------------------------------  */
/*  -------  Speech Recognition  -------  */
/*  ------------------------------------  */

window.SpeechRecognition = window.webkitSpeechRecognition || 
                            window.SpeechRecognition;

const recognition = new window.SpeechRecognition();
recognition.continuous = false
recognition.onaudiostart = function(e) {console.log('audio start')}
recognition.onspeechstart = function (e) {console.log('speech start')}
recognition.onaudioend = function (e) {console.log('audio end')}

var microphone = document.querySelector('.record');
var recognizing = false;

toggleMicColor = function() {
    if (microphone.style.color == "") {
        microphone.style.color = "#6A40C2";
        microphone.firstElementChild.classList.toggle("fa-microphone-slash");
        microphone.firstElementChild.classList.toggle("fa-microphone");
    } else {
        microphone.style.color = "";
        microphone.firstElementChild.classList.toggle("fa-microphone");
        microphone.firstElementChild.classList.toggle("fa-microphone-slash");
    }
}

recognitionEpisode = function() {
    if (!recognizing) {
        toggleMicColor();
        recognition.start();
        recognizing = true;
    } else {
        recognition.abort();
    }
}

recognition.onend = function () {
    recognizing = false;
    toggleMicColor();
    // recognition.start();
}

microphone.addEventListener("click",recognitionEpisode);

recognition.onresult = function (e) {
    console.log(event.results[0][0].transcript);
    sendMessage(event.results[0][0].transcript);
}