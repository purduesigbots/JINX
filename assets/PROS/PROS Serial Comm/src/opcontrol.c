/**
 * File for operator control code.
 *
 * This file should contain the user operatorControl() function and any functions related to it.
 *
 * Copyright (c) 2011-2014, Purdue University ACM SIG BOTS. All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
 *
 * Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
 * Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
 * Neither the name of Purdue University ACM SIG BOTS nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL PURDUE UNIVERSITY ACM SIG BOTS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 *
 * Purdue Robotics OS contains FreeRTOS (http://www.freertos.org) whose source code may be obtained from http://sourceforge.net/projects/freertos/files/ or on request.
 ********************************************************************************/

#include "main.h"

/* set DRIVER to 1 to turn on driver controls 0 to turn it off */
// #define DRIVER 0
// #define OTHER 1
// #define TEST_MOTORS 2

enum Opmode {DRIVER, OTHER, TEST_MOTORS};

#define DEADBAND 5

static int opmode = OTHER;

const unsigned int TRUE_SPEED[128] = {
  0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
  0, 0, 0, 0, 0, 24, 25, 25, 25, 25, 26, 26, 26, 26, 27,
  27, 27, 27, 27, 27, 27, 27, 27, 28, 28, 28, 28, 29, 29, 29,
  29, 29, 29, 29, 29, 30, 30, 30, 30, 30, 31, 31, 31, 31, 32,
  32, 32, 33, 33, 33, 33, 34, 34, 34, 34, 35, 35, 35, 35, 36,
  36, 36, 37, 37, 37, 37, 38, 38, 38, 39, 39, 39, 40, 40, 41,
  42, 42, 42, 42, 42, 43, 43, 44, 44, 45, 45, 46, 47, 47, 47,
  48, 48, 49, 49, 50, 50, 52, 52, 52, 53, 54, 55, 55, 56, 56,
  60, 61, 64, 65, 65, 66, 70, 72, 72, 80, 85, 127, 127
  }; //True Speed array for Turbo Motors

int setOpmode(int mode) {
    if (mode == DRIVER) { //Enable controll via joystick
        opmode = DRIVER;
        return opmode;
    } else if (mode == OTHER) { //Sent test JINX debug data
        opmode = OTHER;
        return opmode;
    } else if (mode == TEST_MOTORS) {
        opmode = TEST_MOTORS;
        return opmode;
    } else { //If not one of the available modes
        return -1;
    }
}

/* analog is always reading some value so if its magnitude is less than DEADBAND, ignore it */
int scaleJoystick(int in) {
	if (in > DEADBAND)
		return (in * in) >> 7;
	else if (in < -DEADBAND)
		return (-in * in) >> 7;
	return 0;
}

/**
  Runs the user operator control code.
 *
 * This function will be started in its own task with the default priority and stack size whenever the robot is enabled via the Field Management System or the VEX Competition Switch in the operator control mode. If the robot is disabled or communications is lost, the operator control task will be stopped by the kernel. Re-enabling the robot will restart the task, not resume it from where it left off.
 *
 * If no VEX Competition Switch or Field Management system is plugged in, the VEX Cortex will run the operator control task. Be warned that this will also occur if the VEX Cortex is tethered directly to a computer via the USB A to A cable without any VEX Joystick attached.
 *
 * Code running in this task can take almost any action, as the VEX Joystick is available and the scheduler is operational. However, proper use of delay() or taskDelayUntil() is highly recommended to give other tasks (including system tasks such as updating LCDs) time to run.
 *
 * This task should never exit; it should end with some kind of infinite loop, even if empty.
 */
void operatorControl() {
  delay(5000);
  double foo = 0.2;
  double bar = 1;
  printf("%f\n\r", foo*bar);

    int i = 0;
    char mess[5];
	while (true) {
if (opmode == DRIVER) {
		/* analog axis are marked on the controllers
		 * left analog is ch3(vertical) and ch4(horizontal) and the right analog is ch1(horizontal) and ch2(vertical)
		 * we do not need the right analog y axis (ch2) because the right analog is only used for turning
		 */
		int ch3 = scaleJoystick(joystickGetAnalog(1, 3));
		int ch4 = scaleJoystick(joystickGetAnalog(1, 4));
		int ch1 = scaleJoystick(joystickGetAnalog(1, 1));

		/* setting each wheel's motor to correct speed given both analogs positions */
		int upperLeft = ch3 + ch4 + ch1;
		int upperRight = -ch3 + ch4 + ch1;
		int lowerLeft = ch3 - ch4 + ch1;
		int lowerRight = -ch3 - ch4 + ch1;

		/* call set drive with calculated values so that it sets each motor accordingly */
		setDrive(upperLeft, upperRight, lowerLeft, lowerRight);

		if (buttonIsNewPress(JOY1_8U)) {
			setLift(50);
		}
		else if(buttonIsNewPress(JOY1_8D)) {
			setLift(-30);
		}
		else if(buttonIsNewPress(JOY1_8L)) {
			setLift(0);
		}
} else if (opmode == OTHER) {
		if (++i > 99) {
            i = -99;
    }
    sprintf(mess, "%d", i);
    sendData("TestData", mess);
    delay(1000);


} else if (opmode == TEST_MOTORS) {

        // writeJINXMessage("Started TEST_MOTERS in Operator Control 0.");
        // writeJINXMessage("Started TEST_MOTERS in Operator Control 1.");
        delay(5000); //Delay 5 seconds to allow JINX time to connect
        int delayTime = 3000; //Run motors for 3 seconds
        int pwm = 0, speed;
        int motorUpperLeftV, motorUpperRightV, motorLowerLeftV, motorLowerRightV; //Store motor velocities
        motorUpperLeftV = 0;
        motorUpperRightV = 0;
        motorLowerLeftV = 0;
        motorLowerRightV = 0;
        char dataToSend[50];
        //writeJINXMessage("Started TEST_MOTERS in Operator Control 1.");
        imeReset(0);
        imeReset(1);
        imeReset(2);
        imeReset(3);

        delay(500);
        imeInitializeAll();
        delay(500);

        for (pwm = 14; pwm < 128; pwm++) {
            speed = TRUE_SPEED[pwm];
            setDrive(speed, speed, speed, speed);

            imeGetVelocity(0, &motorUpperLeftV);  //Get Velocities
            imeGetVelocity(1, &motorUpperRightV);
            imeGetVelocity(2, &motorLowerLeftV);
            imeGetVelocity(3, &motorLowerRightV);

            //Send velocities
            sprintf(dataToSend, "%d", motorUpperLeftV);
            sendData("UpperLeft", dataToSend);
            sprintf(dataToSend, "%d", motorUpperRightV);
            sendData("UpperRight", dataToSend);
            sprintf(dataToSend, "%d", motorLowerLeftV);
            sendData("LowerLeft", dataToSend);
            sprintf(dataToSend, "%d", motorLowerRightV);
            sendData("LowerRight", dataToSend);

            sprintf(dataToSend, "%d", pwm);
            sendData("DesiredPWM", dataToSend);
            sprintf(dataToSend, "%d", speed);
            sendData("TruePWM", dataToSend);

            delay(delayTime);
        }
}
//endif
		delay(30);
	}
}
