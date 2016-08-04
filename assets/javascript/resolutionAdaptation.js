/*
 *Changes format of JINX based on width of browser window
 *Narrow windows stack everything, one on top of the other
 *Normal windows put the graphs next to the terminal, but stack things
 *  within the major divs
 *Wide windows put graphs next to the terminal, and put graphs next to each other //TODO
 */

function adjustStyle(width) {
    width = parseInt(width);
    console.log(width);
    if (width < 701) {
        $("#size-stylesheet").attr("href", "../assets/css/combinedNarrow.css");
    } else if ((width > 1200) && (width < 1600)) {
        $("#size-stylesheet").attr("href", "../assets/css/combinedNormal.css");
    } else {
        $("#size-stylesheet").attr("href", "../assets/css/combinedWide.css");
    }
}

$(document).ready(function() {
    adjustStyle($(this).width());
    $(window).resize(function() {
        adjustStyle($(this).width());
    });
});
