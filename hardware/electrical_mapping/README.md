# Electrical Mapping Hardware

This directory documents the contact-electrical and torso-tank mapping hardware used by the HEartLab platform.

The electrical subsystem includes:

- epicardial/endocardial multi-electrode arrays (MEAs);
- small-heart torso-tank electrodes;
- large-heart tank electrode PCBs;
- acquisition hardware and interconnection;
- reference/ground arrangements;
- configuration-specific channel mapping.

## Directory structure

```text
electrical_mapping/
├── README.md
├── BOM.md
├── contact_meas/
├── small-heart-torso-tank/
└── large-heart-tank-pcb/
```

## Acquisition

The platform implementation uses an [`Intan RHD Recording System`](https://www.intantech.com/RHD_system.html) or an [`Open Ephys`](https://open-ephys.org/) acquisition chain for electrical recordings.

The headstages used were [`Intan RHD 64-Channel Recording Headstages`](https://www.intantech.com/RHD_headstages.html?tabSelect=RHD64ch&yPos=0), the number of headstages used were dependent on which modality was being recorded and the number of recording channels.

Verify with the manufacturer all the necessary equipment for your specific application. 

## Contact electrical mapping

See:

[`contact_meas/`](contact_meas/)

Small-heart experiments use three 16-electrode epicardial MEAs positioned over right atrial, left atrial, and ventricular regions.

The epi-endo configuration uses paired epicardial and endocardial contact arrays.

## Small-heart torso-tank mapping

See:

[`small-heart-torso-tank/`](small-heart-torso-tank/)

The hexagonal small-heart tank contains 60 electrodes, with 10 electrodes distributed on each of six faces.

## Large-heart torso-tank mapping

See:

[`large-heart-tank-pcb/`](large-heart-tank-pcb/)

The large-heart tank uses six custom electrode PCBs. Each PCB contains 15 electrode pads, giving 90 bath-potential electrodes when all six faces are populated.

## Terminology

Repository documentation uses **torso-tank mapping** for electrical recordings from the conductive volume surrounding the preparation.

