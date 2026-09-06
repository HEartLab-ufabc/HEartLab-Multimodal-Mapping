# An Open-Source Platform for Multimodal Electrical and Optical Mapping of Ex Vivo Hearts

**A modular research platform for synchronized optical, contact-electrical, and torso-tank mapping of ex vivo perfused hearts.**

> **Repository status:** Active development. Documentation, design files, protocols, and software are being prepared for the first archived release accompanying the associated *Scientific Reports* manuscript.

## Overview

This repository contains hardware documentation, embedded firmware, experimental-control software, CAD files, experimental protocols, and supporting documentation associated with the HEartLab multimodal mapping platform for ex vivo cardiac electrophysiology.

The platform was developed to integrate complementary measurements of cardiac electrical activity within a common experimental workflow, including:

- optical mapping;
- contact electrical mapping using multi-electrode arrays (MEAs);
- torso-tank electrical mapping;
- electrical stimulation;
- physiological monitoring;
- hardware synchronization;
- experiment control and event logging;
- experiment-specific three-dimensional reconstruction.

The system is intentionally modular rather than preparation specific. Perfusion interfaces, mechanical supports, electrode arrangements, optical geometry, and other components can be adapted according to preparation size, experimental objective, and available equipment while preserving the same general acquisition and control architecture.

---

## Experimental configurations

The platform has been implemented in three principal configurations.

### Small-heart whole-organ configuration

Developed for Langendorff-perfused rabbit hearts and supporting, depending on the experiment:

- panoramic optical mapping using multiple camera views;
- epicardial contact mapping using MEAs;
- torso-tank electrical recordings;
- programmable electrical stimulation;
- physiological monitoring;
- synchronized optical and electrical acquisition;
- experiment metadata and event logging;
- experiment-specific 3D reconstruction.

### Large-heart whole-organ configuration

Developed for intact porcine and human ex vivo hearts and supporting, depending on the experiment:

- optical mapping of large cardiac surfaces;
- electrical recordings from electrodes integrated into the surrounding tank;
- independent coronary perfusion;
- physiological monitoring;
- synchronized acquisition and stimulation;
- mechanical support adapted to larger preparations;
- experiment-specific 3D reconstruction.

### Large-heart epi-endo configuration

Developed for isolated perfused ventricular-wall preparations and supporting, depending on the experiment:

- simultaneous optical mapping of epicardial and endocardial surfaces;
- simultaneous contact-electrical recordings from opposing surfaces;
- paired epicardial and endocardial MEAs;
- mirror-assisted optical access;
- synchronized stimulation and acquisition;
- physiological monitoring.

The configuration defines the available platform modules, while the **scientific objective determines which modules and protocols are used in a particular experiment**.

---

## Platform architecture

HEartLab is organized around interoperable experimental modules that can be combined according to preparation size and scientific objective:

- **Perfusion** – maintains the isolated cardiac preparation under controlled physiological conditions.
- **Physiological monitoring** – records perfusion pressure, flow, and temperature.
- **Optical mapping** – records voltage-sensitive fluorescence from cardiac surfaces.
- **Contact electrical mapping** – records extracellular electrograms using MEAs.
- **Torso-tank mapping** – records cardiac potentials from electrodes distributed around a conductive volume.
- **Electrical stimulation** – provides controlled pacing and arrhythmia-induction protocols.
- **Hardware synchronization** – provides a common timing reference across independent acquisition systems.
- **Experiment control** – coordinates monitoring, stimulation, synchronization, metadata, and experimental events.
- **3D reconstruction** – provides experiment-specific surface geometry for anatomical integration.

---

## Repository structure

```text
HEartLab-Multimodal-Mapping/
├── README.md
├── DISCLAIMER.md
│
├── cad/
│   ├── README.md
│   ├── small-heart/
│   ├── large-heart/
│   └── epi-endo/
│
├── docs/
│   ├── getting_started.md
│   └── protocols/
│       └── README.md
│
├── firmware/
│   ├── sensors/
│   ├── gateway/
│   └── synchronization_controller/
│
├── hardware/
│   └── README.md
│
└── software/
    └── experiment_control/
```

Additional documentation and example files may be added as the repository evolves.

---

## Getting started

Users interested in reproducing or adapting the platform should begin with the:

**[Getting Started guide](docs/getting_started.md)**

The recommended workflow is:

1. choose the experimental configuration;
2. define the scientific objective;
3. select the required platform modules;
4. select the relevant experimental protocols;
5. obtain or fabricate the required hardware;
6. upload and configure the required firmware;
7. install the experiment-control software;
8. validate each subsystem independently;
9. perform an integrated bench test;
10. document the final experiment-specific configuration.

The platform does **not** require every subsystem to be implemented for every experiment.

---

## Experimental protocols

Representative experimental protocols are provided in:

**[`docs/protocols/`](docs/protocols/)**

These documents should be interpreted as **examples of implementations used in HEartLab experiments rather than universal or mandatory experimental procedures**.

Experimental procedures may vary according to:

- scientific objective;
- preparation type;
- species or donor source;
- heart size;
- mapping modalities;
- perfusion configuration;
- available equipment;
- ethical approvals;
- pharmacological intervention;
- stimulation protocol.

Parameters that may vary between experiments include, where appropriate:

- total solution volume;
- perfusion flow and pressure;
- stimulation site and timing;
- recording duration and sequence;
- drug concentration or total administered amount;
- dye-loading strategy;
- motion-suppression strategy;
- electrode and camera positioning;
- arrhythmia-induction procedures;
- use of 3D reconstruction.

Not every parameter should be scaled simply because heart size changes. For example, total perfusate volume and flow may differ substantially between preparations, while the ionic composition of a physiological perfusion solution may remain unchanged unless a deliberate experimental modification is required.

Users are responsible for verifying the applicability of every protocol and parameter before use.

---

## CAD and mechanical designs

Mechanical design files are provided in:

**[`cad/`](cad/)**

The CAD library is organized according to the experimental configuration in which the components were developed:

- [`cad/small-heart/`](cad/small-heart/)
- [`cad/large-heart/`](cad/large-heart/)
- [`cad/epi-endo/`](cad/epi-endo/)

The majority of the supplied CAD files correspond to **custom components that must be fabricated or 3D printed**.

Commercial and off-the-shelf components, such as motors, bearings, pulleys, belts, shafts, fasteners, clamps, and standard mechanical hardware, are identified in the corresponding documentation and assembly drawings but their proprietary CAD models are generally not redistributed.

Where available, designs are provided in multiple formats:

| Format | Purpose |
|---|---|
| `.ipt` | Native Autodesk Inventor source |
| `.f3d` | Native Autodesk Fusion source |
| `.f3z` | Autodesk Fusion assembly/archive |
| `.step` / `.stp` | Vendor-neutral CAD exchange format |
| `.stl` | Mesh file intended primarily for additive manufacturing |
| `.pdf` | Assembly or dimensioned drawing |

Native source files are included when possible to preserve editability, while STEP files improve compatibility with other CAD systems.

The supplied designs correspond to HEartLab implementations and may require adaptation to different preparations, tanks, fabrication methods, or locally available components.

---

## Hardware

Hardware documentation is located in:

**[`hardware/`](hardware/)**

The platform hardware includes, depending on configuration:

- perfusion and fluidic components;
- physiological-monitoring electronics;
- optical-mapping interfaces;
- contact-electrical mapping interfaces;
- torso-tank electrode systems;
- stimulation hardware;
- synchronization hardware;
- mechanical supports;
- 3D-reconstruction hardware.

Commercial equipment referenced in this repository is documented for reproducibility but is not redistributed.

---

## Firmware

Embedded firmware is located in:

**[`firmware/`](firmware/)**

The current control and monitoring architecture includes:

- Arduino Nano-based sensor nodes;
- nRF24L01 wireless communication;
- an ESP32-S3 gateway;
- a Teensy 4.1 synchronization/timing controller.

The corresponding firmware directories document the implementation used by the platform.

Before use, verify:

- board type;
- pin assignments;
- sensor model;
- node identifiers;
- communication settings;
- voltage levels;
- required libraries;
- firmware version.

Configuration values from one experimental setup should not automatically be assumed to be appropriate for another.

---

## Experimental-control software

The experimental-control software is located in:

**[`software/experiment_control/`](software/experiment_control/)**

The application coordinates several experimental functions, including:

- experimental session organization;
- physiological monitoring;
- stimulation control;
- synchronization-related operations;
- recording coordination;
- metadata entry;
- event logging.

Commercial acquisition software supplied with cameras or electrical recording systems is not redistributed unless its license explicitly permits redistribution.

The HEartLab software should therefore be understood as an experimental integration and control layer rather than a replacement for all third-party acquisition software.

---

## What is included

This repository provides original HEartLab materials including, where applicable:

- embedded firmware;
- experimental-control software;
- custom electronic schematics and interfaces;
- CAD and mechanical design files;
- experimental protocol documentation;
- wiring and system-integration documentation;
- assembly and configuration information;
- representative planning and recording templates.

Third-party hardware, proprietary software, manufacturer drivers, and externally licensed materials are not redistributed unless permitted by their respective licenses.

---

## Reproducibility and versioning

The repository is intended to provide sufficient design and implementation information for laboratories to reproduce individual HEartLab modules or adapt them to related ex vivo electrophysiology preparations.

The `main` branch represents continued development.

For published work, the corresponding implementation should be preserved as a **tagged repository release** identifying the exact versions of:

- firmware;
- experimental-control software;
- hardware documentation;
- CAD files;
- protocol documentation;
- configuration information.

When reproducing a published experiment, use the repository release specified by the associated publication whenever possible.

---

## Data availability

Representative example files and data-format documentation may be provided directly in this repository when their size and content are appropriate for GitHub.

Larger experimental datasets supporting the associated publication will be made available according to the Data Availability statement of the final article.

Only data that can be shared in accordance with applicable ethical approvals and institutional requirements should be made publicly available.

---

## Associated publication

This repository accompanies the manuscript:

**Silva, V. P. et al. _An Open-Source Platform for Multimodal Electrical and Optical Mapping of Ex Vivo Hearts_.**

Manuscript in preparation for submission to *Scientific Reports*.

Publication details, DOI, and the repository release associated with the final article will be added when available.

---

## Citation

If you use or adapt this platform in academic work, please cite the associated publication once available.

Machine-readable citation metadata will be provided through a root-level `CITATION.cff` file.

---

## Contact

For technical questions, bug reports, or problems reproducing repository components, please open a GitHub issue.

For research collaboration or questions regarding the associated publication, contact the HEartLab at Universidade Federal do ABC (UFABC).

---

## License

Licensing information for the software, firmware, hardware designs, CAD files, and documentation will be added before the first archived public release.

The final repository licenses may differ by content type.

---

## Disclaimer

The hardware designs, firmware, software, protocols, CAD files, and documentation provided in this repository are supplied **"as is"**, without warranties or guarantees of any kind, either express or implied.

The materials are intended exclusively for experimental research involving ex vivo cardiac preparations. They have not been designed, validated, or approved as medical devices and must not be used for clinical diagnosis, treatment, patient monitoring, or direct use in humans.

Although reasonable efforts are made to document the platform accurately, the repository may contain errors, omissions, outdated information, or implementation-specific assumptions. Users are responsible for independently reviewing and validating all hardware, software, calculations, procedures, electrical connections, experimental parameters, concentrations, and safety measures before use.

The individual researcher or institution conducting an experiment remains responsible for determining whether the platform and associated procedures are appropriate for the intended application and for ensuring compliance with applicable ethical approvals, institutional requirements, laboratory procedures, and safety regulations.

To the maximum extent permitted by applicable law, HEartLab, Universidade Federal do ABC (UFABC), the repository authors, maintainers, contributors, and affiliated institutions shall not be liable for damages, losses, experimental failures, equipment damage, injury, data loss, incorrect experimental results, or other consequences arising from the use, misuse, modification, or interpretation of materials provided in this repository.

Use of this repository does not replace appropriate technical expertise, experimental validation, risk assessment, institutional oversight, or manufacturer documentation.

For the complete disclaimer, see **[`DISCLAIMER.md`](DISCLAIMER.md)**.
