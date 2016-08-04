var inputPIDVars = {'time' : []};
var graphableData = ['time'];
var stopThings = false;

$(document).ready(function() {
    var graphableDataEvent = jQuery.Event("NewData");
    var graphDataEvent = jQuery.Event("GraphData");

    var jsonAddress = "../assets/json/jason.json"
    var eventSourceAddress = "http://localhost:8888/sse.php";   //Address of server side events (sse.php)
                                                                //change when needed
    $.ajaxSetup({	// Disable caching of AJAX responses
        cache: false
    });


    var timestamp = 0									//used to detect when file was updated*/
    var objDiv = document.getElementById("terminal");	//used to scroll to bottom of terminal
    //var evtSource = new EventSource(eventSourceAddress);	//server side events

    /*
    evtSource.addEventListener("ping", function(e) {
        if(!stopThings){
            var obj = JSON.parse(e.data);
            //newElement.innerHTML = "SSE: " + obj.PID;
            addTerminal(obj.PID.time, "robo", objDiv);
            addTerminal(obj.PID.Error, "robo", objDiv);

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
        $.getJSON(jsonAddress, function(data) {
            if(data.PID.MID != timestamp) {
                  handlePIDData(data.PID);
            }
        });
    }

    function handlePIDData(PID) {
        timestamp = PID.MID;
        time = new Date().getTime();
        if (PID.time) {
            time = PID.time;
        }

        for (PIDVar in PID) {
            if(!(PIDVar in inputPIDVars)) {//If the variable hasn't been seen yet
                inputPIDVars[PIDVar] = new Object();
                inputPIDVars[PIDVar].time = [];  //Create an array to store its future data
                inputPIDVars[PIDVar].value = [];
                if (jQuery.type(PID[PIDVar]) == "number") { //if the data is numeric
                    graphableData.push(PIDVar);  //lable it as something to be graphed
                    addValueTracker(PIDVar, PID[PIDVar]);
                    jQuery("body").trigger(graphableDataEvent);//Let everything know there is new graphable data
                }
                //console.log(graphableData);
                //console.log(1);
            }

            if (!stopThings) {  //stopThings set by Freeze button
                if (graphableData.indexOf(PIDVar) > -1) {//If there is new data to graph, graph it
                    jQuery("body").trigger(graphDataEvent);
                    updateValueTracker(PIDVar, PID[PIDVar]);//TODO: Update variable table
                } else {  //Otherwise print it to the terminal
                    addTerminal(PIDVar + ": " + PID[PIDVar], "robo", objDiv);
                }
            }

            //Assosiate a time with each variable, since not all variables always come in together
            inputPIDVars[PIDVar].time.push(time);
            inputPIDVars[PIDVar].value.push(PID[PIDVar]);
            //console.log(inputPIDVars[PIDVar]);
            //console.log(inputPIDVars);
        }

        updateValueTracker("time", time);
    }

    placeholder()
    function placeholder(){
        getJSON();
        setTimeout(placeholder, 1000);	//REMOVE used to append random data to terminal
    }
});
