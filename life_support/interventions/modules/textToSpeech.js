const fs = require('fs');
const playlist = require('../modules/playlist');

// Imports the Google Cloud client library
const textToSpeech = require('@google-cloud/text-to-speech');

// Creates a client
const client = new textToSpeech.TextToSpeechClient();



async function say(something){

    var sayThis = something.replace(/["]+/g, '\"');
    
    const request = {
        input: {text: sayThis},
        voice: {languageCode: 'en-US', ssmlGender: 'NEUTRAL'},
        audioConfig: {audioEncoding: 'MP3'},
    };

    // Performs the Text-to-Speech request
    client.synthesizeSpeech(request, (err, response) => {
        if (err) {
            console.error('ERROR:', err);
            return;
        }
    
        // Write the binary audio content to a local file
        fs.writeFile('output.mp3', response.audioContent, 'binary', err => {
        if (err) {
            console.error('ERROR:', err);
            return;
        }

        playAudio();
        });
    });

}


function playAudio() {
    playlist.addToPlayQueue('output.mp3');
    playlist.addToPlayQueue('output.mp3', () => console.log('TWO'));
    playlist.addToPlayQueue('output.mp3', () => console.log('THREE'));
}

// Export say function
module.exports = {
    say: say
}