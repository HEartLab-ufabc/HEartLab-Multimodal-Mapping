# sensor_plot_window.py

import tkinter as tk
from tkinter import ttk
import time

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class SensorPlotWindow(tk.Toplevel):
    """
    Live plotting window for sensors.

    Layout: 4 rows, each with:
      - Left: line plot
      - Right: value box showing latest reading

      1) Tank Temperature
      2) Line 1 Pressure
      3) Line 1 Temperature
      4) Line 1 Flow Rate

    StimulationGUI calls `add_sample(title, field, value_float)`
    whenever new data arrives. This class stores the data and
    updates the plots from the Tk main thread via .after().
    """

    def __init__(self, master, gui_ref=None, max_points=150, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.gui_ref = gui_ref
        self.max_points = max_points
        self.window_seconds = tk.DoubleVar(value=5.0)  # default 5-second window
        self.title("Live Sensor Graphs")

        self._closed = False
        self._needs_redraw = False
        self._t0 = time.time()

        # When window is closed by the user
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        # --- Matplotlib Figure & Axes (4 rows x 2 columns) ---
        # Left column: plots; right column: value boxes
        self.fig = Figure(figsize=(8, 8), dpi=100)
        self.fig.suptitle("Sensors Data", fontsize=20)

        gs = self.fig.add_gridspec(
            4,
            2,
            width_ratios=[4, 1],
            height_ratios=[1, 1, 1, 1],
            hspace=0.4,
            wspace=0.3,
        )

        ax1 = self.fig.add_subplot(gs[0, 0])
        box1 = self.fig.add_subplot(gs[0, 1])
        ax2 = self.fig.add_subplot(gs[1, 0])
        box2 = self.fig.add_subplot(gs[1, 1])
        ax3 = self.fig.add_subplot(gs[2, 0])
        box3 = self.fig.add_subplot(gs[2, 1])
        ax4 = self.fig.add_subplot(gs[3, 0])
        box4 = self.fig.add_subplot(gs[3, 1])

        ax1.set_ylabel("Tank Temp (°C)")
        ax2.set_ylabel("Pressure (mmHg)")
        ax3.set_ylabel("Temp (°C)")
        ax4.set_ylabel("Flow (mL/min)")
        ax4.set_xlabel("Time (s)")

        for ax in (ax1, ax2, ax3, ax4):
            ax.grid(True)
            

        box_title = ["Tank Temp", "Pressure", "Flow Temp", "Flow  Rate"]
        i = 0 

        # Configure the "box" axes on the right: no ticks, centered text
        for box_ax in (box1, box2, box3, box4):

            box_ax.set_title(box_title[i])
            i=i+1

            box_ax.set_xticks([])
            box_ax.set_yticks([])
            box_ax.set_xlim(0, 1)
            box_ax.set_ylim(0, 1)
            box_ax.set_facecolor("#f7f7f7")
            # Keep a visible frame so it looks like a box
            for spine in box_ax.spines.values():
                spine.set_visible(True)

        # Traces: (title, field) -> dict with x, y, ax, line, value_box, etc.
        self.traces = {}

        self.traces[("Tank", "Temperature")] = self._make_trace(
            ax1, box1, unit="°C"
        )
        self.traces[("Line 1", "Pressure")] = self._make_trace(
            ax2, box2, unit="mmHg"
        )
        self.traces[("Line 1", "Temperature")] = self._make_trace(
            ax3, box3, unit="°C"
        )
        self.traces[("Line 1", "Flow Rate")] = self._make_trace(
            ax4, box4, unit="mL/min"
        )

        # --- Rolling window controls ---
        # --- Rolling window controls (slider + entry) ---
        controls_frame = ttk.Frame(self)
        controls_frame.pack(fill="x", pady=5)

        ttk.Label(controls_frame, text="Rolling window (s):").pack(
            side="left", padx=(5, 2)
        )

        # Slider: 1 to 60 seconds, 0.5s resolution
        self.window_slider = tk.Scale(
            controls_frame,
            from_=1.0,
            to=60.0,
            orient="horizontal",
            resolution=0.5,
            showvalue=False,
            variable=self.window_seconds,
            length=200,
        )
        self.window_slider.pack(side="left", padx=5)

        # Entry box to type exact value
        self.window_entry = ttk.Entry(controls_frame, width=6)
        self.window_entry.pack(side="left", padx=(2, 5))

        # When the variable changes (via slider or programmatically), update entry
        self.window_seconds.trace_add(
            "write",
            lambda *args: self._on_window_seconds_changed()
        )

        # When user edits the entry, update the variable
        self.window_entry.bind("<Return>", self._on_window_entry_commit)
        self.window_entry.bind("<FocusOut>", self._on_window_entry_commit)

        # Initialize entry text
        self._on_window_seconds_changed()


        # Embed Figure into Tk
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(fill="both", expand=True)

        # Start periodic redraw loop
        self._schedule_redraw()

    def _on_window_seconds_changed(self):
        """Update the entry text when the slider / variable changes."""
        if not hasattr(self, "window_entry"):
            return
        value = self.window_seconds.get()
        # Clamp to a reasonable range just in case
        if value < 0.5:
            value = 0.5
        if value > 600:
            value = 600
        # Update entry display
        self.window_entry.delete(0, tk.END)
        self.window_entry.insert(0, f"{value:.1f}")

    def _on_window_entry_commit(self, event=None):
        """When user edits the entry, parse and update the slider/variable."""
        text = self.window_entry.get()
        try:
            value = float(text)
        except ValueError:
            # Restore current variable value if parsing fails
            self._on_window_seconds_changed()
            return

        # Clamp to sane range
        if value < 0.5:
            value = 0.5
        if value > 600:
            value = 600

        self.window_seconds.set(value)  # this will also refresh slider + entry


    def _make_trace(self, ax, value_ax=None, unit=""):
        """Create an empty line on given axes and return trace dict."""
        (line,) = ax.plot([], [], lw=1.5)

        value_text = None
        if value_ax is not None:
            # Placeholder text in the middle of the box
            value_text = value_ax.text(
                0.5,
                0.5,
                "--",
                ha="center",
                va="center",
                fontsize=12,
                transform=value_ax.transAxes,
            )

        return {
            "ax": ax,
            "line": line,
            "x": [],
            "y": [],
            "value_ax": value_ax,
            "value_text": value_text,
            "unit": unit,
            "latest_text": None,
        }

    def add_sample(self, title, field, value):
        """
        Called by StimulationGUI when new numeric data arrives.
        This method MUST NOT touch Tk widgets or Matplotlib canvas
        directly from a non-main thread. It only updates pure Python
        structures and sets a redraw flag.
        """
        key = (title, field)
        if key not in self.traces:
            # Unknown sensor combo; ignore
            return

        trace = self.traces[key]
        # Use elapsed time since window creation as x
        t = time.time() - self._t0

        trace["x"].append(t)
        trace["y"].append(value)

        # Limit the history length
        if len(trace["x"]) > self.max_points:
            trace["x"] = trace["x"][-self.max_points :]
            trace["y"] = trace["y"][-self.max_points :]

        # Prepare latest text for the box, but don't touch Matplotlib yet
        unit = trace.get("unit", "")
        if unit:
            latest_text = f"{value:.2f} {unit}"
        else:
            latest_text = f"{value:.2f}"
        trace["latest_text"] = latest_text

        # Mark that we need a redraw (will be done in Tk main thread)
        self._needs_redraw = True

    def _schedule_redraw(self):
        """Schedule periodic redraw from Tk main loop."""
        if not self._closed:
            # ~5 FPS
            self.after(200, self._redraw)

    def _redraw(self):
        """Redraw plots if there is new data."""
        if self._closed:
            return

        if self._needs_redraw:
            for trace in self.traces.values():
                line = trace["line"]
                x = trace["x"]
                y = trace["y"]
                line.set_data(x, y)

                ax = trace["ax"]
                if x:
                    xmax = max(x)
                    window = self.window_seconds.get()

                    xmin = xmax - window
                    if xmin < 0:
                        xmin = 0

                    ax.set_xlim(xmin, xmax)
                ax.relim()
                ax.autoscale_view(scaley=True)

                # Update the value box text if we have one
                value_text = trace.get("value_text")
                latest = trace.get("latest_text")
                if value_text is not None and latest is not None:
                    value_text.set_text(latest)

            self.canvas.draw_idle()
            self._needs_redraw = False

        # Schedule next redraw
        self._schedule_redraw()

    def on_close(self):
        """Handle window close."""
        self._closed = True
        # Let the parent GUI know that this window is gone
        if self.gui_ref is not None and hasattr(self.gui_ref, "sensor_plot_window"):
            self.gui_ref.sensor_plot_window = None
        self.destroy()
