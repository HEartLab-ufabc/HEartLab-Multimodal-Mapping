import serial
import serial.tools.list_ports

class SerialHandler:
    def __init__(self):
        self.serial_connection = None

    def list_ports(self):
        """List available serial ports."""
        ports = serial.tools.list_ports.comports()
        return [port.device for port in ports]

    def connect(self, port, baudrate=2000000):
        """Connect to a serial port."""
        try:
            if self.serial_connection and self.serial_connection.is_open:
                self.serial_connection.close()
            self.serial_connection = serial.Serial(port, baudrate, timeout=1)
            return f"Connected to {port}"
        except serial.SerialException as e:
            return f"Failed to connect: {e}"

    def send_command(self, command):
        """Send a command via serial."""
        if self.serial_connection and self.serial_connection.is_open:
            self.serial_connection.write(command.encode())
            return "Command sent"
        return "No connection"

    def disconnect(self):
        """Disconnect the serial connection."""
        if self.serial_connection and self.serial_connection.is_open:
            self.serial_connection.close()
            self.serial_connection = None
            return "Disconnected"
        return "No connection to close"
