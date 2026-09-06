# Software

This directory contains software developed for operation of the experimental platform.

The primary software component is the experiment-control graphical interface used to coordinate several experimental subsystems from a common interface.

## Experiment-control software

See:

[`experiment_control/`](experiment_control/)

The application provides functions for:

- experimental session organization;
- stimulation control;
- recording coordination;
- sensor visualization;
- synchronization-related operations;
- metadata entry;
- event logging.

## External acquisition software

The platform also uses software supplied by manufacturers or third-party projects for individual acquisition systems.

These applications are not redistributed in this repository unless their licenses explicitly permit redistribution.

The experimental-control software should therefore be considered an integration and coordination layer rather than a replacement for every hardware manufacturer's acquisition software.
