# Hardware Bill of Materials — Overview

This document provides a high-level overview of the hardware used across the multimodal mapping platform.

It is not intended to replace the subsystem-specific BOMs. Quantities vary according to experimental configuration.

## Perfusion and fluidics

| Item | Representative implementation | Notes |
|---|---|---|
| Peristaltic pump | Laboratory pump | STEP/DIR-compatible implementation |
| Main/bulk perfusate reservoir | Laboratory/custom reservoir | Capacity depends on preparation |
| Perfusion/head reservoir | Laboratory/custom reservoir | Used where hydrostatic pressure control is required |
| Serpentine heat exchanger | Custom/laboratory fabricated | CAD support is provided separately |
| Bubble trap | Inline | Inline bubble-management component |
| Analog flow meter | Inline | Used for visual flow verification |
| Digital flow/temperature sensor | Sensirion SLF3S-4000B | Current sensor firmware identifies this device |
| Digital pressure sensor | Honeywell digital pressure sensor | Honeywell digital pressure-sensor implementation |
| Tubing | Laboratory perfusion tubing | Medical/laboratory perfusion tubing; dimensions depend on interface |
| Valves / stopcocks / Luer fittings | Commercial | Configuration dependent |
| Small-heart aortic cannula | Custom | CAD/drawings provided in `cad/` |
| Large-heart coronary cannulation interfaces | Custom/commercial combination | Preparation-specific interface |
| Epi-endo coronary cannulation interface | Custom/commercial combination | Preparation-specific interface |

## Physiological monitoring electronics

| Item | Representative implementation | Notes |
|---|---|---|
| Sensor-node MCU | Arduino Nano | One node per instrumented perfusion line in the current implementation |
| Wireless module | nRF24L01 | One per sensor node |
| Flow/temperature sensor | Sensirion SLF3S-4000B | I²C |
| Pressure sensor | Honeywell digital sensor | Model-specific implementation |
| Tank temperature probe | K-type thermocouple implementation | K-type thermocouple interface |
| Gateway MCU | ESP32-S3 development board | One gateway |
| Gateway radio | nRF24L01 | Receives sensor-node packets |
| USB connection | ESP32-S3 to experiment computer | Serial data path |

## Optical mapping

| Item | Representative implementation | Notes |
|---|---|---|
| Optical mapping cameras | High-speed cameras | High-speed optical-mapping implementation |
| Camera count | 3 small-heart; 2 large-heart/epi-endo representative implementations | Experiment dependent |
| Lens | 25 mm | 25 mm optical-mapping implementation |
| Excitation LEDs | ~650 nm | Six LEDs used in the representative small-heart arrangement |
| Emission filter | ~715 nm long-pass | Long-pass optical filter |
| Mirror | ~45° epi-endo optical view | Holder CAD provided under `cad/epi-endo/` |
| Camera/LED mounts | Commercial/custom | Commercial/custom mounting |

## Electrical mapping

| Item | Representative implementation | Notes |
|---|---|---|
| Electrical acquisition | Intan RHD / Open Ephys implementation | Configuration-dependent channel count |
| Small-heart MEAs | Three 16-electrode arrays | RA, LA, ventricular placement |
| Small-heart torso-tank electrodes | 60 electrodes | 10 electrodes per face in the representative hexagonal tank |
| Large-heart tank PCB | 15 electrodes per PCB | Six PCBs used around the representative tank |
| Epi-endo MEAs | Paired epicardial/endocardial arrays | Preparation-specific geometry |
| Reference/ground interfaces | Configuration dependent | Reference arrangement depends on mapping modality |

## Electrical stimulation

| Item | Representative implementation | Notes |
|---|---|---|
| Constant-current stimulator | Single-channel PNP current-mirror implementation | Paper-associated validated implementation |
| Compliance supply | Four 9 V batteries in series | Approximately 42 V practical compliance reported for the implementation |
| Output range | ~100 µA to 45 mA | Validated current-mirror implementation |
| Trigger isolation | Isolated trigger interface | Isolated trigger interface |
| Stimulation catheter/electrodes | Bipolar | Experiment dependent |

## Synchronization

| Item | Representative implementation | Notes |
|---|---|---|
| Timing controller | Teensy 4.1 | Current synchronization firmware |
| Timing output | TTL-level timing signal | 500 Hz representative synchronization signal |
| Optical camera trigger interface | Digital timing connection | Camera-specific trigger interface |
| Electrical acquisition timing input | Open Ephys digital input | Representative implementation |

## 3D reconstruction acquisition

| Item | Representative implementation | Notes |
|---|---|---|
| Stepper motor | NEMA 14 | Used for controlled preparation rotation |
| Stepper driver | STEP/DIR-compatible driver | STEP/DIR-compatible implementation |
| Motor controller | Arduino-compatible controller | Firmware provided under `firmware/stepper_motor_control/` |
| Microstepping | 16× representative configuration | Must match driver jumpers/settings |
| Rotational mechanical assembly | Configuration-specific | CAD provided under `cad/` |
| Reconstruction camera option 1 | EVT camera | LabVIEW acquisition software |
| Reconstruction camera option 2 | Imaging Source USB camera | Python/OpenCV acquisition software |
| Calibration object | ChArUco-based calibration object | Calibration performed using MC-Calib |
