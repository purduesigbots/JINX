#Use ctrl-c to stop

import socketserver, urllib
from http.server import SimpleHTTPRequestHandler, HTTPServer
from os import curdir, sep
import threading, time

#I need a better way to talk to the request handler	
magicGlobalDict = {}

'''
    CLASS: Allow simultaneous connections to server
'''
class ThreadingSimpleServer(socketserver.ThreadingMixIn,
                   HTTPServer):
    pass

'''
    CLASS: HTTPRequestHandler
'''
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

    '''
        Return byte encoding of file
    '''
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
        print("Sent 200-OK response:", mimetype, response.decode('utf-8'))

    '''
        Response: String to send over HTML/1.1
        Return byte representation of response
    '''
    def prepareResponse(self, response):
        return response.encode('utf-8')

    '''
        Handle post requests
    '''
    def do_POST(self):
        #Get all posted data
        length = int(self.headers['Content-Length'])
        post_data = urllib.parse.parse_qs(self.rfile.read(length).decode('utf-8'))
        
        #Check the file extension required and
        #set the right mime type
        mimetype, sendReply = self.getMimetype(self.path)
        response = None
        
        #DEBUG: Confirm posted command
        print("Post data:", post_data,"\n")

        #If main directory requested, return main GUI
        if(self.path=="/"):
            self.path="/views/Combined.html"
            mimetype = 'text/html'
            sendReply = True

        #If command is sent, send to main module to send to cortex
        elif(self.path.endswith("command.py")):
            #DEBUG: Confirm command received
            print("Command Received")
            
            #Send command to cortex
            comm = post_data['command'][0]
            response = str(magicGlobalDict["JINX_Controller"].writeSerial(comm))
            response = self.prepareResponse(response)
            sendReply = True
        
        #If GUI is requesting new data and we are talking to cortex
        elif(self.path.endswith("jason.json") and magicGlobalDict["JINX_Controller"]):
             received = int(post_data['received'][0])
             
             #DEBUG: Confirm data query received
             print("Data Received:", received)
             
             response = str(magicGlobalDict["JINX_Controller"].getJSONData(received))
             response = self.prepareResponse(response)
             
             #DEBUG: Confirm proper response
             print("Data Response:", response.decode('utf-8'))
             sendReply = True
        
        try:
            if(sendReply == True):
                if (not response):
                    response = self.getStaticFile()
                self.send200Response(mimetype, response)

        except IOError:
            #DEBUG: Confirm path
            print(self.requestPath)
            self.send_error(404,'File Not Found: %s' % self.path)
      
'''
    CLASS: Control browser communications
'''
class JINX_Server():

    '''
        Controller: Manages communication between browser and cortex
    '''
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

    '''
        Closes all server communications
    '''
    def shutDown(self):

        #Set flag to terminate all indefinite loops
        self.closed=True

        #DEBUG: Confirm active threads
        print(threading.enumerate())

        #Try to prevent any race conditions, so create new thread
        t = threading.Thread(target=self.httpd.server_close(), daemon=True)
        t.run()

        #DEBUG: Confirm state of server, Confirm closed
        print(self.httpd)
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


        #TODO: Finish commenting
        self.httpd.allow_reuse_address = True
        print('running server...')
        #print(self.httpd)
    
        try:
            while(not self.closed):
                #print(dir(self.httpd))
                #print("Closed:", self.closed)
                self.httpd.handle_request()
                #print("Weeee")
                #self.closed=True
            #print("closed: ",self.closed)
        except Exception as e:# KeyboardInterrupt:
            print(e)
        finally:
            self.shutDown()
        print("Server run should be over")

'''
    
'''
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
  

