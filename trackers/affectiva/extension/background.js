var webcamHtml = chrome.extension.getURL('webcam.html');

var config = {
  apiKey: "AIzaSyAKb5zWHCkgmBlQvXu3ge_3uiQ5b8jK9g4",
  authDomain: "tabcounter-3aab1.firebaseapp.com",
  databaseURL: "https://tabcounter-3aab1.firebaseio.com",
  projectId: "tabcounter-3aab1",
  storageBucket: "",
  messagingSenderId: "975979989799"
};

// The "firebase" variable is provided by the "firebase.js" script, which should
// have been listed in the manifest.json so that it loads before this script.
firebase.initializeApp(config);

// Learn more about the Firebase JavaScript API
// at this url: https://firebase.google.com/docs/database/web/read-and-write

var userId = "xujenna"

// Open camera
chrome.browserAction.onClicked.addListener(function(tab) {
  console.log('camera is here!');
  cam = window.open(webcamHtml, '_blank', "height=250,width=340");
  chrome.windows.getCurrent(function(win) {
    console.log(win.id);
    win.id = popupid;
  });
});


var data;

chrome.runtime.onMessage.addListener(function(message, tab) {
  data = message;

  }
});


function saveMetrics(){

  var database = firebase.database();
  var key = "/users/" + userId + "/metrics/" + timestamp;

  console.log("saving metrics to key:", key);

  console.log("ANALYSIS", data)
  database.ref(key).set(data);

};


chrome.alarms.create("everyHour", {
  delayInMinutes: 60,
  periodInMinutes: 60
});

chrome.alarms.onAlarm.addListener(function(alarm){
      saveMetrics();
    })
  })
})