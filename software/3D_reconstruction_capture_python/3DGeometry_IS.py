import cv2
import serial
import time
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from serial.tools import list_ports
import os
import sys
import threading

# Configuration shared with the HEartLab stepper-motor firmware.
SERIAL_BAUD_RATE = 57600
SERIAL_TIMEOUT_S = 0.25
MOTOR_COMPLETION_TIMEOUT_S = 30.0
DEFAULT_NUM_IMAGES = 100
DEFAULT_SETTLING_DELAY_S = 3.0
MAX_CAMERAS = 10


def open_camera(camera_index):
    """Open a camera, preferring DirectShow on Windows."""
    if sys.platform.startswith("win"):
        cap = cv2.VideoCapture(camera_index, cv2.CAP_DSHOW)
        if cap.isOpened():
            return cap
        cap.release()

    return cv2.VideoCapture(camera_index)


def list_cameras(max_cameras=MAX_CAMERAS):
    """Return indices for cameras that OpenCV can open."""
    cameras = []
    for i in range(max_cameras):
        cap = open_camera(i)
        if cap.isOpened():
            cameras.append(i)
        cap.release()
    return cameras


def list_serial_ports():
    """Return available serial/COM port names."""
    return [port.device for port in list_ports.comports()]


def set_camera_exposure(camera, exposure_value):
    """Set OpenCV exposure. Exact behavior is camera/backend dependent."""
    if not camera.set(cv2.CAP_PROP_EXPOSURE, float(exposure_value)):
        print("Warning: camera/backend did not confirm the exposure setting.")


def set_camera_gain(camera, gain_value):
    """Set OpenCV gain. Exact behavior is camera/backend dependent."""
    if not camera.set(cv2.CAP_PROP_GAIN, float(gain_value)):
        print("Warning: camera/backend did not confirm the gain setting.")


def capture_and_save_image(camera, image_num, save_folder):
    """Capture one frame and save it as TIFF."""
    ret, frame = camera.read()
    if not ret or frame is None:
        raise RuntimeError(f"Failed to capture image {image_num}.")

    filename = os.path.join(save_folder, f"image_{image_num:03d}.tiff")
    if not cv2.imwrite(filename, frame):
        raise IOError(f"Failed to save image to {filename}")

    print(f"Saved {filename}")
    return frame


def wait_for_motor_completion(serial_port, timeout_s=MOTOR_COMPLETION_TIMEOUT_S):
    """
    Wait for the current Arduino firmware to report completion.

    The HEartLab stepper firmware prints a line beginning with
    "Step Count:" after runToPosition() finishes.
    """
    deadline = time.monotonic() + timeout_s
    received_lines = []

    while time.monotonic() < deadline:
        raw = serial_port.readline()
        if not raw:
            continue

        line = raw.decode(errors="replace").strip()
        if line:
            received_lines.append(line)
            print(f"Arduino: {line}")

        if line.startswith("Step Count:"):
            return line

    details = " | ".join(received_lines[-5:])
    raise TimeoutError(
        "Timed out waiting for the stepper controller to finish moving."
        + (f" Last messages: {details}" if details else "")
    )


def send_serial_command(serial_port, angle, reverse=False):
    """Command one relative angular movement and wait until it is complete."""
    if reverse:
        angle = -angle

    # The current Arduino firmware expects two numeric values:
    # an initiation value followed by the requested angle.
    command = f"1\n{angle:.4f}\n"

    # Remove any stale startup/debug text before a new command.
    serial_port.reset_input_buffer()
    serial_port.write(command.encode("ascii"))
    serial_port.flush()

    print(f"Sent angle command: {angle:.4f}°")
    return wait_for_motor_completion(serial_port)


def live_feed_for_adjustments(camera):
    """
    Show a live feed for exposure/gain adjustment.

    Exposure and gain ranges are implementation dependent and must be
    verified for the connected Imaging Source camera and OpenCV backend.
    """
    print("Press 'r' when ready to close the adjustment window and continue.")
    cv2.namedWindow("Camera Feed")

    def update_exposure(val):
        # Representative OpenCV/DirectShow mapping used by the original code.
        exposure_value = val / 10.0 - 10.0
        set_camera_exposure(camera, exposure_value)

    def update_gain(val):
        gain_value = float(val)
        set_camera_gain(camera, gain_value)

    cv2.createTrackbar("Exposure", "Camera Feed", 50, 100, update_exposure)
    cv2.createTrackbar("Gain", "Camera Feed", 50, 100, update_gain)

    while True:
        ret, frame = camera.read()
        if not ret or frame is None:
            raise RuntimeError("Failed to read from camera during live preview.")

        cv2.putText(
            frame,
            "Press 'r' when ready",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 0, 255),
            2,
        )
        cv2.imshow("Camera Feed", frame)

        if cv2.waitKey(1) & 0xFF == ord("r"):
            break

        if cv2.getWindowProperty("Camera Feed", cv2.WND_PROP_VISIBLE) < 1:
            break

    cv2.destroyWindow("Camera Feed")


def show_live_feed(camera_index):
    """Show a preview of the selected camera until q or window close."""
    cap = open_camera(camera_index)
    if not cap.isOpened():
        print(f"Failed to open camera {camera_index}")
        return

    try:
        cv2.namedWindow("Live Camera Feed")
        while True:
            ret, frame = cap.read()
            if not ret or frame is None:
                print("Failed to read from camera.")
                break

            cv2.imshow("Live Camera Feed", frame)

            if cv2.getWindowProperty("Live Camera Feed", cv2.WND_PROP_VISIBLE) < 1:
                break

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
    finally:
        cap.release()
        cv2.destroyWindow("Live Camera Feed")


def capture_images(
    camera,
    serial_port,
    save_folder,
    num_images=DEFAULT_NUM_IMAGES,
    settling_delay=DEFAULT_SETTLING_DELAY_S,
    reverse=False,
    return_to_start=True,
):
    """
    Capture exactly num_images unique angular views.

    For N images, the angular increment is 360/N. Images are acquired at:
    0, Δθ, 2Δθ, ... (N-1)Δθ.

    If return_to_start is True, one final movement is made after the last
    image so the stage returns to its starting orientation.
    """
    if num_images < 2:
        raise ValueError("Number of images must be at least 2.")
    if settling_delay < 0:
        raise ValueError("Settling delay cannot be negative.")

    os.makedirs(save_folder, exist_ok=True)
    angle = 360.0 / num_images

    print(
        f"Starting acquisition: {num_images} images, "
        f"{angle:.4f}° increment, reverse={reverse}"
    )

    cv2.namedWindow("Last Capture")

    try:
        for i in range(num_images):
            frame = capture_and_save_image(camera, i, save_folder)
            cv2.imshow("Last Capture", frame)
            cv2.waitKey(1)

            # Move to the next unique imaging position.
            if i < num_images - 1:
                send_serial_command(serial_port, angle, reverse=reverse)
                if settling_delay > 0:
                    time.sleep(settling_delay)

        # The N unique views end at (N-1)*Δθ. One final Δθ move returns
        # the stage to the initial 360°/0° orientation without saving a
        # duplicate image.
        if return_to_start:
            send_serial_command(serial_port, angle, reverse=reverse)

        print("Image acquisition complete.")
    finally:
        cv2.destroyWindow("Last Capture")


def browse_folder():
    return filedialog.askdirectory()


def refresh_com_ports(com_dropdown, com_var):
    com_list = list_serial_ports()
    com_dropdown["values"] = com_list
    if com_list:
        com_var.set(com_list[0])
    else:
        com_var.set("")


def start_capture(
    camera_index,
    com_port,
    save_folder,
    settling_delay,
    num_images,
    reverse=False,
):
    """Open hardware, run the adjustment preview, and acquire the image set."""
    if not save_folder:
        raise ValueError("Select a folder before starting acquisition.")
    if not com_port:
        raise ValueError("Select a serial/COM port before starting acquisition.")

    os.makedirs(save_folder, exist_ok=True)

    cap = open_camera(camera_index)
    if not cap.isOpened():
        raise RuntimeError(f"Failed to open camera {camera_index}.")

    serial_port = None
    try:
        serial_port = serial.Serial(
            com_port,
            SERIAL_BAUD_RATE,
            timeout=SERIAL_TIMEOUT_S,
        )

        # Many Arduino-class boards reset when the serial port is opened.
        time.sleep(2)
        serial_port.reset_input_buffer()

        live_feed_for_adjustments(cap)

        capture_images(
            cap,
            serial_port,
            save_folder,
            num_images=num_images,
            settling_delay=settling_delay,
            reverse=reverse,
            return_to_start=True,
        )
    finally:
        cap.release()
        if serial_port is not None and serial_port.is_open:
            serial_port.close()
        cv2.destroyAllWindows()


def create_gui():
    root = tk.Tk()
    root.title("HEartLab 3D Geometry Image Acquisition")

    frame_camera = ttk.LabelFrame(root, text="Camera", padding="10")
    frame_camera.grid(row=0, column=0, padx=10, pady=5, sticky="ew")

    ttk.Label(frame_camera, text="Select Camera:").grid(
        row=0, column=0, padx=5, pady=5
    )

    camera_list = list_cameras()
    camera_var = tk.StringVar()
    camera_dropdown = ttk.Combobox(
        frame_camera,
        textvariable=camera_var,
        values=camera_list,
        state="readonly",
        width=12,
    )
    camera_dropdown.grid(row=0, column=1, padx=5, pady=5)

    if camera_list:
        camera_dropdown.current(0)

    def launch_live_feed():
        if not camera_var.get():
            messagebox.showerror("Camera", "No camera is selected.")
            return

        camera_index = int(camera_var.get())
        threading.Thread(
            target=show_live_feed,
            args=(camera_index,),
            daemon=True,
        ).start()

    ttk.Button(
        frame_camera,
        text="Show Live Feed",
        command=launch_live_feed,
    ).grid(row=1, column=1, padx=5, pady=5)

    frame_com = ttk.LabelFrame(root, text="Stepper Controller", padding="10")
    frame_com.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

    ttk.Label(frame_com, text="Select COM Port:").grid(
        row=0, column=0, padx=5, pady=5
    )

    com_list = list_serial_ports()
    com_var = tk.StringVar()
    com_dropdown = ttk.Combobox(
        frame_com,
        textvariable=com_var,
        values=com_list,
        state="readonly",
        width=16,
    )
    com_dropdown.grid(row=0, column=1, padx=5, pady=5)

    if com_list:
        com_dropdown.current(0)

    ttk.Button(
        frame_com,
        text="Refresh COM Ports",
        command=lambda: refresh_com_ports(com_dropdown, com_var),
    ).grid(row=1, column=1, padx=5, pady=5)

    frame_folder = ttk.LabelFrame(root, text="Output", padding="10")
    frame_folder.grid(row=2, column=0, padx=10, pady=5, sticky="ew")

    folder_var = tk.StringVar()
    ttk.Entry(frame_folder, textvariable=folder_var, width=45).grid(
        row=0, column=0, padx=5, pady=5
    )
    ttk.Button(
        frame_folder,
        text="Browse",
        command=lambda: folder_var.set(browse_folder()),
    ).grid(row=0, column=1, padx=5, pady=5)

    frame_settings = ttk.LabelFrame(root, text="Acquisition", padding="10")
    frame_settings.grid(row=3, column=0, padx=10, pady=5, sticky="ew")

    ttk.Label(frame_settings, text="Settling delay (s):").grid(
        row=0, column=0, padx=5, pady=5
    )
    delay_var = tk.DoubleVar(value=DEFAULT_SETTLING_DELAY_S)
    ttk.Entry(frame_settings, textvariable=delay_var, width=12).grid(
        row=0, column=1, padx=5, pady=5
    )

    ttk.Label(frame_settings, text="Number of images:").grid(
        row=1, column=0, padx=5, pady=5
    )
    images_var = tk.IntVar(value=DEFAULT_NUM_IMAGES)
    ttk.Entry(frame_settings, textvariable=images_var, width=12).grid(
        row=1, column=1, padx=5, pady=5
    )

    reverse_rotation_var = tk.BooleanVar(value=False)
    ttk.Checkbutton(
        frame_settings,
        text="Reverse rotation",
        variable=reverse_rotation_var,
    ).grid(row=2, column=0, columnspan=2, padx=5, pady=5)

    status_var = tk.StringVar(value="Ready")
    ttk.Label(root, textvariable=status_var).grid(
        row=4, column=0, padx=10, pady=5
    )

    start_button = ttk.Button(root, text="Start Capture")
    start_button.grid(row=5, column=0, padx=10, pady=10)

    def run_capture_worker(camera_index, com_port, folder, delay, n_images, reverse):
        try:
            start_capture(
                camera_index,
                com_port,
                folder,
                delay,
                n_images,
                reverse=reverse,
            )
        except Exception as exc:
            root.after(
                0,
                lambda: messagebox.showerror("Acquisition error", str(exc)),
            )
            root.after(0, lambda: status_var.set("Error"))
        else:
            root.after(0, lambda: status_var.set("Complete"))
            root.after(
                0,
                lambda: messagebox.showinfo(
                    "Acquisition",
                    "Image acquisition completed successfully.",
                ),
            )
        finally:
            root.after(0, lambda: start_button.config(state="normal"))

    def launch_capture():
        if not camera_var.get():
            messagebox.showerror("Camera", "No camera is selected.")
            return
        if not com_var.get():
            messagebox.showerror("Serial port", "No COM port is selected.")
            return
        if not folder_var.get():
            messagebox.showerror("Output", "Select an output folder.")
            return

        try:
            delay = float(delay_var.get())
            n_images = int(images_var.get())
        except (tk.TclError, ValueError):
            messagebox.showerror(
                "Acquisition settings",
                "Delay and number of images must be valid numbers.",
            )
            return

        if delay < 0:
            messagebox.showerror(
                "Acquisition settings",
                "Settling delay cannot be negative.",
            )
            return
        if n_images < 2:
            messagebox.showerror(
                "Acquisition settings",
                "Number of images must be at least 2.",
            )
            return

        start_button.config(state="disabled")
        status_var.set("Acquiring...")

        threading.Thread(
            target=run_capture_worker,
            args=(
                int(camera_var.get()),
                com_var.get(),
                folder_var.get(),
                delay,
                n_images,
                bool(reverse_rotation_var.get()),
            ),
            daemon=True,
        ).start()

    start_button.config(command=launch_capture)

    root.mainloop()


if __name__ == "__main__":
    create_gui()
