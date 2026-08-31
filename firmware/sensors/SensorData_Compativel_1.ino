#include <SPI.h>
#include <Arduino.h>
#include <nRF24L01.h>
#include <RF24.h>
#include "PressureSensor.h"
#include "FlowSensor.h"

// ==== PINOS DO RÁDIO (Arduino) ====
#define CE_PIN 8
#define CSN_PIN 10

RF24 radio(CE_PIN, CSN_PIN);

// Endereço (Mantendo formato string que o ESP32 vai ler)
const uint8_t address[6] = "NODE2";

unsigned long lastSendTime = 0;
const int sendInterval = 200;
const int zero = 0;

void setup() {
  Serial.begin(115200);
  delay(500);  // Pequena pausa para estabilizar
  Serial.println("=== INICIANDO TRANSMISSOR (NODE2) ===");

  SPI.begin();

  // Sensores
  setupPressureSensor();
  setupFlowSensor();

  // Rádio
  if (!radio.begin()) {
    Serial.println("ERRO: Rádio não responde.");
    while (1)
      ;
  }

  // === CONFIGURAÇÕES VITAIS ==
  radio.setPALevel(RF24_PA_HIGH);
  radio.setDataRate(RF24_1MBPS);  // Usando 1MBPS pois funcionou no seu teste
  radio.setChannel(108);
  radio.enableDynamicPayloads();  // Importante para enviar strings
  radio.setAutoAck(true);         // Garante que a mensagem chegou
  radio.setRetries(5, 15);

  radio.openWritingPipe(address);  // Escreve para NODE2
  radio.stopListening();           // Modo transmissor
}

void loop() {
  unsigned long now = millis();

  // Envio periódico
  if (now - lastSendTime >= sendInterval) {
    lastSendTime = now;

    // 1. Leitura (Multiplicado por 100 para evitar float no envio)
    float pressure = readPressureMMHG();
    int pressureVal = (int)(pressure * 100);

    float flowRate, flowTemp;
    int flowVal = 0;
    int tempVal = 0;

    // Se a função readFlowSensor retornar true/false, ajuste aqui:
    readFlowSensor(flowRate, flowTemp);
    flowVal = (int)(flowRate * 100);
    tempVal = (int)(flowTemp * 100);

    // 2. Formatação da Mensagem
    char message[32] = { 0 };
    snprintf(message, sizeof(message), "SN1 %05d %04d %05d %04d",
             flowVal, tempVal, pressureVal, zero);

    Serial.print("Enviando: ");
    Serial.print(message);

    // 3. Envio
    if (radio.write(message, strlen(message))) {
      Serial.println(" [OK]");
    } else {
      Serial.println(" [FALHA - Sem ACK]");
    }
  }
}