#include "Temp_sensor.h"
#include <SPI.h>

#define CS_MAX6675 2  // Pino CS do MAX6675

bool setupTempSensor() {
    SPI.begin();
    pinMode(CS_MAX6675, OUTPUT);
    digitalWrite(CS_MAX6675, HIGH); // desativa inicialmente

    Serial.println("Sensor MAX6675 inicializado.");
    return true;
}

float readTempK() {
    uint16_t v;

    digitalWrite(CS_MAX6675, LOW);
    delayMicroseconds(10);

    v = SPI.transfer(0x00) << 8;
    v |= SPI.transfer(0x00);

    digitalWrite(CS_MAX6675, HIGH);
    delayMicroseconds(10);

    if (v & 0x4) return NAN;        // erro na leitura
    return (v >> 3) * 0.25;         // conversão para °C
}
