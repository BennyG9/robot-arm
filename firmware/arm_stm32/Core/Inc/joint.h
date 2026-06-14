/*
 * joint.h
 *
 *  Created on: May 22, 2026
 *      Author: Benjamin Goldstein
 */

#ifndef INC_JOINT_H_
#define INC_JOINT_H_

#include "motor.h"
#include "encoder.h"
#include "pid.h"

typedef struct{
	Motor* motor;

	Encoder* encoder;

	PID* pid;

	uint16_t limit_switch_pin;

	int16_t target_position;

	float max_angle;

	float min_angle;
} Joint;

void Joint_Init(Joint* j, Motor* m, Encoder* e, PID* p, uint16_t l, int32_t t, float max_a, float min_a);

void Joint_SetTargetCount(Joint* joint, int16_t pos);

void Joint_SetTargetAngle(Joint* joint, float angle);

void Joint_Update(Joint* joint);

void Joint_Reset(Joint* joint);

void Joint_Calibrate(Joint* joint);

#endif /* INC_JOINT_H_ */
