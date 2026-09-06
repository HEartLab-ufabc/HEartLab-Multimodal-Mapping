# 3D Reconstruction Acquisition Hardware

This directory documents the hardware used to acquire rotational image sequences for experiment-specific 3D reconstruction.

The acquisition hardware is separate from the software that performs image capture and later reconstruction processing.

## Mechanical principle

The cardiac preparation is rotated through a complete revolution while images are captured at known angular increments.

The acquisition uses:

- 100 unique angular views;
- 360° total rotation;
- 3.6° between consecutive views.

## Rotational hardware

The current system uses:

- NEMA 14 stepper motor;
- STEP/DIR-compatible stepper driver;
- Arduino-compatible motor controller;
- 16× microstepping in the firmware configuration;
- configuration-specific pulleys, belts, shafts, bearings, and supports.

The exact mechanical arrangement differs between small-heart and large-heart assemblies.

CAD:

[`../../cad/`](../../cad/)

Firmware:

[`../../firmware/stepper_motor_control/`](../../firmware/stepper_motor_control/)

## Image-acquisition options

### EVT / LabVIEW

The EVT-camera implementation is documented under:

[`../../software/3D_reconstruction_capture_labview/`](../../software/3D_reconstruction_capture_labview/)

### Imaging Source USB / Python

The Imaging Source USB-camera implementation is documented under:

[`../../software/3D_reconstruction_capture_python/`](../../software/3D_reconstruction_capture_python/)

## Calibration

Camera calibration is performed using MC-Calib.

The HEartLab repository should link to the upstream MC-Calib instructions rather than duplicating their calibration procedure.

A ChArUco-based calibration object was used in the HEartLab reconstruction workflow.

## Reconstruction processing

The subsequent silhouette/space-carving/mesh processing software is documented separately under the software directory.

## Verification

Before rotational acquisition:

- verify motor direction;
- verify microstepping;
- verify pulley/transmission ratio;
- verify 3.6° movement if using 100 views;
- verify full 360° return;
- verify that tubing/cables do not obstruct rotation;
- verify camera focus and exposure;
- verify calibration-object visibility when required;
- verify image count and naming;
- verify mechanical stability between captures.

See [`BOM.md`](BOM.md).
