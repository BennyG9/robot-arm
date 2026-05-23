/*
 * motor.h
 *
 *  Created on: May 22, 2026
 *      Author: Benjamin Goldstein
 */

#include "main.h"

#ifndef INC_MOTOR_H_
#define INC_MOTOR_H_

typedef struct{
	TIM_HandleTypeDef* timer;

	uint32_t forward_channel;

	uint32_t reverse_channel;

	int min_duty_forward;
	int min_duty_reverse;
} Motor;

void Motor_SetPower(Motor* motor, float power);

void Motor_Stop(Motor* motor);

#endif /* INC_MOTOR_H_ */
