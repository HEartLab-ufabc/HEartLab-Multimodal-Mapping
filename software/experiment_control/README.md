# Experimental-Control Software

This directory contains the graphical user interface developed to coordinate operation of the multimodal ex vivo cardiac mapping platform.

The application was developed to reduce the need to operate stimulation, physiological monitoring, acquisition coordination and experimental logging as completely independent tasks.

## Main functions

The software supports:

- creation and organization of experimental sessions;
- experiment metadata entry;
- recording start/stop coordination;
- stimulation control;
- pacing and arrhythmia-induction protocols;
- real-time visualization of physiological measurements;
- recording of experimental events;
- structured experiment logging.

## Experimental workflow

A typical workflow is:

```text
Create / select experiment
          ↓
Enter experiment metadata
          ↓
Connect monitoring hardware
          ↓
Verify physiological conditions
          ↓
Configure stimulation protocol
          ↓
Start synchronized recording
          ↓
Apply stimulation / interventions
          ↓
Record events and annotations
          ↓
Stop recording
          ↓
Store experiment log
