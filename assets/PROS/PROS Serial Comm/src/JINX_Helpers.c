#include "main.h"
#include "JINX.h"

//*************This space reserved for user-defined functions***************
    //Example of user defined JINX helper function.
    //Since it is at the top of this file, it can be called from anywhere else in this file.
    //Good practice is to put its prototype in JINX.h, though.
    void handleGet(JINX *inStr) {
        getToken(inStr, 1);
        if (strcmp(inStr->token, "DEBUG_JINX") == 0) {
            //Stringify DEBUG_JINX. I think.
            //TODO: Make sure this works
            writeJINXMessage("Asked for Debug");
            sprintf(inStr->token, "%s, %d", inStr->token, DEBUG_JINX);
        } else {
            strcat(inStr->token, " was unable to be gotten.");
        }

        writeJINXMessage(inStr->token);
    }


    void handleDrive(JINX *inStr) {
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

        getToken(inStr, 1);
        opmode = parseInt(inStr->token);

        ret = setOpmode(opmode);
        sprintf(inStr->token, "Operator control mode: %d.", ret);
        writeJINXMessage(inStr->token);
    }

    //Returns integer parsed from character buffer
    int parseInt(const char *intString) {
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

void parseMessage(JINX *inStr) {
    writeJINXMessage(inStr->command);
    getToken(inStr, 0);
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
