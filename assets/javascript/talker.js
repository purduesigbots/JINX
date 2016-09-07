var inputJINXVars = {'time' : []};
var graphableData = ['time'];
var stopThings = false;

$(document).ready(function() {
    var numDatareceived = 0;
    //console.log("In talker");

    var finishedPostEvent = jQuery.Event("FinishedPost");
    var graphableDataEvent = jQuery.Event("NewData");
    var graphDataEvent = jQuery.Event("GraphData");

    var jsonAddress = "../assets/json/jason.json"
    var eventSourceAddress = "http://localhost:8888/sse.php";   //Address of server side events (sse.php)
                                                                //change when needed
    $.ajaxSetup({	// Disable caching of AJAX responses
        cache: false
    });

    //Redundant variable to ensure no duplicate JINX data is received
    var timestamp = 0									//used to detect when file was updated*/
    var objDiv = document.getElementById("terminal");	//used to scroll to bottom of terminal
    //var evtSource = new EventSource(eventSourceAddress);	//server side events

    /*
    evtSource.addEventListener("ping", function(e) {
        if(!stopThings){
            var obj = JSON.parse(e.data);
            //newElement.innerHTML = "SSE: " + obj.JINX;
            addTerminal(obj.JINX.time, "robo", objDiv);
            addTerminal(obj.JINX.Error, "robo", objDiv);

        }
    }, false);
    */

    //Sets an internal 'Freeze' variable to true or false
    //does not actually stop anything on its own, but other functions can
    //check this freeze variable to see if they should take any action
    $('#freezeButton').click(function() {
        //console.log(1);
        if (document.getElementById("freezeButton").innerHTML == "FREEZE") {
            //console.log(2);
            //evtSource.close();
            stopThings = true;
            document.getElementById("freezeButton").innerHTML = "UNFREEZE";
        } else {
            //console.log(3);
            //evtSource = new EventSource("http://localhost:8888/sse.php");
            stopThings = false;
            document.getElementById("freezeButton").innerHTML = "FREEZE";
        }
    });

    //get the newest json data and parse it if the timestamp has changed
    function getJSON(){
        console.log("Asked to get JSON");
        //console.log("received: ", "".concat(numDatareceived));
        $.post(
            jsonAddress,
            {received: "".concat(numDatareceived)},
            function(data) {
                data.JINX.MID = parseInt(data.JINX.MID);
                console.log("JINX Data", data.JINX);
                if(data.JINX.MID > timestamp) { //Assume strictly increasing data
                      numDatareceived = numDatareceived + 1;
                      handleJINXData(data.JINX);
                } else if (data.JINX.MID == timestamp){
                    //If server returns the same or older JSON data from some reason, ask again after 0.5 seconds
                    setTimeout(getJSON, 500);
                }
            }, "json");
    }

    function handleJINXData(JINX) {
        timestamp = JINX.MID;
        time = new Date().getTime();
        if (JINX.time) {
            time = JINX.time;
        }

        for (JINXVar in JINX) {
            if(!(JINXVar in inputJINXVars)) {//If the variable hasn't been seen yet
                inputJINXVars[JINXVar] = new Object();
                inputJINXVars[JINXVar].time = [];  //Create an array to store its future data
                inputJINXVars[JINXVar].value = [];

                //console.log(JINX[JINXVar]);
                //isNumeric(JINX[JINXVar]);

                if (!isNaN(JINX[JINXVar])) { //if the data is numeric
                    graphableData.push(JINXVar);  //lable it as something to be graphed
                    addValueTracker(JINXVar, JINX[JINXVar]);
                    jQuery("body").trigger(graphableDataEvent);//Let everything know there is new graphable data
                }
                //console.log(graphableData);
                //console.log(1);
            }

            if (!stopThings) {  //stopThings set by Freeze button
                if (graphableData.indexOf(JINXVar) > -1) {//If there is new data to graph, graph it
                    jQuery("body").trigger(graphDataEvent);
                    updateValueTracker(JINXVar, JINX[JINXVar]);//TODO: Update variable table
                } else {  //Otherwise print it to the terminal
                    addTerminal(JINXVar + ": " + JINX[JINXVar], "robo", objDiv);
                }
            }

            //Assosiate a time with each variable, since not all variables always come in together
            inputJINXVars[JINXVar].time.push(time);
            inputJINXVars[JINXVar].value.push(JINX[JINXVar]);
            //console.log(inputJINXVars[JINXVar]);
            //console.log(inputJINXVars);
        }

        updateValueTracker("time", time);
        console.log("Finished parsing JSON");
        setTimeout(getJSON, 50);
        console.log("Set timeout to get more data");
    }

    //Ask for JINX Data once every 10 seconds in case of timeout
    function backupRequester() {
        getJSON();
        setTimeout(backupRequester, 10000);
    }
    backupRequester();

});
