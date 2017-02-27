#include "main.h"

// Auto-generated JINX file
if (strcmp("set", inStr->token) == 0) {
	set( getJINXint(inStr, 0), getJINXint(inStr, 1) );
} else if (strcmp("confidentize", inStr->token) == 0) {
	confidentize( getJINX(inStr, 0) );
} else if (strcmp("manualThrow", inStr->token) == 0) {
	manualThrow( getJINXint(inStr, 0), getJINXunsigned_int(inStr, 1) );
} else if (strcmp("newThrow", inStr->token) == 0) {
	newThrow( getJINXint(inStr, 0), getJINXunsigned_int(inStr, 1), getJINXunsigned_int(inStr, 2) );
} else  {
	writeJINXMessage("No Match Found");
}