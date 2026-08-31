#ifndef STIM_CONTROL_H
#define STIM_CONTROL_H

#include <Arduino.h>

// Public API (prototypes) for the STIM functions
void setupSTIM();
void startSTIMContinuous();
void stopSTIMContinuous();
void startSTIMBurst();
void stopSTIMBurst();
void setSTIMTypeParams(uint8_t type, uint32_t pulseWidthMs, uint32_t periodMs, uint8_t pulseCount, bool enabled);

#endif
