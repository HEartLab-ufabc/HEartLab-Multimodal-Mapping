# Getting Started

This guide provides a high-level workflow for reproducing, adapting, or operating components of the HEartLab multimodal mapping platform.

The platform is modular. A laboratory does **not** need to reproduce every subsystem or experimental configuration described in this repository. The recommended approach is to first select the preparation and scientific objective, then select the required platform modules and experiment-specific protocols, and finally assemble and validate those components before use with a biological preparation.

> **Documentation status:** This repository is under active development. Detailed bills of materials, wiring diagrams, calibration procedures, and configuration-specific assembly instructions are being added progressively. Where detailed instructions are not yet available, consult the corresponding subsystem README together with the associated publication, or contact the authors for a more detailed explanation.

---

## 1. Choose the experimental configuration

The platform has been implemented in three main configurations.

### Small-heart whole-organ configuration

Designed for Langendorff-perfused rabbit hearts.

Available modules can include:

- Langendorff perfusion;
- physiological monitoring;
- panoramic optical mapping;
- epicardial contact-electrical mapping using multi-electrode arrays (MEAs);
- torso-tank electrical mapping;
- electrical stimulation;
- hardware synchronization;
- experiment control and logging;
- experiment-specific 3D reconstruction.

### Large-heart whole-organ configuration

Designed for intact porcine and human ex vivo hearts.

Available modules can include:

- independent coronary perfusion;
- physiological monitoring;
- optical mapping;
- torso-tank electrical mapping;
- electrical stimulation when required by the experimental protocol;
- hardware synchronization;
- experiment control and logging;
- mechanical support adapted to large preparations;
- experiment-specific 3D reconstruction.

### Large-heart epi-endo configuration

Designed for isolated perfused ventricular-wall preparations.

Available modules can include:

- coronary perfusion of the isolated preparation;
- physiological monitoring;
- simultaneous epicardial and endocardial optical mapping;
- paired epicardial and endocardial contact-electrical mapping;
- mirror-assisted optical access;
- electrical stimulation when required by the experimental protocol;
- hardware synchronization;
- experiment control and logging.

---

## 2. Define the scientific objective

The experimental configuration defines the available platform modules, but the scientific objective determines which of those modules and protocols are required in a particular experiment.

Examples of experiment-specific decisions include:

- whether torso-tank recordings are required;
- pacing site and pacing protocol;
- whether arrhythmia induction is required;
- whether pharmacological interventions are used;
- whether AV-node ablation is performed;
- whether 3D reconstruction is required;
- whether tissue is collected for subsequent analysis.

Therefore, do not interpret the documentation as a single mandatory protocol that must be followed identically for every experiment.

Representative experimental protocols are available in [`protocols/`](protocols/).

---

## 3. Select the required platform modules

After defining the experimental objective, identify the required modules.

| Module | Function | Repository location |
|---|---|---|
| Perfusion | Maintains the ex vivo cardiac preparation under controlled conditions | [`../hardware/`](../hardware/) |
| Physiological monitoring | Measures perfusion pressure, flow, and temperature | [`../hardware/`](../hardware/) and [`../firmware/sensors/`](../firmware/sensors/) |
| Optical mapping | Records voltage-sensitive fluorescence from cardiac surfaces | [`../hardware/`](../hardware/) |
| Contact electrical mapping | Records local extracellular electrograms using MEAs | [`../hardware/`](../hardware/) |
| Torso-tank mapping | Records cardiac potentials from electrodes surrounding a conductive volume | [`../hardware/`](../hardware/) |
| Electrical stimulation | Provides pacing and arrhythmia-induction stimuli | [`../hardware/`](../hardware/) |
| Hardware synchronization | Provides a common timing reference to independent acquisition systems | [`../firmware/synchronization_controller/`](../firmware/synchronization_controller/) |
| Sensor communication | Transfers physiological measurements from sensor nodes to the experimental computer | [`../firmware/sensors/`](../firmware/sensors/) and [`../firmware/gateway/`](../firmware/gateway/) |
| Experiment control | Coordinates monitoring, stimulation, synchronization, metadata, and experimental events | [`../software/experiment_control/`](../software/experiment_control/) |
| Mechanical components | Supports the preparation and custom experimental interfaces | [`../cad/`](../cad/) |

The exact combination of modules depends on the preparation and experimental objective.

---

## 4. Obtain the repository

Clone the repository using Git:

```bash
git clone https://github.com/HEartLab-ufabc/HEartLab-Multimodal-Mapping.git
cd HEartLab-Multimodal-Mapping
```

For experiments intended to reproduce a published implementation, use the tagged release identified in the publication or repository citation information rather than the continuously updated `main` branch.

---

## 5. Review hardware and fabrication requirements

Before assembling any subsystem, identify:

- commercial components that must be obtained;
- custom mechanical parts that must be fabricated;
- custom electronic interfaces that must be assembled;
- required acquisition equipment;
- required sensors and microcontrollers;
- required power supplies and communication interfaces.

Hardware documentation is located in:

[`../hardware/`](../hardware/)

Mechanical design files are located in:

[`../cad/`](../cad/)

Subsystem bills of materials and component information are provided under [`../hardware/`](../hardware/).

---

## 6. Review the relevant experimental protocols

Protocols are organized separately from hardware and software documentation because they can vary according to experimental goal.

Representative protocols, planning documents, recording forms, and experimental examples are available in:

[`protocols/`](protocols/)

The files document implementations used in HEartLab experiments and are not intended to define a single mandatory workflow for all preparations.

Before using a protocol, verify that it corresponds to the intended preparation, experiment, ethical approval, and current validated laboratory procedure.

---

## 7. Fabricate the required custom components

Custom mechanical components should be fabricated according to files provided in the `cad/` directory.

Depending on the component, the repository may provide:

- editable CAD source files;
- STEP or other neutral CAD formats;
- STL files for additive manufacturing;
- dimensioned drawings;
- fabrication notes.

Before fabrication, verify:

- file units;
- critical dimensions;
- material requirements;
- tolerances;
- expected preparation dimensions;
- compatibility with locally available equipment.

The supplied designs represent implementations used in HEartLab and may require adaptation for different tanks, cameras, cannulae, electrodes, or preparation sizes.

---

## 8. Assemble the physiological-monitoring network

The current embedded monitoring architecture uses independent sensor nodes associated with active perfusion lines.

The general communication path is:

```text
Flow / temperature sensor ─┐
                           │
Pressure sensor ───────────┼──> Sensor node ── wireless ──> Gateway ── USB ──> Computer
                           │
Other local sensors ───────┘
```

The current implementation includes:

- Arduino Nano-based sensor nodes;
- nRF24L01 wireless communication;
- an ESP32-S3 gateway connected to the experimental computer.

Sensor-node firmware:

[`../firmware/sensors/`](../firmware/sensors/)

Gateway firmware:

[`../firmware/gateway/`](../firmware/gateway/)

Before uploading firmware, verify the documented:

- board type;
- sensor model;
- pin assignments;
- node identifier;
- wireless configuration;
- required libraries;
- communication settings.

Do not assume that configuration values from one node or experimental setup are appropriate for another.

---

## 9. Configure the synchronization controller

The current synchronization implementation uses a Teensy 4.1 timing controller.

Firmware is located in:

[`../firmware/synchronization_controller/`](../firmware/synchronization_controller/)

The synchronization controller provides hardware timing signals used to align independent recording systems and experimental events.

Before connecting acquisition equipment, verify:

- accepted trigger voltage;
- trigger polarity;
- pulse-width requirements;
- input impedance;
- grounding arrangement;
- whether galvanic isolation is required.

Hardware trigger requirements should always be checked against the documentation of the connected acquisition device.

---

## 10. Install the experimental-control software

The experimental-control application is located in:

[`../software/experiment_control/`](../software/experiment_control/)

The software is used to coordinate several platform functions, including:

- experimental session organization;
- physiological monitoring;
- stimulation control;
- synchronization-related operations;
- recording coordination;
- metadata entry;
- event logging.

Follow the software README for the tested operating system, Python version, package dependencies, and serial-interface configuration.

The application should be tested with the embedded hardware before use during an experiment.

---

## 11. Validate each subsystem independently

Before combining the system with a biological preparation, validate each required module independently.

### Perfusion

Confirm:

- correct flow direction;
- absence of leaks;
- absence of trapped air;
- stable temperature;
- stable pressure;
- expected flow range.

### Physiological monitoring

Confirm:

- each sensor is detected;
- readings are physically plausible;
- node identifiers are correct;
- wireless packets are received consistently;
- measurements appear correctly in the control software.

### Electrical stimulation

Confirm:

- output is disabled at startup;
- pulse timing is correct;
- output amplitude is verified using an appropriate test load;
- trigger behavior is correct;
- no unintended output occurs during connection or reset.

### Synchronization

Confirm:

- the expected synchronization signal is generated;
- all intended acquisition systems receive the signal;
- frequency and pulse width are correct;
- trigger edges are temporally aligned within the requirements of the experiment.

An oscilloscope or logic analyzer is strongly recommended for synchronization verification.

### Optical and electrical acquisition

Confirm:

- acquisition can be started and stopped reliably;
- trigger configuration is correct;
- signals are recorded using the expected sampling settings;
- reference and grounding arrangements are correct.

---

## 12. Perform an integrated bench test

After individual subsystems have been validated, test the integrated system without a biological preparation.

A recommended bench test includes:

1. power all required devices;
2. connect the sensor nodes and gateway;
3. verify sensor communication;
4. start the experimental-control software;
5. verify the synchronization output;
6. connect acquisition-system trigger inputs;
7. execute a short test recording;
8. generate representative stimulation events using an appropriate test load;
9. confirm that events are correctly logged;
10. confirm that recorded signals can be temporally aligned.

Resolve communication, timing, or stimulation issues before beginning an ex vivo experiment.

---

## 13. Prepare an experiment-specific plan

Before each experiment, document:

- preparation type;
- scientific objective;
- selected mapping modalities;
- selected stimulation protocol;
- optional pharmacological or electrophysiological interventions;
- required solutions;
- required equipment;
- intended recording sequence;
- tissue-processing requirements, if any;
- criteria for optional procedures such as 3D reconstruction.

Use the representative experiment-planning documents in [`protocols/`](protocols/) as a basis for recording the experiment-specific configuration.

---

## 14. Pre-experiment verification

Immediately before an experiment, verify at minimum:

- [ ] required firmware versions are documented;
- [ ] the correct experimental-control software version is being used;
- [ ] sensor nodes have the correct identifiers;
- [ ] physiological sensors are operating;
- [ ] perfusion tubing is correctly connected and primed;
- [ ] no air remains in critical perfusion-line sections;
- [ ] temperature control is operating;
- [ ] pressure and flow readings are plausible;
- [ ] synchronization outputs have been verified;
- [ ] acquisition systems are receiving the intended hardware trigger;
- [ ] stimulation output has been tested on an appropriate load;
- [ ] cameras and electrical acquisition systems have sufficient storage space;
- [ ] experimental metadata and output directories are configured;
- [ ] all required custom hardware is mechanically secure;
- [ ] the experiment-specific protocol and required solutions have been confirmed.

Configuration-specific checklists may contain additional requirements.

---

## 15. Run and document the experiment

During each experiment, preserve enough information to identify:

- preparation and experimental configuration;
- scientific objective;
- platform modules used;
- firmware versions;
- experimental-control software version;
- acquisition settings;
- stimulation protocols;
- sensor configuration;
- pharmacological or procedural interventions;
- recording identifiers;
- deviations from the planned protocol.

Where possible, use Git release or commit identifiers to associate experimental data with the exact software and firmware revision used for acquisition.

---

## 16. After the experiment

After acquisition:

1. verify that all expected files were saved;
2. preserve the experiment log;
3. back up raw optical and electrical data;
4. preserve physiological-monitoring records;
5. preserve configuration and stimulation information;
6. record deviations from the planned protocol;
7. record hardware or software issues encountered during the experiment;
8. associate the dataset with the corresponding repository release or Git commit.

Raw experimental data should be preserved independently of processed or exported data.

---

## Reproducibility and versioning

The `main` branch represents continued platform development.

For published work, a tagged release should identify the exact version of:

- firmware;
- experimental-control software;
- hardware documentation;
- CAD files;
- protocol documentation;
- configuration information.

When reproducing an experiment, use the release specified by the corresponding publication whenever possible.

---

## Safety and intended use

The HEartLab platform is intended for experimental research with ex vivo cardiac preparations.

It is **not a medical device** and has not been designed, validated, or approved for clinical diagnosis, treatment, patient monitoring, or direct use in humans.

Users are responsible for evaluating the electrical, mechanical, biological, chemical, and laboratory safety requirements applicable to their implementation and institution.

---

## Next steps

After completing this guide, consult the subsystem-specific documentation for detailed assembly, configuration, calibration, and operation instructions.

Start with:

- [`../hardware/`](../hardware/) for physical and electronic subsystems;
- [`../firmware/`](../firmware/) for embedded controllers;
- [`../software/`](../software/) for the experimental-control application;
- [`../cad/`](../cad/) for custom mechanical designs;
- [`protocols/`](protocols/) for experimental protocol documentation.
