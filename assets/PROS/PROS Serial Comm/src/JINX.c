/**
 *JINX.c
 *
 *Put this file in your src folder, and JINX.h in your include folder
 *Include JINX.h in your main.h
 *Call initJINX() and create start JINXRun in its own task in initialize()
 *
 *User should replace body of parseMessage() with their own parser
 *They may of course create helper functions to call, if they desire.
 *An example helper function is defined in the space below
 */

#include "main.h"
#include "JINX.h"

#define DEBUG_JINX true

//Port over which all serial communication will occur. STDIN == STDOUT, so either can be used
static FILE* comPort = stdout;

//*************This space reserved for user-defined functions***************
    //Example of user defined JINX helper function.
    //Since it is at the top of this file, it can be called from anywhere else in this file.
    //Good practice is to put its prototype in JINX.h, though.
    void handleGet() {
        char message[100];
        readLine(message);
        if (strcmp(message, "DEBUG_JINX") == 0) {
            //Stringify DEBUG_JINX. I think.
            //TODO: Make sure this works
            writeJINXMessage("Asked for Debug");
            sprintf(message, "%s, %d", message, DEBUG_JINX);
        } else {
            strcat(message, " was unable to be gotten.");
        }

        writeJINXMessage(message);
    }

    void handleDrive() {
        char message[100];
        readLine(message);
        if (strcmp(message, "f") == 0) {
            writeJINXMessage("Driving forward");
            setDrive(120, 120, 120, 120);
        } else if (strcmp(message, "b") == 0) {
            writeJINXMessage("Driving backwards");
            setDrive(-120, -120, -120, -120);
        } else if (strcmp(message, "s") == 0) {
            writeJINXMessage("Stopping");
            setDrive(0,0,0,0);
        } else {
            writeJINXMessage("Invalid drive command. Should be 'f', 'b', or 's'.")
        }
    }

    //Returns integer parsed from character buffer
    int parseInt(char* intString) {
        char digit;

        //Limit to 32 digit integer. Please don't send 32 digit integers
        char tempStr[33] = "";

        int len = strlen(intString);

        //Catch empty string
        if (len == 0) {
            char errorMessage[100];
            sprintf(errorMessage, "Error, unable to parse integer: %s", intString);
            sendData("Error", errorMessage);
        }

        for(int i = 0; i < len; i++) {
            digit = intString[i];
            if ((digit < '0') || (digit > '9')) {
                char errorMessage[100];
                sprintf(errorMessage, "Error, unable to parse integer: %s", intString);
                sendData("Error", errorMessage);
                return -1;
            }

            tempStr[i] = digit;
        }

        return atoi(tempStr);
    }
//**************************************************************************

void initJINX(FILE* port) {
    //If the port is not a valid communications port, inform user of error
    if (!setComPort(port)) {
        //Would print to stderr, but not set for PROS
        printf("Invalid Port specified for JINX communications\n");

        //Optionally allow user to fail on error. Not recommended
        //exit(EXIT_FAILURE);
    }
}

bool setComPort(FILE* port) {
    //If the port is either of the UARTs, set up the pins correctly for serial data
    if (port == uart1 || port == uart2) {
        usartInit(port, 115200, SERIAL_8N1);
        return true;

    //Port is set to STDOUT by default, but still allow users to specify it if they wish.
    } else if (port == stdout) {
        return true;
    }

    #if(DEBUG_JINX)
            printf("Failed to open specified port for JINX (setComPort(FILE* port))\n");
    #endif

    return false;
}

void writeSerial(char* message) {
    fprintf(comPort, "%s%s%s%s", JINX_HEADER, JINX_DELIMETER, message, JINX_TERMINATOR);
    fflush(comPort);
}

//Wrapper function for sendData to send non-numeric data more easily
void writeJINXMessage(char* message) {
    char msg[4] = "msg";
    sendData(msg, message);
}

void sendData(char* name, char* value) {
    // if (strlen(name) + strlen(value) >= MAX_MESSAGE_SIZE + PROTOCOL_SIZE) {
    //     fprintf(comPort, "Warning: Tried to send too large a message named %s", name);
    //     return;
    // }

    char message[100];
    sprintf(message, "%s%s%s", name, JINX_DELIMETER, value);
    writeSerial(message);
}

int readLine(char* stringBuffer) {

    //Terminating character to specify end of line/message
    char term = '\n';

    //Single character read in
    char get;

    //How many characters read in/Index of stringBuffer to write to
    int bufferIndex = 0;

    //Get character from serial. If first character is terminator, quit immediately
    get = fgetc(comPort);
    while(get != term) {
        stringBuffer[bufferIndex++] = get;
        get = fgetc(comPort);
    }

    //Terminate string with null character (Is that the term?)
    //This means that if only a terminator is read, string is only an endstring (Sounds silly, but oh well)
    stringBuffer[bufferIndex] = '\0';

    //Return size of new string
    return bufferIndex;
}

void parseMessage(char* message) {
    writeJINXMessage(message);

    //Example parse. User can should replace with own body.
    if (strcmp(message, "Option 1") == 0) {
        //Do option 1
        writeJINXMessage("Option 1 chosen.");
    } else if(strcmp(message, "get") == 0) {
        //Call another function to handle "get"
        handleGet();
    } else if (strcmp(message, "drive") == 0) {
        handleDrive();
    } else {
        //Do default
        writeJINXMessage("No comparison found");
    }
}

void JINXRun(void* ignore) {
	int del = 500;
	char inStr[100];

    //Delay a second to allow time for communication to open up
	delay(1000);

	while (true) {
#if DEBUG_JINX
        writeJINXMessage("Should wait for new string");
#endif

        //Get message, save in inStr, then parse.
        readLine(inStr);
        parseMessage(inStr);
		delay(del);
	}

}
