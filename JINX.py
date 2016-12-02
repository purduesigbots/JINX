import server
import serialReadWrite
import threading
import time

START_TIME_MILLIS = time.perf_counter() * 1000

'''CLASS: Used when unable to find talker within controller'''
class MissingTalkerError(NameError):
    pass


'''CLASS: Stores JSON data to send to browser, retrieved from cortex'''
class JINX_Data():

    '''Class variable: unique id for each dataset created'''
    MID = 0

    '''
        @param name: name of JSON data
        @param value: Value of JSON data
        Incoming data is not vetted for illegal characters, such as ' " '
    '''
    def __init__(self, name, value, time=-1):
        self.name = name
        self.value = value
        self.time = time

        self.mid = JINX_Data.MID
        JINX_Data.MID += 1

    '''Return string representation of JSON-formatted name/value data'''
    def getJSON(self):
        JSON = '{"JINX": {'
        JSON += '"%s": "%s"' %(self.name, str(self.value))
        JSON += ',"MID": "%s"' %(self.mid)
        if (self.time > -1):
            JSON += ',"time": "%s"' %(self.time)
        JSON += '}}'
        return JSON

    '''For built-int str() function
        Just calls getJSON to return JSON-compliant data'''
    def __str__(self):
        return self.getJSON()


'''CLASS: Allow serial and server modules to communicate
    Passes itself to serial and server instances, and recieves their instances in return'''
class JINX_Controller():

    '''Creat empty array to hold data, and set up talker variables'''
    def __init__(self):
        self.JSONData = []
        self.serialTalker = None
        self.serverTalker = None
        self.closed = False

    '''Assign reference to real serial instance'''
    def setSerialTalker(self, talker):
        self.serialTalker = talker

    '''Assign reference to real server instance'''
    def setServerTalker(self, talker):
        self.serverTalker = talker

    '''Add data to the array. May one day update helper instance variables'''
    def addJSONData(self, data):
        self.JSONData.append(data)
        #DEBUG: Confrim data added. Warning: Gets big
        #print("Data Added:", data, [str(x) for x in self.JSONData][-20:])


    '''
        @param message: Stripped message from cortex
        Splits message by token delimeter specified in JINX Protocol (to be written)
        Parses tokens and acts on requests
    '''
    def parseCortexMessage(self, message):

        #Token delimeter specified in JINX Protocol (to be written)
        #Token 0 is currently always "JINX". May change in future
        JINX_DELIMETER = "&"
        tokens = message.strip().split(JINX_DELIMETER)

        #DEBUG: List tokens
        print("Tokens:", tokens)

        #JSON Data sent
        if (len(tokens) == 3):
            timeMillis = round((time.perf_counter() * 1000) - START_TIME_MILLIS)
            data = JINX_Data(tokens[1], tokens[2], timeMillis)
            self.addJSONData(data)
            #print("Data:", data)

        #Something else happened-unused for now
        else:
            #DEBUG: Verify raw message recieved
            print("Unknown message type: ", message)

    '''
        @param DataNum: Number of values previously received by browser
        Block until new JSON data is available
        @return: JSON-compliant representation of cortex data
    '''
    def getJSONData(self, dataNum):
        #wait until there is data to send
        while(dataNum >= len(self.JSONData)):
            #Don't enter infinite loop if JINX is closed
            if (self.closed or not threading.main_thread().is_alive()):
                return "JINX_Error: JINX Terminated\r\n"
            time.sleep(0.5)

        response = "[" + str(self.JSONData[dataNum])
        MAX_MSGS = 100
        for index in range(1, min(len(self.JSONData) - dataNum, MAX_MSGS)):
            response += ", " + str(self.JSONData[dataNum + index])
        response += "]"

        #DEBUG: Confirm data returned
        #print("New JSON Data:", self.JSONData[dataNum], dataNum)
        print(response)

        return response

    '''
        @param Message: Raw message to send
        *args: Assumed to be string formatting variables
        @return: confirmation that writing works
    '''
    def writeSerial(self, message, *args):
        if (not self.serialTalker):
            raise MissingTalkerError("No serial talker open")

        #TODO: Get confirmation that server wrote correctly
        self.serialTalker.writeJINX(message, *args)

        #TODO: Tie return to value of serialTalker.write
        return "Magic global dict worked"

    def startThreads(self):
        #Communicate with cortex
        self.serialTalker = serialReadWrite.JINX_Serial(controller)
        self.serialThread = threading.Thread(target=self.serialTalker.run, args=(), name="Sam")
        self.serialThread.start()

        #Communicate with browser/GUI
        self.serverTalker = server.JINX_Server(controller)
        self.serverThread = threading.Thread(target=self.serverTalker.run)#, args=(self,), daemon=True)
        self.serverThread.start()

        #Shut everything down when main is shut down
        threadManagerThread = threading.Thread(target=self.threadManagerRun, name="Tom")
        threadManagerThread.start()


    def threadManagerRun(self):
        #Wait for the main thread to shut down
        while(threading.main_thread().is_alive()):
            time.sleep(0)
        threading.main_thread().join()
        self.closed = True

        #Shutdown external communications
        if (self.serialTalker):
            self.serialTalker.shutDown()
        #DEBUG: Confirm shutdown control returns to main controller
        print("JINX Controller has shut down serial talker")

        if (self.serverTalker):
            self.serverTalker.shutDown()
        #DEBUG: Confirm shutdown control returns to main controller
        print("JINX Controller has shut down Server")

        #DEBUG: Waiting for threads to close
        print("Waiting for serial talker and server to shut down.")
        if (self.serialThread.is_alive()):
            self.serialThread.join()
        if (self.serverThread.is_alive()):
            self.serverThread.join()

        #DEBUG: Confirm all stopped
        print("All from JINX stopped")


#DEBUG: Test JINX_Data class
#Should look like '"JINX" {'Hello': "3"}
dat = JINX_Data("Hello", 3)
print(dat)

#Used to bridge gap between serial talker and web server
controller = JINX_Controller()
controller.startThreads()


#Get STDIN messages to send to cortex
JINX_Input = input("Enter message or quit (q): ")
while(JINX_Input != "q"):
    if (JINX_Input == "threading"):
        print(threading.enumerate())
    try:
        controller.writeSerial(JINX_Input)
    except MissingTalkerError as e:
        print("Warning, no cortex connected to send message to")
    JINX_Input = input("Enter message or quit (q): ")
