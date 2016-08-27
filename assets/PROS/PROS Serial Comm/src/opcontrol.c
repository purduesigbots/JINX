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
#define DRIVER 0
#define OTHER 0

#define DEADBAND 5

/* analog is always reading some value so if its magnitude is less than DEADBAND, ignore it */
int scaleJoystick(int in) {
	if (in > DEADBAND)
		return (in * in) >> 7;
	else if (in < -DEADBAND)
		return (-in * in) >> 7;
	return 0;
}

/**
 * Runs the user operator control code.
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
	while (true)
	{
#if DRIVER
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

#elif OTHER
		/* Notice how this is grayed out */

#endif
		delay(30);
	}
}
