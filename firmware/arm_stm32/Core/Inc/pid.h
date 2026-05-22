/*
 * pid.h
 *
 *  Created on: May 22, 2026
 *      Author: Benjamin Goldstein
 */

#ifndef INC_PID_H_
#define INC_PID_H_

typedef struct{
	float Kp;
	float Ki;
	float Kd;

	float integral;

	float prev_error;
} PID;

void PID_Reset(PID* pid);

float PID_Compute(PID* pid, float target, float measurement);

#endif /* INC_PID_H_ */
