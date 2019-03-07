// load modules
var SunCalc = require('suncalc');
const database = require('../modules/datastore');
const textToSpeech = require('../modules/textToSpeech');

// load interventions
var poetry = require('./poetry.json');
var meditation = require('./meditations.json');
var exercise = require('./exercises.json');

// interventions by marker
const moodInterventions = [interactions, goodThings, meditation.mood]
const moraleInterventions = [poetry, videos, exercise.dance]
const stressInterventions = [poetry, videos, exercise.workouts, exercise.dance, meditation.stress]
const fatigueInterventions = [poetry, exercise.dance, meditation.stress]


database.predictionsRef.on("child_added", function(snapshot){
    var newPost = snapshot.val();
    var fatiguePrediction = newPost.LSTM_fatigue_prediction;
    var moodPrediction = newPost.LSTM_mood_prediction;
    var moralePrediction = newPost.LSTM_morale_prediction;
    var stressPrediction = newPost.LSTM_stress_prediction;
    var timestamp = newPost.timestamp;

    var currentTime = + new Date();
    var sunTimes = SunCalc.getTimes(currentTime, 40.7, -74)

    if((currentTime / 1000) - timestamp <= 3700){
        if(fatiguePrediction > 3.2){
            fatigueIntervention(fatiguePrediction, sunTimes);
        }
        else if(moralePrediction < 2.8){
            moraleIntervention(moralePrediction, sunTimes);
        }
    }
});


function fatigueIntervention(prediction, sunTimes){
    console.log("Your fatigue prediction is "+prediction+ ". You should take a walk.")
    textToSpeech.say("You should take a walk.")

    // interventionsRef.push().set(interventionObjTK)
}

function moraleIntervention(prediction, sunTimes){
    console.log("Your morale prediction is "+prediction+ ".\n")

    switch (Math.round(Math.random() * moraleInterventions.length)) {
        case 0:
            let poet = poetry[Math.round(Math.random() * poetry.length)]
            let poem = poet.poems[Math.round(Math.random() * poet['poems'].length)];
            
            console.log(poem.title + '\n');
            textToSpeech.say(poem.title);
            
            poem['text'].forEach(d =>{
                console.log(String(d));
                var cleaned = String(d.replace("'", '').replace(';', '').replace(':', '').replace('?', ''))
                textToSpeech.say(cleaned+ "<break time='200ms'/>");
            })

            database.interventionsRef.push().set({
                marker: "morale",
                prediction: prediction,
                intervention: "poetry",
                content: poem
            })

            break;

        case 1:
            console.log("last has no break")

    }
}

function stressIntervention(prediction){
    // interventionsRef.push().set(interventionObjTK)

}