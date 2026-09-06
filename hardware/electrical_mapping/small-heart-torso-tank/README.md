# Small-Heart Torso-Tank Mapping Hardware

This directory documents the torso-tank electrical recording hardware used in the small-heart whole-organ configuration.

## Tank geometry

The implementation uses a hexagonal acrylic tank surrounding the isolated heart.

The tank volume is approximately 1500 cm³.

The drawings for the tank [`walls`](TankWalls.pdf) and [`base`](TankBase.pdf) are available. The tank was manufactured by a local supplier.

## Electrodes

The implementation contains:

- six tank faces;
- ten electrodes per face;
- 60 recording electrodes in total.

Historical implementations used stainless-steel electrodes, while later implementations used Ag/AgCl sintered electrodes (10mm diameter).

## Reference

A Wilson central terminal implementation is used as the torso-tank reference.

## Conductive solution

The tank solution is an experimental protocol parameter and is documented under:

[`../../../docs/protocols/`](../../../docs/protocols/)

## Acquisition

Tank potentials are acquired through the electrical recording system documented in:

[`../README.md`](../README.md)

