# An Open-Source Platform for Multimodal Electrical and Optical Mapping of Ex Vivo Hearts

**A modular research platform for synchronized optical, contact-electrical, and torso-tank mapping of ex vivo perfused hearts.**

> **Repository status:** Active development. Documentation, design files, protocols, and software are being prepared for the first archived release accompanying the associated *Scientific Reports* manuscript.

## Overview

This repository contains the hardware documentation, embedded firmware, experimental-control software, CAD files, representative experimental protocols, and 3D reconstruction tools associated with the HEartLab multimodal mapping platform for ex vivo cardiac electrophysiology.

The platform integrates complementary experimental modalities within a common workflow:

- optical mapping;
- contact electrical mapping using multi-electrode arrays (MEAs);
- torso-tank electrical mapping;
- electrical stimulation;
- physiological monitoring;
- hardware synchronization;
- experiment control and event logging;
- rotational image acquisition and experiment-specific 3D reconstruction.

The system is modular rather than tied to one preparation. Perfusion interfaces, mechanical supports, electrode arrangements, optical geometry, and selected experimental procedures can be adapted according to preparation size, scientific objective, and available equipment.

---

## Experimental configurations

### Small-heart whole-organ configuration

Validated in Langendorff-perfused rabbit hearts. Depending on the experiment, the configuration supports:

- panoramic optical mapping;
- epicardial contact mapping using MEAs;
- torso-tank electrical recordings;
- programmable electrical stimulation;
- physiological monitoring;
- synchronized optical and electrical acquisition;
- experiment control and logging;
- experiment-specific 3D reconstruction.

### Large-heart whole-organ configuration

Validated in porcine and human ex vivo hearts. Depending on the experiment, the configuration supports:

- optical mapping of large cardiac surfaces;
- torso-tank electrical mapping;
- independent coronary perfusion;
- physiological monitoring;
- synchronized acquisition and stimulation;
- mechanical support adapted to larger preparations;
- experiment-specific 3D reconstruction.

### Large-heart epi-endo configuration

Developed for isolated perfused ventricular-wall preparations. Depending on the experiment, the configuration supports:

- simultaneous epicardial and endocardial optical mapping;
- paired epicardial and endocardial contact-electrical mapping;
- mirror-assisted optical access;
- coronary perfusion;
- synchronized stimulation and acquisition;
- physiological monitoring.

The configuration defines the available platform modules, while the **scientific objective determines which modules and protocols are used in a particular experiment**.

---

## Platform modules

HEartLab is organized around interoperable experimental modules:

- **Perfusion** – maintains the isolated preparation under controlled ex vivo conditions.
- **Physiological monitoring** – records perfusion flow, pressure, and temperature.
- **Optical mapping** – records voltage-sensitive fluorescence from cardiac surfaces.
- **Contact electrical mapping** – records local extracellular electrograms using MEAs.
- **Torso-tank mapping** – records cardiac potentials from electrodes surrounding the preparation in a conductive volume.
- **Electrical stimulation** – provides controlled pacing and arrhythmia-induction stimuli.
- **Hardware synchronization** – provides a common timing reference between acquisition systems.
- **Experiment control** – coordinates monitoring, stimulation, synchronization, metadata, and experimental events.
- **3D reconstruction** – combines rotational image acquisition with silhouette-based processing to obtain experiment-specific surface geometry.

---

## Repository structure

```text
HEartLab-Multimodal-Mapping/
├── README.md
├── DISCLAIMER.md
│
├── cad/
│   ├── README.md
│   ├── small_heart/
│   ├── large-heart/
│   └── epi-endo/
│
├── docs/
│   ├── getting_started.md
│   └── protocols/
│
├── firmware/
│   ├── sensors/
│   ├── gateway/
│   ├── stepper_motor_control/
│   └── synchronization_controller/
│
├── hardware/
│   ├── README.md
│   ├── BOM_overview.md
│   ├── perfusion/
│   ├── physiological_monitoring/
│   ├── optical_mapping/
│   ├── electrical_mapping/
│   ├── stimulation/
│   ├── synchronization/
│   ├── mechanical/
│   └── reconstruction_3d/
│
└── software/
    ├── README.md
    ├── experiment_control/
    ├── 3D_reconstruction_capture_labview/
    ├── 3D_reconstruction_capture_python/
    └── 3d_reconstruction_processing/
```

---

## Getting started

A high-level setup and validation workflow is provided in:

**[`docs/getting_started.md`](docs/getting_started.md)**

A typical workflow is:

1. select the experimental configuration;
2. define the scientific objective;
3. select the required platform modules and representative protocols;
4. obtain or fabricate the required hardware;
5. configure firmware and software;
6. validate each subsystem independently;
7. perform an integrated bench test;
8. document the experiment-specific configuration.

The platform does **not** require every subsystem to be used in every experiment.

---

## Experimental protocols

Representative experimental procedures are provided in:

**[`docs/protocols/`](docs/protocols/)**

These documents describe examples of HEartLab implementations rather than universal mandatory procedures. Parameters can vary according to preparation type, species or donor source, heart size, mapping modality, scientific objective, equipment, pharmacological intervention, stimulation protocol, and the applicable approved experimental protocol.

Users are responsible for confirming that concentrations, calculations, settings, and procedures are appropriate for their own experimental implementation.

---

## CAD and mechanical designs

Custom mechanical designs are provided in:

**[`cad/`](cad/)**

The CAD library is organized according to the configuration in which the components were developed:

- [`cad/small_heart/`](cad/small_heart/)
- [`cad/large-heart/`](cad/large-heart/)
- [`cad/epi-endo/`](cad/epi-endo/)

Depending on the component, files include Autodesk Inventor (`.ipt`), Autodesk Fusion (`.f3d` / `.f3z`), STEP/STP, STL, and PDF drawings.

The repository focuses on custom fabricated components. Commercial motors, bearings, pulleys, shafts, fasteners, clamps, and similar off-the-shelf parts are described in the relevant documentation rather than redistributed as proprietary CAD models.

---

## Hardware

Hardware documentation is located in:

**[`hardware/`](hardware/)**

Subsystem documentation includes:

- [`hardware/perfusion/`](hardware/perfusion/) – perfusion and fluidic hardware;
- [`hardware/physiological_monitoring/`](hardware/physiological_monitoring/) – flow, pressure, temperature, sensor nodes, and gateway hardware;
- [`hardware/optical_mapping/`](hardware/optical_mapping/) – cameras, optics, illumination, and mirror-assisted optical access;
- [`hardware/electrical_mapping/`](hardware/electrical_mapping/) – MEAs, small-heart torso-tank hardware, and large-heart tank PCB files;
- [`hardware/stimulation/`](hardware/stimulation/) – experimental constant-current stimulation hardware;
- [`hardware/synchronization/`](hardware/synchronization/) – timing and trigger-distribution hardware;
- [`hardware/mechanical/`](hardware/mechanical/) – assembly-level mechanical documentation linked to the CAD library;
- [`hardware/reconstruction_3d/`](hardware/reconstruction_3d/) – motorized rotational acquisition hardware.

A high-level component inventory is provided in [`hardware/BOM_overview.md`](hardware/BOM_overview.md).

### Large-heart tank PCB

Editable KiCad source, electrode mapping, Gerber/drill outputs, and manufacturing previews are provided under:

**[`hardware/electrical_mapping/large-heart-tank-pcb/`](hardware/electrical_mapping/large-heart-tank-pcb/)**

The large-heart tank uses six PCB faces with 15 electrode pads per face.

---

## Firmware

Embedded firmware is located in:

**[`firmware/`](firmware/)**

The current implementation includes:

- Arduino Nano-based physiological-monitoring sensor nodes;
- nRF24L01 wireless communication;
- an ESP32-S3 sensor gateway;
- a Teensy 4.1 synchronization/stimulation-control interface;
- an Arduino-controlled stepper system for rotational 3D image acquisition.

Subsystem-specific README files describe the associated interfaces and operating assumptions.

---

## Software

Software is located in:

**[`software/`](software/)**

### Experiment control

[`software/experiment_control/`](software/experiment_control/) contains the Python-based application used for experimental session organization, physiological monitoring, stimulation control, synchronization-related operations, metadata, and event logging.

### 3D image acquisition — LabVIEW / EVT

[`software/3D_reconstruction_capture_labview/`](software/3D_reconstruction_capture_labview/) contains the LabVIEW application used with the EVT camera implementation.

The acquisition workflow rotates the preparation at defined angular increments and stores the image sequence used for subsequent 3D reconstruction.

A RHYTHM-derived LabVIEW VI included in this folder retains its original third-party attribution and MIT license notice.

### 3D image acquisition — Python / Imaging Source USB

[`software/3D_reconstruction_capture_python/`](software/3D_reconstruction_capture_python/) contains the Python/OpenCV implementation used with the Imaging Source USB-camera setup.

### 3D reconstruction processing

[`software/3d_reconstruction_processing/`](software/3d_reconstruction_processing/) contains the silhouette-processing and space-carving workflow used to produce experiment-specific surface meshes.

Camera calibration is performed using [MC-Calib](https://github.com/rameau-fr/MC-Calib); its calibration procedure is not duplicated in this repository.

---

## Reproducibility and scope

The repository documents the implementation used to develop and validate the HEartLab platform. Because the platform is modular, exact equipment combinations and experimental procedures can differ among preparations.

For reproducibility, experimental records should preserve the relevant hardware configuration, firmware/software versions, acquisition settings, channel mapping, and protocol parameters used for a given dataset.

Commercial acquisition software, manufacturer drivers, SDKs, and proprietary third-party design files are not redistributed unless their licenses permit redistribution.


---

## Associated manuscript

This repository accompanies:

**Silva, V. P. et al. _An Open-Source Platform for Multimodal Electrical and Optical Mapping of Ex Vivo Hearts_.**

**Status:** manuscript under review.

---

## Third-party components

Third-party software remains subject to its original license terms.

In particular, the LabVIEW reconstruction-acquisition folder contains a VI derived from the RHYTHM open-source imaging toolkit. Attribution and the applicable MIT license notice are provided in:

[`software/3D_reconstruction_capture_labview/THIRD_PARTY.md`](software/3D_reconstruction_capture_labview/THIRD_PARTY.md)

---

## Contact

For technical questions or reproducibility issues, please open a GitHub issue.

For research collaboration or questions regarding the associated manuscript, contact HEartLab at Universidade Federal do ABC (UFABC).

---

## Disclaimer

The hardware designs, firmware, software, protocols, CAD files, and documentation provided in this repository are supplied **"as is"**, without warranties or guarantees of any kind, either express or implied.

The materials are intended exclusively for experimental research involving ex vivo cardiac preparations. They have not been designed, validated, or approved as medical devices and must not be used for clinical diagnosis, treatment, patient monitoring, or direct use in humans.

Users are responsible for independently reviewing and validating hardware, software, calculations, procedures, electrical connections, experimental parameters, concentrations, and safety measures before use.

The individual researcher or institution conducting an experiment remains responsible for determining whether the platform and associated procedures are appropriate for the intended application and for ensuring compliance with applicable ethical approvals, institutional requirements, laboratory procedures, and safety regulations.

See the complete [`DISCLAIMER.md`](DISCLAIMER.md).
