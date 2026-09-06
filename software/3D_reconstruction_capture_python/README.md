# 3D Reconstruction Image Acquisition — Python / Imaging Source USB Camera

This directory contains the Python application used by HEartLab to automate rotational image acquisition for experiment-specific three-dimensional reconstruction of cardiac preparations.

The application was developed for the **USB camera from The Imaging Source used in the HEartLab implementation**, accessed through OpenCV, and coordinates image capture with the Arduino-controlled rotational stage.

> [!IMPORTANT]
> The current implementation was developed around the HEartLab Imaging Source USB-camera setup. Other cameras that are accessible through OpenCV may also work, but compatibility, camera controls, image format, exposure behavior, and driver support must be independently verified.

The repository also contains a separate LabVIEW acquisition implementation for the EVT camera system.

## Purpose

The application performs the **image-acquisition stage** of the 3D reconstruction workflow.

A representative acquisition captures 100 unique views over one complete 360° rotation:

```text
Image 000:   0.0°
Image 001:   3.6°
Image 002:   7.2°
...
Image 099: 356.4°
```

After the final image, the corrected implementation can perform one additional 3.6° movement to return the rotational stage to its initial 360°/0° orientation without saving a duplicate image.

The acquired images are subsequently used for segmentation and 3D surface reconstruction. This application does **not** itself perform segmentation, space carving, mesh generation, or other reconstruction processing.

## System architecture

```text
Imaging Source USB camera
          │
          ▼
 Python acquisition software
          │
          ├── TIFF image capture
          │
          └── serial angle command
                    │
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
            Rotating support
```

The corresponding rotational-stage firmware is located in:

[`../../firmware/stepper_motor_control/`](../../firmware/stepper_motor_control/)

## Representative acquisition parameters

| Parameter | Representative value |
|---|---:|
| Total angular coverage | 360° |
| Number of unique images | 100 |
| Angular increment | 3.6° |
| Output format | TIFF |
| Stepper-controller baud rate | 57600 baud |
| Default settling delay | 3 s |

The number of images and settling delay can be adjusted in the graphical interface.

If the number of images is changed, the angular increment is calculated as:

```text
angular increment = 360° / number of images
```

The motor and mechanical transmission must be capable of reproducing the requested increment with sufficient accuracy.

## Camera compatibility

The current implementation opens the camera through OpenCV.

On Windows, the corrected version first attempts to use the DirectShow backend and falls back to OpenCV's default backend if necessary.

The application was developed for the HEartLab **Imaging Source USB camera**. Compatibility with other cameras should not be assumed.

Potential camera-dependent differences include:

- device enumeration;
- supported resolutions;
- pixel format;
- exposure range;
- automatic versus manual exposure;
- gain range;
- driver behavior;
- buffering;
- bit depth;
- TIFF output;
- OpenCV backend support.

The exposure and gain sliders in the application use OpenCV's generic camera-property interface. The numeric values are therefore **camera- and backend-dependent** and must be verified for the connected camera.

## Relationship to the LabVIEW / EVT implementation

Two rotational image-acquisition implementations are provided:

The two programs perform the same general task but use different camera interfaces.

Both can use the HEartLab Arduino rotational-stage firmware when configured with a compatible serial protocol.

## Requirements

The Python program requires:

- Python 3;
- OpenCV (`opencv-python`);
- PySerial (`pyserial`);
- Tkinter;
- a compatible camera driver;
- the HEartLab Arduino rotational-stage controller.

Python package requirements are listed in:

[`requirements.txt`](requirements.txt)

Install the Python dependencies with:

```bash
python -m pip install -r requirements.txt
```

Tkinter is included with standard Python distributions on Windows. On some Linux distributions it may need to be installed separately through the operating system package manager.

## Running the application

Run:

```bash
python 3DGeometry_IS.py
```

The graphical interface allows selection of:

- camera index;
- serial/COM port;
- image-output folder;
- settling delay;
- number of images;
- rotation direction.

A camera preview can be opened before acquisition.

When acquisition starts, a second live view allows representative exposure and gain adjustment before the automated rotation begins.

## Acquisition sequence

The corrected acquisition workflow is:

1. open the selected camera;
2. open the Arduino serial connection at 57600 baud;
3. display the camera-adjustment view;
4. capture the current angular position;
5. save the image;
6. command the requested angular increment;
7. wait for the Arduino to report completion of the motor movement;
8. wait for the user-defined mechanical settling delay;
9. capture the next angular position;
10. repeat until the requested number of unique images is acquired;
11. optionally return the stage to its initial orientation.

Waiting for the Arduino movement-completion message prevents the next image from being acquired only on the basis of a fixed time delay.

## Output

Images are saved using the naming convention:

```text
image_000.tiff
image_001.tiff
image_002.tiff
...
```

For the standard 101-image acquisition:

```text
image_000.tiff →   0.0°
image_001.tiff →   3.6°
...
image_100.tiff → 356.4°
```

The program creates the selected output directory if it does not already exist.

The TIFF files contain the frames returned by OpenCV. Camera pixel format and bit depth therefore depend on the camera, driver, and OpenCV backend configuration.

## Serial protocol

The current HEartLab stepper firmware uses:

```text
57600 baud
```

For each movement, the Python application transmits two numeric values:

```text
1
<angle>
```

For example:

```text
1
3.6000
```

The first value preserves compatibility with the current Arduino communication sequence and the second value is the requested relative angular movement.

The corrected Python implementation waits until the Arduino reports:

```text
Step Count:
```

which is printed after the firmware completes `runToPosition()`.

If the firmware communication protocol is changed, this application must be updated accordingly.

## Verification before use

Before an experimental acquisition:

- verify that the correct camera is selected;
- verify camera focus and field of view;
- verify exposure and gain behavior;
- verify the correct COM port;
- verify that Python and the Arduino firmware use the same baud rate;
- verify the stepper microstepping configuration;
- verify the mechanical transmission ratio;
- verify rotation direction;
- verify the angular increment;
- verify that 100 positions correspond to one complete revolution;
- verify that tubing and cables do not obstruct rotation;
- verify that TIFF files are written correctly;
- verify the expected number of output images.

> [!CAUTION]
> Camera communication, motor movement, angular calibration, exposure/gain settings, file output, and mechanical operation must be independently verified before experimental use.

See the repository-level [`DISCLAIMER.md`](../../DISCLAIMER.md).

## Known limitations

The current implementation:

- searches a limited range of OpenCV camera indices;
- assumes one camera is used for this acquisition;
- uses OpenCV's generic exposure and gain properties;
- does not automatically determine camera-specific valid control ranges;
- does not embed acquisition metadata into the TIFF filenames;
- does not perform 3D reconstruction;
- does not guarantee compatibility with cameras other than the tested HEartLab Imaging Source USB setup.

The camera-preview window should be closed before starting the acquisition if the operating system or driver does not permit the same camera to be opened by multiple application instances.

## Source file

The main application is:

[`3DGeometry_IS.py`](3DGeometry_IS.py)

The version provided here includes corrections to the original implementation for image-count logic, serial-port compatibility, motor-completion handling, error handling, device-list validation, and resource cleanup.
