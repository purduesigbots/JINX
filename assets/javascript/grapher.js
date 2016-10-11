/*
 * @author Josh Walker
 *
 * @Version 1.0
 * @Date 02 February 2016
 *
 * Creates new plots
 * Allows plotting of specific JINX data vs. time
 * Allows user to set time between updates
 * Allows user to choose number of points to plot
 * Allows user to add and remove plots
 *
 * @Dependencies talker.js
 *
 * @UsedBy combined.html
 */


//Takes arrays of form [[,],[,]...]

//console.log("In grapher");

function zipArrays(array1, array2, totalPoints) {

    var arrLen = Math.min(array1.reverse().length, array2.reverse().length);
    //console.log(arrLen);
    arrLen = Math.min(arrLen, totalPoints);
    var retArr = [];

    for (var i = 0; i < arrLen; i++) {
        //console.log(i + " " + array1[array1.length - 1 - i]);
        retArr.push([array1[i], array2[i]]);
        //console.log(i);
    }

    array1.reverse();
    array2.reverse();
    retArr.reverse();
    return retArr;
}

//Returns an array no longer than totalPoints, taken from the end of the array
//@param array: array to take slice of
//@param name: Unused
//@param totalPoints: The largest array that can be returned
function getDataSlice(dataArray, toGraph, totalPoints) {

    //if both selections are "time", don't graph anything
    if (toGraph.ySelections == ["time"] && toGraph.xSelection == "time") {
        return [0,0]
    }

    //If there is no data, don't graph anything
    if (!dataArray) {
        return [0,0];
    }

    //If no y selections, don't do anything
    if (!toGraph.ySelections) {
        return [0,0];
    }

    var array = [];

    $.each(toGraph.ySelections, function (index, ySelection) {
        series = new Object();
        label = ySelection;
        axis = toGraph.xSelection == "time" ? 1 : 2;

        if (ySelection == "time") {
            if (toGraph.xSelection == "time") {
                data = [];
            } else {
                data = zipArrays(
                    dataArray[toGraph.xSelection].value,
                    dataArray[toGraph.xSelection].time,
                    totalPoints);
            }
        } else {
            if (toGraph.xSelection == "time") {
                data = zipArrays(
                    dataArray[ySelection].time,
                    dataArray[ySelection].value,
                    totalPoints);
            } else {
                data = zipArrays(
                    dataArray[toGraph.xSelection].value,
                    dataArray[ySelection].value,
                    totalPoints);
                }
        }

        //data = data.slice(-totalPoints);

        series.label = label;
        series.data = data;
        series.xaxis = axis;
        array.push(series);
    });

    //console.log(array);
    return array;
}

//Returns how often graph is updated
//Changes how often a graph is updated
//DOES NOT CHANGE HOW OFTEN talker.js READS DATA
//
//@param inputID: Which input box is changed
function changeUpdateInterval(inputID) {
    var v = $("#" + inputID).val();

    if (v && !isNaN(+v)) {
        updateInterval = +v;

        if (updateInterval < 1) {
            updateInterval = 1;
        } else if (updateInterval > 2000) {
            updateInterval = 2000;
        }

        $("#" + inputID).val("" + updateInterval);
        return updateInterval
    }
}

//Returns how many data points to plot
//Changes how many data points are plotted
// Does not allow < 1 or >2000 points
//
//@param inputID: Which input box is changed
function changeNumDataToPlot(inputID) {
    var v = $("#" + inputID).val();

    if (v && !isNaN(+v)) {
        numDataToPlot = +v;

        if (numDataToPlot < 1) {
            numDataToPlot = 1;
        } else if (numDataToPlot > 2000) {
            numDataToPlot = 2000;
        }

        $("#" + inputID).val("" + numDataToPlot);
        return numDataToPlot
    }
}

function addYAxisSelector(data, plotNum, choosePlotDataID, buttonClass) {
    var dataName = escapeHtml(graphableData[data]);
    //console.log("Data name: ".concat(dataName));
    dataID = dataName.concat(plotNum);
    $("#" + choosePlotDataID).append($(""
        +"<input type='checkbox' id=" + dataID + " class=" + buttonClass
        +" name=" + dataName + "></input><label for=" + dataID
        + ">" + dataName + "</label><br/>"));
}

function parseYAxisSelections(choosePlotDataID) {
    var ySeriesToPlot = [];
    $("#" + choosePlotDataID).find("input:checked").each(function() {
        //console.log(this.name);
        ySeriesToPlot.push(this.name);
    })
    //console.log("ySeriesToPlot: " + ySeriesToPlot);
    return ySeriesToPlot;
}

//Used to display title of Graph
function toGraphToString(toGraph) {
    if (toGraph.ySelections.length == 0) {return "nothing";}

    title = toGraph.ySelections[0];
    $.each(toGraph.ySelections, function(index, ySelection) {
        if(index == 0) {

        } else {
            title = title.concat(", ", ySelection);
        }
    });

    title = title.concat(" vs ", toGraph.xSelection);
    return(title);
}

function parseXAxisSelection(selectorID) {
    //console.log("Selector ", $("#" + selectorID).val());
    return $("#" + selectorID).val();
}

//Creates a new, self-contained plot.
//collective ID is "plotDiv" + plotNum
//plot ID is "placeholder" + plotNum
//All relevant fields and plot-specific events are generated here
//Should not be called until there is something to plot
function newPlot(plotNum) {
    var divID = "plotDiv".concat(plotNum);
    var divClass = "plotDivClass";

    var headerID = "graphing".concat(plotNum);
    var headerClass = "whatGraphing"
    var headerText = "Currently graphing ";

    var plotBackgroundId = "plotBackground".concat(plotNum);
    var plotBackgroundClass = "plotBackground";

    var plotID = "placeholder".concat(plotNum);
    var plotClass = "demo-placeholder";
    //var style = "padding: 0px; position: relative;";
    //var height = '"826"';

    var leftFieldsDivID = "leftFieldsDiv".concat(plotNum);
    var leftFieldsDivClass = "leftFieldsDiv";

    var updateIntervalID = "updateInterval".concat(plotNum);
    //var updateIntervalStyle = "text-align: right; width:5em";
    var updateInterval = 30;

    var numDataToPlotID = "num2Plot".concat(plotNum);
    //var numDataToPlotStyle = "text-align: right; width:5em";
    var numDataToPlot = 30;

    var removeButtonID = "removeButton".concat(plotNum);
    var removeButtonType = "button";

    var rightFieldsDivID = "rightFieldsDiv".concat(plotNum);
    var rightFieldsDivClass = "rightFieldsDiv";

    var choosePlotDataID = "choosePlotData".concat(plotNum);
    var choosePlotDataClass = "choosePlotData";
    //var dataToPlot = graphableData[0]; //represents which y value to plot, given by resArray[dataToPlot]

    var buttonClass = "ChooseData".concat(plotNum);
    var buttonID = [], buttonName = [];
    buttonID[0] = "data0".concat(plotNum), buttonName[0] = "Data Set 0";
    buttonID[1] = "data1".concat(plotNum), buttonName[1] = "Data Set 1";

    //localPlotData = getDataSlice(inputJINXVars[dataToPlot], dataToPlot, numDataToPlot);
    localPlotData = [0,0];

    // Create html elements for plot
    $("#chartContainer").append($("<div id=" + divID + " class=" + divClass + "></div>")); //container for new plot

    $("#" + divID).append($(""    //plot Background area))
        + "<div id=" + plotBackgroundId + " class=" + plotBackgroundClass
        +"></div>"));

    $("#" + plotBackgroundId).append($(""    //Plot Title
        + "<p id=" + headerID + " class=" + headerClass + "> "
        + headerText + " " + escapeHtml(graphableData[0])
        + "</div>"));

    $("#" + plotBackgroundId).append($(""    //new plot canvas area
        + "<div id=" + plotID + " class=" + plotClass// + " style=" + style + " height=" + height
        + "></div>"));

        $("#" + divID).append($(""  //Div to store axis selectors
            + "<div id= " + rightFieldsDivID + " class=" + rightFieldsDivClass
            + "></div>"))
        /*$("#" + divID).append($(""    //BUTTONS to Choose what to plot
            +"<div id=" + choosePlotDataID + " class=" + choosePlotDataClass + " style=\"width:5em; height:5em; float:left\">"
            +"</div>"));

            for (data in graphableData) {//Create a button to plot any data that can be plotted
                var dataName = graphableData[data];
                //console.log(dataName);
                dataID = dataName.concat(plotNum);
                $("#" + choosePlotDataID).append($(""
                    +"<button type=\"button\" + id=" + dataID + " class = " + buttonClass + ">" + dataName
                    +"</button>"));
            }*/

        $("#" + rightFieldsDivID).append($(""  //Dropdown list to choose what to plot (Y axis)
            +"<div class='ySelector selector' id=" + choosePlotDataID + "><p>Y-Axis Selection</p>"
            // +"<select id=" + choosePlotDataID + " class=" + choosePlotDataClass
            // +" multiple=true>"
            // +"</select>"
            +"</div>"));

            for (data in graphableData) {//Create a selection to plot any data that can be plotted
                addYAxisSelector(data, plotNum, choosePlotDataID, buttonClass);
            }

        $("#" + rightFieldsDivID).append($(""  //Dropdown list to choose what to plot (X axis)
            +"<div class = 'xSelector selector'><p>X-Axis Selection</p>"
            +"<select id=" + choosePlotDataID + "X class=" + choosePlotDataClass
            +"X>"
            +"</select>"+"</div>"));

            for (data in graphableData) {//Create a selection to plot any data that can be plotted
                var dataName = graphableData[data];
                //console.log(dataName);
                dataID = dataName.concat(plotNum);
                $("#" + choosePlotDataID + "X").append($(""
                    +"<option id=" + dataID + "X class = " + buttonClass
                    +"X value=" + dataName + ">" + escapeHtml(dataName) + "</option>"));
            }

    $("#" + divID).append($(""  //Div to store time/numPoints/RemovePlot
        + "<div id= " + leftFieldsDivID + " class=" + leftFieldsDivClass
        + "></div>"))

    $("#" + leftFieldsDivID).append($(""  //update interval button
        +"<p>Time between updates: "
        +"<input id=" + updateIntervalID + " type=\"text\" value=\"\" "//style=" + updateIntervalStyle + ">"
        +"milliseconds</p>"));

    $("#" + leftFieldsDivID).append($(""  //Number Data Plotted Input Field
        +"<p>Num points to plot: "
        +"<input id=" + numDataToPlotID + " type=\"text\" value=" + numDataToPlot
        //+" style=" + numDataToPlotStyle + ">"
        +"points</p>"));

    $("#" + leftFieldsDivID).append($(""  //remove plot button
        +"<button type=" + removeButtonType + " id = " + removeButtonID + ">Remove Plot"
        +"</button>"));

    //Create Plot variable
    var plot = $.plot("#" + plotID, [0,0], {
        series: {
            shadowSize: 0	// Drawing is faster without shadows
        },

        //Currently all default values
        yaxis: {

        },

        //Turns milliseconds since epoch into formatted time
        //Minutes:Seconds
        xaxes: [
            {mode: "time",
            timeformat: "%M:%S",
            show: true},

            {mode: null,
            show: false,}]
    });

    //Handle all real-time events
    $(document).ready(function() {
        //console.log(inputJINXVars);
        var toGraph = new Object();
        toGraph.xSelection = "time";

        //Update list of toGraphYValues when new boxes are checked
        function ySelectorChosen() {
            toGraph.ySelections = parseYAxisSelections(choosePlotDataID);
            //console.log(toGraph.yValues);
            //console.log("register click");

            //Update title of graph
            document.getElementById(headerID).innerHTML = headerText + " " + toGraphToString(toGraph);
        }

        $("." + buttonClass).click(function () {
            ySelectorChosen();
        });

        //Update x axis selection
        $("#" + choosePlotDataID + "X").bind("change", function () {
            toGraph.xSelection = parseXAxisSelection(this.id);
            if (toGraph.xSelection == "time") {
                plot.getOptions().xaxes[1].show = false;
                plot.getOptions().xaxes[0].show = true;
                //console.log("Chose to show time");
            } else {
                plot.getOptions().xaxes[0].show = false;
                plot.getOptions().xaxes[1].show = true;
                //console.log("Choose to show numbers");
            }
            plot.setupGrid();
            plot.draw();
            //console.log("X mode", plot.getAxes());

            //Update title of graph
            document.getElementById(headerID).innerHTML = headerText + " " + escapeHtml(toGraphToString(toGraph));
        });

        //Change how often singular plot is updated
        $("#" + updateIntervalID).val(updateInterval).change(function () {
            updateInterval = changeUpdateInterval(updateIntervalID);
            //console.log(updateInterval);
        });

        //Change how much data points to plot
        $("#" + numDataToPlotID).val(numDataToPlot).change(function () {
            numDataToPlot = changeNumDataToPlot(numDataToPlotID);
            //console.log(numDataToPlot);
        });

        //Delete the plot
        $("#" + removeButtonID).click(function() {
            $("#" + divID).remove();
        });

        //"Homemade" event. When signaled that there is new data, make a new button and handler for it
        $("body").on("NewData", function() {
            var dataName = graphableData[graphableData.length - 1];
            dataID = dataName.concat(plotNum);

            //Y axis
            data = graphableData.length - 1;
            addYAxisSelector(data, plotNum, choosePlotDataID, buttonClass);

            //Update list of toGraphYValues when new boxes are checked
            $("." + buttonClass).click(function () {
                ySelectorChosen();
            });

            //X axis
            $("#" + choosePlotDataID + "X").append($(""
                +"<option id=" + dataID + "X class = " + buttonClass
                +"X value=" + dataName + ">" + escapeHtml(dataName) + "</option>"));
        });

        //$("body").on("GraphData", update());

        //Update the graph. Bring in new data points, reset axes, call itself
        function update() {
            localPlotData = getDataSlice(inputJINXVars, toGraph, numDataToPlot);
            //console.log(localPlotData);
            plot.setData(localPlotData);
            //plot.setData[i,i];
            //i+=1;
            plot.draw();
            plot.setupGrid();
            setTimeout(update, updateInterval);
                     // #CHANGEBACK TO updateInterval*****************
        }

        //function setUp() {
        //    plot.setupGrid();
        //    setTimeout(setUp, updateInterval);
        //}

        //Trigger initial plotting cycle
        update();
        //setUp();
    });
}
