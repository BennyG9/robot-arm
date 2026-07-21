#include "protocol_data.h"

uint16_t Protocol_GetPacketLength(uint8_t cmd_id){
	switch((CommandID)cmd_id){
		case JOINT_STATE:
			return 15;
		case SET_POSITION:
			return 15;
		case CALIBRATE:
			return 3;
		case HOME:
			return 3;
		case SET_PID:
			return 16;
		case ESTOP:
			return 3;
		case ERROR_MSG:
			return 4;
	}
	return 0;
}

HAL_StatusTypeDef Protocol_GetArgumentTypes(uint8_t cmd_id, Type* type_list){
	switch((CommandID)cmd_id){
		case JOINT_STATE:
			type_list[0] = FLOAT;
			type_list[1] = FLOAT;
			type_list[2] = FLOAT;
			return HAL_OK;
		case SET_POSITION:
			type_list[0] = FLOAT;
			type_list[1] = FLOAT;
			type_list[2] = FLOAT;
			return HAL_OK;
		case CALIBRATE:
			type_list[0] = NONE;
			return HAL_OK;
		case HOME:
			type_list[0] = NONE;
			return HAL_OK;
		case SET_PID:
			type_list[0] = UINT8_T;
			type_list[1] = FLOAT;
			type_list[2] = FLOAT;
			type_list[3] = FLOAT;
			return HAL_OK;
		case ESTOP:
			type_list[0] = NONE;
			return HAL_OK;
		case ERROR_MSG:
			type_list[0] = UINT8_T;
			return HAL_OK;
	}
	return HAL_ERROR;
}

uint16_t Protocol_GetNumArguments(uint8_t cmd_id){
	switch((CommandID)cmd_id){
		case JOINT_STATE:
			return 3;
		case SET_POSITION:
			return 3;
		case CALIBRATE:
			return 0;
		case HOME:
			return 0;
		case SET_PID:
			return 4;
		case ESTOP:
			return 0;
		case ERROR_MSG:
			return 1;
	}
	return 0;
}

