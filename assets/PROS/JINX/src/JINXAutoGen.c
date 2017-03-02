#include "main.h"
#include "JINX.h"

// Auto-generated JINX file

void autoJINXparse(JINX *inStr) {
if (strcmp("powerLevelBackup", inStr->token) == 0) {
	powerLevelBackup( );
} else if (strcmp("powerLevelMain", inStr->token) == 0) {
	powerLevelMain( );
} else if (strcmp("motorStopAll", inStr->token) == 0) {
	motorStopAll( );
} else if (strcmp("speakerInit", inStr->token) == 0) {
	speakerInit( );
} else if (strcmp("speakerShutdown", inStr->token) == 0) {
	speakerShutdown( );
} else if (strcmp("imeInitializeAll", inStr->token) == 0) {
	imeInitializeAll( );
} else if (strcmp("imeShutdown", inStr->token) == 0) {
	imeShutdown( );
} else if (strcmp("getchar", inStr->token) == 0) {
	getchar( );
} else if (strcmp("putchar", inStr->token) == 0) {
	putchar( getJINXint(inStr, 0) );
} else if (strcmp("taskGetCount", inStr->token) == 0) {
	taskGetCount( );
} else if (strcmp("autonomous", inStr->token) == 0) {
	autonomous( );
} else if (strcmp("initializeIO", inStr->token) == 0) {
	initializeIO( );
} else if (strcmp("initialize", inStr->token) == 0) {
	initialize( );
} else if (strcmp("operatorControl", inStr->token) == 0) {
	operatorControl( );
} else  {
	writeJINXMessage("No Match Found");
}
}