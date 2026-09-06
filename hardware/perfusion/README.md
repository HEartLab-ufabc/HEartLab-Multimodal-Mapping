# Perfusion Hardware

This directory documents the perfusion hardware used to maintain the ex vivo cardiac preparations.

The platform uses a shared perfusion concept that is adapted to the preparation rather than three completely independent systems.

## Common instrumented perfusion line

A perfusion line contains:

- perfusate reservoir(s);
- pump and/or hydrostatic pressure source;
- analog flow indication;
- heat exchange;
- bubble management;
- digital flow and inline temperature sensing;
- pressure sensing close to the preparation;
- tubing and connectors;
- carbogen gas source;
- preparation-specific cannulation interface.

The exact order and placement of these elements should follow the validated configuration schematic for the experiment.

## Configuration-specific interfaces

### Small-heart whole-organ

The small-heart implementation uses an aortic/Langendorff cannulation interface.

The custom rotating cannula assembly is documented under:

[`../../cad/small_heart/cannula/`](../../cad/small_heart/cannula/)

The serpentine support is documented under:

[`../../cad/small_heart/serpentine_support/`](../../cad/small_heart/serpentine_support/)

### Large-heart whole-organ

The large-heart whole-organ configuration uses independent coronary perfusion lines.

The common reservoir/pump architecture can feed two instrumented lines, each with its own monitoring chain, before connection to the appropriate coronary cannulation interface.

### Large-heart epi-endo

The epi-endo preparation uses a coronary perfusion line connected to the isolated tissue preparation.

The epi-endo mechanical support constrains the perfusion tubing to reduce mechanical loading of the tissue:

[`../../cad/epi-endo/`](../../cad/epi-endo/)

## Physiological monitoring

The digital flow, temperature, and pressure sensors are documented in:

[`../physiological_monitoring/`](../physiological_monitoring/)

## Experimental parameters

Perfusion pressure, flow, temperature, solution composition, and total solution volume are experimental parameters rather than fixed hardware specifications.

Protocol values are therefore documented under:

[`../../docs/protocols/`](../../docs/protocols/)

## Verification before use

Before connection to a cardiac preparation:

- leak-test the complete fluidic path;
- verify cannula and connector retention;
- verify bubble-trap operation;
- verify unobstructed tubing;
- verify flow-sensor and pressure-sensor readings;
- verify the pressure measurement near the preparation;
- verify temperature under flow;
- inspect all components that contact perfusate;
- ensure materials are compatible with the intended solution and temperature.

See [`BOM.md`](BOM.md) for the current hardware list.
