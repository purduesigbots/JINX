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

//Port over which all serial communication will occur. STDIN == STDOUT, so either can be used
static FILE* comPort = stdout;

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

void writeSerial(const char *message) {
    fprintf(comPort, "%s%s%s%s", JINX_HEADER, JINX_DELIMETER, message, JINX_TERMINATOR);
    fflush(comPort);
}

//Wrapper function for sendData to send non-numeric data more easily
void writeJINXMessage(const char *message) {
    sendData("msg", message);
}

void sendData(const char *name, const char *value) {
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
    while(((get = fgetc(comPort)) != term) && (bufferIndex < MAX_IN_SIZE)) {
        stringBuffer[bufferIndex++] = get;
        get = fgetc(comPort);
    }

    //Terminate string with null character (Is that the term?)
    //This means that if only a terminator is read, string is only an endstring (Sounds silly, but oh well)
    stringBuffer[bufferIndex] = '\0';

    //Return size of new string
    return bufferIndex;
}

//Get tokenNumth token of incoming string, and put it in inStr.token
//Do not pass a null pointer!
int getToken(JINX *inStr, int tokenNum) {
    //Check for invalid token request
    if ((tokenNum < 0) || (tokenNum > MAX_IN_SIZE)) {
        (inStr->token)[0] = NULL;
        return -1;
    }

    //Hold start and end of token
    char *beginStr, *endStr;
    beginStr = inStr->command;
    int tokenCount = 0;

    //Until we pass the desired number of tokens, move to the next token start
    while (tokenCount++ < tokenNum) {
        beginStr = strchr(beginStr, ' ');
        if (++beginStr == NULL) {
          (inStr->token)[0] = NULL;
          return -1;}
    }

    //Token should be terminated by a space or the null character
    if ((endStr = strchr(beginStr, ' ')) == NULL) {
        endStr = strchr(beginStr, NULL);
    }

    //Set the token
    strncpy(inStr->token, beginStr, endStr - beginStr);
    return 0;
}

void JINXRun(void* ignore) {
	int del = 500;
  JINX inStr;
    //setOpmode(1);
    //Read the garbage. Assume run before serial communications open
	while(fgetc(comPort) != EOF);

	while (true) {
//#if DEBUG_JINX
        writeJINXMessage("Should wait for new string");
//#endif

        //Get message, save in inStr, then parse.
        readLine(inStr.command);
        parseMessage(inStr.command);
		delay(del);
	}

}
