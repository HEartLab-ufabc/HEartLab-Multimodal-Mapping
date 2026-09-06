# Optical Mapping Hardware

This directory documents the hardware used for voltage-sensitive optical mapping.

The optical arrangement changes with preparation geometry while retaining the same main functions:

- illuminate the preparation at the required excitation wavelength;
- collect fluorescence from one or more cardiac surfaces;
- spectrally isolate the emitted fluorescence;
- acquire images at high temporal resolution;
- synchronize image acquisition with electrical recordings.

## Optical components

The HEartLab implementations described in the associated work use:

- high-speed optical cameras;
- approximately 25 mm lenses;
- approximately 650 nm excitation LEDs;
- approximately 715 nm long-pass emission filters;
- camera and illumination supports;
- a 45° mirror in the epi-endo implementation.

Acquisition settings used in the platform include 500 frames/s, 1600 × 1000 pixels, and 12-bit acquisition where supported by the camera configuration.

These values describe the optical-mapping acquisition used in the platform implementation.

## Configuration-specific arrangements

### Small-heart whole-organ

The panoramic arrangement uses three cameras distributed around the preparation, approximately 120° apart, together with multiple excitation LEDs.

### Large-heart whole-organ

The large-heart arrangement uses two camera views to increase surface coverage.

### Large-heart epi-endo

The epi-endo implementation uses two optical cameras and a 45° mirror to provide complementary access to epicardial and endocardial surfaces.

The custom mirror holder is documented under:

[`../../cad/epi-endo/`](../../cad/epi-endo/)

## Synchronization

Camera acquisition is synchronized with the electrical acquisition system using the timing hardware described in:

[`../synchronization/`](../synchronization/)

## Camera models

The EVT and Imaging Source cameras documented under the 3D-reconstruction software are reconstruction/image-capture implementations and should not automatically be assumed to be the same cameras used for high-speed optical mapping.

## Reagents

Voltage-sensitive dye and motion-suppression can be found at:

[`../../docs/protocols/`](../../docs/protocols/)

See [`BOM.md`](BOM.md) for the current optical hardware list.
