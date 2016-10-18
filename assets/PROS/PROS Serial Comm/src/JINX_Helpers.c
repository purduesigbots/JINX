#include "main.h"
#include "JINX.h"

//*************This space reserved for user-defined functions***************
    //Example of user defined JINX helper function.
    //Since it is at the top of this file, it can be called from anywhere else in this file.
    //Good practice is to put its prototype in JINX.h, though.
    void handleGet(JINX *inStr) {
        //Get the first token from the sent command
        getToken(inStr, 1);

        //Host outgoing messages
        char *message = (char*)malloc(sizeof(char) * (strlen(inStr->token) + 30));
        if (strcmp(inStr->token, "DEBUG_JINX") == 0) {
            writeJINXMessage("Asked for Debug");
            sprintf(message, "%s, %d", inStr->token, DEBUG_JINX);
        } else {
            sprintf(message, "%s %s", inStr->token, " was unable to be gotten.");
        }

        //Free malloc'd string
        writeJINXMessage(message);
        free(message);
        message = NULL;
    }

    //Drive a bit
    void handleDrive(JINX *inStr) {
        //Get the first token from the sent command
        getToken(inStr, 1);
        if (strcmp(inStr->token, "f") == 0) {
            writeJINXMessage("Driving forward");
            setDrive(120, 120, 120, 120);
        } else if (strcmp(inStr->token, "b") == 0) {
            writeJINXMessage("Driving backwards");
            setDrive(-120, -120, -120, -120);
        } else if (strcmp(inStr->token, "s") == 0) {
            writeJINXMessage("Stopping");
            setDrive(0,0,0,0);
        } else {
            writeJINXMessage("Invalid drive command. Should be 'f', 'b', or 's'.");
        }
    }

    void handleOpmode(JINX *inStr) {
        int ret;
        int opmode;
        char *message;

        //Get the first token from the sent command
        getToken(inStr, 1);
        opmode = parseInt(inStr->token);
        message = (char*)malloc(40);  //Hold room for below string and integer. More room than needed

        ret = setOpmode(opmode);
        sprintf(message, "Operator control mode: %d.", ret);
        writeJINXMessage(message);

        free(message);
        message = NULL;
    }

    //Returns positive integer parsed from character buffer
    int parseInt(const char *intString) {
        char digit;

        //Limit to 32 digit integer. Please don't send 32 digit integers
        char tempStr[33] = "";

        int len = strlen(intString);

        //Catch empty string
        if (len == 0) {
            char errorMessage[100];
            sprintf(errorMessage, "Error, unable to parse integer: %s", intString);
            writeJINXData("Error ", errorMessage);
        }

        for (int i = 0; i < len; i++) {
            digit = intString[i];
            if ((digit < '0') || (digit > '9')) {
                char errorMessage[100];
                sprintf(errorMessage, "Error, unable to parse integer: %s", intString);
                writeJINXData("Error", errorMessage);
                return -1;
            }

            tempStr[i] = digit;
        }

        return atoi(tempStr);
    }
//**************************************************************************

void parseMessage(JINX *inStr) {
    writeJINXMessage(inStr->command);
    getToken(inStr, 0);   //Set inStr->token to first token (space-delimated word)
    //Example parse. User can should replace with own body.
    if (strcmp(inStr->token, "Option_1") == 0) {
        //Do option 1
        writeJINXMessage("Option 1 chosen.");
    } else if(strcmp(inStr->token, "get") == 0) {
        //Call another function to handle "get"
        handleGet(inStr);
    } else if (strcmp(inStr->token, "drive") == 0) {
        handleDrive(inStr);
    } else if (strcmp(inStr->token, "opmode") == 0) {
        handleOpmode(inStr);
    } else {
        //Do default
        writeJINXMessage("No comparison found");
    }
}
