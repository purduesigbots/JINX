import server
import serialReadWrite
import threading
import time

'''
    CLASS: Used when unable to find talker within controller
'''
class MissingTalkerError(NameError):
    pass


'''
    CLASS: Stores JSON data to send to browser, retrieved from cortex
'''
class JINX_Data():

    '''
        Name: name of JSON data
        Value: Value of JSON data
        Incoming data is not vetted for illegal characters, such as ' " '
    '''
    def __init__(self, name, value):
        self.name = name
        self.value = value

    '''
        Return string representation of JSON-formatted name/value data
    '''
    def getJSON(self):
        JSON = '"JINX": {"%s": "%s"}' %(self.name, str(self.value))
        return JSON

    '''
        For built-int str() function
        Just calls getJSON to return JSON-compliant data
    '''
    def __str__(self):
        return self.getJSON()


'''
    CLASS: Allow serial and server modules to communicate
    Passes itself to serial and server instances, and recieves their instances in return
'''
class JINX_Controller():

    '''
        Creat empty array to hold data, and set up talker variables
    '''
    def __init__(self):
        self.JSONData = []
        self.serialTalker = None
        self.serverTalker = None
    
    '''
        Assign reference to real serial instance
    '''
    def setSerialTalker(self, talker):
        self.serialTalker = talker
    
    '''
        Assign reference to real server isntance
    '''
    def setServerTalker(self, talker):
        self.serverTalker = talker
    
    '''
        Add data to the array. May one day update helper instance variables
    '''
    def addJSONData(self, data):
        self.JSONData.append(data)

    '''
        Message: Stripped message from cortex
        Splits message by token delimeter specified in JINX Protocol (to be written)
        Parses tokens and acts on requests
    '''
    def parseCortexMessage(self, message):

        #Token delimeter specified in JINX Protocol (to be written)
        #Token 0 is currently always "JINX". May change in future
        JINX_DELIMETER = "_"
        tokens = message.strip().split(JINX_DELIMETER)
        
        #DEBUG: List tokens
        print("Tokens:", tokens)
        
        #JSON Data sent
        if (len(tokens) == 3):
            data = JINX_Data(tokens[1], tokens[2])
            self.addJSONData(data)
            #print("Data:", data)
            
        #Something else happened-unused for now
        else:
            #DEBUG: Verify raw message recieved
            print("Unknown message type: ", message)

    '''
        DataNum: Number of values previously received by browser
        Block until new JSON data is available
        Return JSON-compliant representation of cortex data
    '''
    def getJSONData(self, dataNum):
        #wait until there is data to send
        while(dataNum >= len(self.JSONData)):
            time.delay(0.5)

        return self.JSONData[dataNum]

    '''
        Message: Raw message to send
        *args: Assumed to be string formatting variables
        Return confirmation that writing works
    '''
    def writeSerial(self, message, *args):
        if (not self.serialTalker):
            raise MissingTalkerError("No serial talker open")

        #TODO: Get confirmation that server wrote correctly
        self.serialTalker.writeJINX(message, *args)
        
        #TODO: Tie return to value of serialTalker.write
        return "Magic global dict worked"


#DEBUG: Test JINX_Data class
#Should look like '"JINX" {'Hello': "3"}
dat = JINX_Data("Hello", 3)
print(dat)

#Used to bridge gap between serial talker and web server
controller = JINX_Controller()

#Communicate with cortex
serialTalker = serialReadWrite.JINX_Serial(controller)
serialThread = threading.Thread(target=serialTalker.run, args=(controller,), name = "Joe")
serialThread.start()

#Communicate with browser/GUI
serverTalker = server.JINX_Server(controller)
serverThread = threading.Thread(target=serverTalker.run, args=(controller,), daemon=True)
serverThread.start()

#Get STDIN messages to send to cortex
JINX_Input = input("Enter message or quit (q): ")
while(JINX_Input != "q"):
    serialTalker.writeJINX(JINX_Input)
    JINX_Input = input("Enter message or quit (q): ")

#Shutdown external communications
serialTalker.shutDown()
serverTalker.shutDown()

#DEBUG: Confirm all stopped
print("All from JINX stopped")