# Stimulation Hardware — Architecture-Level BOM

This file summarizes the hardware architecture of the validated single-channel constant-current stimulator used with the platform.

| Component | Implementation | Notes |
|---|---|---|
| Current-source topology | PNP current mirror | Single-channel constant-current architecture |
| High-voltage supply | 4 × 9 V batteries in series | Isolated battery supply |
| Trigger interface | Isolated trigger | Receives stimulation commands from the control system |
| Output interface | Bipolar stimulation connection | Connected to the experiment-specific stimulation electrodes/catheter |
| Current-setting network | Adjustable current-control network | Provides the experimental output-current setting |
| PNP transistor stage | Matched/current-mirror stage | Constant-current output stage |
| Protection/interface components | As implemented in the validated circuit | Supports controlled experimental operation |
| Enclosure | Laboratory/custom | Electrically isolated experimental housing |
| Stimulation catheter/electrodes | Bipolar | Experiment dependent |

Operating characteristics are described in [`README.md`](README.md).
