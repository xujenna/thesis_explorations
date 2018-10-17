var margin = {top: 50, right: 40, bottom: 50, left: 40};
var margin2 = {top: 5, right:2, bottom:20, left:2};

var width = (window.innerWidth - (window.innerWidth * .27)) - margin.right - margin.left,
height = 550 - margin.top - margin.bottom;

var height2 = 80 - margin2.top - margin2.bottom;
var width2 = (window.innerWidth - (window.innerWidth * .18)) - margin2.right - margin2.left;
var body = d3.select("body");

var contextSVG = d3.select("#context")
      .attr("width", width2 + margin2.left + margin2.right)
      .attr("height", height2 + margin2.top + margin2.bottom);


var reporterSVG = d3.select("#reporter")
      .attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.top + margin.bottom);


var xScale = d3.scaleTime()
  .range([0,width]);
  // .domain([xMin, xMax]);

var xScale2 = d3.scaleTime()
.range([0,width2]);

var yScale = d3.scaleLinear()
  .range([height,0]);
  // .domain([0.45,1]);

var yScale2 = d3.scaleLinear()
  .range([height2,0]);

var xAxis = d3.axisBottom(xScale).tickPadding(10);
var xAxis2 = d3.axisBottom(xScale2).tickSize(-height2).tickPadding(10);
var yAxis = d3.axisLeft(yScale).tickSize(-width).ticks(5).tickPadding(10).tickSizeOuter(0);


var reporterChart = reporterSVG.append("g")
  .attr("class", "focus")
  .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

var contextChart = contextSVG.append("g")
  .attr("class", "context")
  .attr("transform", "translate(" + margin2.left + "," + margin2.top + ")");


  var brush = d3.brushX()
    .extent([[0,0], [width2, height2]])
    .on("brush end", brushed);


  var moodArea = d3.area()
      // .curve(d3.curveCardinal)
      .x(function(d) { return xScale(d.time); })
      .y1(function(d) { return yScale(d.mood); })
      .y0(height)
        .defined(function(d){return d.mood!=null;});

  var fatigueArea = d3.area()
    // .curve(d3.curveCardinal)
    .x(function(d) { return xScale(d.time); })
    .y1(function(d) { return yScale(d.fatigue); })
    .y0(height)
      .defined(function(d){return d.fatigue!=null;});


  var stressArea = d3.area()
      // .curve(d3.curveCardinal)
      .x(function(d) { return xScale(d.time); })
      .y1(function(d) { return yScale(d.stress); })
      .y0(height)
        .defined(function(d){return d.stress!=null;});

  var moraleArea = d3.area()
      // .curve(d3.curveCardinal)
      .x(function(d) { return xScale(d.time); })
      .y1(function(d) { return yScale(d.morale); })
      .y0(height)
        .defined(function(d){return d.morale!=null;});


  var moodLine = d3.line()
  .defined(function(d){return d.mood!=null})
    .x(function(d) {return xScale(d.time);})
    .y(function(d){return yScale(d.mood) - 1.5;});

  var moodLine2 = d3.line()
  .defined(function(d){return d.mood!=null})
    .x(function(d) {return xScale2(d.time);})
    .y(function(d){return yScale2(d.mood);});

var newResponses = [];



d3.tsv("responses.tsv", function (err, responses) {
    if (err) console.warn(err, "error loading data");


responses.forEach(function(d){
  var dateTime = new Date(d.unix_time * 1e3);
  d.time = dateTime;
  d.mood = +d.mood;
  d.fatigue = +d.fatigue;
  d.morale = +d.morale;
  d.unique_interactions = +d.unique_interactions;
  d.stress = +d.stress;
});



responses.forEach(function(d,i){

newResponses.push(d)

  if(i+1 == responses.length){
    return;
  }


  var timee = responses[i+1].time;


  if(d.time < (timee - 24000000)) {
    var nullTime = new Date(timee - 24000000);
    var nullItems = {};

    nullItems["time"] = nullTime;
    nullItems["mood"] = null;
    nullItems["moodNotes"] = null;
    nullItems["fatigue"] = null;
    nullItems["stress"] = null;
    nullItems["activities"] = null;
    nullItems["morale"] = null;
    nullItems["compulsions"] = null;

    newResponses.push(nullItems);
  }

})


var xScaleMax = d3.max(newResponses, function(d) {return d.time;})
var xScaleMin = new Date(1524982083090)

xScale.domain([xScaleMin, xScaleMax]);
yScale.domain([0,5]);
yScale2.domain(yScale.domain());

var domainMax = new Date(parseInt(newResponses[newResponses.length-1].unix_time * 1000));
var domainMin = new Date();
domainMin.setMonth(domainMax.getMonth() - 1);

xScale2.domain([domainMin, domainMax])


reporterChart.append("g")
  .attr("class", "axis axis--x")
  .attr("transform","translate(0, "+(height)+")")
  .call(xAxis);

reporterChart.append("g")
.attr("class", "axis axis--y")
  .call(yAxis);



reporterChart.append("path")
  .datum(newResponses)
  .attr("class", "moodArea")
  .attr("d", moodArea)
  .attr("fill", "magenta")
  .attr("opacity", 0.4);

reporterChart.append("path")
  .datum(newResponses)
  .attr("class", "moraleArea")
  .attr("d", moraleArea)
  .attr("fill", "gold")
  .attr("opacity", 0.4);


reporterChart.append("path")
  .datum(newResponses)
  .attr("class", "stressArea")
  .attr("d", stressArea)
  .attr("fill", "blue")
  .attr("opacity", 0.25);


reporterChart.append("path")
  .datum(newResponses)
  .attr("class", "fatigueArea")
  .attr("d", fatigueArea)
  .attr("fill", "lavender")
  .attr("opacity", 0.7);



var compulsionCircles = reporterChart.selectAll(".compulsion-circle")
  .data(newResponses)
  .enter()
  .append("text")
  .attr("class","compulsion-x")
  .attr("x", function(d) {return xScale(d.time) - 1200})
  .text(function(d){ return d.compulsions == "False" || d.compulsions == null ? console.log("null") : "×"})
  .attr("y", function(d){return yScale(d.stress) + 3;})
  .attr("opacity", 0.7)
  .attr("fill", "blue");

reporterChart.append("path")
  .datum(newResponses)
  .attr("d", moodLine)
  .attr("stroke", "magenta")
  .attr("stroke-width", 2)
  .attr("fill", "none")
  .attr("class", "moodLine")
  .attr("opacity", 0.7);


var moodCircles = reporterChart.selectAll(".moodCircle")
  .data(newResponses)
  .enter()
  .append("circle")
  .attr("class","moodCircle")
  .attr("cx", function(d) {return xScale(d.time)})
  .attr("r", function(d) {return d.mood == null ? 0 : 3; })
  .attr("cy", function(d) { return yScale(d.mood);})
  .attr("opacity", 0.7)
  .attr("fill", "magenta");





// contextChart.append("path")
//   .attr("d", moodLine2(newResponses))
//   .attr("stroke", "black")
//   .attr("stroke-width", 2)
//   .attr("fill", "none")
//   .attr("class", "line");

var month = new Array();
month[0] = "January";
month[1] = "February";
month[2] = "March";
month[3] = "April";
month[4] = "May";
month[5] = "June";
month[6] = "July";
month[7] = "August";
month[8] = "September";
month[9] = "October";
month[10] = "November";
month[11] = "December";


var dataLength = newResponses.length
var maxDate = newResponses[dataLength-1]['time']
var maxDateDay = new Date(newResponses[dataLength-1]['time'])
maxDateDay.setDate(maxDate.getDate() - 2)


var contextNavBack = d3.select("#viewport-back");
var contextNavForward = d3.select("#viewport-forward");
var currentDisplayDate = new Date(parseInt(newResponses[newResponses.length-1].unix_time * 1000));
var currentDisplayIndex = currentDisplayDate.getMonth();

// var firstDate = new Date(1524982083090);

contextChart.append("g")
    .attr("class", "axis")
    .attr("transform", "translate(0," + height2 + ")")
    .call(xAxis2);

var currentID = "March";

contextChart.selectAll(".mood-bars")
  .data(newResponses)
  .enter().append("rect")
  .filter(function(d) {return d.unix_time > 1524981000})
  .attr("class", "mood-bars")
  .attr("id", function(d){
    var currentDate = new Date(parseInt(d.unix_time * 1000))
    var currentMonth = currentDate.getMonth()
    if (month[currentMonth] == currentID) {
      console.log("skip")
    }
    else {
      currentID = month[currentMonth];
      return currentID;
    }
  })
  .style("fill", "grey")
  .style("opacity", "0.3")
  .attr("x", function(d) {return xScale2(d.time)})
  .attr("width", "3px")
  .attr("y", function(d) {return yScale2(d.mood)})
  .attr("height", function(d) {return height2 - yScale2(d.mood)})


var contextBrush = contextChart.append("g")
    .attr("class", "brush")
    .call(brush)
    .call(brush.move, [maxDateDay, maxDate].map(xScale2));


var prevLink = document.getElementById(month[currentDisplayIndex-1])
var nextLink;


contextNavBack.text("◂ " + month[currentDisplayIndex-1]).style("cursor", "pointer").on("mousedown", function(d){
  // prevLink.scrollIntoView();
  currentDisplayIndex--;

  prevLink = document.getElementById(month[currentDisplayIndex-1])
  nextLink = document.getElementById(month[currentDisplayIndex+1])

  if(prevLink !== null){
    contextNavBack.text("◂ " + month[currentDisplayIndex-1]);
    contextNavForward.text(month[currentDisplayIndex+1] + " ▸")
  }
  else{
    contextNavBack.text(" ");
    contextNavForward.text(month[currentDisplayIndex+1] + " ▸")
  }

  domainMax = new Date(2018, currentDisplayIndex+1)
  domainMax.setDate(domainMax.getDate()-1)
  domainMin = new Date(2018, currentDisplayIndex)
  // domainMax = new Date(d3.select(nextLink).datum().unix_time * 1000)
  // domainMin = new Date(d3.select(nextLink).datum().unix_time * 1000)
  // domainMin.setMonth(domainMin.getMonth() - 1);  

  xScale2.domain([domainMin, domainMax])
  contextChart.selectAll(".axis").call(xAxis2)
  var brushMin = new Date(domainMax)
  brushMin.setDate(brushMin.getDate()-1)

  contextChart.selectAll("rect").attr("x", function(d) { return xScale2(d.time); })
  contextBrush.call(brush.move, [brushMin, domainMax].map(xScale2))

  contextChart.selectAll(".selection").call(contextTip)
  });

contextNavForward.text(" ").style("cursor", "pointer").on("mousedown", function(d){
  // nextLink.scrollIntoView();
  currentDisplayIndex++;

  prevLink = document.getElementById(month[currentDisplayIndex-1])
  nextLink = document.getElementById(month[currentDisplayIndex+1])

  if(nextLink !== null){
    contextNavBack.text("◂ " + month[currentDisplayIndex-1]);
    contextNavForward.text(month[currentDisplayIndex+1] + " ▸")
    // domainMax = new Date(d3.select(nextLink).datum().unix_time * 1000)
    // domainMin = new Date(d3.select(nextLink).datum().unix_time * 1000)
    // domainMin.setMonth(domainMin.getMonth() - 1);  

  }
  else{
    contextNavBack.text("◂ " + month[currentDisplayIndex-1]);
    contextNavForward.text(" ")
    // domainMax = new Date(d3.select(prevLink).datum().unix_time * 1000)
    // domainMin = new Date(d3.select(prevLink).datum().unix_time * 1000)
    // domainMax.setMonth(domainMax.getMonth() + 2);  
    // domainMin.setMonth(domainMin.getMonth() + 1);  

  }

  domainMax = new Date(2018, currentDisplayIndex+1)
  domainMax.setDate(domainMax.getDate()-1)
  domainMin = new Date(2018, currentDisplayIndex)


  xScale2.domain([domainMin, domainMax])
  contextChart.selectAll(".axis").call(xAxis2)
  var brushMin = new Date(domainMax)
  brushMin.setDate(brushMin.getDate()-1)


  contextChart.selectAll("rect").attr("x", function(d) { return xScale2(d.time); })
  contextBrush.call(brush.move, [brushMin, domainMax].map(xScale2))

  contextChart.selectAll(".selection").call(contextTip)
});


  var reporterTip = d3.tip()
    .attr("class", "tooltip")
    .offset([-20,-5])
    .html(function(d,i) {
    return "<b>Activity: </b>" + d.activity + "<br><b>Alone: </b>" + d.alone + "<br><b>Unique Interactions: </b>" + d.unique_interactions
    });

  reporterChart.selectAll(".moodCircle")
  .call(reporterTip)

  .on("mouseover", function(d) {
    reporterTip.show(d);
  })

  .on("mouseout", function(d) {
    reporterTip.hide(d);
  })



  var contextTip = d3.tip()
    .attr("class", "tooltip")
    .offset([-20,-5])
    .html(function(d,i) {
    var brushSelection = d3.brushSelection(contextBrush.node())
var formatTime = d3.timeFormat("%b %d %I:%M%p");

  return "Viewing " + formatTime(xScale2.invert(brushSelection[0])) + " — <br>" + formatTime(xScale2.invert(brushSelection[1]))
    });

  contextChart.selectAll(".selection")
  .call(contextTip)

  .on("mousedown", function(d) {
    contextTip.hide(d);
  })

  .on("mouseover", function(d) {
    contextTip.show(d);
  })

  .on("mouseout", function(d) {
    contextTip.hide(d);
  })


});


function brushed() {
  if (d3.event.sourceEvent && d3.event.sourceEvent.type === "zoom") return; // ignore brush-by-zoom
  var s = d3.event.selection || xScale2.range();
  var formatTime = d3.timeFormat("%b %d %I:%M%p");
  var newDateRange = s.map(xScale2.invert, xScale2);
  for(var i = 0; i < newDateRange.length; i++) {
    newDateRange[i] = formatTime(newDateRange[i])
  }
  xScale.domain(s.map(xScale2.invert, xScale2));
  body.select("#context-description").html("Viewing " + newDateRange[0] + " — " + newDateRange[1]);
  reporterChart.select(".moodArea").attr("d", moodArea);
  reporterChart.select(".moodLine").attr("d", moodLine);
  reporterChart.selectAll(".moodCircle").attr("cx", function(d) {return xScale(d.time)}).attr("cy", function(d) {return yScale(d.mood)});
  reporterChart.select(".moraleArea").attr("d", moraleArea);
  reporterChart.select(".stressArea").attr("d", stressArea);
  reporterChart.select(".fatigueArea").attr("d", fatigueArea);
  reporterChart.selectAll(".compulsion-x").attr("x", function(d) {return xScale(d.time)});
  keyloggerChart.selectAll(".joy-circle").attr("cx", function(d) {return xScale(d.time)}).attr("cy", function(d) {return yScaleKeylogger(d.score)});
  keyloggerChart.selectAll(".sad-circle").attr("cx", function(d) {return xScale(d.time)}).attr("cy", function(d) {return yScaleKeylogger(d.score)});
  keyloggerChart.selectAll(".tentative-circle").attr("cx", function(d) {return xScale(d.time)}).attr("cy", function(d) {return yScaleKeylogger(d.score)});
  keyloggerChart.selectAll(".angry-circle").attr("cx", function(d) {return xScale(d.time)}).attr("cy", function(d) {return yScaleKeylogger(d.score)});
  keyloggerChart.selectAll(".confident-circle").attr("cx", function(d) {return xScale(d.time)}).attr("cy", function(d) {return yScaleKeylogger(d.score)});
  keyloggerChart.selectAll(".analytical-circle").attr("cx", function(d) {return xScale(d.time)}).attr("cy", function(d) {return yScaleKeylogger(d.score)});
  keyloggerChart.selectAll(".disgust-circle").attr("cx", function(d) {return xScale(d.time)}).attr("cy", function(d) {return yScaleKeylogger(d.score)});
  keyloggerChart.selectAll(".fear-circle").attr("cx", function(d) {return xScale(d.time)}).attr("cy", function(d) {return yScaleKeylogger(d.score)});
  blinksChart.selectAll(".blink-circle").attr("cx", function(d) {return xScale(d.time)});
  expressionsChart.select(".productivityArea").attr("d", productivityArea);
  expressionsChart.selectAll(".attentionLines").attr("x1", function(d){ return xScale(d.time);}).attr("x2", function(d) {return xScale(d.time);});
  expressionsChart.selectAll(".valenceLines").attr("x1", function(d){ return xScale(d.time);}).attr("x2", function(d) {return xScale(d.time);});
  emojiChart.selectAll(".emoji").attr("transform", function(d) {return "translate(" + (xScale(d.time)-7) + ")";});
  tabCounterChart.select(".tabLine").attr("d", tabLine);
  // tabCounterChart.select(".windowLine").attr("d", windowLine);
 tabCounterChart.selectAll("rect").attr("x", function(d) { return xScale(dataset[d].timestamp); }).attr("width", (xScale(new Date("Sun Apr 29 2018 02:00:00 GMT-0500 (CDT)")) - xScale( new Date("Sun Apr 29 2018 01:00:00 GMT-0500 (CDT)"))));  tabCounterChart.selectAll(".tabCircle").attr("cx", function(d) {return xScale(dataset[d].timestamp)});
  tabCounterChart.selectAll(".windowCircle").attr("cx", function(d) {return xScale(dataset[d].timestamp)});
  body.selectAll(".axis--x").call(xAxis);
}



let scrub = document.getElementById("context-container")

window.addEventListener("scroll", function(){
  var targetElement = document.getElementById("tabCounter-container");

  if(window.scrollY > (targetElement.offsetTop)){
    scrub.style.position = "inherit"
  }
  else if(window.scrollY <= (targetElement.offsetTop)){
    scrub.style.position = "fixed"

  }
})