# Software

This directory contains software developed or used to support operation of the HEartLab multimodal mapping platform.

The current repository includes software for:

- experiment control and logging;
- rotational image acquisition using the EVT camera system;
- rotational image acquisition using the Imaging Source USB camera.

## Directory structure

```text
software/
├── experiment_control/
├── 3d_reconstruction_capture_labview/
└── 3d_reconstruction_capture_python/
```

## Experimental control

[`experiment_control/`](experiment_control/) contains the Python-based graphical application used to coordinate several experimental functions, including:

- experimental session organization;
- physiological monitoring;
- stimulation control;
- synchronization-related operations;
- recording coordination;
- metadata entry;
- event logging.

The application acts as an integration and control layer and does not replace every manufacturer-supplied acquisition application used by the platform.

## 3D reconstruction image acquisition — LabVIEW / EVT

[`3d_reconstruction_capture_labview/`](3d_reconstruction_capture_labview/) contains the LabVIEW application used to automate rotational image acquisition with the EVT camera system used in HEartLab.

A representative acquisition captures approximately 100 views over a complete 360° rotation.

The application is configured around the EVT acquisition interface and should not be expected to work directly with cameras from other manufacturers without modification.

The folder also contains `saveNumberedImages.vi`, originally obtained from the RHYTHM open-source imaging toolkit and redistributed under its applicable MIT License. See the folder README and the repository-level `THIRD_PARTY.md`.

## 3D reconstruction image acquisition — Python / Imaging Source USB

[`3d_reconstruction_capture_python/`](3d_reconstruction_capture_python/) contains the Python/OpenCV application used with the Imaging Source USB camera in HEartLab.

The application:

- accesses the camera through OpenCV;
- provides a preview for camera adjustment;
- captures numbered TIFF images;
- sends incremental rotation commands to the Arduino rotational controller;
- waits for completion of each motor movement;
- acquires the requested number of unique angular views.

The standard 100-image workflow uses 3.6° increments.

Other OpenCV-accessible cameras may work, but compatibility and camera-property behavior must be independently verified.

## Shared rotational-stage firmware

Both image-acquisition implementations use the motorized rotational stage documented in:

[`../firmware/stepper_motor_control/`](../firmware/stepper_motor_control/)

when configured with compatible serial communication.

## Reconstruction versus image acquisition

The software in these two folders performs **multi-view image acquisition** for 3D reconstruction.

Subsequent processing stages such as:

- camera calibration;
- silhouette segmentation;
- space carving;
- volume reconstruction;
- surface-mesh generation;
- mesh processing;

are separate from the acquisition programs and should be documented independently where the corresponding code or procedures are available.

## 3D reconstruction processing

[`3d_reconstruction_processing/`](3d_reconstruction_processing/) contains the Python workflow used to process rotational image sequences into experiment-specific surface models.

The canonical processing path is:

```text
MC-Calib camera calibration
        ↓
rotational images
        ↓
undistortion
        ↓
silhouette extraction / correction
        ↓
rotational space carving
        ↓
voxel visual hull
        ↓
triangular surface mesh
```

Camera-calibration instructions are not duplicated in this repository. Users should follow the upstream [MC-Calib](https://github.com/rameau-fr/MC-Calib) documentation and provide its camera-parameter YAML output to the HEartLab reconstruction program.

The reconstruction folder also contains an optional PCA-based silhouette-alignment utility. 

## External software and drivers

The platform also uses manufacturer-supplied or third-party software, drivers, and SDKs.

These are not redistributed unless their licenses explicitly allow redistribution.

Users should consult the respective developer or manufacturer for installation and licensing requirements.

## Reproducibility

Each software component should document:

- tested operating system;
- tested language/runtime version;
- required dependencies;
- hardware interfaces;
- communication settings;
- expected inputs and outputs;
- known compatibility limitations.

For published work, use the tagged repository release associated with the publication whenever possible.

## Disclaimer

Software in this repository is provided for experimental research and must be independently verified for the intended hardware and application.

See the repository-level [`DISCLAIMER.md`](../DISCLAIMER.md).
