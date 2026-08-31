# An Open-Source Platform for Multimodal Electrical and Optical Mapping of Ex Vivo Hearts

This repository contains hardware documentation, embedded firmware, experimental-control software, electronic schematics, and mechanical design files associated with the HEartLab experimental platform for synchronized multimodal electrophysiological mapping of ex vivo perfused hearts.

The platform was developed to integrate complementary measurements of cardiac electrical activity within a common experimental workflow, including optical mapping, contact electrical mapping, torso-tank recordings, pacing and arrhythmia induction, physiological monitoring, hardware synchronization, and structured experimental logging.

The system is designed as a modular platform rather than as a preparation-specific apparatus. Components such as the perfusion interfaces, recording chambers, electrode arrays, optical geometry, and mechanical supports can be adapted according to the preparation while preserving the same general experimental architecture.

## Experimental configurations

The platform has been implemented in three main configurations:

### Small-heart whole-organ configuration

Designed for Langendorff-perfused rabbit hearts and supporting:

- panoramic optical mapping using three camera views;
- epicardial contact mapping using multi-electrode arrays (MEAs);
- torso-tank electrical recordings;
- programmable electrical stimulation;
- physiological monitoring of perfusion conditions;
- synchronized optical and electrical acquisition;
- experiment metadata and event logging.

### Large-heart whole-organ configuration

Designed for intact porcine and human ex vivo hearts and supporting:

- optical mapping of large cardiac surfaces;
- electrical recordings from electrodes integrated into the surrounding tank;
- independent coronary perfusion;
- physiological monitoring;
- synchronized acquisition and stimulation;
- mechanical support adapted to larger preparations.

### Large-heart epi-endo configuration

Designed for isolated perfused ventricular-wall preparations and supporting:

- simultaneous optical mapping of epicardial and endocardial surfaces;
- simultaneous contact-electrical recordings from opposing surfaces;
- paired epicardial and endocardial MEAs;
- mirror-assisted optical access;
- synchronized stimulation and acquisition.

## Repository structure

```text
hardware/       Electronic and experimental hardware documentation
firmware/       Embedded firmware for sensors, communication and synchronization
software/       Experimental-control software
cad/            CAD, STL and mechanical design files
docs/           Additional platform documentation
