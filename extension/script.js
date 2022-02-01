const form1 = document.getElementById("sum-form");
const form2 = document.getElementById("trans-form");
const summary = document.getElementById("summary");
const transcript = document.getElementById("transc");

function summarize(){
    summary.innerHTML="Summary: ";
}
function transc(){
    transcript.innerHTML="Transcript: ";
}
form1.onsubmit = function(e){
    e.preventDefault();
    chrome.tabs.query({active: true, currentWindow: true}, function(tabs){
        chrome.tabs.sendMessage(tabs[0].id, {"message": "GENERATE"}, function(response){console.log('response')});
    });
};

chrome.runtime.onMessage.addListener(
    function(request, sender, sendResponse) {
        if(request.msg === "RESULT"){
            summary += request.data;
        }
    }
);