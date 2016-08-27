/**
 * @file include/buttons.h
 * @sa buttons.c @link buttons.c
 *
 ********************************************************************************/

#ifndef BUTTONS_H_
#define BUTTONS_H_

#include "main.h"

/// Represents all available
typedef enum
{
	JOY1_5D = 0,
	JOY1_5U = 1,
	JOY1_6D = 2,
	JOY1_6U = 3,
	JOY1_7U = 4,
	JOY1_7L = 5,
	JOY1_7R = 6,
	JOY1_7D = 7,
	JOY1_8U = 8,
	JOY1_8L = 9,
	JOY1_8R = 10,
	JOY1_8D = 11,

	JOY2_5D = 12,
	JOY2_5U = 13,
	JOY2_6D = 14,
	JOY2_6U = 15,
	JOY2_7U = 16,
	JOY2_7L = 17,
	JOY2_7R = 18,
	JOY2_7D = 19,
	JOY2_8U = 20,
	JOY2_8L = 21,
	JOY2_8R = 22,
	JOY2_8D = 23,

	LCD_LEFT = 24,
	LCD_CENT = 25,
	LCD_RIGHT = 26
} tButton;
///@cond
void initButtons();
bool buttonIsNewPress(tButton);
bool buttonGetState(tButton);
///@endcond
#endif
