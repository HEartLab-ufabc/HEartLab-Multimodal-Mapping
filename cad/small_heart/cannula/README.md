# Small-Heart Cannula Assembly

This directory contains the mechanical design files for the rotating small-heart cannula assembly used in the Langendorff configuration.

The assembly combines machined, printed, and commercially available components.

## Assembly overview

The cannula assembly consists of:

1. two concentric acrylic tubes;
2. a printed spacer positioned between the acrylic tubes;
3. a machined connection piece;
4. a modified medical three-way stopcock forming the heart interface;
5. a separator sleeve between the tube assembly and support bearings;
6. two support bearings;
7. a timing pulley used to rotate the cannula assembly.

## Acrylic tube assembly

The assembly uses two concentric acrylic tubes.

Tube dimensions and assembly geometry are provided in:

`AssemblyTube.pdf`

A custom printed spacer is positioned between the concentric tubes to maintain alignment.

### Spacer

The spacer is provided as:

- Fusion source;
- STEP;
- STL;
- PDF drawing.

## Connection

The connection component joins the acrylic tube assembly to the modified three-way stopcock used for cardiac attachment on the bottom, and to the tubbing at the top.

The part is intended to be **machined rather than 3D printed**.

3D printing is not recommended for this component because dimensional accuracy, sealing quality, and fluid leakage are critical at this interface.

Available files include:

- Autodesk Inventor source;
- PDF drawing.

A neutral STEP model should preferably also be provided when available to facilitate machining using non-Autodesk software.

## Modified stopcock interface

A medical three-way stopcock is modified to provide the final heart-attachment interface.

The Luer-slip region is modified to provide:

- attachment geometry for the preparation;
- retaining grooves;
- appropriate connection to the custom cannula.

The commercial stopcock itself is not redistributed as a CAD model.

## Separator

The separator is a sleeve positioned between the acrylic tube assembly and the support bearings.

It provides the mechanical interface between the rotating cannula tube and two bearings.

**Bearings:** 20 × 32 × 5 mm  
**Quantity:** 2

## Timing pulley

The cannula is driven using a 48-tooth timing pulley.

The commercial pulley CAD model is not included.

The pulley must be modified by increasing its internal bore to approximately **15.1 mm** so that the acrylic tube assembly can pass through it.

Verify the actual tube outside diameter before machining the pulley.

## O-rings

O-rings are used at the connector interfaces where required to maintain sealing.

The appropriate dimensions should be specified in the bill of materials once finalized.

## Assembly considerations

Because this assembly carries perfusate and mechanically supports the heart:

- verify all seals before experimental use;
- pressure/leak-test the assembly before connecting a preparation;
- verify free rotation through the bearings;
- ensure that the modified pulley is concentric with the tube;
- verify that the stopcock and connector cannot separate under the expected mechanical load;
- inspect the heart-attachment interface before every experiment.