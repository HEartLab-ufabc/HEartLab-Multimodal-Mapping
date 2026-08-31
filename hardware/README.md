# Hardware

This directory contains documentation and design information for the hardware components of the multimodal ex vivo cardiac mapping platform.

The platform is modular. Not every hardware module is required for every experiment, and several components are changed or resized depending on whether the platform is being used for a small-heart whole-organ, large-heart whole-organ, or large-heart epi-endo preparation.

## Hardware modules

### `perfusion/`

Perfusion architecture, fluidic connections, cannulation interfaces, reservoirs, heat exchangers and associated components.

### `physiological_monitoring/`

Sensors and embedded hardware used to monitor perfusion pressure, flow and temperature.

### `optical_mapping/`

Illumination arrangement, optical filters, cameras, lenses, mounting considerations and synchronization interfaces used for voltage-sensitive optical mapping.

### `electrical_mapping/`

Contact-electrical and torso-tank recording interfaces, including MEAs, tank electrodes and associated acquisition connections.

### `stimulation/`

Electrical stimulation hardware and interfaces used for pacing and arrhythmia-induction protocols.

### `synchronization/`

Hardware timing and triggering interfaces used to maintain a common temporal reference between acquisition systems.

### `mechanical/`

Mechanical supports, holders, mounts and interfaces used to position the cardiac preparation and experimental equipment.

### `reconstruction_3d/`

Mechanical hardware used for rotational image acquisition and experiment-specific three-dimensional reconstruction.

## Design philosophy

The hardware was developed around common experimental functions rather than a fixed physical arrangement.

For example, the perfusion interface differs substantially between a Langendorff-perfused rabbit heart and an independently coronary-perfused large heart. Similarly, the dimensions and arrangement of optical and electrical interfaces depend on preparation size.

Despite these differences, the same general functions are retained:

- maintain controlled perfusion;
- preserve optical and electrical access;
- monitor preparation conditions;
- provide stimulation when required;
- acquire complementary mapping modalities;
- synchronize the acquired signals.

## Important

Dimensions and component specifications provided here correspond to hardware used during development of the platform unless otherwise indicated.

Some components are custom manufactured and may require adaptation to the available equipment, preparation dimensions or fabrication methods of another laboratory.

Commercial equipment referenced in this repository is not distributed with the repository and remains subject to the manufacturer's specifications and licensing conditions.
