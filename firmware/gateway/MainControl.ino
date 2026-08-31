#include <Arduino.h>
#include "foward_teensy.h"
#include "commands.h"
#include "nrf24_control.h"

void setup() {
    setupSerialCommands();
    // setupUART();
    // setupNRF24(); // Initialize NRF24L01

    Serial.println("ESP Started. Receiving Commands.");
}

void loop() {
    processSerialCommand();    
    readSensorData();
    ForwardToComputer();
}