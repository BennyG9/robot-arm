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
} Encoder;


int32_t Encoder_GetPosition(Encoder* encoder);

void Encoder_Zero(Encoder* encoder);

#endif /* INC_ENCODER_H_ */
