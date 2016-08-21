<?php                               //talker.js points to this address
header('Cache-Control: no-cache'); // recommended to prevent caching of event data.
date_default_timezone_set("America/New_York");
header("Content-Type: text/event-stream\n\n");

$counter = rand(1, 10);
while (1) {
	// Every second, sent a "ping" event.

	echo "event: ping\n";
	$curDate = date(DATE_ISO8601);
	echo 'data: {"time": "' . $curDate . '"}';
	echo "\n\n";

	// Send a simple message at random intervals.

	

	//if (!$counter) {
		echo "event: pros\n";
		echo 'data: {"PID": "This is a message at time ' . $curDate . '"}';
		echo "\n\n";
		
	//}

	ob_end_flush();
	flush();
	sleep(1);
}
