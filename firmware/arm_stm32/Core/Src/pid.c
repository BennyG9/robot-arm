/*
 * pid.c
 *
 *  Created on: May 22, 2026
 *      Author: Benjamin Goldstein
 */

#include "pid.h"


void PID_Reset(PID* pid){
	pid->integral = 0.0f;
	pid->prev_error = 0.0f;
}

float PID_Compute(PID* pid, float target, float measurement){
	float error = target - measurement;

	pid->integral = pid->integral + error;

	float derivative = error - pid->prev_error;
	pid->prev_error = error;

	float out = pid->Kp * error + pid->Ki * pid->integral + pid->Kd * derivative;

	return out;
}

