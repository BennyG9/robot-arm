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

	int32_t target_position;
} Joint;

void Joint_Init(Joint* j, Motor* m, Encoder* e, PID* p, int32_t t);

void Joint_SetTarget(Joint* joint, int32_t pos);

void Joint_Update(Joint* joint);

void Joint_Reset(Joint* joint);

#endif /* INC_JOINT_H_ */
