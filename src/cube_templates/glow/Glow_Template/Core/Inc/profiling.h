#ifndef _PROFILING_H
#define _PROFILING_H

#include "stm32l4xx.h"
//#include "stm32f1xx_hal.h"
#include <stdint.h>
#include <stdio.h>

#define MAX_EVENT_COUNT 50

void PROFILING_START(const char *profile_name);
void PROFILING_EVENT(const char *event);
void PROFILING_STOP(UART_HandleTypeDef *huart2);

#endif // _PROFILING_H
