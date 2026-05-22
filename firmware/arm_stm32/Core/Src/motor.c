/*
 * motor.c
 *
 *  Created on: May 22, 2026
 *      Author: Benjamin Goldstein
 */

#include "motor.h"
#include "main.h"

extern TIM_HandleTypeDef htim3;

void Motor_SetPower(Motor* motor, float power){

	if(power > 1000){
		power = 1000;
	}else if(power < -1000){
		power = -1000;
	}else if(power < 50 && power > -50){
		power = 0;
	}

	if(power >= 0){
		__HAL_TIM_SET_COMPARE(motor->timer, motor->forward_channel, (uint16_t)power);
		__HAL_TIM_SET_COMPARE(motor->timer, motor->reverse_channel, 0);
	}else{
		__HAL_TIM_SET_COMPARE(motor->timer, motor->forward_channel, 0);
		__HAL_TIM_SET_COMPARE(motor->timer, motor->reverse_channel, (uint16_t)(-power));
	}

}


void Motor_Stop(Motor* motor){
	Motor_SetPower(motor, 0);
}

