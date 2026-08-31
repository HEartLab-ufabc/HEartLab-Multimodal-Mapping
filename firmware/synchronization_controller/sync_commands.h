#ifndef SYNC_COMMANDS_H
#define SYNC_COMMANDS_H

#include <Arduino.h>

// Parses a command string (e.g. "SET_SYNC 1 500 45 50", "SYNC_START 12", "SYNC_STOP 1", "SYNC_REC 10")
// and calls the corresponding sync_control functions
void handle_serial_sync_command(const String &command);

#endif
