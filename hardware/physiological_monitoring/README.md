# Physiological Monitoring Hardware

This subsystem monitors perfusion conditions and forwards them to the experiment-control computer.

The current implementation uses independent sensor nodes for active perfusion lines and a central ESP32-S3 gateway.

## Architecture

```text
Perfusion line
    │
    ├── flow + inline temperature sensor
    ├── pressure sensor
    └── optional/local temperature measurement
             │
             ▼
        Arduino Nano
             │
          nRF24L01
             │
             ▼
       ESP32-S3 gateway
             │
            USB
             │
             ▼
   Experiment-control computer
```

## Sensor node

The current sensor-node implementation uses:

- Arduino Nano;
- Sensirion SLF3S-4000B flow/temperature sensor;
- Honeywell digital pressure sensor;
- nRF24L01 wireless transceiver.

One sensor node can be associated with each instrumented perfusion line.

The corresponding firmware is available at:

[`../../firmware/sensors/`](../../firmware/sensors/)

## Gateway

The gateway implementation uses:

- ESP32-S3 development board;
- nRF24L01 wireless transceiver;
- USB serial connection to the experiment computer.

Firmware:

[`../../firmware/gateway/`](../../firmware/gateway/)

## Flow sensor

The current firmware identifies the flow sensor as:

**Sensirion SLF3S-4000B**

The implementation also reads the fluid-temperature value reported by the flow sensor.

## Additional temperature monitoring

HEartLab experiments have also used a tank/chamber temperature measurement based on a K-type thermocouple implementation.

Tank/chamber temperature is measured with a K-type thermocouple implementation using a MAX31855 interface module.

## Adaptation

The Arduino Nano is not a fundamental requirement of the platform.

Other microcontrollers can be used if they provide compatible sensor interfaces and preserve the required data path to the experiment-control software.


See [`BOM.md`](BOM.md).
