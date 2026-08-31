#include "pins_arduino.h"
#include "nrf24_control.h"
#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>

#define CE_PIN 18
#define CSN_PIN 5
#define MOSI_PIN 14
#define MISO_PIN 13
#define SCK_PIN 12

RF24 radio(CE_PIN, CSN_PIN);
const byte nodeAddresses[6][6] = {"NODE1", "NODE2", "NODE3", "NODE4", "NODE5", "NODE6"};

void setupNRF24() {
    SPI.begin(SCK_PIN, MISO_PIN, MOSI_PIN, -1);
    if (!radio.begin()) {
        Serial.println("NRF24L01 initialization failed!");
        while (1);
    }

    radio.setPALevel(RF24_PA_HIGH);
    radio.setDataRate(RF24_250KBPS);
    radio.openReadingPipe(0, nodeAddresses[0]);
    radio.openReadingPipe(1, nodeAddresses[1]);
    radio.openReadingPipe(2, nodeAddresses[2]);
    radio.openReadingPipe(3, nodeAddresses[3]);
    radio.openReadingPipe(4, nodeAddresses[4]);
    radio.startListening();

    Serial.println("NRF24L01 setup complete.");
    // radio.printDetails(); // Print debugging details
}

bool sendNRF24MessageToNode(uint8_t nodeIndex, const String &message) {
    if (nodeIndex < 1 || nodeIndex > 6) {
        Serial.println("Invalid node index (valid range: 1-6).");
        return false;
    }

    radio.stopListening();
    radio.openWritingPipe(nodeAddresses[nodeIndex - 1]);

    bool success = radio.write(message.c_str(), message.length());
    radio.startListening();

    if (success) {
        Serial.printf("Message sent to NODE%d: %s\n", nodeIndex, message.c_str());
    } else {
        Serial.printf("Failed to send message to NODE%d\n", nodeIndex);
    }

    return success;
}

void readSensorData() {
    if (radio.available()) {
        char incomingMessage[32] = {0}; // Buffer for the received message
        radio.read(&incomingMessage, sizeof(incomingMessage)); // Read the message        

        // Check if the message starts with "SN1"
        if (strncmp(incomingMessage, "SN1", 3) == 0) {
            // Print the raw message
            Serial.print("Received: ");
            Serial.println(incomingMessage);

        } else if (strncmp(incomingMessage, "SN2", 3) == 0){
            // Print the raw message
            Serial.print("Received: ");
            Serial.println(incomingMessage);
        
        }else {
            Serial.println("Unknown message received:");
            Serial.println(incomingMessage);
        }
    }
}
