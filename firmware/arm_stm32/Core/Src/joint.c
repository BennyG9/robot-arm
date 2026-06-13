/*
 * joint.c
 *
 *  Created on: May 22, 2026
 *      Author: Benjamin Goldstein
 *
 */

#include "joint.h"

void Joint_Init(Joint* j, Motor* m, Encoder* e, PID* p, uint16_t l, int32_t t){
	j->motor = m;
	j->encoder = e;
	j->pid = p;
	j->limit_switch_pin = l;
	j->target_position = t;
}

void Joint_SetTarget(Joint* joint, int32_t pos){
	joint->target_position = pos;
}


void Joint_Update(Joint* joint){
	int32_t pos = Encoder_GetPosition(joint->encoder);

	float pid_out = PID_Compute(joint->pid, joint->target_position, pos);

	Motor_SetPower(joint->motor, pid_out);
}


void Joint_Reset(Joint* joint){
	joint->target_position = 0;
	Encoder_Zero(joint->encoder);
}

void Joint_Calibrate(Joint* joint){
	//move toward the limit switch at a fair rate
	int pwm = 100 + joint->motor->min_duty_forward;
	Motor_SetPower(joint->motor, pwm);

	//stop when the limit switch is triggered
	while(HAL_GPIO_ReadPin(GPIOC, joint->limit_switch_pin) == GPIO_PIN_RESET){}
	Motor_Stop(joint->motor);
	HAL_Delay(100);

	//move in the reverse direction as slow as possible
	pwm = joint->motor->min_duty_reverse;
	Motor_SetPower(joint->motor, pwm);

	//stop when the limit switch turns off
	while(HAL_GPIO_ReadPin(GPIOC, joint->limit_switch_pin) == GPIO_PIN_SET){}
	Motor_Stop(joint->motor);

	//SET ENCODER HERE
}




