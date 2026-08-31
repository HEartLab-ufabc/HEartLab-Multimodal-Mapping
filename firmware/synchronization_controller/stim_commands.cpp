#include "stim_commands.h"
#include "stim_control.h"
#include "sync_commands.h"
#include "sync_control.h"
// #include "nrf24_control.h"

// If you want to use Serial1 at 115200:
static const uint32_t UART_BAUD = 115200;

// ------------------------------------------------------------------
// Setup Serial Ports
// ------------------------------------------------------------------
void setupSerialCommands() {
    // --- USB Serial ---
    Serial.begin(115200);
    while (!Serial) {
        delay(10); // Wait for USB Serial to be ready (Teensy)
    }
    Serial.println("USB Serial Ready");
}

void setupUARTCommands(){
      // --- Hardware Serial1 ---
    Serial1.begin(UART_BAUD);
    // You can optionally wait for Serial1 here, but hardware UART doesn't require the same handshake as USB
    // If you want a message on USB to confirm:
    Serial1.println("(Teensy) UART (Serial1) Ready");
}

// ------------------------------------------------------------------
// Process *all* serial inputs
// ------------------------------------------------------------------
void processAllSerialInputs() {
    // Check USB Serial
    if (Serial.available() > 0) {
        processSerialCommand(Serial);
    }

    // Check Hardware UART (Serial1)
    if (Serial1.available() > 0) {
        processSerialCommand(Serial1);
    }

    // If you had more serial ports, you could call them here:
    // if (Serial2.available() > 0) { processSerialCommand(Serial2); }
    // etc.
}

// ------------------------------------------------------------------
// Command Parsing from Any Stream
// ------------------------------------------------------------------
void processSerialCommand(Stream &stream) {
    // Read a line from whichever stream is passed in
    String command = stream.readStringUntil('\n');
    command.trim();
    if (command.length() == 0) return;  // No actual command
    
    // Echo the command back
    stream.print("(Teensy) Received command: ");
    stream.println(command);

    // ------------------------------------------------
    // Replace ESP.restart() with Teensy’s reboot or omit
    // ------------------------------------------------
    if (command.equals("ESP RESTART")) {
        stream.println("Teensy does not support ESP.restart().");
        // _reboot_Teensyduino_(); // Uncomment if you want a soft reboot
        return;
    }

    // ------------------------------------------------
    // Start / Stop Continuous
    // ------------------------------------------------
    if (command.startsWith("START_CONTINUOUS")) {
        startSTIMContinuous();
        stream.println("(Teensy) S0 mode started.");
    }
    else if (command.startsWith("STOP_CONTINUOUS")) {
        stopSTIMContinuous();
        stream.println("(Teensy) S0 mode stopped.");
    }

    // ------------------------------------------------
    // Start / Stop Burst
    // ------------------------------------------------
    else if (command.startsWith("START_BURST")) {
        startSTIMBurst();
        stream.println("(Teensy) Burst mode started.");
    }
    else if (command.startsWith("STOP_BURST")) {
        stopSTIMBurst();
        stream.println("(Teensy) Burst mode stopped.");
    }

    // ------------------------------------------------
    // Set STIM Parameters
    // Format: SET_PARAMS <type> <pulseWidthMs> <periodMs> <pulseCount> <ON|OFF>
    // e.g.: SET_PARAMS 1 2 1000 10 ON
    // ------------------------------------------------
    else if (command.startsWith("SET_PARAMS")) {
        uint8_t type;
        uint32_t pulseWidthMs;
        uint32_t periodMs;
        uint8_t pulseCount;
        String enableStr;

        int firstSpace = command.indexOf(' ');
        int secondSpace = command.indexOf(' ', firstSpace + 1);
        int thirdSpace = command.indexOf(' ', secondSpace + 1);
        int fourthSpace = command.indexOf(' ', thirdSpace + 1);
        int fifthSpace = command.indexOf(' ', fourthSpace + 1);

        if (fifthSpace > 0) {
            type          = command.substring(firstSpace + 1, secondSpace).toInt();
            pulseWidthMs  = command.substring(secondSpace + 1, thirdSpace).toInt();
            periodMs      = command.substring(thirdSpace + 1, fourthSpace).toInt();
            pulseCount    = command.substring(fourthSpace + 1, fifthSpace).toInt();
            enableStr     = command.substring(fifthSpace + 1);

            bool enabled  = (enableStr == "ON");
            setSTIMTypeParams(type, pulseWidthMs, periodMs, pulseCount, enabled);

            stream.printf("(Teensy) Parameters set for S%d: PW=%d ms, Period=%d ms, Count=%d, Enabled=%s\n",
                          type-1, pulseWidthMs, periodMs, pulseCount, enabled ? "ON" : "OFF");
        } else {
            stream.println("(Teensy) Invalid SET_PARAMS command format.");
        }
    } 
    else if (command.startsWith("SET_SYNC") || command.startsWith("SYNC_")) {
            handle_serial_sync_command(command); // Delegate handling of sync commands to the sync_commands module
    }    
    // ------------------------------------------------
    // Other commands (sync commands, etc.)
    // ------------------------------------------------
    else {
        stream.println("(Teensy) Unknown command.");
    }
}
