// set up basic variables for app

var record = document.querySelector('.record');
var stop = document.querySelector('.stop');
var mainSection = document.querySelector('.main-controls');
var transcriptions = document.querySelector('.transcriptions');

var options = {
    mimeType : 'audio/ogg; codecs=opus'
}
// disable stop button while not recording

stop.disabled = true;

//main block for doing the audio recording

if (navigator.mediaDevices.getUserMedia) {
  console.log('getUserMedia supported.');

  var constraints = { audio: true };
  var chunks = [];

  var onSuccess = function(stream) {
    console.log(options.mimeType + " is supported? " + MediaRecorder.isTypeSupported(options.mimeType));
    var mediaRecorder = new MediaRecorder(stream);

    record.onclick = function() {
      mediaRecorder.start();
      console.log(mediaRecorder.state);
      console.log("recorder started");
      record.style.background = "red";

      stop.disabled = false;
      record.disabled = true;
    }

    stop.onclick = function() {
      mediaRecorder.stop();
      console.log(mediaRecorder.state);
      console.log("recorder stopped");
      record.style.background = "";
      record.style.color = "";
      // mediaRecorder.requestData();

      stop.disabled = true;
      record.disabled = false;
    }

    mediaRecorder.onstop = function(e) {
      console.log("data available after MediaRecorder.stop() called.");

      var blob = new Blob(chunks, { 'type' : options.mymeType });
      chunks = [];

      var fd = new FormData();
      fd.append('file', blob, 'test.ogg');
      $.ajax({
          type: 'POST',
          url: '/echo',
          data: fd,
          cache: false,
          processData: false,
          contentType: false,
          timeout: 1000

      }).done(function(data) {
          console.log("Done!");
          console.log(data);

          var textContainer = document.createElement('article');
          var deleteButton = document.createElement('button');

          deleteButton.innerHTML = "Delete";
          textContainer.innerHTML = data;

          textContainer.appendChild(deleteButton);

          deleteButton.onclick = function(e) {
            evtTgt = e.target;
            evtTgt.parentNode.parentNode.removeChild(evtTgt.parentNode);
          }

      }).fail(function(data) {
          console.log("Fail!");
          console.log(data);
      });

      console.log("recorder stopped");
    }

    mediaRecorder.ondataavailable = function(e) {
      chunks.push(e.data);
    }
  }

  var onError = function(err) {
    console.log('The following error occured: ' + err);
  }

  navigator.mediaDevices.getUserMedia(constraints).then(onSuccess, onError);

} else {
   console.log('getUserMedia not supported on your browser!');
}
