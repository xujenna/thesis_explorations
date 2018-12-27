
let turns = 0;


let stepTranscripts = [];
let step1 = "We'll do a centering ceremony before you set out on your journey. Please take a comfortable seat at the same level, maintain open body language, and face each other. <silence msec='3000'/> Take a moment to decide which teammate had the original complaint—they are player one. <silence msec='3000'/> Now close your eyes.<silence msec='1000'/> We'll start with a breathing ritual. <silence msec='2500'/> Breathe in for one, <silence msec='1000'/> two, <silence msec='1000'/> three, <silence msec='1000'/> four. And back out for one <silence msec='1000'/>, two <silence msec='1000'/>, three <silence msec='1000'/>, four <silence msec='1000'/>. In for one, <silence msec='1000'/> two, <silence msec='1000'/> three, <silence msec='1000'/> four. Out for one <silence msec='1000'/>, two <silence msec='1000'/>, three <silence msec='1000'/>, four <silence msec='1000'/>. In for one, <silence msec='1000'/> two, <silence msec='1000'/> three, <silence msec='1000'/> four. Out for one <silence msec='1000'/>, two <silence msec='1000'/>, three <silence msec='1000'/>, four <silence msec='3500'/>. Be careful out there: relationships can be treacherous landscapes, so you must tread carefully and deliberately. <silence msec='1000'/> You'll only get out alive if you communicate honestly and listen carefully, without assumptions. <silence msec='1000'/> Focus on the challenge at hand; you will lose points for global statements. <silence msec='1000'/>The quest cannot be completed without the full cooperation of two people, so maintain a positive, generous, and compassionate attitude. <silence msec='1000'/> Remember, there can only be either two winners, or two losers, so leave your ego and pride with me before you go. <silence msec='4000'/> Now open your eyes. Player one, let me know when you're ready, and we can begin."

stepTranscripts.push(step1)



const SpeechRecognition = webkitSpeechRecognition;
const synth = window.speechSynthesis;

async function speak(textInput) {
    if (synth.speaking) {
      console.error('already speaking')
      setTimeout(function () {
        let utterThis = new SpeechSynthesisUtterance(textInput)
        synth.speak(utterThis) 
      }, 2500);
    }
    else{
      let utterThis = new SpeechSynthesisUtterance(textInput)
      await synth.speak(utterThis)
    }
  }

function listen(){
    const recognition = new SpeechRecognition();
    recognition.lang = 'en-US';
    recognition.continuous = true;
    recognition.interimResults = true;
    recognition.start();
  
    recognition.onresult = event => {
        if (typeof (event.results) !== 'undefined') {
            for (var i = event.resultIndex; i < event.results.length; ++i) {
                if(event.results[i][0].transcript.includes("always", "never", "all the time")){
                    speak("Focus on the issue at hand; avoid using global statements.")
                }
                if (event.results[i].isFinal) {
                    recognition.stop();
                    newString += event.results[i][0].transcript;
                }
            }
        }
    }
    recognition.onend = () => {
        if(newString.includes("I'm ready", "I'm done", "next step")){
            nextStep();
        }
        else{
            listen();
        }
    }

    recognition.onerror = event => {
        console.log("error" + event.error);
        speak("I didn't hear you. Try again.");
        listen();
    }
}

function nextStep(){
    turns += 1;
    let currentStep = document.getElementById("step"+turns);
    currentStep.style.display="block";
    currentStep.scrollIntoView({behavior:"smooth", block:"center"});

    speak(stepTranscripts[turns]);
    listen();
}




// function start(){
//     let step1 = document.getElementById("step1");
//     step1.style.display="block";
//     step1.scrollIntoView({behavior:"smooth", block:"center"});

//     speak("We'll do a centering ceremony before you set out on your journey. Please take a comfortable seat at the same level, maintain open body language, and face each other. <silence msec='3000'/> Take a moment to decide which teammate had the original complaint—they are player one. <silence msec='3000'/> Now close your eyes.<silence msec='1000'/> We'll start with a breathing ritual. <silence msec='2500'/> Breathe in for one, <silence msec='1000'/> two, <silence msec='1000'/> three, <silence msec='1000'/> four. And back out for one <silence msec='1000'/>, two <silence msec='1000'/>, three <silence msec='1000'/>, four <silence msec='1000'/>. In for one, <silence msec='1000'/> two, <silence msec='1000'/> three, <silence msec='1000'/> four. Out for one <silence msec='1000'/>, two <silence msec='1000'/>, three <silence msec='1000'/>, four <silence msec='1000'/>. In for one, <silence msec='1000'/> two, <silence msec='1000'/> three, <silence msec='1000'/> four. Out for one <silence msec='1000'/>, two <silence msec='1000'/>, three <silence msec='1000'/>, four <silence msec='3500'/>. Be careful out there: relationships can be treacherous landscapes, so you must tread carefully and deliberately. <silence msec='1000'/> You'll only get out alive if you communicate honestly and listen carefully, without assumptions. <silence msec='1000'/> Focus on the challenge at hand; you will lose points for global statements. <silence msec='1000'/>The quest cannot be completed without the full cooperation of two people, so maintain a positive, generous, and compassionate attitude. <silence msec='1000'/> Remember, there can only be either two winners, or two losers, so leave your ego and pride with me before you go. <silence msec='4000'/> Now open your eyes. Player one, let me know when you're ready, and we can begin.");

//     listen();
// }

// Be careful out there: relationships can be treacherous landscapes, so you must tread carefully and deliberately. <silence msec='1000'/> You'll only get out alive if you communicate honestly and listen carefully, without assumptions.  <silence msec='1000'/> The quest cannot be completed without the full cooperation of two people, so maintain a positive, generous, and compassionate attitude.  <silence msec='1000'/> There can only be either two winners, or two losers, so leave your ego and pride with me before you go.

//Now return your breathing to normal. <silence msec='3000'/>  Player one, repeat after me: <silence msec='1000'/>I promise to communicate honestly and listen carefully, without assumptions. <silence msec='10000'/> I promise to listen with empathy and give the benefit of the doubt. <silence msec='10000'/> I promise to maintain a positive, generous, and compassionate attitude. <silence msec='10000'/> <silence msec='5000'/> Player two, repeat after me: <silence msec='1000'/>I promise to communicate honestly and listen carefully, without assumptions. <silence msec='10000'/> I promise to listen with empathy and give the benefit of the doubt. <silence msec='10000'/> I promise to maintain a positive, generous, and compassionate attitude. <silence msec='5000'/>  You are ready. Remember, there can only be either two winners, or two losers, so leave your ego and pride with me before you go.