===JINX=== 
JINX is composed of 3 parts: A set of PROS functions that run on the cortex, a webpage for the user to interact with, and a controller written in python that mediates between the 2.

The functions written in PROS are responsible for reading and writing data over the specified serial port (UART1, UART2, or stdin), and parsing any commands that it may receive. Generating data to write is relatively simple. A single name/value pair is sent to the sendData function, and that's all the user has to do. Alternatively, the user may generate a string message and pass that to the writeJINXMessage function, where it will be automatically paired with the name "msg". User generated messages should avoid using newlines or underscores, but any other character may be sent.

Reading is controlled through a never-ending task. The reader will retrieve an entire message up to a newline character, then pass the message to a parser. The parser should be re-written by the end user to allow the robot to be controlled from the browser. An example of such implementation is provided in JINX.c



JINX obtains serial data from the VEX Cortex, then sends the data out over a server.
The data, encoded as JSON, is then decoded client side, and plotted.

Example data includes timestamps, Error data, and command strings

JINX also includes the ability to upload command strings to the server

