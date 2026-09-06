# Electrical Mapping BOM

## Acquisition

| Component | Representative implementation | Notes |
|---|---|---|
| Electrical acquisition platform | Intan RHD / Open Ephys |  |
| Acquisition computer | Laboratory workstation | Configuration dependent |
| Digital synchronization input | Open Ephys digital input | Receives common timing signal |
| Headstage | Variable Quantity | Intan RHD 64-Channel Headstage |
| Digital Cable | Variable Quantity | RHD SPI Interface Cables |
| Electrode adapter cabling | Custom/commercial |  2x Intan 36-pin Wire Adapter per headstage|

## Contact MEAs

| Component | Quantity | Representative implementation |
|---|---:|---|
| Small-heart right-atrial MEA | 1 | 16 electrodes |
| Small-heart left-atrial MEA | 1 | 16 electrodes |
| Small-heart ventricular MEA | 1 | 16 electrodes |
| Epi-endo epicardial MEA | 1 | Configuration-specific |
| Epi-endo endocardial MEA | 1 | Configuration-specific |
| Headstage | 1 | Intan RHD 64-Channel Headstage (adapt to your needs)|
| Wiring harness | 1 | Intan 36-pin Wire Adapter |

## Small-heart torso tank

| Component | Quantity | Representative implementation |
|---|---:|---|
| Hexagonal tank | 1 | Acrylic tank custom manufacture |
| Tank electrodes | 60 | 10 per face × 6 faces |
| Electrode material | 60 | Historical stainless-steel and later Ag/AgCl implementations |
| Reference network | 1 | Wilson central terminal implementation |
| Headstage | 1 | Intan RHD 64-Channel Headstage |
| Wiring harness | 1 set | 2x Intan 36-pin Wire Adapters |

## Large-heart tank

| Component | Quantity | Representative implementation |
|---|---:|---|
| Large-heart tank electrode PCB | 6 | 15 electrodes per PCB |
| PCB support assembly | 1 | Custom CAD under `cad/large-heart/transparent-pcb-support/` |
| PCB connector/cabling | 6 sets | Current design uses a 1×16, 2.54 mm header footprint |
| Headstage | 2 | Intan RHD 64-Channel Headstage |
| Wiring harness | 2 sets | 2x Intan 36-pin Wire Adapters per Headstage|
