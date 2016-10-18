var commandInput = 1000;	//text to insert in terminal from user/ send to robot
var arrayOfCommands = [""]; //By default, command is nothing
var upArrow = 38;
var downArrow = 40;
var enterKey = 13;
var commandArrayIndex = 0;     //Keeps track of where in command history you are
var commandAddress = "../assets/python3/command.py";

// Use the browser's built-in functionality to quickly and safely escape
// the string
//from http://shebang.brandonmintern.com/foolproof-html-escaping-in-javascript/
function escapeHtml(str) {
  var div = document.createElement('div');
  div.appendChild(document.createTextNode(str));
  return div.innerHTML;
}

function getCommand() {
    comm = document.getElementById("commandLine").value;
    comm = (comm == "") ? commandInput : comm; //If empty string, use previous input
    console.log("Command is ", comm);
    return comm;
}

function addTerminal(line, Class, terminalObject) {	//append text to the terminal
    var time = new Date();
    var formatTime = time.getMinutes() + ":" + time.getSeconds();//Assume only minutes and seconds matter
    //console.log(formatTime);                              //milliseconds may have to be added at a later date

    var shouldScrollToBottom = (terminalObject.scrollHeight - terminalObject.scrollTop <= 325);

    $("#terminal").append($("<div class = " + Class + ">" + formatTime + "$ " + escapeHtml(line) + "</div>"));	//Insert text into terminal
    if (shouldScrollToBottom) {  //If already near bottom of div before adding text to terminal
        terminalObject.scrollTop = terminalObject.scrollHeight;	//Scroll to bottom of div
    }
}

function postCommand(command) { //POST Command to server
    $.post(commandAddress, {command: "".concat(command)}, function(data) {
        console.log(data);
    });
}

function addCommandHistory(command) {
    var date = new Date();
    var formatTime = date.getMinutes() + ":" + date.getSeconds();//Assume only minutes and seconds matter
    //console.log(formatTime);                              //milliseconds may have to be added at a later date

    var leftTD = "<td class = commandsRecord>" + escapeHtml(command) + "</td>";
    var rightTD = "<td class = commandsTime>" + formatTime + "</td>";
    var tableRow = "<tr>" + leftTD + rightTD + "</tr>";
    $("#commandsTable").append($(tableRow));	//Insert command and time into table

    var historyObj = document.getElementById("prevCommands");
    historyObj.scrollTop = historyObj.scrollHeight;	//Always scroll to bottom of div
}

function submitTerminal(terminalObject) {	//Submits command to terminal from input line
    commandInput = getCommand();
    addTerminal(commandInput, "command", terminalObject);
    postCommand(commandInput);

    //arrayOfCommands = arrayOfCommands.reverse();
    //arrayOfCommands[arrayOfCommands.length - 1] = commandInput;
    //arrayOfCommands.push("");
    //arrayOfCommands = arrayOfCommands.reverse();

    //Only add to history if different command than previous
    if (arrayOfCommands.length == 1 || commandInput != arrayOfCommands[1]) {
        arrayOfCommands[0] = commandInput;  //Add command to front of array of commands
        arrayOfCommands.unshift("");    //make beginning empty string
        //console.log(arrayOfCommands);
    }

    //Add command to history table
    addCommandHistory(commandInput);

    terminalObject.scrollTop = terminalObject.scrollHeight;	//Scroll to bottom of div
    document.getElementById("commandLine").value = "";
    commandArrayIndex = 0;
}

function handleCommandScroll(index, line) {
    line.value = arrayOfCommands[index];
    jQuery(line).trigger("change");
}

function addValueTracker(varName, initialVal) {
    varName = escapeHtml(varName);
    initialVal = escapeHtml(initialVal);

    var nameCell = "<td class=varName id=" + varName + "trackerName>";
    nameCell = nameCell + varName + "</td>";

    var valCell = "<td class = varVal id=" + varName + "trackerVal>";
    valCell = valCell + initialVal + "</td>";

    var trackRow = "<tr>" + nameCell + valCell + "</tr>";
    $("#varTable").append(trackRow);
}

function updateValueTracker(varName, varVal) {
    //console.log(varName);
    //console.log(varVal);
    document.getElementById(varName + "trackerVal").innerHTML = varVal;
}

function downloadVarVals() {
    //var downloadWindow = window.open("", "downloadWindow");
    var toWrite = "";
    $.each(inputJINXVars, function(key, value) {
        if (key == "time") {
            //continue
            return 0;
        }
        toWrite = toWrite + escapeHtml(key);
        $.each(value.value, function() {
            toWrite = toWrite + "," + escapeHtml(this);
        })
        toWrite = toWrite + "\r\n"
        //downloadWindow.document.write("<p>" + toWrite + "</p>");
    });
    dlVarVals.href="data:text/csv,"+encodeURIComponent(toWrite);
}

function addScriptTableRow(numScriptRows) {
    comID = "scriptCom".concat(numScriptRows);
    delayID = "scriptDelay".concat(numScriptRows);

    comCol = "<td id=" + comID + " class='scriptCom'>"
    comCol += ""
    $("#scriptTable").append($("<div class='scripter'>" + formatTime + "$ " + line + "</div>"));
}

$(document).ready(function(){
    var commandLine = document.getElementById("commandLine");
    var date = new Date();
    var prevSubmitTime = date.getTime();
    var objDiv = document.getElementById("terminal");	//used to scroll to bottom of terminal

    $('#commandLine').keyup(function(event) {
        //Submit command to terminal
        if (event.keyCode == enterKey) {
            var date = new Date();
            submitTime = date.getTime();

            //if (submitTime - prevSubmitTime > 1000){ //Restrict to 1 submit per second
                submitTerminal(objDiv);
                prevSubmitTime = submitTime;
            //}
        }

        //Scroll through previous commands
        if (event.keyCode == upArrow) {
            if (commandArrayIndex < arrayOfCommands.length - 1) {
                commandArrayIndex += 1;
                handleCommandScroll(commandArrayIndex, commandLine);
            }
        }

        if (event.keyCode == downArrow) {
            if (commandArrayIndex > 0) {
                commandArrayIndex -= 1;
                handleCommandScroll(commandArrayIndex, commandLine);
            }
        }
    });

    $('#commandLine').change(function() {	//Upon update in prompt, save text
        commandInput = this.value;

        //If you make a change while not accessing archived command, save it in spot 0
        //So you can scroll back down to it.
        if (commandArrayIndex == 0) {
            arrayOfCommands[0] = commandInput;
        }
    });

    $('#terminalButton').click(function() {
        submitTerminal(objDiv);
    });

    document.getElementById("dlVarVals").addEventListener("mouseover", downloadVarVals);
    document.getElementById("dlVarVals").addEventListener("click", downloadVarVals);
});
