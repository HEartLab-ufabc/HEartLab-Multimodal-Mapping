#ifndef TEMP_SENSOR_H
#define TEMP_SENSOR_H

#include <Arduino.h>

// Inicializa o sensor MAX6675
bool setupTempSensor();

// Lê a temperatura em °C
float readTempK();

#endif