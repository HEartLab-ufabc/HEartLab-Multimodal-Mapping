# Synchronization Hardware

This subsystem provides a common timing reference between otherwise independent acquisition systems.

## Current implementation

The current synchronization-controller firmware is associated with a **Teensy 4.1** controller.

Firmware:

[`../../firmware/synchronization_controller/`](../../firmware/synchronization_controller/)

The implementation distributes a 500 Hz TTL-level timing signal to:

- optical camera timing/trigger interfaces;
- the digital input of the Open Ephys electrical acquisition system.

This shared timing signal allows optical and electrical recordings to be aligned during analysis.

## Architecture

```text
Experiment-control computer
            │
            ▼
    Teensy 4.1 controller
            │
       timing output
        ┌───┴───────────┐
        ▼               ▼
 Optical cameras   Open Ephys digital input
```

The experiment-control computer communicates with the timing controller using the serial command interface implemented in the synchronization firmware.

## Electrical interface

> [!CAUTION]
> Do not assume that every camera accepts the same trigger voltage or termination.

Before connecting synchronization hardware, verify:

- controller output voltage;
- camera trigger-input voltage limits;
- electrical acquisition digital-input limits;
- required polarity;
- grounding;
- cable termination;
- edge timing.


See [`BOM.md`](BOM.md).
