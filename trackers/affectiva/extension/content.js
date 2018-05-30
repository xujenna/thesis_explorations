  var divRoot = $("#affdex_elements")[0];
  var width = 640;
  var height = 480;
  var faceMode = affdex.FaceDetectorMode.LARGE_FACES;
  //Construct a CameraDetector and specify the image width / height and face detector mode.
  var detector = new affdex.CameraDetector(divRoot, width, height, faceMode);
  var data =[];
  data.push("{");

  var a       = document.createElement('a');
  // a.href      = 'data:' + data;
  a.download  = 'data.json';
  a.innerHTML = 'download .json file of json';

  document.getElementById('container').appendChild(a);

  //Enable detection of all Expressions, Emotions and Emojis classifiers.
  detector.detectAllEmotions();
  detector.detectAllExpressions();
  detector.detectAllEmojis();
  detector.detectAllAppearance();




  //Add a callback to notify when the detector is initialized and ready for runing.
  detector.addEventListener("onInitializeSuccess", function() {
    log('#logs', "The detector reports initialized");
    //Display canvas instead of video feed because we want to draw the feature points on it
    $("#face_video_canvas").css("display", "block");
    $("#face_video").css("display", "none");
  });

  function log(node_name, msg) {
    $(node_name).append("<span>" + msg + "</span><br />")
  }

  //function executes when Start button is pushed.


  //function executes when the Stop button is pushed.


  function sleep(ms){
    return new Promise(resolve => setTimeout(resolve,ms));
  }

  //Add a callback to notify when camera access is allowed
  detector.addEventListener("onWebcamConnectSuccess", function() {
    log('#logs', "Webcam access allowed");
  });

  //Add a callback to notify when camera access is denied
  detector.addEventListener("onWebcamConnectFailure", function() {
    log('#logs', "webcam denied");
    console.log("Webcam access denied");
  });

  //Add a callback to notify when detector is stopped
  detector.addEventListener("onStopSuccess", function() {
    log('#logs', "The detector reports stopped");
    $("#results").html("");
  });

  //Add a callback to receive the results from processing an image.
  //The faces object contains the list of the faces detected in an image.
  //Faces object contains probabilities for all the different expressions, emotions and appearance metrics
  detector.addEventListener("onImageResultsSuccess", function(faces, image, timestamp) {
    $('#results').html("");


  // var newdata  = "text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(faces[0].expressions));

  // console.log("faces[0].expressions.eyeClosure", faces[0].expressions.eyeClosure);



  var expressions = faces[0].expressions;
  var emotions = faces[0].emotions;

  var newobject = {};
  var bigEvent = false;

  newobject["attention"] = faces[0].expressions["attention"];


  for (var key in expressions) {
    if (expressions[key] > 95) {
      newobject[key] = expressions[key];
      // data.push(newobject);
      bigEvent = true;
    }
  }

  for (var key in emotions) {
    if (emotions[key] > 95){
      newobject[key] = emotions[key];
      bigEvent = true;
      // data.push(newobject);
    }
  }

  if (bigEvent) {
    var emoji = faces[0].emojis["dominantEmoji"];
    newobject["emoji"] = emoji;
    newobject["valence"] = faces[0].emotions["valence"];
    newobject["engagement"] = faces[0].emotions["engagement"];
    newobject["time"] = Date.now();


    data.push(JSON.stringify(newobject));

    console.log("data",data);
    a.href      = 'data:' + data;


    bigEvent = false;

  }





  // if (faces[0].expressions.eyeClosure > 99.7 || ) {

  //    data.push(JSON.stringify(faces[0].expressions));
  // // console.log("data", data);
  //     a.href      = 'data:' + data;


  // }

  // console.log("data", data);


    log('#results', "Timestamp: " + timestamp.toFixed(2));
    log('#results', "Number of faces found: " + faces.length);
    if (faces.length > 0) {
      log('#results', "Appearance: " + JSON.stringify(faces[0].appearance));
      log('#results', "Emotions: " + JSON.stringify(faces[0].emotions, function(key, val) {
        return val.toFixed ? Number(val.toFixed(0)) : val;
      }));
      log('#results', "Expressions: " + JSON.stringify(faces[0].expressions, function(key, val) {
        return val.toFixed ? Number(val.toFixed(0)) : val;
      }));
      log('#results', "Emoji: " + faces[0].emojis.dominantEmoji);
      drawFeaturePoints(image, faces[0].featurePoints);
    }
  });

  //Draw the detected facial feature points on the image
  function drawFeaturePoints(img, featurePoints) {
    var contxt = $('#face_video_canvas')[0].getContext('2d');

    var hRatio = contxt.canvas.width / img.width;
    var vRatio = contxt.canvas.height / img.height;
    var ratio = Math.min(hRatio, vRatio);

    contxt.strokeStyle = "#FFFFFF";
    for (var id in featurePoints) {
      contxt.beginPath();
      contxt.arc(featurePoints[id].x,
        featurePoints[id].y, 2, 0, 2 * Math.PI);
      contxt.stroke();

    }
  }

 detector.start();

  console.log("started");

  setTimeout(function() {
    console.log("stopped");
  detector.removeEventListener();
  detector.stop();
  data["time"] = new Date();
  chrome.runtime.sendMessage(data);

  // });
}, 60000);


   if (window.parent && window.parent.parent){
    window.parent.parent.postMessage(["resultsFrame", {
      height: document.body.getBoundingClientRect().height,
      slug: "opyh5e8d"
    }], "*")
  }
  







   