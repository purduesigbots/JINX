#import ports
import serial
import serial.tools.list_ports
import threading
import time
from queue import Queue
USB_VID = [0x4d8, 0x67b]

'''IO Error, but named specifically for vex ports'''
class VexPortError(IOError):
    pass

'''
    Find serial port connecting to Vex Cortex
    Port is assumed to have vendor ID
    @return: valid serial port that we believe is a VEX Cortex Microcontroller, or None
'''
def findVexPort():
    #return ""
    
    
    ports = [x for x in serial.tools.list_ports.comports()]

    #DEBUG: List found ports
    print("Ports: ", [port.device for port in ports])
    
    for port in ports:
        if port.vid is not None and (port.vid in USB_VID or 'vex' in port.product.lower()):
            return port.device
    raise VexPortError("No connected Vex Cortexes found.")


'''Opens the serial port for communication to vex cortex
    Returns Serial object capable of being read from and written to'''
def openVexPort():
    port = findVexPort()
    vexPort = serial.Serial(port, 115200, timeout=1)
    print("Serial successfully opened")
    return vexPort

'''Do everything necessary to close the port.
    Should be able to be called infinite times without issue,
        as long as port is a valid port'''
def closePort(port):
    try:
        port.close()
    except (IOError, AttributeError) as e:
        #DEBUG: Explain error
        print("Unable to close port:", e)

'''@param message: Stripped message from cortex
    Just prints individual tokens to STDOUT
    TODO: Implement'''
def parseCortexMessage(message):
#    print("Read: %s", message, flush=True)
#    print("End read")
    JINX_DELIMETER = "&"
    tokens = message.strip().split(JINX_DELIMETER)
    print(tokens)

'''
   @param message: Raw message from cortex
   @return tuple(boolean, error): 
        boolean: True if valid
        error: reason for false, or message if True
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
