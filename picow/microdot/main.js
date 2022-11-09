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

let onClickStart = () => {
    console.log("start");
}

let onCommandKeyPress = (e) => {
  console.log(e);
  if (e.keyCode == 13) {
    onSendCommand();
    e.preventDefault();
  }  
}

let onSendCommand = () => {
  console.log($("#command").val());
  $.ajax({
    url: "/command",
    type: "POST",
    data: {command: $("#command").val()},
    success: function(data) {
      console.log(data);
    }
  });
}
