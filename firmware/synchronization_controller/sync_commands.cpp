#include "sync_commands.h"
#include "sync_control.h"

void handle_serial_sync_command(const String &command) {
    if (command.startsWith("SET_SYNC")) {
        // Format: SET_SYNC <signal> <frequency> <phase_degrees> <duty_cycle>
        // Example: SET_SYNC 1 500 45 50
        int signal, frequency, phase_degrees, duty_cycle;
        
        int firstSpace  = command.indexOf(' ');
        int secondSpace = command.indexOf(' ', firstSpace + 1);
        int thirdSpace  = command.indexOf(' ', secondSpace + 1);
        int fourthSpace = command.indexOf(' ', thirdSpace + 1);

        if (fourthSpace < 0) {
            Serial.println("Invalid SET_SYNC format. Use: SET_SYNC s f p d");
            return;
        }

        signal        = command.substring(firstSpace + 1, secondSpace).toInt();
        frequency     = command.substring(secondSpace + 1, thirdSpace).toInt();
        phase_degrees = command.substring(thirdSpace + 1, fourthSpace).toInt();
        duty_cycle    = command.substring(fourthSpace + 1).toInt();

        set_signal_params(signal, frequency, phase_degrees, duty_cycle);
    }

    else if (command.startsWith("SYNC_START")) {
        // e.g. "SYNC_START 12" to start signals #1 & #2
        String signals = command.substring(command.indexOf(' ') + 1);
        start_signals(signals);
    }

    else if (command.startsWith("SYNC_STOP")) {
        // e.g. "SYNC_STOP 123" to stop signals #1, #2, & #3
        String signals = command.substring(command.indexOf(' ') + 1);
        stop_signals(signals);
    }

    else if (command.startsWith("SYNC_REC")) {
        // e.g. "SYNC_REC 10" => REC active for 10 pulses of SYNC1
        uint32_t pulse_count = command.substring(command.indexOf(' ') + 1).toInt();
        start_rec_signal(pulse_count);
    }

    else {
        Serial.println("Unknown SYNC command.");
    }
}
