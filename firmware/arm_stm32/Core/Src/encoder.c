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
	encoder->offset = (int16_t)__HAL_TIM_GET_COUNTER(encoder->timer);
}
