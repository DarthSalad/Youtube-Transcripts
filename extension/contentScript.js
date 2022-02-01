function reqListener() {
    localStorage.setItem("text", this.responseText);
}

function replaceText() {
    //  console.log('REPLACED GENERATED SUMMARY');
    //  console.log(window.location.href);
    var current_url = window.location.href;
    var url = "http://127.0.0.1:8080/api/summarize?url=" + current_url;
    var xhttp = new XMLHttpRequest();
    xhttp.addEventListener("load", reqListener);
    xhttp.open("GET", url);
    xhttp.send();
}

chrome.runtime.onMessage.addListener(function (request, sender, sendResponse) {
    if (request.message === 'GENERATE') {
        //console.log(request);
        replaceText();
        //console.log(localStorage.getItem("text"));
        var text1 = localStorage.getItem("text");
        console.log(text1);
        chrome.runtime.sendMessage({ "msg": "RESULT", "data": text1 }, function (response) {
            //console.log("blahblah");
        });
    }
});