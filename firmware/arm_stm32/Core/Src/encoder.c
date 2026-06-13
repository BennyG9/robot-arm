/*
 * encoder.c
 *
 *  Created on: May 22, 2026
 *      Author: Benjamin Goldstein
 */

#include "encoder.h"

int32_t Encoder_GetPosition(Encoder* encoder){
	int32_t raw_pos = (int16_t)__HAL_TIM_GET_COUNTER(encoder->timer);

	return raw_pos - encoder->offset;
}


void Encoder_Zero(Encoder* encoder){
	//encoder->offset = (int16_t)__HAL_TIM_GET_COUNTER(encoder->timer);
	__HAL_TIM_SET_COUNTER(encoder->timer, 0);
}


float Encoder_GetAngle(Encoder* encoder){
	float inc = 360.0 / ((float)encoder->resolution);
	float angle = ((float)Encoder_GetPosition(encoder)) * inc;
	return angle;
}


void Encoder_SetAngle(Encoder* encoder, float angle){
	float inc = ((float)encoder->resolution) / 360.0;
	int32_t new_pos = (int32_t)(angle * inc);
	__HAL_TIM_SET_COUNTER(encoder->timer, new_pos);
}
