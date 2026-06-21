#ifndef INC_PROTOCOL_DATA_H_
#define INC_PROTOCOL_DATA_H_

#include "main.h"

#define START_BYTE 0xAA
#define MAX_ARG_SIZE 16

typedef enum{
	JOINT_STATE = 1,
	SET_POSITION = 2,
	CALIBRATE = 3,
	HOME = 4,
	SET_PID = 5,
	ESTOP = 6,
	ERROR_MSG = 7,
} CommandID;

uint16_t Protocol_GetPacketLength(uint8_t cmd_id);

#endif