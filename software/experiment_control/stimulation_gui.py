import tkinter as tk
from tkinter import ttk
import threading
import re
import time
from hotkey_control import HotkeyControl
from header_info import HeaderInfo
from pynput import keyboard
import json
import win32gui
import win32con
import pyautogui
import os
import subprocess
import datetime
from directory_monitor import DirectoryMonitor
import csv
import datetime
import pygetwindow as gw

class StimulationGUI:
    def __init__(self, root, serial_handler):
        self.root = root
        self.serial_handler = serial_handler
        self.listener = None  # Reference to the key listener
        self.selected_port = tk.StringVar()
        self.status_text = tk.StringVar(value="No serial connection")
        self.stim_data = []
        self.stimulation_status = tk.StringVar(value="OFF")  # New variable for stimulation status
        self.current_time = tk.StringVar(value="")  # Initialize current time
        self.stream_pix_dir = tk.StringVar(value="")  # Initialize the variable with an empty value or default path
        self.directory_monitor = DirectoryMonitor(self.log_received_message)
        self.monitoring_state = tk.BooleanVar(value=False)  # Checkbox state for monitoring
        self.sync_state = tk.BooleanVar(value=False)
        self.sensor_data = {}
        self.sensor_log_file_name = tk.StringVar(value="sensor_log.csv")
        self.sensor_logging_enabled = tk.BooleanVar(value=False)
        self.sensor_plot_window = None
        self.induction_window = None
        self.tank_temp_indicator = None
        self.tank_temp_led = None
        self.elec_recording_flag = 0   # 1 when electrical recording is active
        self.opt_recording_flag = 0    # 1 when optical recording is active

        # Create GUI components
        self.create_serial_port_frame()
        self.create_stimulation_status_frame()
        self.create_stimulation_frame()
        self.create_hotkey_control_frame()
        self.create_recording_control_frame()  # Add this after creating Stimulation Control
        self.create_logging_frame()
        self.create_sensors_frame()


        
        threading.Thread(target=self.monitor_serial, daemon=True).start()

        
        # Load the hotkey configuration
        self.hotkey_config = self.load_hotkey_config()

        # Start the listener
        self.start_hotkey_listener()
        
        # Bind the quit event to a custom method
        self.root.protocol("WM_DELETE_WINDOW", self.on_quit)


    def create_serial_port_frame(self):
        """Create the frame for serial port selection."""
        serial_frame = ttk.LabelFrame(self.root, text="Serial Port Selection")
        serial_frame.grid(row=0, column=0, padx=3, pady=3, sticky="ew", columnspan=1)

        # Dropdown menu for serial ports
        ttk.Label(serial_frame, text="Select Serial Port:").grid(row=0, column=0, padx=5, pady=5)
        self.port_dropdown = ttk.Combobox(serial_frame, textvariable=self.selected_port, state="readonly", width=30)
        self.port_dropdown.grid(row=0, column=1, padx=5, pady=5)

        # Refresh Button
        ttk.Button(serial_frame, text="Refresh", command=self.refresh_ports).grid(row=0, column=2, padx=5, pady=5)

        # Connect Button
        ttk.Button(serial_frame, text="Connect", command=self.connect_serial).grid(row=0, column=3, padx=5, pady=5)

        # Status Label
        ttk.Label(serial_frame, textvariable=self.status_text, foreground="blue").grid(row=1, column=0, columnspan=2, padx=5, pady=10)
        
        # Restart Button
        restart_button = ttk.Button(serial_frame, text="Restart", command=lambda: self.send_command("ESP RESTART"))
        restart_button.grid(row=1, column=3, padx=5, pady=5, sticky="ew")  # Placed below the Connect button

        self.refresh_ports()
            
    def create_stimulation_status_frame(self):
        """Create the frame for stimulation status."""
        status_frame = ttk.LabelFrame(self.root, text="Stimulation Status")
        status_frame.grid(row=0, column=1, padx=3, pady=3, sticky="nsew")
    
        # Configure the status_frame to center its content
        status_frame.grid_rowconfigure(0, weight=1)
        status_frame.grid_columnconfigure(0, weight=1)
    
        # Use a tk.Frame for precise control of background color
        frame_inner = tk.Frame(status_frame, bg=self.root["bg"])
        frame_inner.grid(row=0, column=0, sticky="nsew")
        frame_inner.grid_rowconfigure(0, weight=1)
        frame_inner.grid_columnconfigure(0, weight=1)  # Center horizontally
    
        # Create a Canvas for the LED indicator
        self.canvas = tk.Canvas(
            frame_inner,
            width=50,
            height=50,
            bg=frame_inner["bg"],  # Match the tk.Frame background color
            highlightthickness=0
        )
        self.canvas.grid(row=0, column=0, padx=10, pady=10)  # Center the canvas
    
        # Draw a black circle to represent the inactive LED
        self.led = self.canvas.create_oval(5, 5, 45, 45, fill="black")  # Ensure proper circle proportions
                   
    def refresh_ports(self):
        """Refresh the list of available serial ports."""
        ports = self.serial_handler.list_ports()
        if ports:
            self.port_dropdown["values"] = ports
            self.selected_port.set(ports[0])
        else:
            self.port_dropdown["values"] = []
            self.selected_port.set("")
            self.status_text.set("No serial ports available")

    def connect_serial(self):
        """Connect to the selected serial port."""
        if not self.selected_port.get():
            self.status_text.set("No serial port selected")
            return

        self.status_text.set(self.serial_handler.connect(self.selected_port.get()))            

    def monitor_serial(self):
        """Continuously monitor the serial port for specific messages, handle logging, LED updates, and sensor updates."""
        starts_with_exceptions = [
            "ESP-ROM", "Build", "rst", "SPIWP", "mode", "load", "entry",
            "Default frequency", "Received command:", "Starting Continuous",
            "Serial Commands Ready", "PULSE", "Stopping Continuous", "Received:"
        ]  # Messages starting with these will be ignored
        contains_exceptions = []  # Messages containing these substrings will be ignored
    
        while True:
            if self.serial_handler.serial_connection and self.serial_handler.serial_connection.is_open:
                try:
                    # Read the incoming message
                    line = self.serial_handler.serial_connection.readline().decode().strip()
                    if not line:  # Ignore empty lines
                        continue
    
                    # Update LED based on Teensy mode messages
                    if "(Teensy) S0 mode started" in line:
                        self.canvas.itemconfig(self.led, fill="#00FF00")
                    elif "(Teensy) Burst mode started" in line:
                        self.canvas.itemconfig(self.led, fill="#00BFFF")
                    elif "(Teensy) Burst mode stopped" in line or "(Teensy) Burst mode completed" in line or "(Teensy) S0 mode stopped" in line:
                        self.canvas.itemconfig(self.led, fill="black")
    
                    # Handle SENSORS messages for updating the Sensors frame
                    if line.startswith("Received: SN2"):
                        # expected: level, temp, flow1, temp1, press1
                        match = re.match(r"Received: SN2 (-?\d+)\s+(-?\d+)\s+(-?\d+)\s+(-?\d+)", line)
                        if match:
                            line1_flow, line1_temp, line1_pressure, tank_temp = match.groups()

                            # UI updates (Tank: temp only, Line 1: all)
                            self.update_sensors_frame("Tank", {"Temperature": tank_temp})
                            self.update_sensors_frame("Line 1", {
                                "Pressure": line1_pressure,
                                "Flow Rate": line1_flow,
                                "Temperature": line1_temp
                            })

                            # optional logging
                            if hasattr(self, "sensor_logging_enabled") and self.sensor_logging_enabled.get():
                                try:
                                    with open(self.sensor_log_file_name.get(), "a", newline="") as f:
                                        writer = csv.writer(f)

                                        now = datetime.datetime.now()
                                        timestamp = now.strftime("%Y-%m-%d %H:%M:%S.") + f"{now.microsecond // 1000:03d}"
                                        row = [
                                            timestamp, "SN1",    
                                            self.elec_recording_flag,          # electrical rec flag
                                            self.opt_recording_flag,           # optical rec flag
                                            f"{float(tank_temp)/100:.2f}",                                        
                                            f"{float(line1_flow)/100:.2f}",
                                            f"{float(line1_temp)/100:.2f}",
                                            f"{float(line1_pressure)/100:.2f}"                                            
                                        ]
                                        writer.writerow(row)
                                except Exception as e:
                                    print(f"Error logging sensor SN1 data: {e}")

                    if line.startswith("Received: SN1"):
                        # you can just log it if logging is on
                        if hasattr(self, "sensor_logging_enabled") and self.sensor_logging_enabled.get():
                            try:
                                with open(self.sensor_log_file_name.get(), "a", newline="") as f:
                                    writer = csv.writer(f)
                                    now = datetime.datetime.now()
                                    timestamp = now.strftime("%Y-%m-%d %H:%M:%S.") + f"{now.microsecond // 1000:03d}"
                                    writer.writerow([timestamp, "SN2", "","","",""])
                            except Exception as e:
                                print(f"Error logging sensor SN2 data: {e}")
                        # no UI update — we don’t have Line 2 / Reservoir anymore

                                    
                    # Skip logging for messages matching exception rules
                    if any(line.startswith(prefix) for prefix in starts_with_exceptions):
                        continue
                    if any(substring in line for substring in contains_exceptions):
                        continue
    
                    # Log valid messages
                    self.log_received_message(line)
    
                except Exception as e:
                    print(f"Error reading serial: {e}")
            time.sleep(0.1)  # Polling interval


    def log_received_message(self, message):
        """Log received serial messages to the log file."""
        timestamp = datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3]  # Timestamp with milliseconds
        log_entry = f"[{timestamp}] {message}"
        try:
            with open(self.log_file_name.get(), "a") as log_file:
                log_file.write(log_entry + "\n")
            print(f"Logged serial message: {log_entry}")
        except Exception as e:
            print(f"Failed to log serial message: {e}")

            
    def create_hotkey_control_frame(self):
        """Create the Hotkey Control frame with a button to open a new window."""
        hotkey_frame = ttk.LabelFrame(self.root, text="Hotkey Control")
        hotkey_frame.grid(row=0, column=2, padx=3, pady=3, sticky="nsew", columnspan=1)
    
        # Add the "Open Hotkey Control" button
        open_hotkey_button = ttk.Button(hotkey_frame, text="Open Hotkey Control", command=self.open_hotkey_window)
        open_hotkey_button.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        
    def open_hotkey_window(self):
        """Open the Hotkey Control window."""
        def reload_hotkey_config():
            """Reload the hotkey configuration after the Hotkey Control window is closed."""
            self.hotkey_config = self.load_hotkey_config()  # Reload the JSON file
            print(f"Hotkey configuration reloaded: {self.hotkey_config}")
    
        # Pass the reload callback to the Hotkey Control
        self.hotkey_control = HotkeyControl(self.root, on_close_callback=reload_hotkey_config)
        
    def load_hotkey_config(self):
        """Load hotkey configuration from a JSON file."""
        try:
            with open("hotkey_config.json", "r") as file:
                return json.load(file)
        except FileNotFoundError:
            print("Hotkey configuration file not found. Using default.")
            return {f"f{i}": {"command": "None", "description": "--"} for i in range(1, 13)}
        except json.JSONDecodeError:
            print("Invalid JSON format. Using default.")
            return {f"f{i}": {"command": "None", "description": "--"} for i in range(1, 13)}

        
    def reload_hotkey_config(self):
        """Reload the hotkey configuration from the JSON file."""
        try:
            with open("hotkey_config.json", "r") as file:
                self.hotkey_config = json.load(file)
            print("Hotkey configuration reloaded successfully.")
        except FileNotFoundError:
            print("Hotkey configuration file not found. Using default configuration.")
        except Exception as e:
            print(f"Error reloading hotkey configuration: {e}")


    def start_hotkey_listener(self):
        """Start the hotkey listener."""
        print("Starting hotkey listener...")
        self.listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        self.listener.start()
        print("Hotkey listener started.")


    def process_hotkey(self, key_name):
        """Process the detected hotkey."""
        config = self.hotkey_config.get(key_name, None)
        if config and config['command'] != 'None':
            print(f"Hotkey detected: {key_name} -> {config['command']}")
            self.send_command(config['command'])
    
    def on_press(self, key):
        """Handle key press events."""
        try:
            if hasattr(key, 'name') and key.name in self.hotkey_config:
                config = self.hotkey_config[key.name]
                if config['command'] != 'None':
                    print(f"Hotkey detected: {key.name} -> {config['command']}")
                    self.send_command(config['command'])
        except Exception as e:
            print(f"Error in on_press: {e}")
            
    def on_release(self, key):
        """Handle key release events."""  

    def validate_integer_input(self, new_value):
        """Ensure only integers are entered."""
        if new_value == "" or new_value.isdigit():
            return True
        return False              


    def send_command(self, command):
        """Send a command via the serial connection."""
        try:
            if self.serial_handler.serial_connection and self.serial_handler.serial_connection.is_open:
                self.serial_handler.serial_connection.write(f"{command}\n".encode())
                print(f"Command sent: {command}")
            else:
                print(f"Error: Serial connection is not open.")
        except Exception as e:
            print(f"Error sending command: {e}")        

    def create_stimulation_frame(self):
        """Create the frame for stimulation control."""
        stim_frame = ttk.LabelFrame(self.root, text="Stimulation Control")
        stim_frame.grid(row=1, column=0, padx=3, pady=3, sticky="ew", columnspan=3)
    
        # Create subframes for S0 to S4
        for i in range(5):
            subframe = ttk.LabelFrame(stim_frame, text=f"S{i}")
            subframe.grid(row=0, column=i, padx=5, pady=5, sticky="nsew")
            self.create_stim_fields(subframe, i)
    
        # Unified Start/Stop Burst Button
        self.burst_state = tk.BooleanVar(value=False)  # False = Stopped, True = Started
        self.start_stop_burst_button = ttk.Button(
            stim_frame, text="Start Burst", command=self.toggle_burst
        )
        self.start_stop_burst_button.grid(row=1, column=0, columnspan=5, pady=10)

        # Induction Protocol button
        self.induction_button = ttk.Button(
            stim_frame,
            text="Induction Protocol",
            command=self.open_induction_protocol_window,
        )
        self.induction_button.grid(row=2, column=0, columnspan=5, pady=5)

    def open_induction_protocol_window(self):
        """Open (or raise) the Induction Protocol window."""
        from induction_protocol_window import InductionProtocolWindow

        # If it doesn't exist or was destroyed, recreate it
        if self.induction_window is None or not self.induction_window.winfo_exists():
            self.induction_window = InductionProtocolWindow(self.root, gui_ref=self)
        else:
            # If already open, just bring it to front
            self.induction_window.lift()
            self.induction_window.focus_set()

    def create_stim_fields(self, subframe, stim_index):
        """Create input fields, a checkbox, and Apply button for a stimulation subframe."""
        stim_settings = {
            "pulse_width": tk.StringVar(value="2"),  # Default in ms
            "period": tk.StringVar(value="1000"),   # Default in ms
            "num_pulses": tk.StringVar(value="8"),  # Default
            "enabled": tk.BooleanVar(value=False)   # Default disabled
        }
        self.stim_data.append(stim_settings)
        
        # Validation command
        vcmd = (self.root.register(self.validate_integer_input), "%P")
        
        # Pulse Width
        ttk.Label(subframe, text="Pulse Width (ms):").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        ttk.Entry(subframe, textvariable=stim_settings["pulse_width"], width=10, validate="key", validatecommand=vcmd).grid(
            row=0, column=1, padx=5, pady=5
        )
        
        # Period
        ttk.Label(subframe, text="Period (ms):").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        ttk.Entry(subframe, textvariable=stim_settings["period"], width=10, validate="key", validatecommand=vcmd).grid(
            row=1, column=1, padx=5, pady=5
        )
        
        # Num Pulses (only for S1-S4)
        if stim_index > 0:
            ttk.Label(subframe, text="Num Pulses:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
            ttk.Entry(subframe, textvariable=stim_settings["num_pulses"], width=10, validate="key", validatecommand=vcmd).grid(
                row=2, column=1, padx=5, pady=5
            )
            ttk.Checkbutton(subframe, text="Enabled", variable=stim_settings["enabled"]).grid(
                row=3, column=0, columnspan=2, padx=5, pady=5
            )
        
        # Apply Button
        ttk.Button(subframe, text="Apply", command=lambda: self.apply_stim_settings(stim_index)).grid(
            row=4, column=0, columnspan=2, padx=5, pady=5
        )
    
        # Unified Start/Stop Button for S0
        if stim_index == 0:
            self.s0_state = tk.BooleanVar(value=False)  # False = OFF, True = ON
            self.start_stop_button = ttk.Button(
                subframe, text="Start", command=self.toggle_stim
            )
            self.start_stop_button.grid(row=5, column=0, columnspan=2, padx=5, pady=5)
            
    def toggle_stim(self):
        """Toggle stimulation between Start and Stop for S0."""
        if not self.s0_state.get():  # Currently OFF
            self.start_stim()
            self.start_stop_button.config(text="Stop")
            self.s0_state.set(True)
        else:  # Currently ON
            self.stop_stim()
            self.start_stop_button.config(text="Start")
            self.s0_state.set(False)
            
    def toggle_burst(self):
        """Toggle between Start Burst and Stop Burst."""
        if not self.burst_state.get():  # Currently Stopped
            self.start_burst()
            self.start_stop_burst_button.config(text="Stop Burst")
            self.burst_state.set(True)
            
            # Schedule returning to Start Burst / Start after 5 seconds
            self.root.after(5000, self.reset_burst_button)
            self.root.after(5000, self.reset_stim_button)
            
        else:  # Currently Started
            self.stop_burst()
            self.start_stop_burst_button.config(text="Start Burst")
            self.burst_state.set(False)
            
    def reset_burst_button(self):
        """Reset the Start/Stop Burst button to Start Burst."""
        self.burst_state.set(False)
        self.start_stop_burst_button.config(text="Start Burst")
        
    def reset_stim_button(self):
        """Reset the Start/Stop button to Start."""
        self.s0_state.set(False)
        self.start_stop_button.config(text="Start")

    def apply_stim_settings(self, stim_index):
        """Apply settings for a specific stimulation subframe and send a serial command."""
        settings = self.stim_data[stim_index]
        pulse_width = settings["pulse_width"].get()
        period = settings["period"].get()
    
        # Default values for S0
        num_pulses = "1"
        state = "ON"
    
        # For S1-S4, get `num_pulses` and `state` from settings
        if stim_index > 0:
            num_pulses = settings["num_pulses"].get()
            state = "ON" if settings["enabled"].get() else "OFF"
    
        # Construct the command
        command = f"SET_PARAMS {stim_index + 1} {pulse_width} {period} {num_pulses} {state}\n"
        print(f"Sending command: {command.strip()}")
    
        # Send the command via serial
        if self.serial_handler.serial_connection and self.serial_handler.serial_connection.is_open:
            self.serial_handler.serial_connection.write(command.encode())
        else:
            print("No active serial connection.")

    def start_stim(self):
        """Send command to start stimulation for S0."""
        command = "START_CONTINUOUS"
        print(f"Sending command: {command}")
        self.send_command(command)
    
    def stop_stim(self):
        """Send command to stop stimulation for S0."""
        command = "STOP_CONTINUOUS"
        print(f"Sending command: {command}")
        self.send_command(command)
    
    def start_burst(self):
        """Send command to start burst stimulation."""
        command = "START_BURST"
        print(f"Sending command: {command}")
        self.send_command(command)
    
    def stop_burst(self):
        """Send command to stop burst stimulation."""
        command = "STOP_BURST"
        print(f"Sending command: {command}")
        self.send_command(command)
            
    def create_recording_control_frame(self):
        """Create the frame for recording control."""
        recording_frame = ttk.LabelFrame(self.root, text="Recording Control")
        recording_frame.grid(row=2, column=0, padx=3, pady=3, sticky="ew", columnspan=3)  # Positioned below Stimulation Control
        
        # Add subframes for Sync 1, Sync 2, Sync 3, and Sync Recording
        self.create_sync_subframes(recording_frame)
        
    def create_sync_subframes(self, parent_frame):
        """Create subframes for Sync 1, Sync 2, Sync 3, and Sync Recording."""
        sync_data = {}  # Store settings for each sync

        parent_frame.grid_columnconfigure(1, weight=1)
    
        # Add Sync Recording Subframe
        sync_rec_frame = ttk.LabelFrame(parent_frame, text="Sync Recording")
        sync_rec_frame.grid(row=0, column=1, padx=10, pady=5, sticky="nsew")  # Side by side with Sync 1, 2, 3
    
        # Configure columns within Sync Recording frame
        sync_rec_frame.grid_columnconfigure(0, weight=1)  # Left padding
        sync_rec_frame.grid_columnconfigure(1, weight=1)  # Right padding
    
        # Record Frames Field with default value
        rec_frames_var = tk.StringVar(value="5005")  # Default: 5005 frames
        ttk.Label(sync_rec_frame, text="Record Frames (total):").grid(row=0, column=1, padx=5, pady=5, sticky="w")
        rec_frames_entry = ttk.Entry(sync_rec_frame, textvariable=rec_frames_var, width=10)
        rec_frames_entry.grid(row=0, column=1, padx=5, pady=5)
    
        # StreamPix Window Field
        ttk.Label(sync_rec_frame, text="StreamPix Window:").grid(row=1, column=1, padx=5, pady=5, sticky="w")
        stream_pix_var = tk.StringVar(value="StreamPix 9")  # Default value
        stream_pix_entry = ttk.Entry(sync_rec_frame, textvariable=stream_pix_var, width=20)
        stream_pix_entry.grid(row=1, column=1, padx=5, pady=5)

        # OpenEphys Window Field
        ttk.Label(sync_rec_frame, text="OpenEphys Window:").grid(row=2, column=1, padx=5, pady=5, sticky="w")
        openephys_var = tk.StringVar(value="Open Ephys GUI")  # Default value
        openephys_entry = ttk.Entry(sync_rec_frame, textvariable=openephys_var, width=20)
        openephys_entry.grid(row=2, column=1, padx=5, pady=5)
        
        # Enable Checkbox for Sync Recording
        rec_enable_var = tk.BooleanVar(value=True)  # Default: Enabled
        rec_enable_check = ttk.Checkbutton(sync_rec_frame, text="Enable", variable=rec_enable_var)
        rec_enable_check.grid(row=3, column=0, columnspan=2, pady=5)
    
        # Centralized Record Start Button
        record_start_button = ttk.Button(sync_rec_frame, text="Record Start", command=self.record_start)
        record_start_button.grid(row=4, column=0, columnspan=2, padx=20, pady=5, sticky="")  # Narrower and centered
    
        # Store Sync Recording references
        sync_data["sync_recording"] = {
            "record_frames": rec_frames_var,
            "stream_pix": stream_pix_var,
            "openephys": openephys_var,
            "enabled": rec_enable_var,
        }
    
        # Store sync settings for access across methods
        self.sync_data = sync_data        
      
    def stop_sync(self):
        """Send SYNC_STOP command for all Sync subframes."""
        command = "SYNC_STOP 1 2 3\n"
        if self.serial_handler.serial_connection and self.serial_handler.serial_connection.is_open:
            self.serial_handler.serial_connection.write(command.encode())
            print(f"Command sent: {command.strip()}")
        else:
            print("No active serial connection.")          
    
    def bring_window_to_front(self, window_title):
        """Bring a specific window to the front by its title."""
        hwnd = win32gui.FindWindow(None, window_title)
        if hwnd:
            win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)  # Restore if minimized
            win32gui.SetForegroundWindow(hwnd)  # Bring to the front
            print(f"Brought window '{window_title}' to the front.")
        else:
            print(f"Window with title '{window_title}' not found.")
        
    def record_start(self):
        """Handle the recording process with combined functionality."""
        try:
            # Pause induction protocol if its window is open
            if hasattr(self, "induction_window"):
                win = self.induction_window
                if win is not None and win.winfo_exists():
                    try:
                        win.pause_from_record_start()
                    except Exception as e:
                        print(f"Error pausing induction protocol from Record Start: {e}")

            # Step 1: Check if Sync Recording is enabled
            sync_rec = self.sync_data["sync_recording"]
            if sync_rec["enabled"].get():
                # Send SYNC_STOP 1
                command_stop = "SYNC_STOP 1\n"
                if self.serial_handler.serial_connection and self.serial_handler.serial_connection.is_open:
                    self.serial_handler.serial_connection.write(command_stop.encode())
                    print(f"Command sent: {command_stop.strip()}")
                else:
                    print("No active serial connection.")
                
                # Wait 100ms (non-blocking)
                time.sleep(0.1)
    
                # Send SYNC_REC XX
                frames = sync_rec["record_frames"].get()
                try:
                    frames_int = int(frames)  # Ensure it's an integer
                    command_rec = f"SYNC_REC {frames_int}\n"
                    if self.serial_handler.serial_connection and self.serial_handler.serial_connection.is_open:
                        self.serial_handler.serial_connection.write(command_rec.encode())
                        print(f"Command sent: {command_rec.strip()}")
                    else:
                        print("No active serial connection.")
                except ValueError:
                    print("Invalid Record Frames value. Ensure it is a valid integer.")
    
            # Step 2: Bring the StreamPix Window to the front
            stream_pix_title = sync_rec["stream_pix"].get()
            self.bring_window_to_front(stream_pix_title)
    
            # Step 3: Simulate Ctrl+R
            pyautogui.hotkey("ctrl", "r")
            print("Simulated Ctrl+R")
            
            # Step 4: Bring the OpenEphys Window to the front
            openephys_title = sync_rec["openephys"].get()
            self.bring_window_to_front(openephys_title)
    
            # # Click in the record button
            win = gw.getWindowsWithTitle(openephys_title)[0]
            rec_x = win.right - 225
            rec_y = win.top + 75
            pyautogui.click(rec_x, rec_y)
            
            # Wait 100ms (non-blocking)
            time.sleep(0.1)
    
            # Step 4: Send SYNC_START 1
            command_start = "SYNC_START 1\n"
            if self.serial_handler.serial_connection and self.serial_handler.serial_connection.is_open:
                self.serial_handler.serial_connection.write(command_start.encode())
                print(f"Command sent: {command_start.strip()}")
            else:
                print("No active serial connection.")

            rec_enabled = self.sync_data["sync_recording"]["enabled"].get()
            if rec_enabled:
                # Enable on → both electric and optical are considered active
                self.elec_recording_flag = 1
                self.opt_recording_flag = 1
            else:
                # Enable off → only electrical recording
                self.elec_recording_flag = 1
                self.opt_recording_flag = 0  
                
            # Automatically turn off both after 10 seconds
            self.root.after(10_000, self._auto_disable_recording_flags)
    
        except Exception as e:
            print(f"Error in Record Start: {e}")
            # In case of error, we consider that no recording is active
            self.elec_recording_flag = 0
            self.opt_recording_flag = 0

    def _auto_disable_recording_flags(self):
        """Turn off recording flags after 10 seconds."""
        self.elec_recording_flag = 0
        self.opt_recording_flag = 0
            
    def create_logging_frame(self):
        """Create the frame for logging controls."""
        logging_frame = ttk.LabelFrame(self.root, text="Logging")
        logging_frame.grid(row=3, column=0, padx=3, pady=3, sticky="ew", columnspan=3)  # Positioned below all other frames
    
        # Configure the grid for the logging frame
        logging_frame.grid_columnconfigure(0, weight=1)  # For "Select Path"
        logging_frame.grid_columnconfigure(1, weight=2)  # For "File Name"
        logging_frame.grid_columnconfigure(2, weight=1)  # For "Header Info"
        logging_frame.grid_columnconfigure(3, weight=1)  # For "Create Log"
        logging_frame.grid_columnconfigure(4, weight=1)  # For "Log"
        logging_frame.grid_columnconfigure(4, weight=1)  # For "Open Log"
        logging_frame.grid_columnconfigure(5, weight=2)  # For "Time Stamp"
        logging_frame.grid_columnconfigure(5, weight=3)  # For "Note"
    
        # Variables for file name and note
        self.log_file_name = tk.StringVar(value="logfile.txt")
        self.log_note = tk.StringVar(value="")
    
        # Select Path Button
        select_path_button = ttk.Button(logging_frame, text="Select Path", command=self.select_path)
        select_path_button.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
    
        # File Name Entry
        file_name_entry = ttk.Entry(logging_frame, textvariable=self.log_file_name, width=25)
        file_name_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
    
        # Header Info Button
        header_info_button = ttk.Button(logging_frame, text="Header Info", command=self.open_header_info_window)
        header_info_button.grid(row=0, column=2, padx=5, pady=5, sticky="ew")

    
        # Create Log Button
        create_log_button = ttk.Button(logging_frame, text="Create Log", command=self.create_log)
        create_log_button.grid(row=0, column=3, padx=5, pady=5, sticky="ew")
        
        # Open Log Button
        open_log_button = ttk.Button(logging_frame, text="Open Log", command=self.open_log)
        open_log_button.grid(row=0, column=4, padx=5, pady=5, sticky="ew")
        
        # Time Stamp Label
        time_stamp_label = ttk.Label(logging_frame, textvariable=self.current_time, anchor="center")
        time_stamp_label.grid(row=0, column=5, padx=5, pady=5, sticky="ew")
        
        # StreamPix Saving Dir Button and Entry
        ttk.Label(logging_frame, text="StreamPix Saving Dir:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        dir_entry = ttk.Entry(logging_frame, textvariable=self.stream_pix_dir, width=25)
        dir_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        dir_button = ttk.Button(logging_frame, text="Select Dir", command=self.select_stream_pix_dir)
        dir_button.grid(row=1, column=2, padx=5, pady=5, sticky="ew")
    
        # Start Monitoring Checkbox
        monitor_checkbox = ttk.Checkbutton(
            logging_frame,
            text="Start Monitoring",
            variable=self.monitoring_state,
            command=self.toggle_monitoring
        )
        monitor_checkbox.grid(row=1, column=3, columnspan=2, padx=5, pady=5, sticky="ew")
            
        # Log Button
        log_button = ttk.Button(logging_frame, text="Log", command=self.log_data)
        log_button.grid(row=2, column=0, padx=5, pady=5, sticky="ew", columnspan=1)  # Spanning 1 columns for alignment
    
        # Note Entry
        note_entry = ttk.Entry(logging_frame, textvariable=self.log_note, width=50)
        note_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew", columnspan=5)  # Spanning 5 columns for alignment
        
        # Bind the "Enter" key press to log_data when the note entry is focused
        note_entry.bind("<Return>", self.log_data)

        # Start the time update
        self.update_time()
        
    def toggle_monitoring(self):
        """Toggle the directory monitoring state based on the checkbox."""
        if self.monitoring_state.get():
            self.directory_monitor.start(self.stream_pix_dir.get())
        else:
            self.directory_monitor.stop()

    def select_stream_pix_dir(self):
        """Open a directory selection dialog for StreamPix saving directory."""
        from tkinter import filedialog
        selected_dir = filedialog.askdirectory()
        if selected_dir:
            self.stream_pix_dir.set(selected_dir)
            print(f"Selected directory: {selected_dir}")        
              
    def select_path(self):
        from tkinter import filedialog
        selected_path = filedialog.askdirectory(parent=self.root)
        if selected_path:
            self.log_file_name.set(selected_path)
            print(f"Selected path: {selected_path}")
            
    def create_log(self):
        """Create a new log file."""
        try:
            with open(self.log_file_name.get(), "w") as log_file:
                log_file.write("Log Created\n")
            print(f"Log file created at: {self.log_file_name.get()}")
        except Exception as e:
            print(f"Error creating log file: {e}")
            
    def open_log(self):
        """Open a new log file."""
        log_path = self.log_file_name.get()
        
        try:
            if os.path.exists(log_path):
                # Open file in the default editor based on the platform
                if os.name == 'nt':  # Windows
                    os.startfile(log_path)
                elif os.name == 'posix':  # Linux/Mac
                    subprocess.run(['xdg-open', log_path], check=True)
                else:
                    print("Unsupported OS for opening the file.")
            else:
                print("File Not Found", f"The file '{log_path}' does not exist.")
        except Exception as e:
            print("Error", f"Failed to open file: {e}")
            
    def update_time(self):
        """Update the time stamp every second."""
        now = datetime.datetime.now()
        self.current_time.set(now.strftime("Time: %H:%M:%S -- %m-%d-%Y"))  # Format: HH:MM:SS
        self.root.after(1000, self.update_time)  # Schedule the next update in 1 second

            
    def open_header_info_window(self):
        """Open the Header Info configuration window."""
        self.header_info_window = HeaderInfo(self.root, self.log_file_name.get())
    
    def log_data(self, event=None):
        """Log data and a note to the log file."""
        log_text = self.log_note.get().strip()  # Get the text and strip extra spaces
        if not log_text:  # Do nothing if the field is empty
            return
    
        try:
            # Get the current timestamp in the desired format
            now = datetime.datetime.now()
            timestamp = now.strftime("[%H:%M:%S.") + f"{now.microsecond // 1000:03d}]"  # Milliseconds only
    
            # Write to the log file
            with open(self.log_file_name.get(), "a") as log_file:
                log_file.write(f"{timestamp} Note: {log_text}\n")
            
            print(f"Logged: {timestamp} {log_text}")  # Debug message in console
            self.log_note.set("")  # Clear the log note field after logging
        except Exception as e:
            print(f"Error logging data: {e}")   
    
    def on_quit(self):
        """Ask for confirmation before quitting and stop the key listener."""
        if tk.messagebox.askyesno("Quit", "Are you sure you want to quit?"): # type: ignore[arg-type]
            # Stop the key listener
            if self.listener:
                self.listener.stop()
                print("Key listener stopped.")
            
            # Close the serial connection
            if self.serial_handler.serial_connection and self.serial_handler.serial_connection.is_open:
                self.serial_handler.serial_connection.close()
                print("Serial port closed.")
            
            # Destroy the GUI window
            self.root.destroy()
            
    def start_directory_monitoring(self):
        """Start monitoring the StreamPix saving directory."""
        directory_to_monitor = self.stream_pix_dir.get()
        if not directory_to_monitor:
            print("No directory selected for monitoring.")
            return
    
        self.directory_monitor.start(directory_to_monitor)
        
    def stop_directory_monitoring(self):
        """Stop the directory monitoring observer."""
        self.directory_monitor.stop()
        self.root.destroy()

    def create_sensors_frame(self):
        """Create a minimal sensors panel: Tank (temp only) + Line 1 (all)."""
        sensors_frame = ttk.LabelFrame(self.root, text="Sensors")
        sensors_frame.grid(row=4, column=0, columnspan=3, padx=3, pady=3, sticky="nsew")

        # top row: logging controls for sensors
        top = ttk.Frame(sensors_frame)
        top.grid(row=0, column=0, columnspan=2, sticky="ew", padx=5, pady=5)
        top.columnconfigure(1, weight=1)

        # use vars created in __init__
        btn_path = ttk.Button(top, text="Select Sensor Log Path", command=self.select_sensor_log_path)
        btn_path.grid(row=0, column=0, padx=5, pady=2, sticky="ew")

        entry_file = ttk.Entry(top, textvariable=self.sensor_log_file_name)
        entry_file.grid(row=0, column=1, padx=5, pady=2, sticky="ew")

        btn_create = ttk.Button(top, text="Create Sensor Log", command=self.create_sensor_log)
        btn_create.grid(row=0, column=2, padx=5, pady=2, sticky="ew")

        chk_enable = ttk.Checkbutton(top, text="Enable Sensor Logging", variable=self.sensor_logging_enabled)
        chk_enable.grid(row=0, column=3, padx=5, pady=2, sticky="ew")
        
        # Button to open the live sensor graphs window
        btn_graphs = ttk.Button(top, text="Live Sensor Graphs", command=self.open_sensor_plot_window)
        btn_graphs.grid(row=0, column=4, padx=5, pady=2, sticky="ew")

        # 1) Tank -> only Temperature
        tank_subframe = self.create_sensor_subframe(
            parent_frame=sensors_frame,
            title="Tank",
            fields_with_units={"Temperature": "°C"},
            row=1,
            col=0
        )

        # Small circular LED indicator next to Tank Temperature (row 0, col 2)
        self.tank_temp_indicator = tk.Canvas(
            tank_subframe,
            width=20,
            height=20,
            highlightthickness=0
        )
        self.tank_temp_indicator.grid(row=0, column=2, padx=5, pady=5, sticky="w")

        # Draw the LED (start as black / off)
        self.tank_temp_led = self.tank_temp_indicator.create_oval(
            2, 2, 18, 18,
            fill="black",
            outline=""
        )

        # 2) Line 1 -> Pressure, Temperature, Flow Rate
        self.create_sensor_subframe(
            parent_frame=sensors_frame,
            title="Line 1",
            fields_with_units={"Pressure": "mmHg", "Temperature": "°C", "Flow Rate": "mL/min"},
            row=1,
            col=1
        )

        # Start periodic temperature indicator updates
        self.update_tank_temperature_indicator()

    def update_tank_temperature_indicator(self):
        """
        Update the Tank Temperature LED based on Tank_Temperature value:
          - < 37°C  -> blink blue
          - 37–39°C -> solid green
          - > 39°C  -> blink red
          - invalid / missing -> grey
        """
        # If the canvas isn't ready yet, try again later
        if self.tank_temp_indicator is None or self.tank_temp_led is None:
            self.root.after(1000, self.update_tank_temperature_indicator)
            return

        # Get the displayed tank temperature from sensor_data
        temp = None
        value_var = self.sensor_data.get("Tank_Temperature")
        if value_var is not None:
            raw = value_var.get()
            try:
                temp = float(raw)
            except (ValueError, TypeError):
                temp = None

        # Decide base color + blinking mode
        color = "grey"
        blink = False

        if temp is not None:
            if temp < 37.0:
                color = "blue"
                blink = True
            elif 37.0 <= temp <= 39.0:
                color = "green"
                blink = False
            else:  # temp > 39
                color = "red"
                blink = True

        if blink:
            # Toggle between color and "off" (no fill) to blink
            current = self.tank_temp_indicator.itemcget(self.tank_temp_led, "fill")
            new_color = color if current == "" else ""
            self.tank_temp_indicator.itemconfig(self.tank_temp_led, fill=new_color)
        else:
            # Solid color
            self.tank_temp_indicator.itemconfig(self.tank_temp_led, fill=color)

        # Schedule next update
        self.root.after(500, self.update_tank_temperature_indicator)


    def select_sensor_log_path(self):
        from tkinter import filedialog
        selected_path = filedialog.askdirectory(parent=self.root)
        if selected_path:
            # log file will live inside that directory
            self.sensor_log_file_name.set(os.path.join(selected_path, "sensor_log.csv"))
            print(f"Selected sensor log path: {self.sensor_log_file_name.get()}")

    def create_sensor_log(self):
        """Create CSV with columns only for what we actually show."""
        try:
            with open(self.sensor_log_file_name.get(), "w", newline="") as f:
                writer = csv.writer(f)
                # minimal header for our reduced panel
                header = [
                    "Timestamp", "MessageType",
                    "ElecRec", "OptRec",
                    "Tank Temperature",
                    "Line1 Flow", "Line1 Temperature", "Line1 Pressure"
                ]
                writer.writerow(header)
            print(f"Sensor CSV log file created at: {self.sensor_log_file_name.get()}")
        except Exception as e:
            print(f"Error creating sensor CSV log file: {e}")

    def create_sensor_subframe(self, parent_frame, title, fields_with_units, row, col=0):
        subframe = ttk.LabelFrame(parent_frame, text=title)
        subframe.grid(row=row, column=col, padx=10, pady=5, sticky="nsew")
        subframe.grid_columnconfigure(0, weight=1)
        subframe.grid_columnconfigure(1, weight=1)

        for r, (field, unit) in enumerate(fields_with_units.items()):
            ttk.Label(subframe, text=f"{field} ({unit}):").grid(row=r, column=0, padx=5, pady=5, sticky="w")
            value_var = tk.StringVar(value="N/A")
            ttk.Entry(subframe, textvariable=value_var, width=15, state="readonly").grid(row=r, column=1, padx=5, pady=5)
            # key like "Tank_Temperature" or "Line 1_Pressure"
            self.sensor_data[f"{title}_{field}"] = value_var

        return subframe

    def update_sensors_frame(self, title, updates: dict):
        """
        Update sensor entries if they exist and forward numeric data to
        the live plot window (if it is open).

        `title` examples: "Tank", "Line 1"
        `updates` keys: "Pressure", "Temperature", "Flow Rate"
        """
        for field, value in updates.items():
            key = f"{title}_{field}"
            plot_value = None  # numeric value for plotting, if applicable

            if field in ["Pressure", "Temperature", "Flow Rate"]:
                try:
                    numeric = float(value) / 100.0  # ints*100 from ESP
                    plot_value = numeric
                    display_value = f"{numeric:.2f}"
                except Exception:
                    # Fallback: just show raw
                    display_value = str(value)
            else:
                display_value = str(value)

            if key in self.sensor_data:
                self.sensor_data[key].set(display_value)
            # else: it’s okay to be silent here

            # Forward to plot window (only touches pure Python lists, no Tk)
            if (
                plot_value is not None
                and self.sensor_plot_window is not None
                and self.sensor_plot_window.winfo_exists()
            ):
                # This will only modify internal buffers; actual redraw is done
                # in the Tk main thread via SensorPlotWindow.after()
                self.sensor_plot_window.add_sample(title, field, plot_value)



    def open_sensor_plot_window(self):
        """Open (or raise) the live sensor graphs window."""
        from sensor_plot_window import SensorPlotWindow

        # If it doesn't exist or was destroyed, recreate it
        if self.sensor_plot_window is None or not self.sensor_plot_window.winfo_exists():
            self.sensor_plot_window = SensorPlotWindow(self.root, gui_ref=self)
        else:
            # If already open, just bring it to front
            self.sensor_plot_window.lift()
            self.sensor_plot_window.focus_set()





                
                
                



