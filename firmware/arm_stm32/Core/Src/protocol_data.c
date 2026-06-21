#include "protocol_data.h"

uint16_t Protocol_GetPacketLength(uint8_t cmd_id){
	switch(cmd_id){
		case JOINT_STATE:
			return 19;

		case SET_POSITION:
			return 19;

		case CALIBRATE:
			return 3;

		case HOME:
			return 3;

		case SET_PID:
			return 16;

		case ESTOP:
			return 3;

		case ERROR:
			return 4;

	}
	return 0;
}

