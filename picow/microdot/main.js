let rpm = 100;
const mmperrev = 10;

let mmIncrease = 1;
let run = false;

window.addEventListener('load', function() {
  console.log('window loaded');
var content = document.getElementById('content');
// load htmlfile and insert into content div
  var xhr = new XMLHttpRequest();
  xhr.open('GET', 'views/home.html', true);
  xhr.onreadystatechange = function() {
      if (xhr.readyState == 4) {
          content.innerHTML = xhr.responseText;
          document.getElementById("command").addEventListener("keypress", onCommandKeyPress);
      }
  };
  xhr.send(null);  
});

let sendCommand = (command) => {
  console.log('sending command: ' + command);
  $.ajax({
    url: "/command",
    type: "POST",
    data: {command: command},
    success: function(data) {
      console.log(data);
    }
  });
}

let onClickStart = () => {
  if (run == false) {
    run = true;
    turn();
    console.log("start");
    setTimeout(turn, timeout);
  }
}

let onClickStop = () => {
  run = false;
  console.log("stop");
}

let onRPMChange = () => {
  rpm = $("#speed").val();
  $("#rpm").text(rpm);
}

let turn = () => {
  if (run == true) {
    let timeout = 300;
    if (rpm > 0) {
      let mmpermin = rpm * mmperrev ;
      timeout = mmIncrease * 60000 / mmpermin;
      if (timeout < 200) {
        timeout = 200;
        mmIncrease = timeout * mmpermin / 60000;
      }
      sendCommand(`G1 G91 X${mmIncrease} F${mmpermin}`);
    }
   setTimeout(turn, timeout-1);
  }
}


let onCommandKeyPress = (e) => {
  console.log(e);
  if (e.keyCode == 13) {
    onSendCommand();
    e.preventDefault();
  }  
}

let onSendCommand = () => {
  sendCommand($("#command").val());
}
