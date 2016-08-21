#include "main.h"
#include "JINX.h"

#define DEBUG_JINX false

static FILE* comPort = stdout;
//static char unused;

void initJINX(FILE* port) {
    if (!setComPort(port)) {
        //Would print to stderr, but not set for PROS
        printf("Invalid Port specified for JINX communications\n");
        //exit(EXIT_FAILURE);
    }
}

bool setComPort(FILE * port) {
    if (port == uart1 || port == uart2) {
        usartInit(port, 115200, SERIAL_8N1);
        return true;
    } else if (port == stdout) {
        return true;
    }

    #if(DEBUG_JINX)
            printf("failed to open port %d for JINX\n", port);
    #endif

    return false;
}


char * getMessage(char* JINXMessage) {
    return NULL;
}

//NOTE: Because vfprintf is not implemented in PROS, I am not allowing
//Variable length arguments/string formatting in this method.
//Strings must be formatted with sprintf or like before being passed as the message
void writeJINXMessage(char* message) {
    fprintf(comPort, "%s%s%s%s", JINX_HEADER, JINX_DELIMETER, message, JINX_TERMINATOR);
    fflush(comPort);
}

void sendData(char* name, char* value) {
    char message[50];
    sprintf(message, "%s%s%s", name, JINX_DELIMETER, value);
    writeJINXMessage(message);
}

int readLine(FILE* port, char* string) {
    char term = '\n';
    char get;
    int count = 0;

    string[0] = '\0';

    get = fgetc(port);
    while(get != term) {
        string[count++] = get;
        get = fgetc(port);
    }
    string[count] = '\0';
    return count;
}


void parseMessage(char* message) {
    writeJINXMessage(message);
}

void JINXRun(void* ignore) {
	int error, time, command, charsWrit, string;
	int del = 500;
	//int inInt;
	char inStr[50];
	//char * inStrPtr = inStr;
	time = millis();

	delay(1000);
	usartInit(uart1, 115200, SERIAL_8N1);

	//if(false)
	while (true) {
        writeJINXMessage("Should wait for new string");
        readLine(comPort, inStr);
        parseMessage(inStr);


		//delay(10000);
		//scan(inStr, 10);

		//fprintf(33, "TEST 2");
		// command = joystickGetDigital(1,1,1);
		// error = joystickGetAnalog(1,1);
		// string = joystickGetAnalog(1,3);
		//printf("{\"PID\": {\"Error\": %d,\"Command_Value\": %d,\"string\": \"%d\",\"time\": %d}}\n", error, command, string, time);
		//charsWrit = fprintf(uart1,
		//				"{\"PID\": {\"Error\": %d,\"Command_Value\": %d,\"string\": \"%d\",\"time\": %d}}\n",
		//				error, string, string, time);
		//printf(("{\"JINX\": {\"Error\": %d,\"Command_Value\": %d,\"string\": \"%d\",\"time\": %d}}\n\r",
		//		error, string, string, time));
		//printf("%d\n", charsWrit);
        //fprintf(stdout, "%d\n", charsWrit);
        //writeJINXMessage(("Good Message d"));
        //printf("Bad Begin %s", JINX_TERMINATOR);
        //printf("%s Bad End", JINX_HEADER);
		//time = millis();


		delay(del);
	}

}
