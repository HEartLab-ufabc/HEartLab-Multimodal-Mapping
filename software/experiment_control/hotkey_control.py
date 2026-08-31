import json
import tkinter as tk
from tkinter import ttk, filedialog, messagebox


class HotkeyControl:
    def __init__(self, root, config_file="hotkey_config.json", on_close_callback=None):
        """Initialize the Hotkey Control window."""
        self.root = root
        self.config_file = config_file
        self.hotkey_config = self.load_config()
        self.open_hotkey_window()
        self.on_close_callback = on_close_callback  # Callback to notify the main GUI


    def open_hotkey_window(self):
        """Open the hotkey configuration window."""
        hotkey_window = tk.Toplevel(self.root)
        hotkey_window.title("Hotkey Control")
        hotkey_window.geometry("600x500")  # Default size

        # Match the background color to the root window
        bg_color = self.root.cget("bg")
        hotkey_window.configure(bg=bg_color)

        # Configure resizing behavior
        hotkey_window.grid_rowconfigure(0, weight=1)  # Hotkey frame (expandable)
        hotkey_window.grid_rowconfigure(1, weight=0)  # Button frame (fixed)
        hotkey_window.grid_columnconfigure(0, weight=1)

        # Main Frame for Hotkey Configurations
        self.hotkey_frame = tk.Frame(hotkey_window, bg=bg_color)
        self.hotkey_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        self.refresh_hotkey_labels(self.hotkey_frame)

        # Bottom Frame for Buttons
        bottom_frame = tk.Frame(hotkey_window, bg=bg_color)
        bottom_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=10)

        # Centralize Save and Load Buttons
        save_button = tk.Button(
            bottom_frame, text="Save Config", command=self.save_config, bg=bg_color
        )
        save_button.pack(side=tk.LEFT, padx=20)
        
        # Trigger callback on window close
        hotkey_window.protocol("WM_DELETE_WINDOW", lambda: self.on_close(hotkey_window))
        
    def load_config(self):
        """Load the configuration from the JSON file."""
        try:
            with open(self.config_file, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            print(f"{self.config_file} not found. Creating default configuration.")
            default_config = {
                f"f{i}": {"command": "None", "description": "--"} for i in range(1, 13)
            }
            self.save_to_file(default_config)
            return default_config
        except json.JSONDecodeError:
            print("Invalid JSON format. Using default configuration.")
            default_config = {
                f"f{i}": {"command": "None", "description": "--"} for i in range(1, 13)
            }
            self.save_to_file(default_config)
            return default_config

    def save_to_file(self, config):
        """Save the given configuration to the JSON file."""
        try:
            with open(self.config_file, "w") as file:
                json.dump(config, file, indent=4)
            print(f"Configuration saved to {self.config_file}.")
        except Exception as e:
            print(f"Error saving configuration: {e}")

    def save_config(self):
        """Save the current hotkey configuration to the JSON file."""
        # Collect current entries from the UI
        for child in self.hotkey_frame.winfo_children():
            if isinstance(child, tk.Frame):  # Each frame corresponds to a hotkey row
                hotkey_label = None
                command = None
                description = None
    
                # Iterate over widgets in the frame
                for widget in child.winfo_children():
                    if isinstance(widget, tk.Label) and not hotkey_label:
                        # Use the first Label as the hotkey label
                        hotkey_label = widget.cget("text").split()[-1].lower()
                    elif isinstance(widget, tk.Entry) and not command:
                        # Use the first Entry as the command entry
                        command = widget.get()
                    elif isinstance(widget, tk.Entry):
                        # Use the second Entry as the description entry
                        description = widget.get()
    
                # If all required widgets are identified, update the hotkey config
                if hotkey_label and command and description:
                    if hotkey_label in self.hotkey_config:
                        self.hotkey_config[hotkey_label]["command"] = command
                        self.hotkey_config[hotkey_label]["description"] = description
                else:
                    print(f"Could not extract complete data for hotkey row: {child}")
    
        # Save to file
        self.save_to_file(self.hotkey_config)
        messagebox.showinfo("Success", "Configuration saved successfully.")


    def refresh_hotkey_labels(self, hotkey_frame):
        """Refresh the hotkey configuration display."""
        for widget in hotkey_frame.winfo_children():
            widget.destroy()

        header_frame = tk.Frame(hotkey_frame)
        header_frame.pack(fill=tk.X, pady=5)

        tk.Label(header_frame, text="Hotkey", width=15, anchor="w").pack(side=tk.LEFT, padx=5)
        tk.Label(header_frame, text="Command", width=25, anchor="w").pack(side=tk.LEFT, padx=5)
        tk.Label(header_frame, text="Description", width=40, anchor="w").pack(side=tk.LEFT, padx=5)

        for key, config in self.hotkey_config.items():
            frame = tk.Frame(hotkey_frame)
            frame.pack(fill=tk.X, pady=5)

            tk.Label(frame, text=f"Ctrl + Alt + {key.upper()}", width=15, anchor="w").pack(side=tk.LEFT, padx=5)

            command_entry = tk.Entry(frame, width=25)
            command_entry.insert(0, config['command'])
            command_entry.pack(side=tk.LEFT, padx=5)

            description_entry = tk.Entry(frame, width=40)
            description_entry.insert(0, config['description'])
            description_entry.pack(side=tk.LEFT, padx=5)
            
            
    def on_close(self, hotkey_window):
        """Handle the window close event."""
        # Save the configuration before closing
        self.save_config()
        print("Hotkey configuration saved on close.")
    
        # Notify the main GUI (if callback is provided)
        if self.on_close_callback:
            self.on_close_callback()
    
        # Destroy the window
        hotkey_window.destroy()
