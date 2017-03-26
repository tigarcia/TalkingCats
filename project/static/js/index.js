var mediaConstraints = {
    audio: true
};

let mediaRecorder;
let $recordBtn = $("#record");
let $demoBtn = $("#demo");
let fd;
const DATA = 'data';
const FILENAME = 'filename';

function onMediaError(e) {
  console.error('media error', e);
}


function onMediaSuccess(stream) {
  fd = new FormData();
  mediaRecorder = new MediaStreamRecorder(stream);
  mediaRecorder.mimeType = 'audio/wav';
  mediaRecorder.ondataavailable = function(blob) {
    fd.append(DATA, blob);
  };
  mediaRecorder.onstop = function() {
    $recordBtn.removeClass();
    $recordBtn.addClass("btn btn-default");
    $recordBtn.html("RECORD");
    $.ajax({
      type: 'POST',
      url: '/sound',
      data: fd,
      processData: false,
      contentType: false
    }).done(function(data) {
      dataObj = JSON.parse(data);
      $div = $("#content").append(dataObj.text);
      $("#content").append("<div>" + dataObj.vtext + "</div>");
    });
  };

  mediaRecorder.start();
}


$demoBtn.click(function() {
  $.ajax({
      type: 'GET',
      url: '/demo',
    }).done(function(data) {
      dataObj = JSON.parse(data);
      $div = $("#content").append(dataObj.text);
      $("#content").append("<div>" + dataObj.vtext + "</div>");
    });
});

$recordBtn.click(function(e) {
  if ($recordBtn.html() === 'RECORD') {
    $recordBtn.removeClass();
    $recordBtn.addClass("btn btn-danger");
    $recordBtn.html("STOP REC")
    navigator.getUserMedia(mediaConstraints, onMediaSuccess, onMediaError);
  } else {
    if (mediaRecorder) {
      mediaRecorder.stop();
      mediaRecorder.onstop();
    }
  }
});
