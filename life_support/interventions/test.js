// load node modules
var SunCalc = require('suncalc');
var exec = require('child_process').execSync;


// initialize firebase
var admin = require("firebase-admin");
var serviceAccount = require('./mood-predictions-firebase-adminsdk-0ns22-7a7b9f250c.json');

admin.initializeApp({
    credential: admin.credential.cert(serviceAccount),
    databaseURL: 'https://mood-predictions.firebaseio.com/'
});

var db = admin.database();
var predictionsRef = db.ref("predictions");
var interventionsRef = db.ref("interventions");
// https://firebase.google.com/docs/database/admin/save-data


// watson speech
// https://cloud.ibm.com/apidocs/text-to-speech
var TextToSpeechV1 = require('watson-developer-cloud/text-to-speech/v1');
var watsonCredentials = require('./watsonAPI.json');
var textToSpeech = new TextToSpeechV1(watsonCredentials);
var fs = require('fs');

function say(something){
    something.forEach((d,i) => {
        var sayThis = d.replace(/["]+/g, '\"');
        // SSML doc https://console.bluemix.net/docs/services/text-to-speech/SSML-transformation.html#transformation
        
        var synthesizeParams = {
            text: "<voice-transformation type='Custom' glottal_tension='-60%' pitch_range='10%' rate='10%'>" + sayThis + "</voice-transformation>",
            accept: 'audio/wav',
            voice: 'en-US_LisaVoice'
        };

        textToSpeech
        .synthesize(synthesizeParams, function(err, audio) {
            if (err) {
                console.log(err);
                return;
            }
            textToSpeech.repairWavHeader(audio);
            fs.writeFileSync('audio' + i + '.wav', audio);
            command = util.format('afplay audio' + i + '.wav');
            exec(command);
        });
    })
}

// function say(something){
//     command = "say ";
//     exec(command + something);
//   }
  

// load interventions
var poetry = require('./poetry.json');
var meditation = require('./meditations.json');
var exercise = require('./exercises.json');

const moodInterventions = [interactions, goodThings, meditation.mood]
const moraleInterventions = [poetry, videos, exercise.dance]
const stressInterventions = [poetry, videos, exercise.workouts, exercise.dance, meditation.stress]
const fatigueInterventions = [poetry, exercise.dance, meditation.stress]



predictionsRef.on("child_added", function(snapshot){
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
    say("You should take a walk.")

    // interventionsRef.push().set(interventionObjTK)
}

function moraleIntervention(prediction, sunTimes){
    console.log("Your morale prediction is "+prediction+ ".\n")

    switch (Math.round(Math.random() * moraleInterventions.length)) {
        case 0:
            let poet = poetry[Math.round(Math.random() * poetry.length)]
            let poem = poet.poems[Math.round(Math.random() * poet['poems'].length)];
            
            console.log(poem.title + '\n');
            say(poem.title);
            
            let singleLinePoem = ""
            poem['text'].forEach(d =>{
                console.log(String(d));
                var cleaned = String(d.replace("'", '').replace(';', '').replace(':', '').replace('?', ''))
                singleLinePoem += (cleaned + "<break time='200ms'/>")
            })

            say(singleLinePoem);
            console.log('\n')


            interventionsRef.push().set({
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