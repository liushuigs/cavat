// http://stackoverflow.com/questions/11684454/getting-the-source-html-of-the-current-page-from-chrome-extension
chrome.runtime.onMessage.addListener(function (request, sender) {
  if (request.action == "getSource") {
    var payload = {
      source: request.source,
      url: request.url
    }
    postToServer(payload)
  }
});

function showMessage(text) {
  var message = document.querySelector('#message');
  message.innerText = text
}

function postToServer(data) {
  showMessage('uploading...')
  var xhr = new XMLHttpRequest();
  xhr.open("POST", "http://127.0.0.1:5000/raw_data", true);
  xhr.setRequestHeader('Content-Type', 'application/json')
  xhr.onreadystatechange = function () {
    if (xhr.readyState == 4) {
      showMessage('upload success')
    }
  }
  xhr.send(JSON.stringify(data));
}

function inject() {
  chrome.tabs.executeScript(null, {
    file: "getPagesSource.js"
  }, function () {
    // If you try and inject into an extensions page or the webstore/NTP you'll get an error
    if (chrome.runtime.lastError) {
      showMessage('There was an error injecting script : \n' + chrome.runtime.lastError.message)
    }
  });
}

function onWindowLoad() {
  inject()
  //document.getElementById('button').addEventListener('click', inject, false)
}

window.onload = onWindowLoad;