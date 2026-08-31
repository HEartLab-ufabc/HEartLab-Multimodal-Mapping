# %%
import os

os.environ["MPLBACKEND"] = "TkAgg"
import matplotlib
matplotlib.use("TkAgg")
import tkinter as tk
from serial_handler import SerialHandler
from stimulation_gui import StimulationGUI

def main():
    root = tk.Tk()
    root.title("Stimulation Controller")

    # Serial handler instance
    serial_handler = SerialHandler()

    # Create stimulation GUI and pass serial handler
    StimulationGUI(root, serial_handler)

    root.mainloop()

if __name__ == "__main__":
    main()