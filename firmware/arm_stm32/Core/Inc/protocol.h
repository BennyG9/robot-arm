/*
 * protocol.h
 *
 *  Created on: Jun 20, 2026
 *      Author: Benny Goldstein
 */

#ifndef INC_PROTOCOL_H_
#define INC_PROTOCOL_H_

#include "main.h"
#include "serial.h"
#include "protocol_data.h"

typedef struct{
	uint8_t command;

	uint8_t args[MAX_ARG_SIZE];

	uint16_t arg_length;
} Packet;

HAL_StatusTypeDef Protocol_ReadPacket(Packet* packet);

void Protocol_WritePacket(Packet* packet);

uint8_t Protocol_Checksum(Packet* packet);

void Protocol_WriteError(uint8_t error_code);

#endif /* INC_PROTOCOL_H_ */
