#ifndef JINX_H
#define JINX_H

//INCLUDES
#include <string.h>
#include <stdarg.h>

//CONSTANTS
#define JINX_HEADER "JINX"
#define JINX_DELIMETER "_"
#define JINX_TERMINATOR "\r\n"

//#define MAX_MESSAGE_SIZE 100
//#define PROTOCOL_SIZE 10
// #define PROTOCOL_SIZE (strlen(JINX_HEADER) + strlen(JINX_DELIMETER) \
//     + strlen(JINX_TERMINATOR))

//Functions
/**
 *port: which port to accept communications from. Should be UART1, UART2, or stdout/in
 */
void initJINX(FILE* port);

/**
 *port: which port to accept communications from. Should be UART1, UART2, or stdout/in
 *
 *Returns false if port is not one of above
 */
bool setComPort(FILE* port);

/**
 *message: raw string to send. Don't pass newlines.
 *
 *Formats outgoing message to fulfil JINX Protocol
 */
void writeSerial(char* message);

/**
 *message: raw string to send. Don't pass newlines.
 *
 *Calls sendData with name "msg" and value message
 *Just a convinience to make it easy to send raw strings to GUI
 */
void writeJINXMessage(char* message);

/**
 *port: which port to accept communications from. Should be UART1, UART2, or stdout/in
 *string: String to copy line into
 *
 *Blocks until done
 *terminator is "/n"
 */
int readLine(FILE* port, char* string);

/**
 *message: message recieved from comPort
 *
 *User should define function and handle requests as they see fit.
 */
void parseMessage(char* message);

/**
 *name: identifier in JSON sent to Front End. Should not have any whitespace
 *value: value in JSON sent to Front End. No newline characters.
 *      Users should convert numeric data to a string beforehand, because I am too lazy to implement myself
 *      Recommended that users declare temp string and use sprintf
 */
void sendData(char* name, char* value);

/**
 *ignore: Do not use
 *
 *Repeatedly reads serial data, then passes of to parser to be handled.
 */
void JINXRun(void* ignore);
#endif
