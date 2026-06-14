/*
 * encoder.h
 *
 *  Created on: May 22, 2026
 *      Author: Benjamin Goldstein
 */

#include "main.h"

#ifndef INC_ENCODER_H_
#define INC_ENCODER_H_

typedef struct{
	TIM_HandleTypeDef* timer;

	int32_t offset;

	uint16_t resolution;
} Encoder;


int32_t Encoder_GetPosition(Encoder* encoder);

void Encoder_Zero(Encoder* encoder);

float Encoder_CountToAngle(Encoder* encoder, int16_t count);

int16_t Encoder_AngleToCount(Encoder* encoder, float angle);

float Encoder_GetAngle(Encoder* encoder);

void Encoder_SetAngle(Encoder* encoder, float angle);

#endif /* INC_ENCODER_H_ */
