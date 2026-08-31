# Embedded Firmware

This directory contains firmware used by the embedded control, monitoring and synchronization subsystems of the experimental platform.

The firmware is separated according to hardware function.

## Directory structure

### `sensor_node/`

Firmware for the Arduino Nano nodes associated with individual perfusion lines.

The nodes acquire local sensor measurements and transmit them wirelessly to the gateway.

### `sensor_gateway/`

Firmware for the ESP32-S3 gateway.

The gateway receives measurements from the wireless sensor nodes and forwards them to the experimental-control computer.

### `synchronization_controller/`

Firmware for the Teensy 4.1 timing controller used to generate and distribute experimental synchronization signals.

## Architecture

```text
                         ┌──────────────────────┐
                         │ Experiment computer  │
                         │        + GUI         │
                         └──────────┬───────────┘
                                    │
                      ┌─────────────┴─────────────┐
                      │                           │
                    USB                         USB
                      │                           │
               ┌──────▼──────┐            ┌──────▼──────┐
               │  ESP32-S3   │            │ Teensy 4.1  │
               │   gateway   │            │ timing ctrl │
               └──────▲──────┘            └─────────────┘
                      │
                   nRF24L01
                ┌─────┴─────┐
                │           │
          ┌─────▼────┐ ┌────▼─────┐
          │ Sensor   │ │ Sensor   │
          │ node 1   │ │ node 2   │
          └──────────┘ └──────────┘
