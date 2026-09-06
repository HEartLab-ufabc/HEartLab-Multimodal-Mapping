# Perfusion Hardware BOM

Quantities depend on preparation and experimental configuration.

| Component | Quantity | Specification | Status / notes |
|---|---:|---|---|
| Peristaltic pump | 1 | Laboratory perfusion pump | Any model that can deliver more than 150mL/min |
| Main/bulk reservoir | 1+ | Large Beaker | 2L for small hearts/4L for large hearts |
| Head/perfusion reservoir | 1 | [`Water-Oil separator`](https://stonylab.com/products/b09mmwj8zc-water-oil-receiver-separator) works well for this application | Prioritize larger volumes at least 200mL |
| Analog flow meter | 1 per active line | Appropriate perfusion flow range | Selected according to the expected flow range of the preparation |
| Serpentine heat exchanger | 1 per active line | Laboratory helical condenser | Related CAD support available |
| Inline Bubble trap | 1 per active line | [`PEEK 300uL bubble trap`](https://www.precigenome.com/microfluidic-fluidic/bubble-trap) |  |
| Digital flow/temperature sensor | 1 per instrumented line | [`Sensirion SLF3S-4000B`](https://sensirion.com/products/catalog/SLF3S-4000B) | Current firmware implementation |
| Digital pressure sensor | 1 per instrumented line | Honeywell digital pressure sensor | Relative liquid-pressure measurement appropriate to the perfusion range |
| Tubing 6mm OD | As required (at least 2 meters) | Medical grade | Silicone or PVC, ID/OD 4/6mm. NOTE: Some manufactures have internal grooves in their tubing, those will leak if used. |
| Tubing 8mm OD | As required (at least 1 meter) | Medical grade | Silicone or PVC, ID/OD 6/8mm. Used to connect the flow sensor and the main reservoir. NOTE: Some manufactures have internal grooves in their tubing, those will leak if used. |
| 2-way Luer connectors | As required | Commercial |  |
| 6mm to 6mm quick connect | As required | Commercial | Useful for quickly changing configurations |
| 8mm to 6mm quick connectors | As required | Commercial | Useful for connecting the flow sensor (8mm) to the other tubing. |
| Three-way stopcocks | As required | Medical grade | Facilitate the removal of air bubbles in different points of the perfusion line. Small-heart cannula includes a modified stopcock interface |
| Aortic cannula | 1 | Custom | Made from a modified 3-way stopcock |
| Coronary cannula / interface | 1–2 | Preparation specific | Large-heart / epi-endo. Made from a blunt 14G needle and a silicone stopper with varying sizes depending on the coronary size gauge. |
| Clamps and tubing holders | As required | Commercial/custom | See CAD for custom supports |
| Carbogen gas interface | 1+ | 95% O₂ / 5% CO₂ experimental supply |  |
