// the total number of tabs open at the end of the hour
//    chrome.tabs.query(object queryInfo, function callback)
// the total number of windows open at the end of the hour
//    chrome.windows.getAll(object getInfo, function callback)
// the total number of tabs opened during the hour
//    chrome.tabs.onCreated.addListener(function callback)
// the total number of windows opened during the hour
//    chrome.windows.onCreated.addListener(function callback)
// the total number of tabs looked at during the hour
//    chrome.tabs.onActivated.addListener(function callback)
// the favicon from every updated tab
//    chrome.tabs.onUpdated.addListener(function callback)
// tab.favIconUrl (this requires the “tabs” permission)


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
var current_tabCount = 0;
var current_windowCount = 0;
var tabs_created = 0;
var tabs_activated = 0;
var windows_created = 0;
var favicons = [];


//constant
chrome.tabs.onCreated.addListener(function(){
  tabs_created += 1;
  console.log("tabs created: ", tabs_created);
})

chrome.windows.onCreated.addListener(function(){
  windows_created +=1;
  console.log("windows created: ", windows_created);

})

chrome.tabs.onActivated.addListener(function(tab) {
	chrome.tabs.get(tab.tabId, function(tab) {
		if(tab.favIconUrl !== favicons[favicons.length - 1] &&
			 tab.favIconUrl !== undefined &&
			 tab.favIconUrl.length > 0 &&
			 tab.favIconUrl !== "https://www.google.com/favicon.ico") {
			var currentFavicon = tab.favIconUrl;
			favicons.push(currentFavicon);
		}
	})
	console.log("favicons", favicons)
  tabs_activated +=1;
  console.log("tabs activated: ", tabs_activated);
})

chrome.tabs.onUpdated.addListener(function(tab) {
	chrome.tabs.get(tab, function(tab) {
		if(tab.favIconUrl !== favicons[favicons.length - 1] &&
			tab.favIconUrl !== undefined &&
			tab.favIconUrl.length > 0 &&
		  tab.favIconUrl !== "https://www.google.com/favicon.ico") {
			var currentFavicon = tab.favIconUrl;
			favicons.push(currentFavicon);
		}
	})
	console.log("favicons", favicons)
})


// on the hour

function saveMetrics(){

	var timestamp = Date.now();
	var database = firebase.database();
	var key = "/users/" + userId + "/metrics/" + timestamp;

	console.log("saving metrics to key:", key);

	var hourlyData = {
		current_tabCount: current_tabCount,
		current_windowCount: current_windowCount,
		tabs_created: tabs_created,
		tabs_activated: tabs_activated,
		windows_created: windows_created,
		favicons: favicons,
		timestamp: timestamp
	};

	console.log("METRICS", hourlyData)

	if(tabs_created > 1){
		database.ref(key).set(hourlyData);
	}

	current_tabCount = 0;
	current_windowCount = 0;
	tabs_created = 0;
	tabs_activated = 0;
	windows_created = 0;
	favicons = [];
};

chrome.alarms.create("everyHour", {
	delayInMinutes: 60,
	periodInMinutes: 60
});

chrome.alarms.onAlarm.addListener(function(alarm){
	chrome.windows.getAll({populate:true}, function(windows){
		current_windowCount = windows.length;
		console.log("current window count:", current_windowCount)
		chrome.tabs.query({}, function(tabs){
			current_tabCount = tabs.length;
			console.log("current tab count:", current_tabCount)
			saveMetrics();
		})
	})
})
