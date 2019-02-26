var admin = require("firebase-admin");

var serviceAccount = require('./mood-predictions-firebase-adminsdk-0ns22-7a7b9f250c.json');

admin.initializeApp({
    credential: admin.credential.cert(serviceAccount),
    databaseURL: 'https://mood-predictions.firebaseio.com/'
});

var db = admin.database();
var ref = db.ref("predictions");



// var TextToSpeechV1 = require('watson-developer-cloud/text-to-speech/v1');

// var watsonCredentials = require('./watsonAPI.json');
// var textToSpeech = new TextToSpeechV1(watsonCredentials);
// var fs = require('fs');

// function speak(something){
//     textToSpeech
//     .synthesize(something, function(err, audio) {
//         if (err) {
//             console.log(err);
//             return;
//         }
//         textToSpeech.repairWavHeader(audio);
//         fs.writeFileSync('audio.wav', audio);
//     });
// }

// var synthesizeParams = {
//     text: 'Hello world',
//     accept: 'audio/wav',
//     voice: 'en-US_AllisonVoice'
// };

// speak(synthesizeParams)




var exec = require('child_process').execSync;

function say(something){
    command = "say ";                      // "say" in this case is a built-in shell command on MAC OS.
    // command = "say -v \"Victoria\" ";   // use the flag "-v" to change to a different voice
    exec(command + something);
  }
  


ref.on("child_added", function(snapshot){
    var newPost = snapshot.val();
    var fatiguePrediction = newPost.LSTM_fatigue_prediction;
    var moodPrediction = newPost.LSTM_mood_prediction;
    var moralePrediction = newPost.LSTM_morale_prediction;
    var stressPrediction = newPost.LSTM_stress_prediction;
    var timestamp = newPost.timestamp;

    console.log(fatiguePrediction)
    console.log(moodPrediction)
    console.log(moralePrediction)
    console.log(stressPrediction)
    console.log(timestamp)
});

