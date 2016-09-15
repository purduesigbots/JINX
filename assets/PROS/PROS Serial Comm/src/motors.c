/*
 * motors.c
 *
 *  Created on: Aug 17, 2016
 *  Author: Brian
 */

#include "main.h"

// set power to drive motors
//	+ value makes robot drive forward
//	- value makes robot drive reverse
// TODO: Validate that correct signess of power is issued to each motor
void setDrive(int upperLeft, int upperRight, int lowerLeft, int lowerRight) {
	motorSet(MOTOR_UPPER_LEFT, upperLeft);
	motorSet(MOTOR_UPPER_RIGHT, upperRight);
	motorSet(MOTOR_LOWER_LEFT, lowerLeft);
	motorSet(MOTOR_LOWER_RIGHT, lowerRight);
}

// set power to lift motors
// TODO: create function for lifting mechanism

void setLift(int liftSpeed) {
	// left side and right side motors turn opposite directions
	motorSet(MOTOR_LIFT_LEFT_TOP, liftSpeed);
	motorSet(MOTOR_LIFT_LEFT_BOT, liftSpeed);
	motorSet(MOTOR_LIFT_RIGHT_TOP, -liftSpeed);
	motorSet(MOTOR_LIFT_RIGHT_BOT, -liftSpeed);
}
/*
void setLift(int topLeft, int bottomLeft, int topRight, int bottomRight) {
	// left side and right side motors turn opposite directions
	motorSet(MOTOR_LIFT_LEFT_TOP, -topLeft);
	motorSet(MOTOR_LIFT_LEFT_BOT, -bottomLeft);
	motorSet(MOTOR_LIFT_RIGHT_TOP, topRight);
	motorSet(MOTOR_LIFT_RIGHT_BOT, bottomRight);
}
*/
