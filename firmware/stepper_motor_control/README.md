# Stepper Motor Control

This directory contains the Arduino firmware used to control the motorized rotational stage for experiment-specific 3D reconstruction image acquisition.

The controller receives angular movement commands from the acquisition computer and rotates the cardiac preparation by the requested angular increment.

In the representative HEartLab workflow, 100 unique images are acquired over one complete 360° rotation, corresponding to an angular increment of 3.6°.

## Purpose

```text
Image-acquisition software
          │
          │ Serial
          ▼
       Arduino
          │
      STEP / DIR
          ▼
   Stepper driver
          │
          ▼
    Stepper motor
          │
          ▼
 Rotational support
```

The firmware itself does not perform image acquisition or 3D reconstruction.

## Current configuration

| Parameter | Value |
|---|---:|
| Motor full steps/revolution | 200 |
| Microstepping | 16 |
| Microsteps/revolution | 3200 |
| STEP pin | 2 |
| DIR pin | 5 |
| Serial baud rate | 57600 |
| Maximum speed | 400 steps/s |
| Acceleration | 100 steps/s² |

The firmware uses the `AccelStepper` library.

## Angular resolution

```text
3200 microsteps / 360° = 8.8889 microsteps/degree
```

For 100 imaging positions:

```text
360° / 100 = 3.6°
```

which corresponds to approximately:

```text
3.6° × 8.8889 = 32 microsteps
```

per imaging increment.

The actual preparation rotation must be verified because pulley ratio, gearing, coupling, or other mechanical transmission can alter the relationship between motor rotation and preparation rotation.

## Serial protocol

The current firmware operates at:

```text
57600 baud
```

and reads two numeric values for each movement command:

```text
<initiation value>\n<relative angle>
```

The current acquisition applications send:

```text
1\n<relative angle>
```

After movement is completed, the firmware reports the accumulated step count using:

```text
Step Count:
```

The Python image-acquisition application uses this response as a movement-completion acknowledgement.

## Related acquisition software

### LabVIEW / EVT camera system

[`../../software/3D_reconstruction_capture_labview/`](../../software/3D_reconstruction_capture_labview/)

This implementation is configured for the EVT camera interface.

### Python / Imaging Source USB camera

[`../../software/3D_reconstruction_capture_python/`](../../software/3D_reconstruction_capture_python/)

This implementation uses Python and OpenCV with the Imaging Source USB camera.

Both applications perform the same general rotational acquisition task but use different camera interfaces.

## Verification

Before rotating a cardiac preparation:

1. verify motor direction;
2. verify microstepping;
3. verify the mechanical transmission ratio;
4. verify the serial baud rate;
5. verify the commanded angular increment;
6. verify a complete revolution;
7. confirm unobstructed tubing/cable movement;
8. verify communication with the selected acquisition software.

> [!CAUTION]
> Motor parameters and angular calibration must be independently verified for the specific motor, driver, microstepping configuration, pulley ratio, and mechanical assembly being used.

See the repository-level `DISCLAIMER.md`.
