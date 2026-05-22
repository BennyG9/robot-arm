/*
 * joint.c
 *
 *  Created on: May 22, 2026
 *      Author: Benjamin Goldstein
 *
 */

#include "joint.h"


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




