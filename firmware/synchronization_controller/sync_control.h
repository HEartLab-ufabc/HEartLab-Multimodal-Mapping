#ifndef SYNC_CONTROL_H
#define SYNC_CONTROL_H

#include <Arduino.h>

// Sets up the SYNC timer, pins, etc.
void setup_sync_control();

// Adjust per-signal parameters
void set_signal_params(int signal, int frequency, int phase_degrees, int duty_cycle);

// Start/stop specific SYNC signals (1,2,3)
void start_signals(const String &signals);
void stop_signals(const String &signals);

// Start the REC signal for a specified number of SYNC1 pulses
void start_rec_signal(uint32_t pulse_count);

// Expose a flag so the main code can detect when REC completes
extern volatile bool rec_signal_complete;

#endif
