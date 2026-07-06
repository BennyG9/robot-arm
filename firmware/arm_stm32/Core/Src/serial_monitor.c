/*
 * serial_monitor.c
 *
 *  Created on: Jun 23, 2026
 *      Author: benny
 */

#include "serial_monitor.h"

//static SerialMonitor serial_monitor;

volatile uint8_t buffer[BUFFER_SIZE];
volatile uint16_t head;
volatile uint16_t tail;

void SerialMonitor_Init(void){
//	serial_monitor.head = NULL;
//	serial_monitor.tail = NULL;
//	serial_monitor.length = 0;
	head = 0;
	tail = 0;
}


void SerialMonitor_Append(uint8_t byte){
//	SerialMonitorEntry* new_entry = (SerialMonitorEntry*)malloc(sizeof(SerialMonitorEntry));
//	if(new_entry == NULL) return;
//
//	new_entry->byte = byte;
//	new_entry->next = NULL;
//
//	if(serial_monitor.head == NULL){
//		serial_monitor.head = new_entry;
//		serial_monitor.tail = new_entry;
//	}else{
//		serial_monitor.tail->next = new_entry;
//		serial_monitor.tail = new_entry;
//	}
//
//	serial_monitor.length++;
	uint16_t next = (tail + 1) % BUFFER_SIZE;
	if(next == head){
		return;
	}
	buffer[tail] = byte;
	tail = next;
}


//SerialMonitorEntry* SerialMonitor_Pop(void){
//	if(serial_monitor.head == NULL){
//		return NULL;
//	}else if(serial_monitor.head == serial_monitor.tail){
//		SerialMonitorEntry* entry = serial_monitor.head;
//		serial_monitor.head = NULL;
//		serial_monitor.tail = NULL;
//		serial_monitor.length--;
//		return entry;
//	}else{
//		SerialMonitorEntry* entry = serial_monitor.head;
//		serial_monitor.head = entry->next;
//		serial_monitor.length--;
//		return entry;
//	}
//}

HAL_StatusTypeDef SerialMonitor_ReadByte(uint8_t* byte){
//	SerialMonitorEntry* entry = SerialMonitor_Pop();
//	if(entry == NULL){
//		return HAL_ERROR;
//	}else{
//		*byte = entry->byte;
//		free(entry);
//		return HAL_OK;
//	}
	if(SerialMonitor_Available() > 0){
		*byte = buffer[head];
		head = (head + 1) % BUFFER_SIZE;
		return HAL_OK;
	}else{
		return HAL_ERROR;
	}
}


HAL_StatusTypeDef SerialMonitor_ReadBytes(uint8_t* bytes, uint16_t length){
//	if(serial_monitor.length < length) return HAL_ERROR;
//
//	SerialMonitorEntry* entry;
//	for(int i = 0; i < length; i++){
//		entry = SerialMonitor_Pop();
//
//		if(entry == NULL) return HAL_ERROR;
//
//		bytes[i] = entry->byte;
//		free(entry);
//	}
//
//	return HAL_OK;
	if(SerialMonitor_Available() < length) return HAL_ERROR;

	uint8_t byte;
	for(int i = 0; i < length; i++){
		if(SerialMonitor_ReadByte(&byte) == HAL_ERROR) return HAL_ERROR;

		bytes[i] = byte;
	}

	return HAL_OK;
}


uint16_t SerialMonitor_Available(void){
//	return serial_monitor.length;
	if(tail >=  head) return tail - head;
	else return BUFFER_SIZE - (head - tail);
}








