# 3D Reconstruction Acquisition BOM

| Component | Quantity | Implementation | Notes |
|---|---:|---|---|
| Stepper motor | 1 | NEMA 14 | Current rotational implementation |
| Stepper driver | 1 | DRV8825 | STEP/DIR driver used in the implementation |
| Motor controller | 1 | Arduino-compatible | See firmware |
| Timing belt | 1 | Configuration specific | Small/large assemblies use different lengths |
| Pulleys | 2+ | Configuration specific | See CAD assembly |
| Rotation shaft | 1 | Configuration specific | See CAD |
| Bearings | 2+ | Configuration specific | See CAD |
| Reconstruction camera | 1 | EVT or Imaging Source USB implementation | Capture software differs |
| Camera lens | 1 | Camera dependent | Selected according to the reconstruction camera and field of view |
| Calibration object | 1 | ChArUco-based | MC-Calib workflow |
