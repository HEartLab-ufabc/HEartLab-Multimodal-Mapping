
# Sensor Node Firmware

Firmware for the Arduino Nano-based physiological monitoring nodes.

Each node is associated with one active perfusion line and is responsible for acquiring local sensor measurements and transmitting them to the gateway.

## Hardware

The current implementation uses:

- Arduino Nano;
- Sensirion SLF3S-4000B flow/temperature sensor;
- Honeywell HSCMRNV160MG2A3 pressure sensor;
- nRF24L01 radio module.

Additional sensors can be incorporated if required by the experimental configuration.

## Function

The firmware performs the following general sequence:

1. initialize the connected sensors;
2. initialize wireless communication;
3. acquire sensor measurements;
4. package the measurements with the node identifier;
5. transmit the data to the gateway;
6. repeat continuously during the experiment.

## Multiple perfusion lines

Each perfusion line uses an independent node.

Node identifiers must therefore be configured so that measurements received by the gateway can be associated with the correct perfusion line.

## Configuration

Before uploading the firmware, verify:

- node identifier;
- sensor addresses;
- nRF24L01 communication settings;
- required pin assignments;
- communication rate.

Configuration constants are defined in the source files.

## Gateway

Data transmitted by this firmware are received by the ESP32-S3 gateway.

See:

[`../sensor_gateway/`](../sensor_gateway/)

## Adaptation

Other microcontrollers can be used in place of the Arduino Nano, but the acquisition and communication code will need to be adapted accordingly.

The provided implementation corresponds to the hardware used in the current platform.
