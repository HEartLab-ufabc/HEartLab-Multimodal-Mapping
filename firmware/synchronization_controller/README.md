# Synchronization Controller Firmware

Firmware for the Teensy 4.1 timing controller used by the experimental platform.

The controller provides hardware timing signals used to synchronize acquisition devices and experimental events.

## Purpose

Optical cameras and electrical acquisition systems operate independently and may use different sampling frequencies and internal clocks.

The synchronization controller provides a shared hardware timing reference so that recordings can subsequently be aligned.

## Hardware

Current implementation:

- Teensy 4.1;
- TTL-compatible trigger outputs;

## Function

Depending on the experimental configuration, the controller can provide timing or trigger signals to:

- optical cameras;
- electrical acquisition systems;
- stimulation interfaces;
- auxiliary recording equipment.

## Important

Before connecting an external acquisition device, verify its trigger-input specifications.

Do not assume that all equipment accepts the same voltage levels, polarity or pulse duration.

Where galvanic isolation is required, an appropriate isolated interface should be used.

## Related documentation

Hardware connections are documented in:

[`../../hardware/synchronization/`](../../hardware/synchronization/)
