#ifndef NRF24_CONTROL_H
#define NRF24_CONTROL_H

#include <Arduino.h>

// Initializes the NRF24L01 module
void setupNRF24();

// Sends data via NRF24L01
bool sendNRF24MessageToNode(uint8_t arduinoIndex, const String &message);

// Checks for and processes received messages
// void checkNRF24Messages();

// Reads sensor data from NRF24L01
void readSensorData();

#endif // NRF24_CONTROL_H
