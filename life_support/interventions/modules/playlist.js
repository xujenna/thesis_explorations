const player = require('play-sound')(opts = {})

let playQueue = []
let callbackQueue = []
let isPlaying = false

const PLAYLIST_DELAY = 0

// This does nothing
function noOp() {
    return
}

function addToPlayQueue(file, callback) {
    // Add file to play queue
    playQueue.push(file)
    // Add callback to queue, pass noOp if no callback was called
    callbackQueue.push(callback || noOp)

    // Check if currently playing file
    if(!isPlaying) {
        // Play the first file in the queue
        playFile(playQueue[0]);
    }
}

function playFile(file, playingFromQueue) {
    // play file with callback
    player.play(file, { timeout: playingFromQueue ? PLAYLIST_DELAY : 0 }, onPlayDone);
    
    // remove first file from queue (just played)
    playQueue.shift();

    // mark is currently playing
    isPlaying = true
}

function onPlayDone() {

    // Mark as done playing
    isPlaying = false

    // Get corresponding callback
    var callback = callbackQueue.shift()

    // Call it
    callback()

    // check if any files remain in the queue
    if(playQueue.length) {
        // play first file in the queue
        playFile(playQueue[0], true);
    }
}

// Export playlist functions
module.exports = {
    addToPlayQueue: addToPlayQueue,
    onPlayDone: onPlayDone,
    playFile: playFile
}