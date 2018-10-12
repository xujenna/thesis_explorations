const functions = require('firebase-functions');
const {dialogflow, SimpleResponse} = require('actions-on-google');
const app = dialogflow();

const play = require('audio-play');
const load = require('audio-loader');

const breathingExercise = '<speak>' + "Okay, let's do a breathing exercise to activate the parasympathetic nervous system. <break time = '1'/>We're going to breathe in for five counts, then breathe out for five counts. <break time = '2' /> Let's begin. <break time = '1'/> Breathe in for one... <break time = '1'/> two... <break time = '1'/> three... <break time = '1'/> four... <break time = '1'/> five... <break time = '1'/>Out for one... <break time = '1'/> two... <break time = '1'/> three... <break time = '1'/> four... <break time = '1'/> five... <break time = '1'/> Breathe in for one... <break time = '1'/> two... <break time = '1'/> three... <break time = '1'/> four... <break time = '1'/> five... <break time = '1'/>Out for one... <break time = '1'/> two... <break time = '1'/> three... <break time = '1'/> four... <break time = '1'/> five..." + "</speak>";

const oneSec =  "<audio src='https://actions.google.com/sounds/v1/alarms/beep_short.ogg'></audio>"
var thirtySecs = ""
for(var i = 0; i <= 30; i++){
	thirtySecs += oneSec;
}
var tenSecs = ""
for(var j = 0; j <= 10; j++){
	tenSecs += oneSec;
}

const sevenMinWorkout = "<speak>" + "Okay, let's do the seven minute workout!" + "<audio src='https://actions.google.com/sounds/v1/alarms/bugle_tune.ogg'></audio>" + "Start with jumping jacks. <break time = '2'/>" + thirtySecs+ "Now rest for ten seconds. <break time = '1'/>" + tenSecs + "Next, a wall sit. <break time = '2'/>" + thirtySecs + "Now rest. <break time = '1'/>" + tenSecs + "Next, push-ups. <break time = '2'/>" + thirtySecs + "Now rest. <break time = '1'/>" + tenSecs + "Next up, abdominal crunches. <break time = '2'/>" + thirtySecs + "Now rest. <break time = '1'/>" + tenSecs + "Next, step-up onto a chair. <break time = '2'/>" + thirtySecs + "Now rest. <break time = '1'/>" + tenSecs + "Next up, squats. <break time = '2'/>" + thirtySecs + "Now rest. <break time = '1'/>" + tenSecs + "Next, tricep dips on a chair. <break time = '2'/>" + thirtySecs + "Now rest. <break time = '1'/>" + tenSecs + "Next up, plank. <break time = '2'/>" + thirtySecs + "Now rest. <break time = '1'/>" + tenSecs + "Next, high knees running in place. <break time = '2'/>" + thirtySecs + "Now rest. <break time = '1'/>" + tenSecs + "Next up, lunges. <break time = '2'/>" + thirtySecs + "Now rest. <break time = '1'/>" + tenSecs + "Next, push-ups with rotation. <break time = '2'/>" + thirtySecs + "Now rest. <break time = '1'/>" + tenSecs + "Last up, a side plank. <break time = '2'/>" + thirtySecs + "<audio src='https://actions.google.com/sounds/v1/alarms/bugle_tune.ogg'></audio>" + "You did it! That's the end of the seven minute workout." + "</speak>";



app.intent('guided-exercise', (conv, params) => {
	if(params.discomfort === "stress"){
		conv.ask("Laughter can reduce cortisol levels; here's a clip from John Mulaney's comedy special.")
		load('http://www.xujenna.com/delta_airlines.mp3').then(play).catch(console.log("error"))
	}
	else if(params.discomfort === "anxiety"){
		conv.ask(new SimpleResponse({
			speech: breathingExercise,
			text: "Okay, let's do a breathing exercise.",
		  }))
	}
	else if(params.discomfort === "burn out"){
		conv.ask(new SimpleResponse({
			speech: sevenMinWorkout,
			text: "Okay, let's do the seven minute workout!",
		  }))
	}
});


exports.lifeSupport = functions.https.onRequest(app);
// // Create and Deploy Your First Cloud Functions
// // https://firebase.google.com/docs/functions/write-firebase-functions
//
// exports.helloWorld = functions.https.onRequest((request, response) => {
//  response.send("Hello from Firebase!");
// });
