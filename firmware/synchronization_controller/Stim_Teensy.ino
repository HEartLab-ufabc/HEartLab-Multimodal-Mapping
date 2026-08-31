#include <Arduino.h>
#include "stim_control.h"
#include "stim_commands.h"
#include "sync_commands.h"
#include "sync_control.h"

void setup() {
    // Initialize STIM pin/timers
    setupSTIM();

    // Initialize SYNC pin/timers
    setup_sync_control();

    // Initialize USB Serial & UART (Serial1)
    // setupSerialCommands();   
    setupUARTCommands(); 
}

void loop() {
    // Continuously check for commands on both USB Serial and UART
    processAllSerialInputs();    
        // Check if REC just completed
    if (rec_signal_complete) {
      // Print a message to Serial1
      Serial1.println("(Teensy) Recording completed.");
      // Clear the flag
      rec_signal_complete = false;
    }
}
