#include "sync_control.h"
#include <IntervalTimer.h>

// ------------------------------------------------------------------------
// PIN DEFINITIONS (Update for Teensy 4.1!)
// ------------------------------------------------------------------------
const int SIGNAL_PINS[] = {6, 7, 8};  // Three SYNC signals
const int REC_PIN       = 9;         // REC signal
static const int NUM_SIGNALS = sizeof(SIGNAL_PINS) / sizeof(SIGNAL_PINS[0]);

// ------------------------------------------------------------------------
// TIMER SETTINGS
// ------------------------------------------------------------------------
static const uint32_t TIMER_INTERVAL_US = 1;  // 10 microseconds => 100 kHz interrupt
volatile uint32_t master_counter = 0;          // increments each ISR cycle

// ------------------------------------------------------------------------
// SIGNAL PARAMETERS
// ------------------------------------------------------------------------
volatile uint32_t toggle_ticks[NUM_SIGNALS] = {2000, 2000, 2000}; // default 500Hz
volatile uint32_t high_ticks[NUM_SIGNALS]   = {1000, 1000, 1000}; // 50% duty
volatile uint32_t phase_ticks[NUM_SIGNALS]  = {0, 0, 0};
volatile bool     enabled[NUM_SIGNALS]      = {false, false, false};
volatile bool     high_state[NUM_SIGNALS]   = {false, false, false};

// ------------------------------------------------------------------------
// REC SIGNAL
// ------------------------------------------------------------------------
volatile bool rec_waiting             = false; 
volatile bool rec_active              = false;
volatile uint32_t rec_remaining_pulses= 0;
volatile bool prev_sync1_state        = false;
volatile bool rec_signal_complete     = false; // set true when REC finishes
// Keep track when a signal is freshly enabled
static volatile bool justEnabled[NUM_SIGNALS] = {false, false, false};

// ------------------------------------------------------------------------
// IntervalTimer for the SYNC loop
// ------------------------------------------------------------------------
IntervalTimer syncTimer;

// ------------------------------------------------------------------------
// onSyncTimer: Fires every 10µs
// ------------------------------------------------------------------------
static void onSyncTimer() {
    master_counter++;

   for (int i = 0; i < NUM_SIGNALS; i++) {
        if (enabled[i]) {

            // If we just enabled this signal, force the next cycle to start at 0
            if (justEnabled[i]) {
                // Force the local_counter to 0 by aligning master_counter
                // or just treat it like the first iteration
                // Option A: subtract (master_counter % toggle_ticks[i]) 
                //           so we appear to be "start of period"
                master_counter -= (master_counter % toggle_ticks[i]);
                
                // This ensures the next local_counter = 0
                justEnabled[i] = false;
            }

            // Now compute local_counter
            uint32_t local_counter = (master_counter + phase_ticks[i]) % toggle_ticks[i];
            bool shouldBeHigh = (local_counter < high_ticks[i]);

            // ... existing code ...
            if (shouldBeHigh && !high_state[i]) {
                high_state[i] = true;
                digitalWrite(SIGNAL_PINS[i], HIGH);
            } else if (!shouldBeHigh && high_state[i]) {
                high_state[i] = false;
                digitalWrite(SIGNAL_PINS[i], LOW);
            }
        }
    }

    // 2) Handle REC signal
    //    a) If waiting, start once SYNC1 is high
    if (rec_waiting) {
        // SYNC1 = index 0
        if (enabled[0] && high_state[0]) {
            rec_waiting = false;
            rec_active = true;
            digitalWrite(REC_PIN, HIGH);
        }
    }

    //    b) If active, decrement on each SYNC1 rising edge
    if (rec_active) {
        bool sync1_state = high_state[0];
        if (enabled[0] && !prev_sync1_state && sync1_state) {
            // Rising edge
            if (--rec_remaining_pulses == 0) {
                rec_active = false;
                digitalWrite(REC_PIN, LOW);
                rec_signal_complete = true;  // main loop can detect
            }
        }
        prev_sync1_state = sync1_state;
    }
}

// ------------------------------------------------------------------------
// Setup: Configure pins & start IntervalTimer
// ------------------------------------------------------------------------
void setup_sync_control() {
    for (int i = 0; i < NUM_SIGNALS; i++) {
        pinMode(SIGNAL_PINS[i], OUTPUT);
        digitalWrite(SIGNAL_PINS[i], LOW);
    }
    pinMode(REC_PIN, OUTPUT);
    digitalWrite(REC_PIN, LOW);

    // Start the hardware timer at 10µs intervals
    syncTimer.begin(onSyncTimer, (float)TIMER_INTERVAL_US);

    // (Optional) set a priority
    // syncTimer.priority(128);
}

// ------------------------------------------------------------------------
// set_signal_params: frequency (Hz), phase (degrees), duty_cycle (%)
// ------------------------------------------------------------------------
void set_signal_params(int signal, int frequency, int phase_degrees, int duty_cycle) {
    if (signal < 1 || signal > NUM_SIGNALS) {
        Serial1.println("(Teensy) Invalid signal number.");
        return;
    }
    int idx = signal - 1;

    // period in microseconds
    uint32_t period_us = 1000000UL / frequency;
    // convert period to "ticks" of 10us
    toggle_ticks[idx] = period_us / TIMER_INTERVAL_US;
    if (toggle_ticks[idx] < 1) toggle_ticks[idx] = 1;

    // compute high portion in ticks
    uint32_t tHigh = (toggle_ticks[idx] * duty_cycle) / 100;
    if (duty_cycle < 100 && tHigh > 0) {
        tHigh--;
    }
    high_ticks[idx] = tHigh;

    // phase offset in ticks
    uint32_t tPhase = (phase_degrees * toggle_ticks[idx]) / 360;
    phase_ticks[idx] = tPhase;

    Serial1.printf("(Teensy) Signal %d => freq=%d Hz, phase=%d°, duty=%d%%\n",
                  signal, frequency, phase_degrees, duty_cycle);
}

// ------------------------------------------------------------------------
// start_signals / stop_signals
// pass a string like "1", "12", or "123"
// ------------------------------------------------------------------------
void start_signals(const String &signals) {
    for (unsigned i = 0; i < signals.length(); i++) {
        int s = signals.charAt(i) - '0';
        if (s >= 1 && s <= NUM_SIGNALS) {
            if (!enabled[s - 1]) {
                // We are transitioning from OFF to ON
                justEnabled[s - 1] = true;
                enabled[s - 1] = true;
                high_state[s - 1] = false;
                digitalWrite(SIGNAL_PINS[s - 1], LOW);
                Serial1.printf("Signal %d started.\n", s);
            }
            else {
                // Already enabled; do nothing (or print message if you prefer)
                Serial1.printf("Signal %d was already running.\n", s);
            }
        }
    }
}

void stop_signals(const String &signals) {
    for (unsigned i = 0; i < signals.length(); i++) {
        int s = signals.charAt(i) - '0';
        if (s >= 1 && s <= NUM_SIGNALS) {
            enabled[s - 1] = false;
            high_state[s - 1] = false;
            digitalWrite(SIGNAL_PINS[s - 1], LOW);
            Serial1.printf("(Teensy) Signal %d stopped.\n", s);
        }
    }
}

// ------------------------------------------------------------------------
// start_rec_signal: Wait or start capturing pulses on SYNC1
// ------------------------------------------------------------------------
void start_rec_signal(uint32_t pulse_count) {
    // If SYNC1 not yet running or not enabled, set waiting flag
    if (!enabled[0]) {
        Serial1.println("(Teensy) REC waiting for SYNC1 to start...");
        rec_waiting = true;
        rec_remaining_pulses = pulse_count;
        return;
    }

    // Otherwise, start now
    rec_active = true;
    rec_remaining_pulses = pulse_count;
    digitalWrite(REC_PIN, HIGH);
    Serial1.printf("(Teensy) REC started for %u pulses of SYNC1.\n", pulse_count);
}
