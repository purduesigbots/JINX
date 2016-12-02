from JINXHelperFunctions import *

#JINXOutboundQueue = Queue()
class JINX_Serial():

    '''Controller: Mediatior designed to allow serial module to talk to server'''
    def __init__(self, controller):
        #Encode and decode serial messages with ASCII
        self.encoding = "ascii"

        #Used to keep track of and kill Serial threads
        self.JINXThreads = []
        self.shutdownJINX = threading.Event()

        #Try to open port once every 5 seconds, until told to shutdown or success
        portThread = threading.Thread(target=self.setPort, daemon=True)
        portThread.start()

        #Pass self to controller so it can write to cortex
        self.JINX_Controller = controller
        try:
            self.JINX_Controller.setSerialTalker(self)
        except:
            pass

    '''Repeatedly attempt to open port.
        Should be called in own thread so it can be terminated'''
    def setPort(self):
        #pyserial port to cortex
        self.vexPort = None
        while(not self.vexPort): #Try to open port every 5 seconds
            try:
                self.vexPort = openVexPort()
            except VexPortError as e:
                print("vexPort Error:", e)
                time.sleep(5)
            finally:
                if(self.shutdownJINX.isSet()): #Allow external threads to call shutdown
                    closePort(self.vexPort)
                    break
        #DEBUG: Confirm stop trying to open port
        print("Setport thread closed")
        print(threading.enumerate())


    '''
        Designed to run as its own thread
        Continuosly reads all incoming messages from cortex
        Messages should begin with "JINX" and and with "\r\n"
    '''
    def readJINX(self):

        #Wait until there is a port or told to shutdown before continuing
        while((not self.vexPort) and (not self.shutdownJINX.isSet())):
            time.sleep(0.5)
        if (self.shutdownJINX.isSet()): #Return instantly if told to shutdown
            return

        #Attempt to set timeout on vexPort. Not actually sure if it works
        vexPort = self.vexPort
        vexPort.timeout = 1

        #MESSAGE_DEFAULT- defined as "No new message"
        #Raw message- reads from cortex. If no message, defaults to MESSAGE_DEFAULT
        MESSAGE_DEFAULT = ""
        rawMessage = MESSAGE_DEFAULT

        #DEBUG: Start
        print("\nStart read thread")

        #Shutdown thread when flag is set
        while(not self.shutdownJINX.isSet()):

            #Necessary because timeout does not work for some reason. Skips loop if no incoming bytes
            if(vexPort.inWaiting() < 1):
                #print("Waiting")
                time.sleep(0)
                continue

            #Reads until newline character. Should timeout if takes too long (But doesn't)
            #Guaranteed at least 1 byte to read. Protocal dictates that newline promptly follows
            #TODO: Fix timeout issue
            rawMessage = vexPort.readline()
            try:
                rawMessage = rawMessage.decode(self.encoding)
            except UnicodeDecodeError:
                print("Error decoding message: ", rawMessage)
                continue

            #If nothing was read (timeout occurred) skip message handling
            if(rawMessage == MESSAGE_DEFAULT):
                #DEBUG: Nothing Read
                print("timeout occurred")
                continue

            #DEBUG: receivedProperMessage
            #print(receivedProperMessage(rawMessage))
            if(not receivedProperMessage(rawMessage)[0]):
                #writeJINX(vexPort, receivedProperMessage(rawMessage))
                print("Raw Message:", rawMessage, ":", receivedProperMessage(rawMessage), flush=True)
                continue

            #DEBUG: Raw Message
            #print(rawMessage)
            #Let controller handle the message. If no controller, just make best effort
            try:
                self.JINX_Controller.parseCortexMessage(rawMessage)
            except AttributeError as e: #TODO: Find what the exception should be
                print("Probably no JINX controller.", e)

                parseCortexMessage(rawMessage)

            #reset message
            rawMessage = MESSAGE_DEFAULT
            #END: Read

        #DEBUG: Confirm stop
        print("Stopped read thread")

    '''
        Message: Raw message to send
        *args: Currently assumed to be arguments passed to string formatter (%d, %s, etc.)
            May someday attempt intelligent parsing of args, e.g., passing multiple valid strings
        Assumes message is written in unicode, and converts to bytes before writing to cortex
    '''
    #JINXWriteLock = threading.RLock
    def writeJINX(self, message, *args):

        #If any args given, format the message before encoding
        if (args):
            message = message %(args)

        #If not port open, raise error and let caller handle it
        if(not self.vexPort):
            raise VexPortError("Unable to write message '%s': No vexPort yet opened"
                               %(message))

        #Strip message of whitespace for easy tokenization,
        #   then append newline to signify end of message
        #Unicode necessary to send over serial
        message = message.strip() + "\n"
        message = message.encode(self.encoding)

        #Not actually used-
        #   Most writing jobs happen fast enough that they don't overwrite each other
        #Lock access to outbound serial writing, release automatically when done
        #JINXWriteLock.acquire()

        #DEBUG: Confirm proper encryption
        #print("Write log: ", message.decode(self.encoding))
        self.vexPort.write(message)
        self.vexPort.flush()
        #JINXWriteLock.release()

        #Signify proper writing.
        #Should probably be integer or boolean, but wider variety of returns may be added
        return "Send successful"

    '''Sets flags to terminate indefinite loops, closes files/ports, if any
       Only returns when all serial-related threads are dead'''
    def shutDown(self):

        #Flag to terminate indefinite loops
        self.shutdownJINX.set()

        #Wait for all loops to end
        for thread in self.JINXThreads:
            thread.join()

        #Close the port if possible. Function called handles exceptions
        closePort(self.vexPort)

        #DEBUG: Confirm port is closed
        print("vexPort: ", self.vexPort)

        #DEBUG: Confirm end of all serial communications
        print("Serial: Everything is ending")


    '''
        Creates as many threads as necessary (Currently only 1)
        Initializes reading of threads. Can be extended to test functionality as well
    '''
    def run(self):
        readThread = threading.Thread(target=self.readJINX, args=())
        self.JINXThreads.append(readThread)

        #DEBUG: List active threads
        print("Threads at serial start:", threading.enumerate())

        for thread in self.JINXThreads:
            thread.start()

        #DEBUG: Confirm all threads succsessfully started
        print("All serial threads started", flush=True)



'''
    If run as own module, should attempt to read serial data and print to STDOUT
    Accepts input to send to cortex
    Quit with 'q' or ctrl + c or cntrl + z (q, Keyboard Interrupt, kill)
'''
#print(__name__)
if (__name__ == "__main__"):
    #Start reading
    talker = JINX_Serial(object())
    talker.run()

    #Get message to write
    message = "blah"
    while(message is not "q"):
        try:
            message = input("Press 'q' to quit\n")
            talker.writeJINX(message)
        except VexPortError as e:
            print(e)
        except KeyboardInterrupt:
            print("hello ki")
            break
        except EOFError:
            break
        except Error as e:
            print(e)
            break


    #Close things
    talker.shutDown()
