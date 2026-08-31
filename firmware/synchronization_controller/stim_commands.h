#ifndef STIM_COMMANDS_H
#define STIM_COMMANDS_H

#include <Arduino.h>

// Sets up all serial ports you want to use (USB Serial, UART, etc.)
void setupSerialCommands();   
void setupUARTCommands(); 

// Processes commands from USB Serial and a hardware UART
void processAllSerialInputs();

// (Optional) A lower-level function that parses commands from *any* Stream object
void processSerialCommand(Stream &stream);

#endif
