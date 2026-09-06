# CAD and Mechanical Design Files

This directory contains mechanical design files for custom components used in the HEartLab multimodal mapping platform.

The designs are organized according to the experimental configuration in which they were developed:

- [`small-heart/`](small-heart/) – components used with the small-heart whole-organ configuration;
- [`large-heart/`](large-heart/) – components used with the large-heart whole-organ configuration;
- [`epi-endo/`](epi-endo/) – components used with the large-heart epi-endo configuration.

The majority of the files provided here correspond to **custom components that must be fabricated or 3D printed**.

Commercial and off-the-shelf components, such as motors, bearings, pulleys, belts, shafts, fasteners, clamps, and other standard mechanical components, are identified in the corresponding documentation and assembly drawings but their proprietary CAD models are generally not redistributed in this repository.

## File formats

Where available, components are provided in several formats to facilitate both reproduction and modification.

| Format | Purpose |
|---|---|
| `.ipt` | Native Autodesk Inventor source file |
| `.f3d` | Native Autodesk Fusion design file |
| `.f3z` | Autodesk Fusion archive containing an assembly and/or externally referenced components |
| `.step` / `.stp` | Vendor-neutral CAD exchange format |
| `.stl` | Mesh file intended primarily for additive manufacturing |
| `.pdf` | Assembly drawings, dimensioned drawings, or reference documentation |

Native CAD files are provided whenever possible to preserve design history and editability. STEP files are included to improve compatibility with other CAD software, while STL files are intended primarily for fabrication of 3D-printed components.

## General fabrication notes

The supplied designs correspond to implementations used in HEartLab experiments and should be treated as reference designs rather than universal dimensions.

Mechanical components may require adaptation according to:

- preparation size;
- tank geometry;
- cannula dimensions;
- locally available bearings, shafts, motors, and pulleys;
- camera and electrode positioning;
- available fabrication methods.

Before fabrication, verify:

- model units;
- critical dimensions;
- fit between mating components;
- shaft and bearing tolerances;
- required threaded inserts or fasteners;
- intended material;
- compatibility with the experimental environment.

Components exposed to moisture, perfusate, or corrosive environments should be manufactured using materials and hardware appropriate for those conditions.

## Assemblies and off-the-shelf components

Assembly drawings may show commercial components that are not included as CAD files in this repository.

This is intentional. Their presence in an assembly is intended to document the mechanical interface and reproduce the experimental arrangement, not to redistribute manufacturer designs.

Relevant specifications for these components are listed in the corresponding README or bill of materials.

## Configuration-specific documentation

Each configuration directory contains additional information describing:

- the purpose of each custom component;
- required quantities;
- associated commercial components;
- assembly considerations;
- fabrication recommendations;
- files available for each part.

## Modification and reuse

The mechanical system is intentionally modular. Users may modify the designs to accommodate different preparations, tanks, equipment, or experimental objectives.

Any modified design should be mechanically verified before experimental use.

See the repository-level `DISCLAIMER.md` for additional information regarding validation, responsibility, and intended use.