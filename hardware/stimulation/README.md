# Electrical Stimulation Hardware

This directory documents the stimulation hardware associated with the platform implementation described in the paper.

## Validated paper-associated implementation

The stimulator is a single-channel constant-current design based on a PNP current-mirror architecture.

Characteristics include:

- approximately 100 µA to 45 mA adjustable current range;
- four 9 V batteries in series as the isolated high-voltage supply;
- approximately 42 V practical compliance in the implementation;
- isolated trigger input;
- 2 ms pacing pulse duration.

The pulse duration and stimulation protocol are experiment parameters and are controlled through the corresponding stimulation/control software.

## Intended use

The stimulator is used for experimental procedures such as:

- capture testing;
- regular pacing;
- S1–S2 pacing;
- burst pacing;
- arrhythmia-induction protocols.

## Repository contents

This directory provides an architecture-level description and component summary of the experimentally validated single-channel current-mirror stimulator.

## Required verification

Before connection to a biological preparation:

- verify output current into representative loads;
- verify pulse duration;
- verify compliance behavior;
- verify startup/reset behavior;
- verify battery condition;

> [!WARNING]
> This stimulation hardware is intended exclusively for experimental ex vivo research. Verify output amplitude, timing, polarity, isolation, and startup behavior using appropriate test equipment and a representative load before connection to a biological preparation.

See [`BOM.md`](BOM.md) and the repository-level `DISCLAIMER.md`.
