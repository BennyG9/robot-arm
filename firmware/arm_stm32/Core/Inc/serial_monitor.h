/*
 * serial_monitor.h
 *
 *  Created on: Jun 23, 2026
 *      Author: benny
 */

#ifndef INC_SERIAL_MONITOR_H_
#define INC_SERIAL_MONITOR_H_

#include "main.h"
#include <stdlib.h>

typedef struct SerialMonitorEntry{

	uint8_t byte;

	struct SerialMonitorEntry* next;

} SerialMonitorEntry;

typedef struct{

	SerialMonitorEntry* head;

	SerialMonitorEntry* tail;

} SerialMonitor;

void SerialMonitor_Init(void);

void SerialMonitor_Append(uint8_t byte);

HAL_StatusTypeDef SerialMonitor_ReadByte(uint8_t* byte);


#endif /* INC_SERIAL_MONITOR_H_ */
