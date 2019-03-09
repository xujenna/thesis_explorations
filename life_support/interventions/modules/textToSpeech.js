const fs = require('fs');
const playlist = require('../modules/playlist');

// Imports the Google Cloud client library
const textToSpeech = require('@google-cloud/text-to-speech');

// Creates a client
const client = new textToSpeech.TextToSpeechClient();


//en-GB-Standard-D
async function say(something){
    let arrayTranscript = [];
    let playlist = [];
    if(typeof something == "string"){
        arrayTranscript.push(something)
    }
    else{
        arrayTranscript = something
    }

    arrayTranscript.forEach((d,i) =>{
        var sayThis = d.replace(/["]+/g, '\"');
        playlist.push('output'+i+'.mp3');

        const request = {
            input: {text: sayThis},
            voice: {languageCode: 'en-US', ssmlGender: 'NEUTRAL'},
            audioConfig: {audioEncoding: 'MP3'},
        };
        // console.log(d);
    
        // Performs the Text-to-Speech request
        client.synthesizeSpeech(request, (err, response) => {
            if (err) {
                console.error('ERROR:', err);
                return;
            }
        
            // Write the binary audio content to a local file
            fs.writeFile('output'+i+'.mp3', response.audioContent, 'binary', err => {
            if (err) {
                console.error('ERROR:', err);
                return;
            }
            if(i == arrayTranscript.length-1){
                console.log(playlist)
                playlist.forEach(d=>{
                    playAudio(d)
                })
            }
            });
        });

    })
}


function playAudio(file) {
    playlist.addToPlayQueue(file);
}

// Export say function
module.exports = {
    say: say
}