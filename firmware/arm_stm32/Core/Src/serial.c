/*
 * serial.c
 *
 *  Created on: Jun 20, 2026
 *      Author: Benny Goldstein
 */

#include "serial.h"


static UART_HandleTypeDef* serial_uart;


void Serial_Init(UART_HandleTypeDef* huart){
	serial_uart = huart;
}


// returns HAL_OK if the byte was read
HAL_StatusTypeDef Serial_ReadByte(uint8_t* byte){
	if(serial_uart == NULL) return HAL_ERROR;
	return HAL_UART_Receive(serial_uart, byte, 1, SERIAL_TIMEOUT_MS);
}


// returns HAL_OK if the bytes were read
HAL_StatusTypeDef Serial_ReadBytes(uint8_t* bytes, uint16_t length){
	if(serial_uart == NULL) return HAL_ERROR;
	return HAL_UART_Receive(serial_uart, bytes, length, SERIAL_TIMEOUT_MS);
}


void Serial_WriteByte(uint8_t* byte){
	if(serial_uart == NULL) return;
	HAL_UART_Transmit(serial_uart, byte, 1, SERIAL_TIMEOUT_MS);
}


void Serial_WriteBytes(uint8_t* bytes, uint16_t length){
	if(serial_uart == NULL) return;
	HAL_UART_Transmit(serial_uart, bytes, length, SERIAL_TIMEOUT_MS);
}
