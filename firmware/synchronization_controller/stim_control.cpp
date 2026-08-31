#include "stim_control.h"
#include <Arduino.h>

// Use Teensy IntervalTimer
#include <IntervalTimer.h>

// -----------------------
// Pin Definitions
// -----------------------
#define STIM_PIN 21  // Adjust for your wiring on Teensy

// -----------------------
// Modes and State
// -----------------------
enum STIMMode { CONTINUOUS, BURST, IDLE };
volatile STIMMode stimMode = CONTINUOUS;

// -----------------------
// Type Parameters
// -----------------------
struct STIMType {
    uint32_t pulseWidth;  // In microseconds
    uint32_t period;      // In microseconds
    uint8_t pulseCount;   // Number of pulses
    bool enabled;         // Enabled/Disabled
};

// Example default configuration (adjust as needed)
STIMType stimTypes[5] = {
    {2000, 1000000, 1, true},   // S0
    {2000, 1000000, 8, false},  // S1
    {2000, 1000000, 8, false},  // S2
    {2000, 1000000, 8, false},  // S3
    {2000, 1000000, 8, false}   // S4
};

// -----------------------
// Internal State
// -----------------------
volatile uint8_t currentType = 0;
volatile uint8_t currentPulse = 0;
volatile bool stimRunning = false;
volatile bool startBurstPending = false; // Flag to switch from CONTINUOUS to BURST

// -----------------------
// Teensy IntervalTimers
// -----------------------
IntervalTimer continuousTimer;
IntervalTimer burstTimer;
// -----------------------
// Forward Declarations
// -----------------------
void onSTIMContinuous();
void onSTIMBurst();

// -----------------------
// Setup
// -----------------------
void setupSTIM() {
    pinMode(STIM_PIN, OUTPUT);
    digitalWrite(STIM_PIN, LOW);
}

// -----------------------
// Continuous Mode Callback
// -----------------------
void onSTIMContinuous() {
    // Stop repeating so we can manually restart (mimics "one-shot")
    continuousTimer.end();

    static bool state = false;
    state = !state; // Toggle HIGH/LOW each time

    if (state) {
        digitalWrite(STIM_PIN, HIGH);
        // Serial.printf("PULSE_%d_%02d\n", 0, stimTypes[0].pulseWidth / 1000);

        // Schedule turning the pin LOW after pulseWidth microseconds
        continuousTimer.begin(onSTIMContinuous, stimTypes[0].pulseWidth);
    } else {
        digitalWrite(STIM_PIN, LOW);

        if (startBurstPending) {
            // We’ve just finished a pulse in continuous mode
            // Now switch to burst mode
            startBurstPending = false;
            stimMode = BURST;
            currentType = 0;   // Start with S0
            currentPulse = 1;  // We already did one pulse for S0?

            // Instead of continuing continuous mode, use the burstTimer to handle next step
            burstTimer.begin(onSTIMBurst, stimTypes[0].period - stimTypes[0].pulseWidth);
        } else {
            // Remain in continuous mode
            // Wait for the remainder of the period before the next pulse
            continuousTimer.begin(onSTIMContinuous, stimTypes[0].period - stimTypes[0].pulseWidth);
        }
    }
}

// -----------------------
// Burst Mode Callback
// -----------------------
void onSTIMBurst() {
    // Stop repeating
    burstTimer.end();

    if (!stimRunning) {
        digitalWrite(STIM_PIN, LOW);
        return;
    }

    static bool state = false;
    state = !state;

    if (state) {
        digitalWrite(STIM_PIN, HIGH);
        // Serial.printf("PULSE_%d_%02d\n", currentType, stimTypes[currentType].pulseWidth / 1000);

        // Schedule pin LOW after pulseWidth microseconds
        burstTimer.begin(onSTIMBurst, stimTypes[currentType].pulseWidth);
    } else {
        digitalWrite(STIM_PIN, LOW);

        currentPulse++;
        // Check if we’ve done enough pulses for this STIM type
        if (currentPulse >= stimTypes[currentType].pulseCount) {
            currentPulse = 0;
            currentType++;
            // Skip disabled types
            while (currentType < 5 && !stimTypes[currentType].enabled) {
                currentType++;
            }

            if (currentType >= 5) {
                // Completed all enabled bursts
                stimRunning = false;
                Serial.println("(Teensy) Burst mode completed.");
                Serial1.println("(Teensy) Burst mode completed.");
                digitalWrite(STIM_PIN, LOW);
                return;
            }
        }

        // Schedule next pulse (HIGH) after the rest of the period
        burstTimer.begin(onSTIMBurst, stimTypes[currentType].period - stimTypes[currentType].pulseWidth);
    }
}


// -----------------------
// Public Control Functions
// -----------------------
void startSTIMContinuous() {
    stimMode = CONTINUOUS;
    stimRunning = true;

    // Immediately schedule the first “LOW → HIGH” event after a full period
    continuousTimer.begin(onSTIMContinuous, stimTypes[0].period);
}

void stopSTIMContinuous() {
    stimRunning = false;
    digitalWrite(STIM_PIN, LOW);
    continuousTimer.end();
}

void startSTIMBurst() {
    if (stimMode == CONTINUOUS && stimRunning) {
        // We’re mid-continuous-pulse; wait for the current S0 cycle to finish
        startBurstPending = true;
        return;
    }
    // Otherwise, start the burst sequence
    stimMode = BURST;
    stimRunning = true;
    currentType = 1;  // Start at S1, skipping S0
    currentPulse = 0;

    // Schedule the first pulse for the new type
    burstTimer.begin(onSTIMBurst, stimTypes[currentType].period);
}

void stopSTIMBurst() {
    stimRunning = false;
    digitalWrite(STIM_PIN, LOW);
    burstTimer.end();
}

// -----------------------
// Update Parameters
// -----------------------
void setSTIMTypeParams(uint8_t type, uint32_t pulseWidthMs, uint32_t periodMs, uint8_t pulseCount, bool enabled) {
    if (type < 1 || type > 5) {
        Serial.printf("Invalid STIM type: %d\n", type);
        return;
    }
    type--; // Convert from 1-based to 0-based indexing

    stimTypes[type].pulseWidth = pulseWidthMs * 1000; // ms → µs
    stimTypes[type].period     = periodMs  * 1000;    // ms → µs
    stimTypes[type].pulseCount = pulseCount;
    stimTypes[type].enabled    = enabled;

    // Apply built-in offset
    stimTypes[type].pulseWidth -= 2;
    stimTypes[type].period     -= 10;

    // For debugging
    // Serial.printf("Type %d: PulseWidth=%dus, Period=%dus, PulseCount=%d, Enabled=%s\n",
    //               type, stimTypes[type].pulseWidth, stimTypes[type].period,
    //               stimTypes[type].pulseCount, enabled ? "ON" : "OFF");
}
