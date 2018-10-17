const functions = require('firebase-functions');
const {dialogflow, SimpleResponse} = require('actions-on-google');
const app = dialogflow();

var admin = require("firebase-admin");

var serviceAccount = require("./selfcare-bot-firebase-adminsdk-x1k54-e7e3675a58.json");

admin.initializeApp({
  credential: admin.credential.cert(serviceAccount),
  databaseURL: "https://selfcare-bot.firebaseio.com"
});


var userId = "xujenna"
var database = admin.database();

// events used to trigger an intent
// sys.any
// routines (actions on google)
// start exercise intent, continue exercise intent, stop exerise intent
// conv.data.currentExercise to koeep place in the workout
// data persists within a session

// const lovingKindness = "<speak>" + "Okay, let's do a loving-kindness meditation. <break time = '2'/>" + "<audio src='https://emmaseppala.com/wp-content/uploads/2014/04/Loving-KindnessMeditation.mp3'></audio>" + "</speak>";

const breathingExercise = '<speak>' + "Okay, let's do a breathing exercise. <break time = '1'/>We're going to breathe in for five counts, then breathe out for five counts. <break time = '2' /> Let's begin. <break time = '1'/> Breathe in for one... <break time = '1'/> two... <break time = '1'/> three... <break time = '1'/> four... <break time = '1'/> Out for one... <break time = '1'/> two... <break time = '1'/> three... <break time = '1'/> four... <break time = '1'/> In for one... <break time = '1'/> two... <break time = '1'/> three... <break time = '1'/> four... <break time = '1'/>Out for one... <break time = '1'/> two... <break time = '1'/> three... <break time = '1'/> four... <break time = '1'/> In for one... <break time = '1'/> two... <break time = '1'/> three... <break time = '1'/> four... <break time = '1'/>Out for one... <break time = '1'/> two... <break time = '1'/> three... <break time = '1'/> four... <break time = '1'/> In for one... <break time = '1'/> two... <break time = '1'/> three... <break time = '1'/> four... <break time = '1'/> Out for one... <break time = '1'/> two... <break time = '1'/> three... <break time = '1'/> four... <break time = '1'/> five..." + "</speak>";

const oneSec =  "<audio src='https://actions.google.com/sounds/v1/alarms/beep_short.ogg'></audio>"
var thirtySecs = ""
for(var i = 0; i <= 30; i++){
	thirtySecs += oneSec;
}
var tenSecs = ""
for(var j = 0; j <= 10; j++){
	tenSecs += oneSec;
}

const sevenMinWorkout_pt1 = "<speak>" + "Great! Let's start with jumping jacks. <break time = '2'/>" + thirtySecs + "Now rest for ten seconds. <break time = '1'/>" + tenSecs+ "</speak>";

const sevenMinWorkout_pt2 = "<speak>" + "Next up, a wall sit. <break time = '2'/>" + thirtySecs + "Now rest. <break time = '1'/>" + tenSecs + "</speak>";

const sevenMinWorkout_pt3 = "<speak>" + "Next up, push-ups. <break time = '2'/>" + thirtySecs + "Now rest. <break time = '1'/>" + tenSecs + "</speak>";

const sevenMinWorkout_pt4 = "<speak>" + "Abdominal crunches are next. <break time = '2'/>" + thirtySecs + "Now rest. <break time = '1'/>" + tenSecs + "</speak>";

const sevenMinWorkout_pt5 = "<speak>" + "Next, step-up onto a chair. <break time = '2'/>" + thirtySecs + "Now rest. <break time = '1'/>" + tenSecs + "</speak>";

const sevenMinWorkout_pt6 = "<speak>" + "Next up, squats. <break time = '2'/>" + thirtySecs + "Now rest. <break time = '1'/>" + tenSecs + "</speak>";

const sevenMinWorkout_pt7 = "<speak>" + "Next, tricep dips on a chair. <break time = '2'/>" + thirtySecs + "Now rest. <break time = '1'/>" + tenSecs + "</speak>"

const sevenMinWorkout_pt8 = "<speak>" + "Next up, plank. <break time = '2'/>" + thirtySecs + "Now rest. <break time = '1'/>" + tenSecs + "</speak>"

const sevenMinWorkout_pt9 = "<speak>" + "Next, high knees running in place. <break time = '2'/>" + thirtySecs + "Now rest. <break time = '1'/>" + tenSecs + "</speak>"

const sevenMinWorkout_pt10 = "<speak>" + "Next up, lunges. <break time = '2'/>" + thirtySecs + "Now rest. <break time = '1'/>" + tenSecs + "</speak>"

const sevenMinWorkout_pt11 = "<speak>" + "Next, push-ups with rotation. <break time = '2'/>" + thirtySecs + "Now rest. <break time = '1'/>" + tenSecs + "</speak>"

const sevenMinWorkout_pt12 = "<speak>" + "Last up, a side plank. <break time = '2'/>" + thirtySecs + "<audio src='https://actions.google.com/sounds/v1/alarms/bugle_tune.ogg'></audio>" + "You did it! That's the end of the seven minute workout." + "</speak>"

var sevenMinWorkout = new Array(sevenMinWorkout_pt1, sevenMinWorkout_pt2, sevenMinWorkout_pt3, sevenMinWorkout_pt4, sevenMinWorkout_pt5, sevenMinWorkout_pt6, sevenMinWorkout_pt7, sevenMinWorkout_pt8, sevenMinWorkout_pt9, sevenMinWorkout_pt10, sevenMinWorkout_pt11, sevenMinWorkout_pt12)


app.intent('7-min-workout-start', (conv,params) => {
	// agent.setContext({
	// 	name:'7-min-workout',
	// 	lifespan: 12,
	// 	parameters:{
	// 	  'currentExercise': 0
	// 	  }
	//   });
	conv.data.currentExercise = 0;

	conv.ask(new SimpleResponse({
		speech: sevenMinWorkout_pt1,
		text: "Great! Let's start with jumping jacks."
	}))
	conv.ask("Would you like to continue?")
})

app.intent('7-min-workout-continue', (conv,params) => {
	conv.data.currentExercise += 1;

	conv.ask(new SimpleResponse({
		speech: sevenMinWorkout[conv.data.currentExercise],
		text: "Step" + conv.data.currentExercise
	}))
	conv.ask("Would you like to continue?")
})


app.intent('guided-exercise', (conv, params) => {
	if(params.discomfort === "stress"){
		discomfort = "stress";
		conv.ask("Laughter can reduce cortisol levels; here's a clip from John Mulaney's comedy special.")
		load('http://www.xujenna.com/delta_airlines.mp3').then(play).catch(console.log("error"))
	}
	// else if(params.discomfort === "depression"){
	// 	conv.ask(new SimpleResponse({
	// 		speech: lovingKindness,
	// 		text: "Okay, let's do a loving-kindness meditation."
	// 	}))
	// }
	else if(params.discomfort === "anxiety"){
		discomfort = "anxiety";
		conv.ask(new SimpleResponse({
			speech: breathingExercise,
			text: "Okay, let's do a breathing exercise.",
		  }))
	}
});

app.intent('breathing-exercise', (conv,params)=>{
	conv.ask(new SimpleResponse({
		speech: breathingExercise,
		text: "Okay, let's do a breathing exercise.",
	  }))
	})

app.intent('good-things-log', (conv,params)=>{
	conv.ask("That's great! Tell me what I should add to your good things log.")
})

app.intent('good-things-log-get-thing', (conv)=>{
	let goodThing = conv.query;
	let timestamp = Date.now();
	var key = "/users/" + userId + "/good-things/" + timestamp;

	var newGoodItem = {
		timestamp: timestamp,
		goodThing: goodThing
	};
	
	database.ref(key).set(newGoodItem);
	conv.ask("Awesome! Your good thing has been saved to your log. Do you want to add to your gratitude log as well?")
})

app.intent('good-things-log-gratitude-log', (conv)=>{
	conv.ask("Amazing. Tell me what you're grateful for!")

})

app.intent('good-things-log-gratitude-log-get-response', (conv)=>{
	let gratitudeItem = conv.query;
	let timestamp = Date.now();
	var key = "/users/" + userId + "/gratitude/" + timestamp;

	var newGratitudeItem = {
		timestamp: timestamp,
		goodThing: gratitudeItem
	};
	
	database.ref(key).set(newGratitudeItem);

	conv.close("Great job! I've added your response to your gratitude log.")
})



app.intent('gratitude-log', (conv,params)=>{
	conv.ask("That's great! Tell me what I should add to your gratitude log.")
})

app.intent('gratitude-log-get-thing', (conv, params)=>{
	let gratitudeItem = conv.query;
	let timestamp = Date.now();
	var key = "/users/" + userId + "/gratitude/" + timestamp;

	var newGratitudeItem = {
		timestamp: timestamp,
		goodThing: gratitudeItem
	};
	
	database.ref(key).set(newGratitudeItem);
})

// app.intent('guided-exercise-repeat', (conv, params)=>{
// 	console.log("params.discomfort: " + params.discomfort)
	
// })

exports.lifeSupport = functions.https.onRequest(app);