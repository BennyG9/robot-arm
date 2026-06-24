/*
 * protocol.c
 *
 *  Created on: Jun 20, 2026
 *      Author: Benny Goldstein
 */

#include "protocol.h"

static ReadState current_state = WaitStart;


HAL_StatusTypeDef Protocol_ReadPacket(Packet* packet){
	// state machine
	switch(current_state){

		// waits for start byte
		case WaitStart:

			// look for byte in the serial monitor
			if(SerialMonitor_Available() > 0){

				// get byte from serial monitor
				uint8_t byte;
				if(SerialMonitor_ReadByte(&byte) == HAL_ERROR) return HAL_ERROR;

				// check for start byte
				if(byte == START_BYTE){

					// go to next state
					current_state = WaitCmd;

				// break and continue waiting
				}else break;
			}else break;


		// waits for cmd byte
		case WaitCmd:

			// look for byte in serial monitor
			if(SerialMonitor_Available() > 0){

				// get command byte from serial monitor
				if(SerialMonitor_ReadByte(&(packet->command)) == HAL_ERROR) return HAL_ERROR;

				// save command length
				packet->arg_length = Protocol_GetPacketLength(packet->command) - 3;

				// go to next state
				current_state = WaitArgs;

			// break and continue waiting
			}else break;


		// waits for all argument bytes
		case WaitArgs:

			// look for enough bytes in serial monitor
			if(SerialMonitor_Available() >= packet->arg_length){

				// get all argument bytes from serial monitor
				if(SerialMonitor_ReadBytes(packet->args, packet->arg_length) == HAL_ERROR) return HAL_ERROR;

				// go to next state
				current_state = WaitChecksum;

			// break and continue waiting
			}else break;


		// waits for checksum
		case WaitChecksum:

			// look for byte in serial monitor
			if(SerialMonitor_Available() > 0){

				// get checksum byte from serial monitor
				uint8_t byte;
				if(SerialMonitor_ReadByte(&byte) == HAL_ERROR) return HAL_ERROR;

				// get and verify checksum
				if(byte != Protocol_Checksum(packet)){

					// ditch corrupted packet
					current_state = WaitStart;
					return HAL_ERROR;
				}

				// reset state machine
				current_state = WaitStart;

				// give the green light
				return HAL_OK;

			}else break;
	}
	return HAL_TIMEOUT;
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
	uint16_t checksum = (uint16_t)(packet->command);
	for(int i = 0; i < packet->arg_length; i++){
		checksum += (uint16_t)((packet->args)[i]);
	}
	return (uint8_t)(checksum % 0xFF);
}


void Protocol_WriteError(uint8_t error_code){
	Packet err;
	err.arg_length = 1;
	err.args[0] = error_code;
	err.command = 0x07;
	Protocol_WritePacket(&err);
}











//HAL_StatusTypeDef Protocol_ReadPacket(Packet* packet){
//	uint8_t byte;
//
//	// look for start byte
//	if(Serial_ReadByte(&byte) != HAL_OK) return HAL_ERROR;
//
//	if(byte != START_BYTE) return HAL_ERROR;
//
//	Protocol_WriteError(0x41);
//
//	// read command byte
//	if(Serial_ReadByte(&(packet->command)) != HAL_OK){
//		Protocol_WriteError(0x03);
//		return HAL_ERROR;
//	}
//
//	Protocol_WriteError(0x42);
//
//	// get command argument length
//	packet->arg_length = Protocol_GetPacketLength(packet->command) - 3;
//
//	Protocol_WriteError(0x43);
//
//	// get all arguments
//	if(Serial_ReadBytes(packet->args, packet->arg_length) != HAL_OK){
//		Protocol_WriteError(0x04);
//		return HAL_ERROR;
//	}
//
//	Protocol_WriteError((packet->args)[0]);
//
//	// get and verify checksum
//	if(Serial_ReadByte(&byte) != HAL_OK){
//		Protocol_WriteError(0x05);
//		return HAL_ERROR;
//	}
//
//	Protocol_WriteError(0x45);
//
//	if(byte != Protocol_Checksum(packet)){
//		Protocol_WriteError(0x06);
//		return HAL_ERROR;
//	}
//
//	Protocol_WriteError(0x46);
//
//	return HAL_OK;
//}

