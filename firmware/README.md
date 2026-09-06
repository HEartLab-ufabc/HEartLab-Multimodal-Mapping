# Embedded Firmware

This directory contains firmware used by the embedded control, monitoring, synchronization, and motor-control subsystems of the HEartLab multimodal mapping platform.

## Directory structure

### `sensors/`

Firmware for Arduino Nano-based physiological-monitoring nodes.

### `gateway/`

Firmware for the ESP32-S3 gateway that receives physiological-monitoring data and interfaces with the experimental-control computer.

### `synchronization_controller/`

Firmware for the Teensy 4.1 timing controller used to generate and distribute experimental synchronization signals.

### `stepper_motor_control/`

Arduino firmware for the motorized rotational stage used during experiment-specific 3D reconstruction image acquisition.

The controller receives angular movement commands through the serial interface and drives a STEP/DIR stepper-motor driver.

A representative reconstruction acquisition uses approximately 100 positions over 360°, corresponding to 3.6° increments.

See:

[`stepper_motor_control/README.md`](stepper_motor_control/README.md)

## Monitoring and synchronization architecture

```text
Sensor node 1 --\
                 \
Sensor node 2 ----> wireless --> ESP32-S3 gateway --> USB --> Experiment computer
                 /
Additional ------/
nodes

Experiment computer --> timing/synchronization controller --> acquisition systems
```

Refer to the subsystem-specific README files for exact interfaces.

## Rotational image-acquisition architecture

```text
Image-acquisition software
        |
        | Serial/USB
        v
     Arduino
        |
    STEP / DIR
        v
 Stepper driver
        |
        v
 Stepper motor
        |
        v
Rotational support
```

The current LabVIEW image-acquisition implementation is designed for EVT cameras:

[`../software/3D_reconstruction_capture_labview/`](../software/3D_reconstruction_capture_labview/)

The Python/OpenCV acquisition implementation for the Imaging Source USB-camera setup is available at:

[`../software/3D_reconstruction_capture_python/`](../software/3D_reconstruction_capture_python/)

## Development environment

Controller, library, pin-assignment, communication, and upload information is provided in the subsystem-specific README files together with the corresponding source code.


## Disclaimer

Firmware in this repository is provided for experimental research and must be independently verified with the intended electronics and mechanical system before experimental use.

See the repository-level [`DISCLAIMER.md`](../DISCLAIMER.md).
