# Hardware

This directory contains documentation and design information for the hardware used in the HEartLab multimodal ex vivo cardiac mapping platform.

The platform is modular. A particular experiment does not require every module, and some mechanical, perfusion, optical, and electrical interfaces change according to preparation size and scientific objective.

## Hardware modules

```text
hardware/
├── README.md
├── BOM_overview.md
├── perfusion/
├── physiological_monitoring/
├── optical_mapping/
├── electrical_mapping/
├── stimulation/
├── synchronization/
├── mechanical/
└── reconstruction_3d/
```

### `perfusion/`

Perfusion architecture, reservoirs, pumps, tubing, heat exchange, bubble management, flow monitoring, pressure monitoring, and cannulation interfaces.

### `physiological_monitoring/`

Sensor nodes and gateway hardware used to monitor perfusion flow, pressure, and temperature.

### `optical_mapping/`

Cameras, lenses, excitation illumination, emission filtering, mirror-assisted views, and hardware interfaces used for voltage-sensitive optical mapping.

### `electrical_mapping/`

Contact-electrical mapping and torso-tank mapping hardware, including MEAs, small-heart tank electrodes, large-heart tank PCBs, acquisition interfaces, and channel organization.

### `stimulation/`

Electrical stimulation hardware used for pacing and arrhythmia-induction protocols.

### `synchronization/`

Hardware timing interfaces used to provide a common temporal reference between optical and electrical acquisition systems.

### `mechanical/`

A guide to mechanical hardware and the corresponding CAD repository. Detailed custom mechanical designs are maintained under [`../cad/`](../cad/) rather than duplicated here.

### `reconstruction_3d/`

Motorized rotational hardware and imaging components used to acquire multi-view images for experiment-specific 3D reconstruction.

## Configuration overview

The table below summarizes the typical relationship between hardware modules and the three principal platform configurations.

| Module | Small-heart whole-organ | Large-heart whole-organ | Large-heart epi-endo |
|---|---|---|---|
| Perfusion | Aortic/Langendorff | Independent coronary perfusion | Coronary perfusion |
| Physiological monitoring | Used as required | Used as required | Used as required |
| Optical mapping | Panoramic multi-camera | Large-surface multi-camera | Dual-surface / mirror-assisted |
| Contact electrical mapping | Epicardial MEAs | Experiment dependent | Epicardial + endocardial MEAs |
| Torso-tank mapping | 60-electrode tank implementation | Six-face tank PCB implementation | Not a defining module |
| Electrical stimulation | Experiment dependent | Experiment dependent | Experiment dependent |
| Synchronization | When multimodal acquisition is used | When multimodal acquisition is used | When multimodal acquisition is used |
| 3D reconstruction hardware | Experiment dependent | Experiment dependent | Experiment dependent |

The table describes representative HEartLab implementations and should not be interpreted as a mandatory experimental sequence.

## Design philosophy

The hardware was developed around experimental functions rather than a single fixed physical arrangement.

Common design goals include:

- maintaining controlled perfusion;
- preserving optical and electrical access to the preparation;
- monitoring relevant physiological conditions;
- enabling programmable stimulation where required;
- acquiring complementary electrical and optical measurements;
- providing a common timing reference between acquisition systems;
- allowing adaptation to different preparation dimensions.

## Documentation convention

Each hardware directory contains, where applicable:

- a subsystem overview;
- representative bill of materials;
- configuration-specific notes;
- links to firmware or software;
- links to CAD files;
- fabrication/manufacturing files;
- operating notes, limitations, and compatibility information.

Commercial components are identified to support reproducibility but their proprietary design files are not redistributed.

## Important

The listed hardware corresponds to HEartLab implementations used during platform development. Exact component models, dimensions, calibration, electrical limits, and material compatibility must be independently verified before use.

See the repository-level [`DISCLAIMER.md`](../DISCLAIMER.md).
