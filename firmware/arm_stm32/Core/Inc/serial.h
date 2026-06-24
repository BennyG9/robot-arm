/*
 * serial.h
 *
 *  Created on: Jun 20, 2026
 *      Author: Benny Goldstein
 */

#ifndef INC_SERIAL_H_
#define INC_SERIAL_H_

#include "main.h"

#define SERIAL_TIMEOUT_MS 0


void Serial_Init(UART_HandleTypeDef* huart);

// returns HAL_OK if the byte was read
HAL_StatusTypeDef Serial_ReadByte(uint8_t* byte);

// returns HAL_OK if the bytes were read
HAL_StatusTypeDef Serial_ReadBytes(uint8_t* bytes, uint16_t length);

void Serial_WriteByte(uint8_t* byte);

void Serial_WriteBytes(uint8_t* bytes, uint16_t length);


#endif /* INC_SERIAL_H_ */
