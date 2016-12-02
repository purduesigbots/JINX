#Use ctrl-c to stop

import socketserver, urllib
from http.server import SimpleHTTPRequestHandler, HTTPServer
from os import curdir, sep
import threading, time

#I need a better way to talk to the request handler
magicGlobalDict = {"JINX_Controller": None}

'''CLASS: Allow simultaneous connections to server'''
class ThreadingSimpleServer(socketserver.ThreadingMixIn,
                   HTTPServer):
    pass

'''CLASS: HTTPRequestHandler'''
class JINX_HTTP_ServerRequestHandler(SimpleHTTPRequestHandler):

    '''
        Path: Requested file address
        Parse requests
        Return mimetype/ whether to send data
    '''
    def getMimetype(self, path):
        sendReply = False
        mimetype = ''
        if self.path.endswith(".html"):
            mimetype='text/html'
            sendReply = True
        if self.path.endswith(".js"):
            mimetype='application/javascript'
            sendReply = True
        if self.path.endswith(".css"):
            mimetype='text/css'
            sendReply = True
        if ".json" in self.path:
            mimetype='application/json'
            sendReply = True
            self.path = self.path[:self.path.index('.json')]
            self.path += '.json'
        return mimetype, sendReply

    '''Return byte encoding of file'''
    def getStaticFile(self):
        f = open(curdir + sep + self.path)
        data = f.read().encode("utf-8")
        f.close()
        return data

    '''
        Mimetype: Sent in header to browser, specified by HTML/1.1
        Response: Byte encoding of message to send
        Send response with 200 OK header
    '''
    def send200Response(self, mimetype, response):
        self.send_response(200)
        self.send_header('Content-type', mimetype)
        self.end_headers()
        self.wfile.write(response)

        #DEBUG: Confirm response sent
        #print("Sent 200-OK response:", mimetype, response.decode('utf-8'))

    '''
        Response: String to send over HTML/1.1
        Return byte representation of response
    '''
    def prepareResponse(self, response):
        return response.encode('utf-8')

    '''Handle post requests'''
    def do_POST(self):
        #Get all posted data
        length = int(self.headers['Content-Length'])
        post_data = urllib.parse.parse_qs(self.rfile.read(length).decode('utf-8'))

        #Check the file extension required and
        #set the right mime type
        mimetype, sendReply = self.getMimetype(self.path)
        response = None

        #DEBUG: Confirm posted command
        #print("Post data:", post_data,"\n")

        #If main directory requested, return main GUI
        if(self.path=="/"):
            self.path="/views/Combined.html"
            mimetype = 'text/html'
            sendReply = True

        #If command is sent, send to main module to send to cortex
        elif(self.path.endswith("command.py")):
            #DEBUG: Confirm command received
            #print("Command Received")

            #Send command to cortex
            comm = post_data['command'][0]

            try:
                response = str(magicGlobalDict["JINX_Controller"].writeSerial(comm))
                response = self.prepareResponse(response)
            except AttributeError as e:
                print("Error: Unable to prepare response:", e)
            sendReply = True

        #If GUI is requesting new data and we are talking to cortex
        elif(self.path.endswith("jason.json") and magicGlobalDict["JINX_Controller"]):
             received = int(post_data['received'][0])

             #DEBUG: Confirm data query received
             #print("Data Received:", received)

             response = str(magicGlobalDict["JINX_Controller"].getJSONData(received))
             response = self.prepareResponse(response)

             #DEBUG: Confirm proper response
             #print("Data Response:", response.decode('utf-8'))
             sendReply = True

        #If request is not one of above, or server is running without a working controller
        try:
            if(sendReply):

                #If a response has not already been created
                if (not response):

                    #Read data from file and convert to bytes
                    response = self.getStaticFile()

                #Release response to server
                self.send200Response(mimetype, response)

        except IOError:
            #DEBUG: Confirm path
            #print(self.requestPath)
            self.send_error(404,'File Not Found: %s' % self.path)


'''CLASS: Control browser communications'''
class JINX_Server():

    '''Controller: Manages communication between browser and cortex'''
    def __init__(self, controller):

        #Create potential server instance, call it closed until its opened
        self.httpd = None
        self.closed = True

        #Set controller
        self.JINX_Controller = controller
        magicGlobalDict["JINX_Controller"] = controller

        #If controller is not None (Running as standalone passes None)
        if(self.JINX_Controller):
            self.JINX_Controller.setServerTalker(self)

    '''Closes all server communications'''
    def shutDown(self):

        #Set flag to terminate all indefinite loops
        self.closed=True

        #DEBUG: Confirm active threads
        print(threading.enumerate())

        #print(self.httpd.server_close)
        #print(self.httpd.shutdown)
        #print(self.httpd.shutdown_request)

        #Try to prevent any race conditions, so create new thread
        t=[]
        t.append(threading.Thread(target=self.httpd.server_close, daemon=False))
        t.append(threading.Thread(target=self.httpd.shutdown, daemon=False))
        #t.append(threading.Thread(target=self.httpd.shutdown_request, daemon=False))
        [th.start() for th in t]
        [th.join() for th in t]

        #print([(atr) for atr in dir(self.httpd)])
        #print(dir(self.httpd.RequestHandlerClass.MessageClass))

        #DEBUG: Confirm state of server, Confirm closed
        print("Server httpd:", self.httpd, end = " ")
        print("Server closed")

    '''
        Port: Port to bind server to. Default is 9001
        Server is bound to localhost/IP Address of computer running program
        Root access is usually needed to bind port to 80, default for web servers
    '''
    def run(self, port=9001):

        #Haven't actually started server yet, but close enough
        self.closed = False

        #DEBUG: Confirm server starting
        print('starting server...')

        # Server settings
        server_address_port = ('', 9001)

        #Create threaded server
        self.httpd = ThreadingSimpleServer(server_address_port, JINX_HTTP_ServerRequestHandler)

        #Non-threaded server
        #self.httpd = HTTPServer(server_address_port, JINX_HTTP_ServerRequestHandler)

        #Supposed to allow port to be immediately reused by another application after this one ends
        self.httpd.allow_reuse_address = True

        #DEBUG: Confirm server startup
        print('running server...')

        try:
            #while(not self.closed):
                #print(dir(self.httpd))
                #print("Closed:", self.closed)
            foreverThread = threading.Thread(target=self.httpd.serve_forever, daemon=True, name="Sally")
            foreverThread.start()
                #print("Weeee")
                #self.closed=True
            #print("closed: ",self.closed)
        except Exception as e:# KeyboardInterrupt:
            print("Error in handling server request:", e)
        # finally:
        #     pass
        print("Server finished initializing (and maybe failed")

'''Run as standalone server'''
if (__name__=="__main__"):
    controller = None
    serv = JINX_Server(controller)

    serverThread = threading.Thread(target=serv.run)
    serverThread.start()
    #print(threading.enumerate())

    while(input("Enter q to quit: ") != "q"):
        time.sleep(1)

    #print("?")
    serv.shutDown()
    print("Should be quit")
    #print(threading.enumerate())
