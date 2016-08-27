#import ports
import serial
import serial.tools.list_ports
import threading
import time
from queue import Queue

'''
    IO Error, but named specifically for vex ports
'''
class VexPortError(IOError):
    pass

'''
    Find serial port connecting to Vex Cortex
    Port is assumed to have product description
    "CDC RC Controller"
    Returns device name of first matching port found
'''
def findVexPort():
    port = ""
    vexPortProduct = ["CDC RC Controller", "Vex Robotics Prog Board"]
    for listPort in serial.tools.list_ports.comports():
        print("Port product: ", listPort)
        if (str(listPort.product).strip() in (vexPortProduct)):
            port = listPort.device
            #print("found port with path", listPort.device)
            break

    if(port == ""):
        raise VexPortError("No Vex Ports were found. \n"
                    + "Vex ports should have product attribute '{}'"
                    .format(vexPortProduct))
    print("Port: ", port)
    return port


'''
    Opens the serial port for communication to vex cortex
    Returns Serial object capable of being read from and written to
'''
def openVexPort():
    port = findVexPort()
    vexPort = serial.Serial(port, 115200, timeout=1)
    print("Serial successfully opened")
    return vexPort

'''
    Do everything necessary to close the port. 
    Should be able to be called infinite times without issue,
        as long as port is a valid port
'''
def closePort(port):
    try:
        port.close()
    except (IOError, AttributeError) as e:
        #DEBUG: Explain error
        print("Unable to close port:", e)

'''
    Message: Stripped message from cortex
    Just prints individual tokens to STDOUT
'''
def parseCortexMessage(message):
#    print("Read: %s", message, flush=True)
#    print("End read")
    JINX_DELIMETER = "_"
    tokens = message.strip().split(JINX_DELIMETER)
    print(tokens)

'''
   Message: Raw message from cortex
   Returns boolean, error
'''
def receivedProperMessage(message):

    #Specified by JINX Protocol (To be written)
    JINX_HEADER = "JINX"
    JINX_TERMINATOR = "\r\n"
    
    #Error responses
    BAD_HEADER_MESSAGE = "BadStart"
    BAD_TERMINATOR_MESSAGE = "BadTerm"

    #Message must begin with "JINX"
    if(not message.startswith(JINX_HEADER)):
        return (False, BAD_HEADER_MESSAGE)

    #Message must end with CRLF, and not start new message
    if((not message.endswith(JINX_TERMINATOR))
       or (message.count(JINX_HEADER) != 1)):
        return (False, BAD_TERMINATOR_MESSAGE)

    #Return original message if good. May strip header and terminator in future
    return (True, message)
