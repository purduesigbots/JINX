/*
 * motors.h
 *
 *  Created on: Aug 17, 2016
 *      Author: Brian
 */

#ifndef MOTORS_H_
#define MOTORS_H_

#define EAT 127
#define SPIT -127
#define MOTOR_MIN 0

/********************************************************************************
 *                                                                              *
 *                          MOTOR DEFINITIONS                                   *
 *                                                                              *
*********************************************************************************/
// TODO: define all motor ports for basic functionality
/////////////////////////// DRIVE MOTORS ////////////////////////////////////////
#define MOTOR_UPPER_LEFT	3
#define MOTOR_UPPER_RIGHT	4
#define MOTOR_LOWER_LEFT	2
#define MOTOR_LOWER_RIGHT	5


/////////////////////////// LIFT MOTORS /////////////////////////////////////
#define MOTOR_LIFT_LEFT_TOP   	6
#define MOTOR_LIFT_LEFT_BOT		8
#define MOTOR_LIFT_RIGHT_TOP	7
#define MOTOR_LIFT_RIGHT_BOT  	9

/********************************************************************************
 *                                                                              *
 *                          MOTOR BASIC FUNCTIONS                               *
 *                                                                              *
*********************************************************************************/
// Movement Helper Functions
void setDrive(int upperLeft, int upperRight, int lowerLeft, int lowerRight);
void setLift(int liftSpeed);
//void setLift(int topLeft, int bottomLeft, int topRight, int bottomRight);

#endif /* MOTORS_H_ */
