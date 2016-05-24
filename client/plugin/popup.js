// http://stackoverflow.com/questions/11684454/getting-the-source-html-of-the-current-page-from-chrome-extension
chrome.runtime.onMessage.addListener(function (request, sender) {
  if (request.action == "getSource") {
    message.innerText = request.source;
    postToServer(request)
  }
});

function postToServer(data) {
  var xhr = new XMLHttpRequest();
  xhr.open("POST", "http://127.0.0.1:5000/raw_data", true);
  xhr.setRequestHeader('Content-Type', 'application/json')
  xhr.onreadystatechange = function () {
    if (xhr.readyState == 4) {
      console.log(xhr.responseText)
    }
  }
  xhr.send(JSON.stringify(data));
}

function inject() {
  var message = document.querySelector('#message');
  chrome.tabs.executeScript(null, {
    file: "getPagesSource.js"
  }, function () {
    // If you try and inject into an extensions page or the webstore/NTP you'll get an error
    if (chrome.runtime.lastError) {
      message.innerText = 'There was an error injecting script : \n' + chrome.runtime.lastError.message;
    }
  });
}

function onWindowLoad() {
  document.getElementById('button').addEventListener('click', inject, false)
}

window.onload = onWindowLoad;