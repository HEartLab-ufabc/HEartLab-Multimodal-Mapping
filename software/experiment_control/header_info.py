import tkinter as tk
from tkinter import ttk, messagebox


class HeaderInfo:
    def __init__(self, root, log_file_name):
        """Initialize the Header Info window."""
        self.root = root
        self.log_file_name = log_file_name  # File path from the main application
        self.header_data = self.initialize_header_data()
        self.header_window = None  # Initialize header window reference
        self.open_window()

    def initialize_header_data(self):
        """Set up the structure for all header fields."""
        return {
            "Experiment Info": {
                "Operator Name": tk.StringVar(value=""),
                "Experiment Type": tk.StringVar(value="Tank/MEA"),
                "Date": tk.StringVar(value="MM/DD/YYYY"),
                "Time": tk.StringVar(value="HH:MM"),
            },
            "Subject Info": {
                "Subject": tk.StringVar(value="Rabbit"),
                "Sex": tk.StringVar(value="Male"),
                "Age": tk.StringVar(value="2"),
                "Weight (Kg)": tk.StringVar(value="4.5"),
                "Additional Notes": tk.StringVar(value="None"),
            },
            "Heart Info": {
                "Weight (g)": tk.StringVar(value="30"),
                "Dimensions (HHxWW) (mm)": tk.StringVar(value="20x50"),
                "Heart out": tk.StringVar(value="HH:MM"),
                "Perfusion Start": tk.StringVar(value="HH:MM"),
                "Additional Notes": tk.StringVar(value="None"),
            },
            "Optical Mapping Info": {
                "Camera Type": tk.StringVar(value="Emergent HR-1800-S-M"),
                "Number of Cameras": tk.StringVar(value="3"),
                "Resolution": tk.StringVar(value="1600x1000"),
                "Frame Rate (fps)": tk.StringVar(value="500"),
                "Dyes Used": tk.StringVar(value="--"),
                "Excitation At (nm)": tk.StringVar(value="590"),
                "LED Filters": tk.StringVar(value="520/20"),
                "Cam Filters": tk.StringVar(value="720/20"),
                "Additional Notes": tk.StringVar(value="None"),
            },
            "Electrical Mapping Info": {
                "Tank Used": tk.StringVar(value="Yes"),
                "Tank Sample Rate(S/s)": tk.StringVar(value="4000"),
                "Tank Electrode Count": tk.StringVar(value="60"),
                "MEAs Used": tk.StringVar(value="Yes"),
                "MEA Sample Rate": tk.StringVar(value="4000"),
                "Additional Notes": tk.StringVar(value="None"),
            },
            "Additional Notes": {
                "Additional Notes": tk.StringVar(value="None"),
            },
            "--LOG START--": tk.StringVar(value=""),
        }

    def open_window(self):
        """Open the Header Info configuration window."""
        
        # Populate header_data from the log file
        self.load_header_from_log()
        
        header_window = tk.Toplevel(self.root)
        header_window.title("Header Info Configuration")
        header_window.geometry("1300x800")
        header_window.resizable(False, False)
    
        # Configure parent columns
        for col in range(9):  # Adjust this based on your maximum column count
            header_window.grid_columnconfigure(col, weight=1)
    
        # Add Frames
        self.create_experiment_info_frame(header_window)
        self.create_subject_info_frame(header_window)
        self.create_heart_info_frame(header_window)
        self.create_optical_mapping_info_frame(header_window)
        self.create_electrical_mapping_info_frame(header_window)
        self.create_additional_notes_frame(header_window)
    
        # Save and Close Buttons
        buttons_frame = tk.Frame(header_window)
        buttons_frame.pack(pady=10, fill=tk.X)
    
        save_button = ttk.Button(buttons_frame, text="Save", command=self.save_header_info)
        save_button.pack(side=tk.LEFT, padx=10)
    
        close_button = ttk.Button(buttons_frame, text="Close", command=header_window.destroy)
        close_button.pack(side=tk.LEFT, padx=10)
        
        # Bind the "Enter" key press to log_data when the note entry is focused
        # header_window.bind("<Return>", self.save_header_info)


    def create_section_frame(self, parent, section_name, column_count=1):
        """Helper to create a section frame with consistent column configuration."""
        section_frame = ttk.LabelFrame(parent, text=section_name)
        section_frame.pack(fill=tk.X, padx=10, pady=5)
    
        # Configure columns for alignment
        for col in range(column_count):
            section_frame.grid_columnconfigure(col, weight=1)
    
        return section_frame

    
    def create_experiment_info_frame(self, parent):
        """Create the Experiment Info section with consistent alignment."""
        frame = self.create_section_frame(parent, "Experiment Info", column_count=9)
    
        # Row 1
        ttk.Label(frame, text="Operator Name:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        ttk.Entry(frame, textvariable=self.header_data["Experiment Info"]["Operator Name"], width=20).grid(
            row=0, column=1, padx=5, pady=5, sticky="w"
        )
        ttk.Label(frame, text="Experiment Type:").grid(row=0, column=2, padx=5, pady=5, sticky="e")
        ttk.Entry(frame, textvariable=self.header_data["Experiment Info"]["Experiment Type"], width=20).grid(
            row=0, column=3, padx=5, pady=5, sticky="w"
        )
    
        # Row 2
        ttk.Label(frame, text="Date:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        ttk.Entry(frame, textvariable=self.header_data["Experiment Info"]["Date"], width=20).grid(
            row=1, column=1, padx=5, pady=5, sticky="w"
        )
        ttk.Label(frame, text="Time:").grid(row=1, column=2, padx=5, pady=5, sticky="e")
        ttk.Entry(frame, textvariable=self.header_data["Experiment Info"]["Time"], width=20).grid(
            row=1, column=3, padx=5, pady=5, sticky="w"
        )

    def create_subject_info_frame(self, parent):
        """Create the Subject Info section."""
        frame = self.create_section_frame(parent, "Subject Info", column_count=9)  # 9 columns for Subject Info
    
        # Row 1
        ttk.Label(frame, text="Subject:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        ttk.Entry(frame, textvariable=self.header_data["Subject Info"]["Subject"], width=20).grid(
            row=0, column=1, padx=5, pady=5, sticky="w"
        )
    
        ttk.Label(frame, text="Sex:").grid(row=0, column=2, padx=5, pady=5, sticky="e")
        ttk.Entry(frame, textvariable=self.header_data["Subject Info"]["Sex"], width=20).grid(
            row=0, column=3, padx=5, pady=5, sticky="w"
        )
    
        ttk.Label(frame, text="Age:").grid(row=0, column=4, padx=5, pady=5, sticky="e")
        ttk.Entry(frame, textvariable=self.header_data["Subject Info"]["Age"], width=20).grid(
            row=0, column=5, padx=5, pady=5, sticky="w"
        )
    
        ttk.Label(frame, text="Weight (Kg):").grid(row=0, column=6, padx=5, pady=5, sticky="e")
        ttk.Entry(frame, textvariable=self.header_data["Subject Info"]["Weight (Kg)"], width=20).grid(
            row=0, column=7, padx=5, pady=5, sticky="w"
        )
    
        # Row 2: Additional Notes
        ttk.Label(frame, text="Additional Notes:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        ttk.Entry(frame, textvariable=self.header_data["Subject Info"]["Additional Notes"], width=120).grid(
            row=2, column=1, columnspan=9, padx=5, pady=5, sticky="w"
        )


    def create_heart_info_frame(self, parent):
        """Create the Heart Info section."""
        frame = self.create_section_frame(parent, "Heart Info", column_count=9)  # 9 columns for Subject Info

        # Row 1
        ttk.Label(frame, text="Weight (g):").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        ttk.Entry(frame, textvariable=self.header_data["Heart Info"]["Weight (g)"], width=10).grid(
            row=0, column=1, padx=5, pady=5, sticky="w"
        )

        ttk.Label(frame, text="Dimensions (HHxWW) (mm):").grid(row=0, column=2, padx=5, pady=5, sticky="e")
        ttk.Entry(frame, textvariable=self.header_data["Heart Info"]["Dimensions (HHxWW) (mm)"], width=20).grid(
            row=0, column=3, padx=5, pady=5, sticky="w"
        )
        
        # Row 2
        ttk.Label(frame, text="Heart out:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        ttk.Entry(frame, textvariable=self.header_data["Heart Info"]["Heart out"], width=10).grid(
            row=1, column=1, padx=5, pady=5, sticky="w"
        )

        ttk.Label(frame, text="Perfusion Start").grid(row=1, column=2, padx=5, pady=5, sticky="e")
        ttk.Entry(frame, textvariable=self.header_data["Heart Info"]["Perfusion Start"], width=20).grid(
            row=1, column=3, padx=5, pady=5, sticky="w"
        )

        # Row 3: Additional Notes
        ttk.Label(frame, text="Additional Notes:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        ttk.Entry(frame, textvariable=self.header_data["Heart Info"]["Additional Notes"], width=120).grid(
            row=2, column=1, columnspan=8, padx=5, pady=5, sticky="w"
        )

    def create_optical_mapping_info_frame(self, parent):
        """Create the Optical Mapping Info section."""
        frame = self.create_section_frame(parent, "Optical Mapping Info", column_count=9)  # 9 columns for Subject Info

        # Row 1
        ttk.Label(frame, text="Camera Type:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        ttk.Entry(frame, textvariable=self.header_data["Optical Mapping Info"]["Camera Type"], width=20).grid(
            row=0, column=1, padx=5, pady=5, sticky="w"
        )

        ttk.Label(frame, text="Number of Cameras:").grid(row=0, column=2, padx=5, pady=5, sticky="e")
        ttk.Entry(frame, textvariable=self.header_data["Optical Mapping Info"]["Number of Cameras"], width=20).grid(
            row=0, column=3, padx=5, pady=5, sticky="w"
        )

        ttk.Label(frame, text="Resolution:").grid(row=0, column=4, padx=5, pady=5, sticky="e")
        ttk.Entry(frame, textvariable=self.header_data["Optical Mapping Info"]["Resolution"], width=20).grid(
            row=0, column=5, padx=5, pady=5, sticky="w"
        )
        
        ttk.Label(frame, text="Frame Rate (fps):").grid(row=0, column=6, padx=5, pady=5, sticky="e")
        ttk.Entry(frame, textvariable=self.header_data["Optical Mapping Info"]["Frame Rate (fps)"], width=20).grid(
            row=0, column=7, padx=5, pady=5, sticky="w"
        )

        # Row 2
        ttk.Label(frame, text="Dyes Used:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        ttk.Entry(frame, textvariable=self.header_data["Optical Mapping Info"]["Dyes Used"], width=20).grid(
            row=1, column=1, padx=5, pady=5, sticky="w"
        )

        ttk.Label(frame, text="Excitation At (nm):").grid(row=1, column=2, padx=5, pady=5, sticky="e")
        ttk.Entry(frame, textvariable=self.header_data["Optical Mapping Info"]["Excitation At (nm)"], width=20).grid(
            row=1, column=3, padx=5, pady=5, sticky="w"
        )

        ttk.Label(frame, text="LED Filters:").grid(row=1, column=4, padx=5, pady=5, sticky="e")
        ttk.Entry(frame, textvariable=self.header_data["Optical Mapping Info"]["LED Filters"], width=20).grid(
            row=1, column=5, padx=5, pady=5, sticky="w"
        )
        
        ttk.Label(frame, text="Cam Filters:").grid(row=1, column=6, padx=5, pady=5, sticky="e")
        ttk.Entry(frame, textvariable=self.header_data["Optical Mapping Info"]["Cam Filters"], width=20).grid(
            row=1, column=7, padx=5, pady=5, sticky="w"
        )
        
        # Row 3
        ttk.Label(frame, text="Additional Notes:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        ttk.Entry(frame, textvariable=self.header_data["Optical Mapping Info"]["Additional Notes"], width=120).grid(
            row=2, column=1, columnspan=8, padx=5, pady=5, sticky="w"
        )


    def create_electrical_mapping_info_frame(self, parent):
        """Create the Electrical Mapping Info section."""
        frame = self.create_section_frame(parent, "Electrical Mapping Info", column_count=9)  # 9 columns for Subject Info
        
        # ECG Used
        ttk.Label(frame, text="ECG Used:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        ttk.Entry(frame, textvariable=self.header_data["Electrical Mapping Info"]["Tank Used"], width=20).grid(
            row=0, column=1, padx=5, pady=5, sticky="w"
        )

        ttk.Label(frame, text="ECG Sample Rate(S/s):").grid(row=0, column=2, padx=5, pady=5, sticky="e")
        ttk.Entry(frame, textvariable=self.header_data["Electrical Mapping Info"]["Tank Sample Rate(S/s)"], width=20).grid(
            row=0, column=3, padx=5, pady=5, sticky="w"
        )
        
        ttk.Label(frame, text="ECG Electrode Count:").grid(row=0, column=4, padx=5, pady=5, sticky="e")
        ttk.Entry(frame, textvariable=self.header_data["Electrical Mapping Info"]["Tank Electrode Count"], width=20).grid(
            row=0, column=5, padx=5, pady=5, sticky="w"
        )

        # MEAs Used
        ttk.Label(frame, text="MEAs Used:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        ttk.Entry(frame, textvariable=self.header_data["Electrical Mapping Info"]["MEAs Used"], width=20).grid(
            row=1, column=1, padx=5, pady=5, sticky="w"
        )

        ttk.Label(frame, text="MEA Sample Rate:").grid(row=1, column=2, padx=5, pady=5, sticky="e")
        ttk.Entry(frame, textvariable=self.header_data["Electrical Mapping Info"]["MEA Sample Rate"], width=20).grid(
            row=1, column=3, padx=5, pady=5, sticky="w"
        )
        
        # Additional Notes
        ttk.Label(frame, text="Additional Notes").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        ttk.Entry(frame, textvariable=self.header_data["Electrical Mapping Info"]["Additional Notes"], width=120).grid(
            row=2, column=1,columnspan=8, padx=5, pady=5, sticky="w"
        )
        


    def create_additional_notes_frame(self, parent):
        """Create the Additional Notes section."""
        frame = self.create_section_frame(parent, "Additional Notes")
        ttk.Entry(
            frame, textvariable=self.header_data["Additional Notes"]["Additional Notes"], width=50
        ).pack(fill=tk.X, padx=10, pady=5)

    def save_header_info(self, event=None):
            """Save the header info to the shared log file."""
            try:
                # Path to the log file
                log_file_path = self.log_file_name
    
                # Prepare the new header content
                header_lines = ["--- Header Information ---\n"]
                for section, fields in self.header_data.items():
                    header_lines.append(f"--- {section} ---\n")
                    if isinstance(fields, dict):
                        for label, var in fields.items():
                            header_lines.append(f"{label}: {var.get()}\n")
                    else:
                        header_lines.append(f"{fields.get()}\n")
                    header_lines.append("\n")
    
                # Count the number of lines in the new header
                num_header_lines = len(header_lines)
    
                # Read the current content of the log file
                try:
                    with open(log_file_path, "r") as file:
                        lines = file.readlines()
                except FileNotFoundError:
                    lines = []  # If the file doesn't exist, start with an empty list
    
                # Prepare the updated content
                updated_content = header_lines + lines[num_header_lines:]  # Exclude lines from 2X onward
    
                # Write the updated content back to the file
                with open(log_file_path, "w") as file:
                    file.writelines(updated_content)
    
                # Show success message
                messagebox.showinfo("Success", "Header Info saved successfully.")
    
                # Close only the header info window
                if self.header_window is not None:
                    self.header_window.destroy()
    
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save header info: {e}")
                
    def load_header_from_log(self):
        """Load header fields from the log file if available."""
        try:
            with open(self.log_file_name, "r") as file:
                lines = file.readlines()
    
            # Parse header information from the file
            current_section = None
            for line in lines:
                line = line.strip()
                if line.startswith("---") and line.endswith("---"):
                    # Detect section headers
                    section_name = line.strip("- ").strip()
                    if section_name in self.header_data:
                        current_section = section_name
                elif current_section and ":" in line:
                    # Parse key-value pairs
                    key, value = line.split(":", 1)
                    key, value = key.strip(), value.strip()
                    if key in self.header_data[current_section]:
                        self.header_data[current_section][key].set(value)
    
        except FileNotFoundError:
            print(f"Log file {self.log_file_name} not found. Using default values.")
        except Exception as e:
            print(f"Error loading header from log: {e}")







