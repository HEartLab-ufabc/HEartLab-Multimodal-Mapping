import tkinter as tk
from tkinter import ttk
import math
import time


class InductionProtocolWindow(tk.Toplevel):
    """
    Induction protocol window.

    Uses the SAME serial commands as the normal stimulation/burst protocol:
      - SET_PARAMS {channel} {pulse_width} {period} {num_pulses} {state}\n
      - START_BURST
      - STOP_BURST

    For S1–S4 we specify:
      - Pulse Width (ms)
      - Frequency (Hz)
      - Period (ms)
      - Duration (s)

    The GUI keeps frequency and period consistent:
      period_ms  = 1000 / frequency
      frequency  = 1000 / period_ms

    On Apply:
      - period_ms_int  = ceil(period_ms_from_UI)
      - num_pulses_int = ceil(frequency * duration)

    The induction protocol repeats bursts:
      - interval_between_bursts (s)
      - number_of_bursts (integer)

    And displays:
      - Burst count (done / total)
      - Time after last burst
      - Time after last burst protocol (only starts after all bursts are done)
    """

    def __init__(self, master, gui_ref=None, *args, **kwargs):
        """
        :param master: parent Tk widget (usually the main root)
        :param gui_ref: reference to StimulationGUI instance so we can call
                        gui_ref.send_command(...)
        """
        super().__init__(master, *args, **kwargs)

        self.gui_ref = gui_ref
        self.title("Induction Protocol")
        self.geometry("950x440")
        self.resizable(False, False)

        # Track running state of the induction burst protocol
        self.induction_running = False

        # Store S1–S4 settings here: index 0 -> S1, 1 -> S2, etc.
        self.induction_stim_data = []

        # Repetition parameters
        self.interval_between_bursts_var = tk.StringVar(value="10.0")  # seconds
        self.num_bursts_var = tk.StringVar(value="8")                 # count

        # Status counters / timers
        self.bursts_done = 0
        self.total_bursts = 0
        self.last_burst_time = None
        self.protocol_complete_time = None

        # For cancelling scheduled bursts
        self._next_burst_after_id = None

        # Status label textvars
        self.burst_count_text = tk.StringVar(value="Burst Count: 0 / 0")
        self.time_after_last_burst_text = tk.StringVar(
            value="Time after last burst: ---"
        )
        self.time_after_protocol_text = tk.StringVar(
            value="Time after last protocol: ---"
        )

        # Proper close behaviour
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        self._build_ui()

        # Start periodic timer updates
        self._update_timers()

    # ---------------------------------------------------------
    # UI BUILDING
    # ---------------------------------------------------------
    def _build_ui(self):
        main_frame = ttk.Frame(self, padding=10)
        main_frame.pack(fill="both", expand=True)

        # Title
        ttk.Label(
            main_frame,
            text="Induction Protocol",
            font=("TkDefaultFont", 14, "bold")
        ).pack(pady=(0, 10))

        # Frame for S1–S4
        stim_frame = ttk.LabelFrame(main_frame, text="S1–S4 Parameters")
        stim_frame.pack(fill="x", pady=5)

        # Make columns expand a bit
        for col in range(4):
            stim_frame.grid_columnconfigure(col, weight=1)

        # Create S1–S4 panels
        for col, stim_index in enumerate(range(1, 5)):  # 1,2,3,4
            sub = ttk.LabelFrame(stim_frame, text=f"S{stim_index}")
            sub.grid(row=0, column=col, padx=5, pady=5, sticky="nsew")
            settings = self._create_stim_subpanel(sub, stim_index)
            self.induction_stim_data.append(settings)

        # ---- Repetition controls + Start/Stop button ----
        control_frame = ttk.Frame(main_frame)
        control_frame.pack(fill="x", pady=10)
        control_frame.columnconfigure(0, weight=1)
        control_frame.columnconfigure(1, weight=0)

        # Left side container
        left_frame = ttk.Frame(control_frame)
        left_frame.grid(row=0, column=0, sticky="w")

        # Validation commands
        int_vcmd = (self.register(self._validate_int), "%P")
        float_vcmd = (self.register(self._validate_float), "%P")

        # Top: interval + number of bursts
        params_frame = ttk.Frame(left_frame)
        params_frame.grid(row=0, column=0, sticky="w")

        ttk.Label(params_frame, text="Interval between bursts (s):").grid(
            row=0, column=0, padx=5, pady=2, sticky="w"
        )
        ttk.Entry(
            params_frame,
            textvariable=self.interval_between_bursts_var,
            width=8,
            validate="key",
            validatecommand=float_vcmd,
        ).grid(row=0, column=1, padx=5, pady=2)

        ttk.Label(params_frame, text="Number of bursts:").grid(
            row=1, column=0, padx=5, pady=2, sticky="w"
        )
        ttk.Entry(
            params_frame,
            textvariable=self.num_bursts_var,
            width=8,
            validate="key",
            validatecommand=int_vcmd,
        ).grid(row=1, column=1, padx=5, pady=2)

        # Below: status in its own labeled frame
        status_frame = ttk.LabelFrame(left_frame, text="Protocol Status")
        status_frame.grid(row=0, column=3, padx=15, pady=(8, 0), sticky="e")
        status_font = ("TkDefaultFont", 14)

        ttk.Label(
            status_frame,
            textvariable=self.burst_count_text,
            font = status_font
        ).grid(row=0, column=0, padx=5, pady=2, sticky="w")

        ttk.Label(
            status_frame,
            textvariable=self.time_after_last_burst_text,
            font = status_font
        ).grid(row=1, column=0, padx=5, pady=2, sticky="w")

        ttk.Label(
            status_frame,
            textvariable=self.time_after_protocol_text,
            font = status_font
        ).grid(row=2, column=0, padx=5, pady=2, sticky="w")

        # Right side: Start/Stop button
        self.start_stop_button = ttk.Button(
            params_frame,
            text="Start Burst Protocol",
            command=self.toggle_induction_burst
        )
        self.start_stop_button.grid(row=0, column=2, padx=100, pady=10)

        # Reset button (below Start/Stop)
        self.reset_button = ttk.Button(
            params_frame,
            text="Reset",
            command=self.reset_protocol_status
        )
        self.reset_button.grid(row=1, column=2, padx=100, pady=10)

    def reset_protocol_status(self):
        """
        Reset burst counters and timers without changing S1–S4 parameters.
        Also stops any running protocol and cancels scheduled bursts.
        """
        # Stop protocol and cancel scheduled bursts
        self.induction_running = False
        burst_id = self._next_burst_after_id
        if getattr(self, "_next_burst_after_id", None) is not None:
            try:
                self.after_cancel(burst_id) # type: ignore[arg-type]
            except Exception:
                pass
            self._next_burst_after_id = None

        # Reset counters and timestamps
        self.bursts_done = 0
        self.total_bursts = 0
        self.last_burst_time = None
        self.protocol_complete_time = None

        # Reset status texts
        self.burst_count_text.set("Burst Count: 0 / 0")
        self.time_after_last_burst_text.set("Time after last burst: ---")
        self.time_after_protocol_text.set("Time after last protocol: ---")

        # Reset Start/Stop button label
        self.start_stop_button.config(text="Start Induction Burst Protocol")

        print("[Induction] Protocol status reset.")


    def _create_stim_subpanel(self, parent, stim_index):
        """
        Build one S-panel (S1..S4) with:
        - Pulse Width (ms)
        - Frequency (Hz)
        - Period (ms)
        - Duration (s)
        - Enabled
        - Apply button (uses apply_induction_settings)
        """
        settings = {
            "pulse_width": tk.StringVar(value="2"),    # ms
            "frequency": tk.StringVar(value="50"),     # Hz
            "period": tk.StringVar(value="20"),        # ms (linked to frequency)
            "duration": tk.StringVar(value="2"),       # s
            "enabled": tk.BooleanVar(value=False),
            # guard to avoid recursive updates when syncing freq/period
            "updating": False,
        }

        # Integer validation (for pulse width)
        int_vcmd = (self.register(self._validate_int), "%P")
        # Float validation (for frequency, period, duration)
        float_vcmd = (self.register(self._validate_float), "%P")

        # Pulse Width
        ttk.Label(parent, text="Pulse Width (ms):").grid(
            row=0, column=0, padx=5, pady=3, sticky="w"
        )
        ttk.Entry(
            parent,
            textvariable=settings["pulse_width"],
            width=8,
            validate="key",
            validatecommand=int_vcmd,
        ).grid(row=0, column=1, padx=5, pady=3)

        # Frequency
        ttk.Label(parent, text="Frequency (Hz):").grid(
            row=1, column=0, padx=5, pady=3, sticky="w"
        )
        ttk.Entry(
            parent,
            textvariable=settings["frequency"],
            width=8,
            validate="key",
            validatecommand=float_vcmd,
        ).grid(row=1, column=1, padx=5, pady=3)

        # Period
        ttk.Label(parent, text="Period (ms):").grid(
            row=2, column=0, padx=5, pady=3, sticky="w"
        )
        ttk.Entry(
            parent,
            textvariable=settings["period"],
            width=8,
            validate="key",
            validatecommand=float_vcmd,
        ).grid(row=2, column=1, padx=5, pady=3)

        # Duration
        ttk.Label(parent, text="Duration (s):").grid(
            row=3, column=0, padx=5, pady=3, sticky="w"
        )
        ttk.Entry(
            parent,
            textvariable=settings["duration"],
            width=8,
            validate="key",
            validatecommand=float_vcmd,
        ).grid(row=3, column=1, padx=5, pady=3)

        # Enabled checkbox
        ttk.Checkbutton(
            parent,
            text="Enabled",
            variable=settings["enabled"]
        ).grid(row=4, column=0, columnspan=2, padx=5, pady=3)

        # Apply button
        ttk.Button(
            parent,
            text="Apply",
            command=lambda idx=stim_index: self.apply_induction_settings(idx),
        ).grid(row=5, column=0, columnspan=2, padx=5, pady=5)

        # Link frequency <-> period
        settings["frequency"].trace_add(
            "write",
            lambda *args, s=settings: self._on_freq_changed(s)
        )
        settings["period"].trace_add(
            "write",
            lambda *args, s=settings: self._on_period_changed(s)
        )

        return settings

    # ---------------------------------------------------------
    # VALIDATION
    # ---------------------------------------------------------
    def _validate_int(self, value):
        """Allow empty or purely integer strings."""
        if value == "":
            return True
        return value.isdigit()

    def _validate_float(self, value):
        """Allow empty or simple float-like strings."""
        if value == "":
            return True
        try:
            float(value)
            return True
        except ValueError:
            return False

    # ---------------------------------------------------------
    # FREQ <-> PERIOD LINKING
    # ---------------------------------------------------------
    def _on_freq_changed(self, settings):
        """Update period when frequency changes (if valid)."""
        if settings["updating"]:
            return

        freq_str = settings["frequency"].get()
        try:
            f = float(freq_str)
        except ValueError:
            return

        if f <= 0:
            return

        period_ms = 1000.0 / f
        period_int = int(math.ceil(period_ms))

        settings["updating"] = True
        settings["period"].set(str(period_int))
        settings["updating"] = False

    def _on_period_changed(self, settings):
        """Update frequency when period changes (if valid)."""
        if settings["updating"]:
            return

        period_str = settings["period"].get()
        try:
            p = float(period_str)
        except ValueError:
            return

        if p <= 0:
            return

        f = 1000.0 / p

        # format frequency with a reasonable precision
        freq_str = f"{f:.3f}".rstrip("0").rstrip(".")
        settings["updating"] = True
        settings["frequency"].set(freq_str)
        settings["updating"] = False

    # ---------------------------------------------------------
    # APPLY SETTINGS (S1–S4)
    # ---------------------------------------------------------
    def apply_induction_settings(self, stim_index):
        """
        Apply settings for a given S (1..4) and send a SET_PARAMS command.

        S1..S4 are specified using:
            pulse_width (ms), frequency (Hz), period (ms), duration (s)

        We compute:
            period_ms_int  = ceil(period_ms_from_UI)
            num_pulses_int = ceil(frequency * duration)

        and then send:
            SET_PARAMS {channel} {pulse_width} {period_ms_int} {num_pulses_int} {state}\n

        Here:
          S1 -> stim_index=1 -> channel=2
          S2 -> stim_index=2 -> channel=3
          S3 -> stim_index=3 -> channel=4
          S4 -> stim_index=4 -> channel=5
        """
        list_index = stim_index - 1  # S1..S4 -> 0..3
        settings = self.induction_stim_data[list_index]

        # Pulse width
        pw_str = settings["pulse_width"].get() or "0"
        try:
            pulse_width = int(float(pw_str))
        except ValueError:
            print(f"[Induction] Invalid pulse width: {pw_str!r}")
            return

        # Frequency & duration
        freq_str = settings["frequency"].get() or "0"
        dur_str = settings["duration"].get() or "0"

        try:
            frequency = float(freq_str)
            duration = float(dur_str)
        except ValueError:
            print(f"[Induction] Invalid frequency or duration: f={freq_str!r}, d={dur_str!r}")
            return

        if frequency <= 0 or duration <= 0:
            print(f"[Induction] Frequency and duration must be > 0 (f={frequency}, d={duration})")
            return

        # Period from UI (prefer this so what the user sees is what we send)
        period_str = settings["period"].get() or "0"
        try:
            period_val = float(period_str)
        except ValueError:
            # fallback: compute from frequency
            period_val = 1000.0 / frequency

        if period_val <= 0:
            period_val = 1000.0 / frequency

        # Round UP to integer for period and number of pulses
        period_ms_int = int(math.ceil(period_val))
        num_pulses_int = int(math.ceil(frequency * duration))

        state = "ON" if settings["enabled"].get() else "OFF"

        # Same convention as main GUI: stim_index + 1
        channel = stim_index + 1  # S1->2, S2->3, ...

        command = (
            f"SET_PARAMS {channel} {pulse_width} {period_ms_int} "
            f"{num_pulses_int} {state}\n"
        )

        print(
            f"[Induction] S{stim_index}: f={frequency}Hz, dur={duration}s, "
            f"period={period_ms_int}ms, pulses={num_pulses_int}"
        )
        print(f"[Induction] Sending command: {command.strip()}")

        self._send_command(command)

    # ---------------------------------------------------------
    # BURST PROTOCOL CONTROL (REPEATING BURSTS)
    # ---------------------------------------------------------
    def toggle_induction_burst(self):
        """Start or stop the induction burst protocol."""
        if not self.induction_running:
            self.start_induction_burst()
        else:
            self.stop_induction_burst()

    def start_induction_burst(self):
        """Initialize and start the repeating burst protocol."""
        # Parse interval
        interval_str = self.interval_between_bursts_var.get() or "0"
        num_bursts_str = self.num_bursts_var.get() or "0"

        try:
            interval = float(interval_str)
        except ValueError:
            print(f"[Induction] Invalid interval between bursts: {interval_str!r}")
            return

        try:
            total_bursts = int(num_bursts_str)
        except ValueError:
            print(f"[Induction] Invalid number of bursts: {num_bursts_str!r}")
            return

        if interval <= 0 or total_bursts <= 0:
            print(f"[Induction] Interval and number of bursts must be > 0 "
                  f"(interval={interval}, bursts={total_bursts})")
            return

        # Initialize counters
        self.induction_running = True
        self.interval_seconds = interval
        self.total_bursts = total_bursts
        self.bursts_done = 0
        self.last_burst_time = None
        self.protocol_complete_time = None

        # Update button text
        self.start_stop_button.config(text="Stop Induction Burst Protocol")

        print(f"[Induction] Starting protocol: {total_bursts} bursts, "
              f"interval={interval} s")

        # Start first burst immediately
        self._start_single_burst()

    def _start_single_burst(self):
        """Send a single START_BURST, update counters, and schedule next if needed."""
        if not self.induction_running:
            return  # Protocol was stopped

        if self.bursts_done >= self.total_bursts:
            # Already complete
            return

        # Send START_BURST (same command as main GUI)
        command = "START_BURST"
        print(f"[Induction] Burst {self.bursts_done + 1}/{self.total_bursts}: {command}")
        self._send_command(command)

        # Update counters
        self.bursts_done += 1
        self.last_burst_time = time.time()

        # If more bursts remain, schedule the next one
        if self.bursts_done < self.total_bursts and self.induction_running:
            delay_ms = int(self.interval_seconds * 1000)
            self._next_burst_after_id = self.after(delay_ms, self._start_single_burst)
        else:
            # Protocol complete (all bursts sent)
            self.induction_running = False
            self.protocol_complete_time = time.time()
            self.start_stop_button.config(text="Start Induction Burst Protocol")
            self._next_burst_after_id = None
            print("[Induction] Protocol complete: all bursts sent.")

    def stop_induction_burst(self):
        """Stop the induction protocol and send STOP_BURST once."""
        if not self.induction_running and self.bursts_done == 0:
            return  # Nothing to stop

        self.induction_running = False
        self.protocol_complete_time = time.time()
        self.start_stop_button.config(text="Start Induction Burst Protocol")

        # Cancel scheduled next burst if any
        if self._next_burst_after_id is not None:
            try:
                self.after_cancel(self._next_burst_after_id)
            except Exception:
                pass
            self._next_burst_after_id = None

        # Send STOP_BURST once to be safe
        command = "STOP_BURST"
        print(f"[Induction] Stopping protocol early: {command}")
        self._send_command(command)

    # ---------------------------------------------------------
    # TIMERS / STATUS LABEL UPDATES
    # ---------------------------------------------------------
    def _update_timers(self):
        """Periodic update of burst count, time after last burst, and protocol time."""
        now = time.time()

        # Burst count label
        self.burst_count_text.set(
            f"Burst Count: {self.bursts_done} / {self.total_bursts}"
        )

        # Time after last burst
        if self.last_burst_time is not None:
            # If protocol is complete, freeze at the moment it completed
            if self.protocol_complete_time is not None:
                dt = self.protocol_complete_time - self.last_burst_time
            else:
                dt = now - self.last_burst_time

            if dt < 0:
                dt = 0.0

            self.time_after_last_burst_text.set(
                f"Time after last burst: {dt:.1f} s"
            )
        else:
            self.time_after_last_burst_text.set(
                "Time after last burst: ---"
            )

        # Time after last protocol (MM:SS.ms) – only after protocol_complete_time is set
        if self.protocol_complete_time is not None:
            dtp = now - self.protocol_complete_time
            if dtp < 0:
                dtp = 0.0

            minutes = int(dtp // 60)
            remaining = dtp - minutes * 60
            seconds = int(remaining)
            millis = int(round((remaining - seconds) * 1000))

            # Format as MM:SS.mmm
            time_str = f"{minutes:02d}:{seconds:02d}.{millis:03d}"
            self.time_after_protocol_text.set(
                f"Time after last protocol: {time_str}"
            )
        else:
            self.time_after_protocol_text.set(
                "Time after last protocol: ---"
            )

        # Schedule next update
        if self.winfo_exists():
            self.after(200, self._update_timers)

    def pause_from_record_start(self):
        """
        Called by the main window when Record Start is pressed.
        For now, we treat 'pause' as 'stop the protocol immediately'.
        """
        if self.induction_running:
            print("[Induction] Record Start pressed → pausing induction protocol.")
            self.stop_induction_burst()


    # ---------------------------------------------------------
    # SERIAL SENDER + CLOSE HANDLING
    # ---------------------------------------------------------
    def _send_command(self, command: str):
        """
        Helper to send a command using the main GUI's send_command method,
        if available.
        """
        if self.gui_ref is not None:
            try:
                self.gui_ref.send_command(command)
            except Exception as e:
                print(f"[Induction] Error sending command via gui_ref: {e}")
        else:
            print(f"[Induction] gui_ref not set. Command would be: {command!r}")

    def on_close(self):
        """Handle window close (stop protocol, cancel timers, then destroy)."""
        # Stop any running protocol
        if self.induction_running or self.bursts_done > 0:
            self.stop_induction_burst()

        # Just destroy; StimulationGUI will recreate if needed
        self.destroy()
