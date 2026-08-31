# Sensor Gateway Firmware

Firmware for the ESP32-S3 gateway used by the physiological monitoring system.

The gateway provides the interface between the wireless sensor nodes and the experimental-control computer.

## Function

The gateway:

1. receives data from the nRF24L01 sensor network;
2. identifies the transmitting sensor node;
3. organizes the received measurements;
4. forwards the data to the experimental computer through USB serial communication.

## Hardware

Current implementation:

- ESP32-S3 development board;
- nRF24L01 radio module;
- USB connection to the experiment-control computer.

## Data path

```text
Sensor node 1 ──┐
                │
Sensor node 2 ──┼── nRF24L01 ──> ESP32-S3 ── USB ──> Experiment GUI
                │
Additional ─────┘
nodes
