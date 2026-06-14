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

float Encoder_CountToAngle(Encoder* encoder, int16_t count){
	float inc = 360.0f / ((float)encoder->resolution);
	return ((float)count) * inc;
}

int16_t Encoder_AngleToCount(Encoder* encoder, float angle){
	float inc = ((float)encoder->resolution) / 360.0;
	return (int16_t)(angle * inc);
}


float Encoder_GetAngle(Encoder* encoder){
	//float inc = 360.0 / ((float)encoder->resolution);
	//float angle = ((float)Encoder_GetPosition(encoder)) * inc;
	float angle = Encoder_CountToAngle(encoder, Encoder_GetPosition(encoder));
	return angle;
}


void Encoder_SetAngle(Encoder* encoder, float angle){
	//float inc = ((float)encoder->resolution) / 360.0;
	//int16_t new_pos = (int16_t)(angle * inc);
	int16_t new_pos = Encoder_AngleToCount(encoder, angle);
	__HAL_TIM_SET_COUNTER(encoder->timer, new_pos);
}
