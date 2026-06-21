/*
 * protocol.c
 *
 *  Created on: Jun 20, 2026
 *      Author: Benny Goldstein
 */

#include "protocol.h"


HAL_StatusTypeDef Protocol_ReadPacket(Packet* packet){
	uint8_t byte;

	// look for start byte
	if(Serial_ReadByte(&byte) != HAL_OK) return HAL_ERROR;
	if(byte != START_BYTE) return HAL_ERROR;

	// read command byte
	if(Serial_ReadByte(&(packet->command)) != HAL_OK) return HAL_ERROR;

	// get command argument length
	 packet->arg_length = Protocol_GetPacketLength(packet->command) - 3;

	// get all arguments
	if(Serial_ReadBytes(packet->args, packet->arg_length) != HAL_OK) return HAL_ERROR;

	// get and verify checksum
	if(Serial_ReadByte(&byte) != HAL_OK) return HAL_ERROR;
	if(byte != Protocol_Checksum(packet)) return HAL_ERROR;

	return HAL_OK;
}


void Protocol_WritePacket(Packet* packet){
	uint8_t bytes[MAX_ARG_SIZE + 3];

	// pack start byte and command
	bytes[0] = START_BYTE;
	bytes[1] = packet->command;

	// pack arguments
	int i;
	for(i = 0; i < packet->arg_length; i++){
		bytes[i+2] = (packet->args)[i];
	}

	// calculate and pack checksum
	bytes[i+2] = Protocol_Checksum(packet);

	// write packet
	Serial_WriteBytes(bytes, packet->arg_length + 3);
}


uint8_t Protocol_Checksum(Packet* packet){
	uint8_t checksum = packet->command;
	for(int i = 0; i < packet->arg_length; i++){
		checksum ^= packet->args[i];
	}
	return checksum;
}


